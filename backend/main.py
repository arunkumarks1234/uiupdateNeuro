# -*- coding: utf-8 -*-
import os
import sys
# Force UTF-8 output on Windows so emoji in print() never crashes
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
import re
import tempfile
import joblib
import librosa
import numpy as np
import torch
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import (
    HubertModel,
    Wav2Vec2FeatureExtractor,
    WhisperProcessor,
    WhisperForConditionalGeneration,
)
from groq import Groq

from pydantic import BaseModel
from database import init_db, get_db_connection
import json

# Initialize DB
init_db()

# ─────────────────────────────────────────────
# 1. App & CORS  (allow all local dev ports)
# ─────────────────────────────────────────────
app = FastAPI(title="NeuroSpeak-AI Clinical Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins for local development
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# 2. Device & paths
# ─────────────────────────────────────────────
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DTYPE  = torch.float16 if torch.cuda.is_available() else torch.float32
GROQ_API_KEY        = os.environ.get("GROQ_API_KEY", "")
SEVERITY_MODEL_PATH = r"C:\NeuroSpeak\Outputs\severity_classifier_hubert.pkl"

if not GROQ_API_KEY:
    print("[WARN] GROQ_API_KEY not set - LLM stages will echo ASR output.")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# ─────────────────────────────────────────────
# 3. Load models at startup
# ─────────────────────────────────────────────
print("Loading HuBERT (GPU FP16)…")
hubert_extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/hubert-base-ls960")
hubert_model = HubertModel.from_pretrained(
    "facebook/hubert-base-ls960", torch_dtype=DTYPE
).to(DEVICE)
hubert_model.eval()

print("Loading Whisper Large-v3 (GPU FP16)…")
whisper_processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")
whisper_model = WhisperForConditionalGeneration.from_pretrained(
    "openai/whisper-large-v3", torch_dtype=DTYPE
).to(DEVICE)
whisper_model.eval()

print("[INFO] Loading SVM severity classifier...")
if not os.path.exists(SEVERITY_MODEL_PATH):
    raise FileNotFoundError(f"Classifier not found: {SEVERITY_MODEL_PATH}")
severity_clf = joblib.load(SEVERITY_MODEL_PATH)

print("[INFO] Backend ready. All models loaded.")


# ─────────────────────────────────────────────
# 4. Helper functions
# ─────────────────────────────────────────────
PHONETIC_FIXES = {
    r"\bur\b": "her", r"\bwsh\b": "wash", r"\bwter\b": "water",
    r"\bsut\b": "suit", r"\bgresy\b": "greasy",
}

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r"[^\w\s']", "", text.lower())
    return " ".join(text.split())

def phonetic_preprocess(text: str) -> str:
    text = text.lower()
    for pat, rep in PHONETIC_FIXES.items():
        text = re.sub(pat, rep, text)
    return " ".join(text.split())

def get_clinical_features(y: np.ndarray, sr: int = 16000):
    """Returns (7-dim clinical feature vector, metrics_dict)."""
    pitches, voiced, _ = librosa.pyin(y, fmin=60, fmax=300, sr=sr,
                                       frame_length=1024, hop_length=512)
    f0_mean = float(np.nanmean(pitches[voiced])) if np.any(voiced) else 0.0
    f0_std  = float(np.nanstd(pitches[voiced]))  if np.any(voiced) else 0.0

    rms            = librosa.feature.rms(y=y, frame_length=1024, hop_length=512)[0]
    pause_ratio    = float(np.sum(rms < 0.02) / max(len(rms), 1))
    speech_rate    = float(np.sum(rms > 0.02) / max(len(rms), 1))
    duration       = float(len(y) / sr)

    mfccs          = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=512)
    mfcc_var       = float(np.mean(np.var(mfccs, axis=1))) if mfccs.size else 0.0
    spec_centroid  = float(np.mean(
        librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=512)
    ))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))

    feature_vec = np.array(
        [f0_mean, f0_std, pause_ratio, duration, mfcc_var, speech_rate, spec_centroid],
        dtype=np.float32,
    )
    metrics = {
        "f0_mean":          round(f0_mean, 2),
        "f0_std":           round(f0_std, 2),
        "spectral_centroid": round(spec_centroid, 2),
        "zcr":              round(zcr, 4),
    }
    return feature_vec, metrics

def run_hubert(y: np.ndarray, sr: int = 16000) -> np.ndarray:
    """Extract mean-pooled HuBERT embedding (768-dim, float32)."""
    inp = hubert_extractor(y, sampling_rate=sr, return_tensors="pt").input_values
    inp = inp.to(device=DEVICE, dtype=DTYPE)
    with torch.no_grad():
        out = hubert_model(inp, output_hidden_states=True)
    return out.hidden_states[-1].mean(dim=1).squeeze().cpu().numpy().astype(np.float32)

def run_whisper(y: np.ndarray, sr: int = 16000) -> str:
    feats = whisper_processor(y, sampling_rate=sr, return_tensors="pt").input_features
    feats = feats.to(device=DEVICE, dtype=DTYPE)
    with torch.no_grad():
        ids = whisper_model.generate(feats, language="english",
                                     task="transcribe", max_new_tokens=96)
    return whisper_processor.batch_decode(ids, skip_special_tokens=True)[0].strip()

def llm_debate(s2: str, duration_sec: float) -> tuple[str, str]:
    """Proposer → Critic via Groq. Falls back to echo if no API key."""
    if not groq_client or len(s2.split()) < 2:
        return s2, s2

    ref_words = max(3, int(duration_sec * 2.5))

    # Stage 3 – Proposer
    try:
        r = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system",
                 "content": (f"Fix this garbled dysarthric speech transcript into a fluent "
                              f"English sentence of ~{ref_words} words. "
                              f"Output ONLY the corrected sentence.")},
                {"role": "user", "content": s2},
            ],
            temperature=0, max_tokens=60,
        )
        s3 = clean_text(r.choices[0].message.content)
    except Exception:
        s3 = s2

    # Stage 4 – Critic
    try:
        crit_prompt = (
            f'ASR input: "{s2}"\n'
            f'Proposed: "{s3}"\n'
            f'Duration: {duration_sec:.1f}s (≤{int(duration_sec*3.5)} words)\n'
            f"Reply EXACTLY:\nVERDICT: ACCEPT or REJECT\nREVISED: <final sentence>"
        )
        r2 = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": crit_prompt}],
            temperature=0, max_tokens=60,
        )
        raw = r2.choices[0].message.content
        s4 = clean_text(raw.split("REVISED:")[-1]) if "REVISED:" in raw else s3
    except Exception:
        s4 = s3

    return s3, s4


# ─────────────────────────────────────────────
# 5. Endpoints
# ─────────────────────────────────────────────
@app.get("/api/ping")
def ping():
    """Health-check – open http://localhost:8000/api/ping to verify backend is up."""
    return {"status": "ok", "device": str(DEVICE)}


@app.post("/api/analyze-utterance")
async def analyze_utterance(file: UploadFile = File(...), patient_id: int = Form(None)):
    import traceback
    # Write uploaded bytes to temp file
    orig_name = file.filename or "audio.webm"
    suffix = os.path.splitext(orig_name)[1] or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    wav_path = None
    try:
        # ── Strategy 1: librosa direct (works if ffmpeg is on PATH)
        try:
            y, _ = librosa.load(tmp_path, sr=16000, mono=True)
            print(f"[audio] loaded directly via librosa, {len(y)/16000:.2f}s")
        except Exception as e1:
            print(f"[audio] direct load failed ({e1}), trying ffmpeg conversion...")
            # ── Strategy 2: convert via ffmpeg subprocess → WAV
            wav_path = tmp_path + "_converted.wav"
            ffmpeg_bins = ["ffmpeg", r"C:\ffmpeg\bin\ffmpeg.exe", r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"]
            converted = False
            for ff in ffmpeg_bins:
                try:
                    import subprocess
                    result = subprocess.run(
                        [ff, "-y", "-i", tmp_path, "-ar", "16000", "-ac", "1", "-f", "wav", wav_path],
                        capture_output=True, timeout=30
                    )
                    if result.returncode == 0:
                        y, _ = librosa.load(wav_path, sr=16000, mono=True)
                        print(f"[audio] ffmpeg conversion succeeded with {ff}")
                        converted = True
                        break
                except Exception:
                    continue
            if not converted:
                # ── Strategy 3: try soundfile (handles WAV/FLAC/OGG natively)
                try:
                    import soundfile as sf
                    data, sr = sf.read(tmp_path, dtype='float32', always_2d=False)
                    import resampy
                    y = resampy.resample(data, sr, 16000) if sr != 16000 else data
                    print(f"[audio] soundfile fallback succeeded")
                except Exception as e3:
                    raise HTTPException(
                        status_code=422,
                        detail=f"Cannot decode audio. Please install ffmpeg and add it to PATH. "
                               f"Download: https://ffmpeg.org/download.html | Error: {str(e1)}"
                    )

        dur = float(len(y) / 16000)
        if dur < 0.3:
            raise HTTPException(status_code=422,
                                detail="Recording too short (< 0.3 s). Please speak for at least 1 second.")

        # Severity (HuBERT + SVM)
        embedding         = run_hubert(y)
        clin_vec, metrics = get_clinical_features(y)
        # feat_1031         = np.concatenate([embedding, clin_vec]).reshape(1, -1)
        severity          = str(severity_clf.predict(embedding.reshape(1, -1))[0])

        # ASR
        raw = run_whisper(y)
        s1  = clean_text(raw)
        s2  = clean_text(phonetic_preprocess(raw))

        # LLM debate
        s3, s4 = llm_debate(s2, dur)

        # Save to Database if patient_id is provided
        if patient_id is not None:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO assessments (patient_id, severity, final_text, duration, metrics) VALUES (?, ?, ?, ?, ?)",
                (patient_id, severity, s4, dur, json.dumps(metrics))
            )
            conn.commit()
            conn.close()

        return {
            "duration":    round(dur, 2),
            "severity":    severity,
            "s1_raw":      s1,
            "s2_phonetic": s2,
            "s3_qwen":     s3,
            "s4_final":    s4,
            "metrics":     metrics,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[analyze] Unexpected error:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
    finally:
        for p in [tmp_path, wav_path]:
            try:
                if p and os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass




class AuthRequest(BaseModel):
    username: str
    password: str
    role: str = "patient"

@app.post("/api/register")
def register(req: AuthRequest):
    conn = get_db_connection()
    try:
        cursor = conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (req.username, req.password, req.role))
        user_id = cursor.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    conn.close()
    return {"success": True, "user": {"id": user_id, "username": req.username, "role": req.role}}

@app.post("/api/login")
def login(req: AuthRequest):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (req.username, req.password)).fetchone()
    conn.close()
    if user:
        return {"success": True, "user": dict(user)}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/patients")
def get_patients():
    conn = get_db_connection()
    patients = conn.execute("SELECT id, username FROM users WHERE role = 'patient'").fetchall()
    
    result = []
    for p in patients:
        assessments = conn.execute("SELECT severity, timestamp FROM assessments WHERE patient_id = ? ORDER BY id ASC", (p['id'],)).fetchall()
        p_dict = dict(p)
        
        if assessments:
            p_dict['baseline_severity'] = assessments[0]['severity']
            p_dict['latest_severity'] = assessments[-1]['severity']
            p_dict['last_active'] = assessments[-1]['timestamp']
            p_dict['session_count'] = len(assessments)
        else:
            p_dict['baseline_severity'] = 'N/A'
            p_dict['latest_severity'] = 'N/A'
            p_dict['last_active'] = 'Never'
            p_dict['session_count'] = 0
            
        result.append(p_dict)
        
    conn.close()
    return result

@app.get("/api/patient/{id}/progress")
def get_patient_progress(id: int):
    conn = get_db_connection()
    assessments = conn.execute("SELECT * FROM assessments WHERE patient_id = ? ORDER BY id ASC", (id,)).fetchall()
    
    # Also fetch rehab word stats
    rehab_stats = conn.execute('''
        SELECT cw.word, rp.score, rp.attempts 
        FROM rehab_progress rp
        JOIN custom_words cw ON rp.word_id = cw.id
        WHERE rp.patient_id = ?
    ''', (id,)).fetchall()
    
    conn.close()
    return {
        "assessments": [dict(a) for a in assessments],
        "rehab": [dict(r) for r in rehab_stats]
    }

class WordRequest(BaseModel):
    word: str
    clinician_id: int

@app.post("/api/add-word")
def add_word(req: WordRequest):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO custom_words (word, added_by) VALUES (?, ?)", (req.word.lower(), req.clinician_id))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Already exists
    finally:
        conn.close()
    return {"success": True}

@app.get("/api/words")
def get_words():
    conn = get_db_connection()
    words = conn.execute("SELECT * FROM custom_words").fetchall()
    conn.close()
    return [dict(w) for w in words]

class RehabScoreRequest(BaseModel):
    patient_id: int
    word_id: int
    score: int

@app.post("/api/rehab/score")
def submit_rehab_score(req: RehabScoreRequest):
    conn = get_db_connection()
    existing = conn.execute("SELECT attempts FROM rehab_progress WHERE patient_id = ? AND word_id = ?", (req.patient_id, req.word_id)).fetchone()
    
    if existing:
        conn.execute('''
            UPDATE rehab_progress 
            SET score = ?, attempts = attempts + 1, last_practiced = CURRENT_TIMESTAMP
            WHERE patient_id = ? AND word_id = ?
        ''', (req.score, req.patient_id, req.word_id))
    else:
        conn.execute('''
            INSERT INTO rehab_progress (patient_id, word_id, score, attempts) 
            VALUES (?, ?, ?, 1)
        ''', (req.patient_id, req.word_id, req.score))
    
    conn.commit()
    conn.close()
    return {"success": True}