import React, { useState, useRef, useEffect, useCallback } from "react";
import { BrowserRouter, Routes, Route, useNavigate, Navigate } from "react-router-dom";
import axios from "axios";
import {
  Activity, Mic, Square, User, Lock, LogOut, Users,
  Plus, TrendingUp, CheckCircle, ChevronRight, Volume2,
  Brain, Zap, Star, Upload, BarChart2, X, Flame, Calendar,
  Sparkles, ShieldCheck, ArrowUpRight, Award, Shield,
} from "lucide-react";
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

const API = "http://localhost:8000";

/* ─── Gamification ─────────────────────────────── */
const LEVELS = [
  { name: "Beginner",     emoji: "🌱", min: 0  },
  { name: "Apprentice",   emoji: "💧", min: 5  },
  { name: "Practitioner", emoji: "⚡", min: 15 },
  { name: "Advanced",     emoji: "🔥", min: 30 },
  { name: "Master",       emoji: "👑", min: 60 },
];
function getLevel(sessions) {
  let lv = LEVELS[0];
  for (const l of LEVELS) if (sessions >= l.min) lv = l;
  const idx  = LEVELS.indexOf(lv);
  const next = LEVELS[idx + 1];
  const pct  = next
    ? Math.min(100, Math.round(((sessions - lv.min) / (next.min - lv.min)) * 100))
    : 100;
  return { ...lv, idx, next, pct };
}

/* ─── Severity helpers ──────────────────────────── */
const SEV_MAP = { Normal: 4, Mild: 3, Moderate: 2, Severe: 1 };
const SEV_CLR = {
  Normal:   { 
    pill: "bg-emerald-50 text-emerald-700 border border-emerald-200/80 shadow-2xs", 
    card: "bg-gradient-to-br from-emerald-50/90 to-teal-50/50 border-emerald-200/80 text-emerald-800 shadow-sm" 
  },
  Mild:     { 
    pill: "bg-sky-50 text-sky-700 border border-sky-200/80 shadow-2xs", 
    card: "bg-gradient-to-br from-sky-50/90 to-blue-50/50 border-sky-200/80 text-sky-800 shadow-sm" 
  },
  Moderate: { 
    pill: "bg-amber-50 text-amber-800 border border-amber-200/80 shadow-2xs", 
    card: "bg-gradient-to-br from-amber-50/90 to-orange-50/50 border-amber-200/80 text-amber-900 shadow-sm" 
  },
  Severe:   { 
    pill: "bg-rose-50 text-rose-700 border border-rose-200/80 shadow-2xs", 
    card: "bg-gradient-to-br from-rose-50/90 to-red-50/50 border-rose-200/80 text-rose-900 shadow-sm" 
  },
};

/* ════════════════════════════════════════════════
   ROOT
════════════════════════════════════════════════ */
export default function App() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    try { const s = localStorage.getItem("ns_user"); if (s) setUser(JSON.parse(s)); } catch {}
  }, []);
  const login  = u => { setUser(u); localStorage.setItem("ns_user", JSON.stringify(u)); };
  const logout = () => { setUser(null); localStorage.removeItem("ns_user"); };

  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Header user={user} onLogout={logout} />
        <main className="flex-1 max-w-[1200px] w-full mx-auto px-4 py-5">
          <Routes>
            <Route path="/"          element={!user ? <AuthScreen onLogin={login} /> : <Navigate to={`/${user.role}`} />} />
            <Route path="/patient"   element={user?.role === "patient"   ? <PatientDashboard user={user} />   : <Navigate to="/" />} />
            <Route path="/clinician" element={user?.role === "clinician" ? <ClinicianDashboard user={user} /> : <Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

/* ════════════════════════════════════════════════
   HEADER
════════════════════════════════════════════════ */
function Header({ user, onLogout }) {
  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-2xl border-b border-slate-200/70 shadow-xs">
      <div className="max-w-[1240px] mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-sky-500 via-sky-400 to-cyan-300 flex items-center justify-center shadow-md shadow-sky-500/25 ring-2 ring-white">
            <Brain size={20} className="text-white" />
          </div>
          <div className="leading-tight">
            <div className="text-[18px] font-black bg-gradient-to-r from-sky-800 via-blue-900 to-slate-900 bg-clip-text text-transparent tracking-tight">
              NeuroSpeak<span className="text-sky-500 font-extrabold text-sm ml-1">AI</span>
            </div>
            <div className="text-[10px] text-slate-500 font-semibold tracking-wider uppercase flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Clinical Speech Biomarkers
            </div>
          </div>
        </div>

        {/* User */}
        {user && (
          <div className="flex items-center gap-3.5">
            <div className="flex items-center gap-2.5 bg-slate-100/80 border border-slate-200/60 px-3 py-1.5 rounded-2xl">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-sky-500 to-blue-600 flex items-center justify-center text-white text-xs font-black shadow-xs">
                {user.username[0].toUpperCase()}
              </div>
              <div className="leading-tight hidden sm:block text-left">
                <div className="text-xs font-bold text-slate-800">{user.username}</div>
                <div className="text-[10px] text-sky-600 font-bold capitalize">{user.role}</div>
              </div>
            </div>
            <button onClick={onLogout}
              className="flex items-center gap-1.5 text-xs font-bold text-slate-600 border border-slate-200 bg-white/90 rounded-xl px-3.5 py-2 hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition-all shadow-2xs">
              <LogOut size={13} /> Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
}

/* ════════════════════════════════════════════════
   AUTH SCREEN
════════════════════════════════════════════════ */
function AuthScreen({ onLogin }) {
  const [reg, setReg]           = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole]         = useState("patient");
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);
  const nav = useNavigate();

  const submit = async e => {
    e.preventDefault(); setLoading(true); setError("");
    try {
      const ep  = reg ? "/api/register" : "/api/login";
      const res = await axios.post(`${API}${ep}`, reg ? { username, password, role } : { username, password });
      onLogin(res.data.user); nav(`/${res.data.user.role}`);
    } catch (err) { setError(err.response?.data?.detail || "Authentication failed."); }
    finally { setLoading(false); }
  };

  return (
    <div className="max-w-md mx-auto mt-12 fade-up px-3">
      <div className="text-center mb-8">
        <div className="w-18 h-18 rounded-3xl bg-gradient-to-tr from-sky-500 via-sky-400 to-cyan-300 flex items-center justify-center mx-auto mb-4 shadow-xl shadow-sky-500/25 ring-4 ring-white/80">
          <Brain size={36} className="text-white drop-shadow-xs" />
        </div>
        <h1 className="text-3xl font-black bg-gradient-to-r from-sky-800 via-blue-900 to-slate-900 bg-clip-text text-transparent tracking-tight">
          NeuroSpeak AI
        </h1>
        <p className="text-slate-500 text-xs font-semibold uppercase tracking-wider mt-1.5 flex items-center justify-center gap-1.5">
          <Sparkles size={13} className="text-sky-500" />
          Clinical Speech Assessment Platform
        </p>
      </div>

      <div className="glass-panel rounded-3xl p-8 border border-white/80 shadow-xl shadow-slate-200/50">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-extrabold text-slate-800 tracking-tight">
            {reg ? "Create Clinical Account" : "Access Workspace"}
          </h2>
          <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-sky-50 text-sky-700 border border-sky-100">
            {reg ? "Registration" : "Secure Portal"}
          </span>
        </div>

        {error && (
          <div className="bg-red-50/90 border border-red-200 text-red-700 text-xs font-semibold rounded-2xl px-4 py-3 mb-5 leading-relaxed">
            {error}
          </div>
        )}

        <form onSubmit={submit} className="flex flex-col gap-3.5">
          <div className="relative">
            <User size={15} className="absolute left-3.5 top-3.5 text-slate-400" />
            <input className="w-full pl-10 pr-4 py-3 rounded-2xl border border-slate-200/80 bg-white/70 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-sky-400 focus:bg-white focus:ring-4 focus:ring-sky-500/10 transition-all font-medium"
              type="text" placeholder="Username" value={username} required onChange={e => setUsername(e.target.value)} />
          </div>
          <div className="relative">
            <Lock size={15} className="absolute left-3.5 top-3.5 text-slate-400" />
            <input className="w-full pl-10 pr-4 py-3 rounded-2xl border border-slate-200/80 bg-white/70 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-sky-400 focus:bg-white focus:ring-4 focus:ring-sky-500/10 transition-all font-medium"
              type="password" placeholder="Password" value={password} required onChange={e => setPassword(e.target.value)} />
          </div>
          {reg && (
            <select value={role} onChange={e => setRole(e.target.value)}
              className="w-full px-4 py-3 rounded-2xl border border-slate-200/80 bg-white/70 text-sm text-slate-800 focus:outline-none focus:border-sky-400 focus:ring-4 focus:ring-sky-500/10 transition-all font-semibold">
              <option value="patient">Patient Mode</option>
              <option value="clinician">Clinician Mode</option>
            </select>
          )}
          <button type="submit" disabled={loading}
            className="w-full py-3.5 rounded-2xl bg-gradient-to-r from-sky-500 via-sky-400 to-blue-600 text-white font-extrabold text-sm shadow-md shadow-sky-500/25 hover:shadow-lg hover:shadow-sky-500/35 hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 mt-2">
            {loading ? <><Activity size={15} className="spinner" /> Authenticating…</> : reg ? "Register Account →" : "Sign In to Portal →"}
          </button>
        </form>

        <p className="text-center text-xs text-slate-400 mt-5 font-medium">
          {reg ? "Already have an account? " : "New to NeuroSpeak? "}
          <span onClick={() => setReg(!reg)} className="text-sky-600 font-extrabold cursor-pointer hover:underline">
            {reg ? "Sign In" : "Register now"}
          </span>
        </p>


      </div>
    </div>
  );
}

/* ════════════════════════════════════════════════
   PATIENT DASHBOARD
════════════════════════════════════════════════ */
function PatientDashboard({ user }) {
  const [data, setData]             = useState({ assessments: [], rehab: [] });
  const [words, setWords]           = useState([]);
  const [tab, setTab]               = useState("progress");
  const [profileOpen, setProfileOpen] = useState(false);

  const refresh = useCallback(() => {
    axios.get(`${API}/api/patient/${user.id}/progress`).then(r => setData(r.data)).catch(console.error);
    axios.get(`${API}/api/words`).then(r => setWords(r.data)).catch(console.error);
  }, [user.id]);
  useEffect(() => { refresh(); }, [refresh]);

  const [chartView, setChartView] = useState("all");

  const chartData = data.assessments.map((a, i) => {
    let m = {};
    try { m = JSON.parse(a.metrics || "{}"); } catch {}
    return {
      name: `S${i + 1}`,
      session: i + 1,
      score: SEV_MAP[a.severity] || 0,
      severity: a.severity,
      confidence: m.confidence || (a.severity === "Normal" ? 85 : 78),
      dysarthria_index: m.risk_score !== undefined ? m.risk_score : (4 - (SEV_MAP[a.severity] || 4)) * 25,
      f0_std: m.f0_std || 0,
      jitter_pct: m.jitter ? +(m.jitter * 100).toFixed(2) : 0,
      shimmer_pct: m.shimmer ? +(m.shimmer * 100).toFixed(1) : 0,
      pause_pct: m.pause_ratio ? Math.round(m.pause_ratio * 100) : 0,
      centroid: m.spectral_centroid || 0,
      timestamp: a.timestamp || null
    };
  });

  const sessions   = data.assessments.length;
  const level      = getLevel(sessions);
  const mastered   = data.rehab.filter(r => r.score >= 80).length;
  const rehabScore = data.rehab.reduce((s, r) => s + (r.score || 0), 0);
  const latestSev  = sessions ? data.assessments.at(-1).severity : null;
  const apptDate   = new Date(); apptDate.setDate(apptDate.getDate() + 4);
  const apptStr    = apptDate.toLocaleDateString("en-US", { day: "numeric", month: "short" });

  return (
    <div className="flex flex-col gap-5">

      {/* ── Level Banner (Sleek light gradient) ── */}
      <div className="rounded-3xl bg-gradient-to-r from-sky-500 via-sky-400 to-cyan-400 text-white px-7 py-5 flex flex-wrap items-center gap-6 shadow-xl shadow-sky-500/15 border border-white/20 relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 w-44 h-44 rounded-full bg-white/10 blur-2xl pointer-events-none" />
        
        {/* Level info */}
        <div className="flex items-center gap-3.5 flex-1 min-w-[220px]">
          <div className="w-13 h-13 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-3xl shadow-inner border border-white/30">
            {level.emoji}
          </div>
          <div>
            <div className="text-[10px] font-bold uppercase tracking-widest text-sky-100 flex items-center gap-1.5">
              <span>Patient Progress Tier</span>
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-200 animate-ping" />
            </div>
            <div className="text-2xl font-black leading-tight tracking-tight mt-0.5">Level {level.idx + 1} · {level.name}</div>
            <div className="text-xs text-sky-100 font-medium">Continuous neuro-speech rehabilitation</div>
          </div>
        </div>

        {/* Progress bar */}
        <div className="flex-1 min-w-[180px]">
          <div className="flex justify-between text-xs font-semibold text-white/90 mb-1.5">
            <span>{level.name}</span>
            <span className="text-sky-100">{level.next?.name ?? "Master Level"}</span>
          </div>
          <div className="level-bar"><div className="level-bar-fill" style={{ width: `${level.pct}%` }} /></div>
          <div className="text-[11px] text-white/80 font-medium mt-1.5 flex justify-between">
            <span>{level.pct}% to next level</span>
            <span className="font-bold">{sessions} sessions logged</span>
          </div>
        </div>

        {/* Streak + Appointment */}
        <div className="flex gap-2.5">
          <button onClick={() => setProfileOpen(true)}
            className="bg-white/15 hover:bg-white/25 border border-white/20 backdrop-blur-md transition-all rounded-2xl px-4 py-2.5 text-center min-w-[76px] hover:scale-102">
            <Flame size={18} className="mx-auto mb-0.5 text-amber-300" />
            <div className="text-sm font-black">2</div>
            <div className="text-[10px] font-semibold text-white/80">Day Streak</div>
          </button>
          <div className="bg-white/15 border border-white/20 backdrop-blur-md rounded-2xl px-4 py-2.5 text-center min-w-[76px]">
            <Calendar size={18} className="mx-auto mb-0.5 text-sky-200" />
            <div className="text-sm font-black">{apptStr}</div>
            <div className="text-[10px] font-semibold text-white/80">Next Review</div>
          </div>
        </div>
      </div>

      {/* ── Stat Cards (Modern Light Cards with Soft Glow Accents) ── */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {[
          { Icon: BarChart2, label: "Total Clinical Sessions", value: sessions, sub: "Longitudinal tracking", color: "text-sky-500", bg: "bg-sky-500/10", border: "border-sky-200/50" },
          { Icon: CheckCircle, label: "Vocabulary Mastered", value: mastered, sub: "≥80% phonetic accuracy", color: "text-emerald-500", bg: "bg-emerald-500/10", border: "border-emerald-200/50" },
          { Icon: Star, label: "Rehab Fluency Score", value: rehabScore, sub: "Cumulative progress", color: "text-violet-500", bg: "bg-violet-500/10", border: "border-violet-200/50" },
        ].map(({ Icon, label, value, sub, color, bg, border }, i) => (
          <div key={i} className={`glass-panel glass-panel-hover rounded-2xl p-5 border ${border} flex items-center gap-4 fade-up`} style={{ animationDelay: `${i * 60}ms` }}>
            <div className={`w-12 h-12 rounded-2xl ${bg} flex items-center justify-center ${color} shrink-0`}>
              <Icon size={24} />
            </div>
            <div>
              <div className="text-3xl font-black text-slate-800 tracking-tight leading-none">{value}</div>
              <div className="text-xs font-bold text-slate-600 mt-1">{label}</div>
              <div className="text-[11px] text-slate-400 font-medium">{sub}</div>
            </div>
          </div>
        ))}
      </div>

      {/* ── Tabs ── */}
      <div className="flex gap-2">
        <TabBtn active={tab === "progress"} onClick={() => setTab("progress")}><TrendingUp size={15} /> Clinical Progress &amp; Analytics</TabBtn>
        <TabBtn active={tab === "rehab"}    onClick={() => setTab("rehab")}><Zap size={15} /> Speech Rehabilitation Studio</TabBtn>
      </div>

      {/* ── Progress Tab ── */}
      {tab === "progress" && (
        <div className="flex flex-col gap-5 fade-up">
          <Card>
            <SectionHeader Icon={Mic} title="Clinical Utterance Analyzer"
              sub="Record live speech · HuBERT feature extraction + Calibrated multi-tier dysarthria screening"
              badge="Active Diagnostic" />
            <AudioAnalyzer patientId={user.id} onComplete={refresh} showPipeline />
          </Card>

          {/* Recovery Trajectory Chart with interactive view toggle */}
          <Card>
            <div className="flex flex-wrap items-center justify-between gap-3 mb-5">
              <div>
                <div className="flex items-center gap-2.5">
                  <div className="w-7 h-7 rounded-lg bg-sky-100 border border-sky-200/60 flex items-center justify-center text-sky-600">
                    <TrendingUp size={16} />
                  </div>
                  <h2 className="text-[16px] font-extrabold text-slate-800 tracking-tight">Longitudinal Speech Recovery Trajectory</h2>
                </div>
                <p className="text-xs text-slate-400 ml-9 mt-0.5 font-medium">Session-by-session clinical severity and acoustic evolution</p>
              </div>

              {/* View filter buttons */}
              <div className="flex items-center gap-1.5 bg-slate-100/90 p-1 rounded-xl border border-slate-200/60">
                {[
                  { id: "all", label: "Severity Tier" },
                  { id: "risk", label: "Dysarthria Index" },
                  { id: "vocal", label: "Pitch Perturbation" },
                ].map(b => (
                  <button
                    key={b.id}
                    onClick={() => setChartView(b.id)}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                      chartView === b.id
                        ? "bg-white text-sky-600 shadow-xs"
                        : "text-slate-500 hover:text-slate-800"
                    }`}
                  >
                    {b.label}
                  </button>
                ))}
              </div>
            </div>

            {chartData.length > 0 ? (
              <div>
                {chartView === "all" && (
                  <GlowChart 
                    data={chartData} 
                    dataKey="score" 
                    color="#0ea5e9" 
                    yDomain={[0, 4]}
                    height={230}
                    yFormatter={v => v===4?"Normal":v===3?"Mild":v===2?"Moderate":v===1?"Severe":""}
                    tooltipFn={(v, p) => [p.severity, "Status"]} 
                  />
                )}
                {chartView === "risk" && (
                  <GlowChart 
                    data={chartData} 
                    dataKey="dysarthria_index" 
                    color="#f59e0b" 
                    yDomain={[0, 100]}
                    height={230}
                    unit="/ 100"
                    tooltipFn={(v) => [`${v} / 100`, "Impairment Index"]} 
                  />
                )}
                {chartView === "vocal" && (
                  <GlowChart 
                    data={chartData} 
                    dataKey="f0_std" 
                    color="#10b981" 
                    height={230}
                    unit="Hz"
                    tooltipFn={(v) => [`${v} Hz`, "F0 Instability"]} 
                  />
                )}
              </div>
            ) : (
              <EmptyState />
            )}
          </Card>

          {/* Secondary Acoustic Analytics Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <Card>
              <SectionHeader 
                Icon={Activity} 
                title="Vocal Tremor &amp; Perturbation (Jitter %)" 
                sub="Lower values indicate stabilized phonation control"
                badge="Laryngeal Biomarker" 
              />
              {chartData.length > 0 ? (
                <GlowChart 
                  data={chartData} 
                  dataKey="jitter_pct" 
                  color="#10b981" 
                  unit="%"
                  height={190}
                  tooltipFn={v => [`${v}%`, "Pitch Jitter"]} 
                />
              ) : (
                <EmptyState />
              )}
            </Card>

            <Card>
              <SectionHeader 
                Icon={Zap} 
                title="Consonant Precision (Centroid Hz)" 
                sub="Target range 1,800 - 3,200 Hz for clear speech articulation"
                badge="Articulatory Dynamics" 
              />
              {chartData.length > 0 ? (
                <GlowChart 
                  data={chartData} 
                  dataKey="centroid" 
                  color="#8b5cf6" 
                  unit="Hz"
                  height={190}
                  tooltipFn={v => [`${Math.round(v)} Hz`, "Spectral Centroid"]} 
                />
              ) : (
                <EmptyState />
              )}
            </Card>
          </div>
        </div>
      )}

      {/* ── Rehab Tab ── */}
      {tab === "rehab" && (
        <div className="fade-up">
          <RehabStudio user={user} words={words} rehabData={data.rehab} onRefresh={refresh} />
        </div>
      )}

      {/* ── Profile Modal ── */}
      {profileOpen && (
        <ProfileModal user={user} level={level} sessions={sessions} mastered={mastered}
          rehabScore={rehabScore} latestSev={latestSev} baseSev={data.assessments[0]?.severity}
          apptStr={apptStr} onClose={() => setProfileOpen(false)} />
      )}
    </div>
  );
}

/* ── Profile Modal ── */
function ProfileModal({ user, level, sessions, mastered, rehabScore, latestSev, baseSev, apptStr, onClose }) {
  return (
    <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center z-[999]" onClick={onClose}>
      <div className="bg-gradient-to-b from-[#eaf3fa] to-[#f2f1fb] rounded-[24px] shadow-2xl w-[380px] p-7 relative" onClick={e => e.stopPropagation()}>
        <button onClick={onClose} className="absolute top-4 right-4 w-7 h-7 rounded-full bg-sky-100/50 flex items-center justify-center hover:bg-sky-200 transition">
          <X size={14} className="text-sky-700" />
        </button>

        {/* Avatar */}
        <div className="flex items-center gap-4 mb-6">
          <div className="w-14 h-14 rounded-full bg-gradient-to-br from-sky-400 to-blue-600 flex items-center justify-center text-white text-2xl font-black shadow-lg shadow-blue-400/40">
            {user.username[0].toUpperCase()}
          </div>
          <div>
            <div className="font-black text-slate-800 text-xl leading-tight">{user.username}</div>
            <div className="text-sm text-slate-500 font-medium">Patient Profile</div>
          </div>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="bg-[#2bc27c] rounded-xl p-4 text-white shadow-sm shadow-[#2bc27c]/20">
            <div className="text-[10px] font-bold uppercase tracking-widest opacity-90 mb-2">Gamification Level</div>
            <div className="flex items-center gap-2">
              <div className="text-2xl text-amber-300">⚡</div>
              <div>
                <div className="font-black text-lg leading-tight">Level {level.idx + 1}</div>
                <div className="text-[13px] font-semibold opacity-90">{level.name}</div>
              </div>
            </div>
          </div>
          
          <div className="bg-[#e2f3ee] border border-[#cbebe1] rounded-xl p-4 shadow-sm">
            <div className="text-[10px] font-bold uppercase tracking-widest text-slate-500 mb-1">Current Severity</div>
            <div className="text-[26px] font-black text-[#1a9a62] leading-tight">{latestSev || "Normal"}</div>
            <div className="text-xs text-slate-500 font-medium mt-1">Baseline: {baseSev || "Severe"}</div>
          </div>
          
          <div className="bg-[#f3f2e8] border border-[#e8e6d6] rounded-xl p-4 flex items-center gap-3 shadow-sm">
            <div className="text-2xl">🔥</div>
            <div>
              <div className="text-xl font-black text-[#d97706] leading-none mb-0.5">2</div>
              <div className="text-xs text-slate-500 font-medium">Day Streak</div>
            </div>
          </div>
          
          <div className="bg-[#e4f0fa] border border-[#cbe4f6] rounded-xl p-4 flex items-center gap-3 shadow-sm">
            <div className="text-2xl text-sky-500"><Calendar size={22} /></div>
            <div>
              <div className="font-black text-[#0369a1] text-sm leading-none mb-0.5">7 Oct</div>
              <div className="text-[11px] text-slate-500 font-medium leading-tight">Next Appointment</div>
            </div>
          </div>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          {[["Sessions", sessions, "text-[#0369a1]"],["Mastered", mastered, "text-[#15803d]"],["Rehab Score", rehabScore, "text-[#7e22ce]"]].map(([l,v,c]) => (
            <div key={l} className="bg-white rounded-xl py-3 px-1 text-center shadow-sm">
              <div className={`text-xl font-black ${c}`}>{v}</div>
              <div className="text-[11px] text-slate-500 font-medium mt-0.5">{l}</div>
            </div>
          ))}
        </div>

        {/* Journey */}
        <div className="text-[11px] font-bold uppercase tracking-widest text-slate-500 mb-4">Level Journey</div>
        <div className="flex justify-between items-center relative z-10 px-2">
          {/* Connecting Line background */}
          <div className="absolute top-1/2 left-4 right-4 h-0.5 bg-blue-100 -z-10 -translate-y-[10px]"></div>
          
          {LEVELS.map((l, i) => {
            const isCurrent = i === level.idx;
            const isPast = i < level.idx;
            return (
              <div key={l.name} className={`flex flex-col items-center group ${i > level.idx ? "opacity-60" : ""}`}>
                <div className="bg-white p-0.5 rounded-full mb-1.5 relative">
                  {/* Connecting Line foreground for past levels */}
                  {i > 0 && isPast && (
                    <div className="absolute top-1/2 right-full w-[40px] h-0.5 bg-blue-500 -z-10 -translate-y-1/2 rounded"></div>
                  )}
                  {isCurrent && i > 0 && (
                    <div className="absolute top-1/2 right-full w-[40px] h-0.5 bg-blue-500 -z-10 -translate-y-1/2 rounded"></div>
                  )}
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center text-xl shadow-md
                    ${isCurrent ? "bg-[#34d399] shadow-[#34d399]/40 ring-4 ring-[#a7f3d0]" 
                      : isPast ? "bg-[#38bdf8] shadow-sky-300/40" 
                      : "bg-[#e2e8f0] shadow-slate-200"}`}>
                    {l.emoji}
                  </div>
                </div>
                <div className={`text-[10px] font-bold ${isCurrent ? "text-[#10b981]" : isPast ? "text-sky-500" : "text-slate-400"}`}>
                  {l.name}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ════════════════════════════════════════════════
   SHARED PRIMITIVES
════════════════════════════════════════════════ */
function Card({ children, className = "" }) {
  return (
    <div className={`glass-panel rounded-2xl p-6 glass-panel-hover border border-slate-150/80 shadow-sm ${className}`}>{children}</div>
  );
}

function TabBtn({ active, onClick, children }) {
  return (
    <button onClick={onClick}
      className={`flex items-center gap-2 px-5 py-2.5 rounded-full text-xs font-bold transition-all duration-300
        ${active
          ? "bg-gradient-to-r from-sky-500 to-blue-600 text-white shadow-md shadow-sky-500/25 ring-2 ring-sky-300/40 translate-y-[-1px]"
          : "bg-white/90 text-slate-600 border border-slate-200/80 hover:bg-sky-50/80 hover:text-sky-600 hover:border-sky-200 shadow-xs"}`}>
      {children}
    </button>
  );
}

function SectionHeader({ Icon, title, sub, badge }) {
  return (
    <div className="mb-4 flex items-center justify-between">
      <div>
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-sky-100/70 border border-sky-200/50 flex items-center justify-center text-sky-600">
            <Icon size={15} />
          </div>
          <h2 className="text-[15px] font-extrabold text-slate-800 tracking-tight">{title}</h2>
        </div>
        {sub && <p className="text-xs text-slate-400 ml-9 mt-0.5 font-medium">{sub}</p>}
      </div>
      {badge && (
        <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200/60 shadow-2xs">
          {badge}
        </span>
      )}
    </div>
  );
}

function CustomChartTooltip({ active, payload, label, formatter, unit = "" }) {
  if (active && payload && payload.length) {
    const val = payload[0].value;
    const name = payload[0].name || label;
    const itemPayload = payload[0].payload;
    const formattedVal = formatter ? formatter(val, itemPayload) : `${val} ${unit}`;

    return (
      <div className="bg-white/95 backdrop-blur-md border border-slate-200/80 px-3.5 py-2.5 rounded-xl shadow-xl shadow-slate-300/30 text-xs">
        <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-1">{itemPayload.name || label}</div>
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: payload[0].color || "#0ea5e9" }} />
          <span className="font-extrabold text-slate-800 text-sm">{formattedVal}</span>
        </div>
        {itemPayload.severity && (
          <div className="mt-1.5 pt-1.5 border-t border-slate-100 flex items-center justify-between gap-3 text-[10px]">
            <span className="text-slate-400">Severity:</span>
            <span className="font-bold text-sky-600">{itemPayload.severity}</span>
          </div>
        )}
      </div>
    );
  }
  return null;
}

function GlowChart({ data, dataKey, color = "#0ea5e9", gradientId = "chartGrad", yDomain, yFormatter, tooltipFn, unit = "", height = 210 }) {
  const gradId = `grad_${dataKey}_${color.replace("#","")}`;
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={data} margin={{ top: 12, right: 12, left: -10, bottom: 0 }}>
        <defs>
          <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={color} stopOpacity={0.32} />
            <stop offset="95%" stopColor={color} stopOpacity={0.01} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" strokeOpacity={0.6} />
        <XAxis 
          dataKey="name" 
          tick={{ fontSize: 11, fill: "#64748b", fontWeight: 600 }} 
          axisLine={{ stroke: "#e2e8f0" }} 
          tickLine={false} 
        />
        <YAxis 
          domain={yDomain} 
          tickFormatter={yFormatter} 
          tick={{ fontSize: 11, fill: "#64748b", fontWeight: 500 }}
          axisLine={false} 
          tickLine={false} 
          width={yFormatter ? 64 : 36} 
        />
        <Tooltip content={<CustomChartTooltip formatter={tooltipFn} unit={unit} />} />
        <Area 
          type="monotone" 
          dataKey={dataKey} 
          stroke={color} 
          strokeWidth={2.8} 
          fillOpacity={1} 
          fill={`url(#${gradId})`}
          dot={{ r: 4, fill: "#fff", stroke: color, strokeWidth: 2.5 }}
          activeDot={{ r: 6.5, fill: color, stroke: "#fff", strokeWidth: 3 }} 
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center py-10 gap-2">
      <Activity size={26} className="text-slate-200" />
      <p className="text-slate-400 text-sm">No data yet — record an utterance to begin</p>
    </div>
  );
}

/* ════════════════════════════════════════════════
   AUDIO ANALYZER  (all original logic kept)
════════════════════════════════════════════════ */
function AudioAnalyzer({ patientId, onComplete, showPipeline }) {
  const [phase, setPhase]           = useState("idle");
  const [result, setResult]         = useState(null);
  const [error, setError]           = useState("");
  const [audioUrl, setAudioUrl]     = useState(null);
  const [recSeconds, setRecSeconds] = useState(0);
  const recorderRef  = useRef(null);
  const chunksRef    = useRef([]);
  const fileInputRef = useRef(null);
  const timerRef     = useRef(null);

  const startRecording = async () => {
    setError(""); setResult(null); setAudioUrl(null); setRecSeconds(0);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio:{ echoCancellation:true, noiseSuppression:true, sampleRate:16000 } });
      const mimeType = ["audio/webm;codecs=opus","audio/webm","audio/ogg"].find(t => MediaRecorder.isTypeSupported(t)) || "";
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      recorderRef.current = recorder; chunksRef.current = [];
      recorder.ondataavailable = e => { if (e.data?.size > 0) chunksRef.current.push(e.data); };
      recorder.onstop = () => {
        stream.getTracks().forEach(t => t.stop()); clearInterval(timerRef.current);
        if (!chunksRef.current.length) { setError("No audio captured."); setPhase("idle"); return; }
        const blob = new Blob(chunksRef.current, { type: mimeType || "audio/webm" });
        setAudioUrl(URL.createObjectURL(blob)); submit(blob);
      };
      recorder.start(200); setPhase("recording");
      timerRef.current = setInterval(() => setRecSeconds(s => s + 1), 1000);
    } catch { setError("Microphone blocked — open browser settings and allow microphone access."); }
  };

  const stopRecording = () => { if (recorderRef.current?.state !== "inactive") recorderRef.current.stop(); setPhase("processing"); };
  const handleFile = e => { const f = e.target.files?.[0]; if (!f) return; setAudioUrl(URL.createObjectURL(f)); submit(f); e.target.value = ""; };

  const submit = async blob => {
    setPhase("processing"); setError("");
    const fd = new FormData();
    fd.append("file", new File([blob], "recording.webm", { type: blob.type || "audio/webm" }));
    if (patientId) fd.append("patient_id", String(patientId));
    try {
      const res = await axios.post(`${API}/api/analyze-utterance`, fd, { timeout: 180000 });
      setResult(res.data); setPhase("done"); if (onComplete) onComplete();
    } catch (err) {
      const msg = err.response?.data?.detail || err.message;
      setError(msg.includes("ffmpeg") ? msg : `Analysis error: ${msg}`); setPhase("idle");
    }
  };

  const sc = result ? (SEV_CLR[result.severity] || SEV_CLR.Normal) : null;

  return (
    <div>
      {/* Controls */}
      <div className="flex flex-wrap gap-2 items-center mb-4">
        <input type="file" accept="audio/*" ref={fileInputRef} onChange={handleFile} className="hidden" />
        <button onClick={() => fileInputRef.current.click()} disabled={phase==="recording"||phase==="processing"}
          className="flex items-center gap-1.5 text-xs font-semibold text-sky-600 border border-sky-200 bg-white rounded-full px-4 py-2 hover:bg-sky-50 transition disabled:opacity-50">
          <Upload size={13} /> Upload Audio
        </button>

        {(phase==="idle"||phase==="done") && (
          <button onClick={startRecording}
            className="flex items-center gap-1.5 text-xs font-semibold text-white bg-gradient-to-r from-sky-500 to-cyan-500 rounded-full px-4 py-2 shadow-md shadow-sky-200 hover:shadow-lg hover:-translate-y-0.5 transition">
            <Mic size={13} /> Start Recording
          </button>
        )}
        {phase==="recording" && (
          <div className="flex items-center gap-3">
            <button onClick={stopRecording}
              className="recording flex items-center gap-1.5 text-xs font-semibold text-white bg-gradient-to-r from-red-500 to-rose-500 rounded-full px-4 py-2 shadow-md shadow-red-200">
              <Square size={13} /> Stop &amp; Analyse
            </button>
            <span className="flex items-center gap-1.5 text-red-500 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />{recSeconds}s
            </span>
          </div>
        )}
        {phase==="processing" && (
          <button disabled className="flex items-center gap-1.5 text-xs font-semibold text-white bg-sky-400 rounded-full px-4 py-2 opacity-75 cursor-not-allowed">
            <Activity size={13} className="spinner" /> Analysing…
          </button>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 text-sm rounded-xl px-4 py-3 mb-4 leading-relaxed">
          {error}
          {error.includes("ffmpeg") && (
            <div className="mt-2 text-xs font-mono bg-red-100 rounded-lg px-3 py-2">
              Download: <a href="https://ffmpeg.org/download.html" className="text-sky-600 underline" target="_blank" rel="noreferrer">ffmpeg.org/download.html</a>
            </div>
          )}
        </div>
      )}

      {/* Result */}
      {result && phase==="done" && (
        <div className="flex gap-4 flex-wrap fade-up">
          {/* Left: severity + metrics */}
          <div className="flex flex-col gap-3" style={{ flex:"0 0 240px" }}>
            <div className={`rounded-xl border p-4 shadow-sm ${sc.card}`}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-[10px] font-bold uppercase tracking-wider opacity-75">Clinical Assessment</span>
                {result.confidence && (
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-white/80 shadow-xs">
                    {result.confidence}% Conf.
                  </span>
                )}
              </div>
              <div className="text-3xl font-black leading-tight tracking-tight">{result.severity}</div>
              
              {result.dysarthria_index !== undefined && (
                <div className="mt-2.5 pt-2 border-t border-current/15">
                  <div className="flex justify-between text-[11px] font-medium opacity-85 mb-1">
                    <span>Dysarthria Index:</span>
                    <span className="font-bold">{result.dysarthria_index}/100</span>
                  </div>
                  <div className="w-full bg-black/10 rounded-full h-1.5 overflow-hidden">
                    <div 
                      className="h-full bg-current rounded-full transition-all duration-500" 
                      style={{ width: `${Math.min(100, Math.max(5, result.dysarthria_index))}%` }} 
                    />
                  </div>
                </div>
              )}

              {/* Multi-tier probability distribution */}
              {result.severity_probs && (
                <div className="mt-3 pt-2 border-t border-current/15 space-y-1">
                  <div className="text-[9px] uppercase tracking-wider font-bold opacity-70 mb-1">Multi-Class Likelihood</div>
                  {Object.entries(result.severity_probs).map(([tier, prob]) => (
                    <div key={tier} className="flex items-center justify-between text-[10px] leading-tight opacity-90">
                      <span>{tier}</span>
                      <span className="font-semibold">{Math.round(prob * 100)}%</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Clinical Indicators if detected */}
            {result.clinical_notes && result.clinical_notes.length > 0 && (
              <div className="bg-amber-50/70 border border-amber-200/60 rounded-xl p-3 text-amber-900 text-[11px] leading-snug">
                <div className="font-bold text-[10px] uppercase tracking-wider text-amber-700 mb-1">Diagnostic Biomarkers:</div>
                <ul className="list-disc pl-3.5 space-y-0.5">
                  {result.clinical_notes.slice(0, 3).map((note, i) => (
                    <li key={i}>{note}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="bg-slate-50 border border-slate-100 rounded-xl p-3.5">
              <div className="text-[11px] font-bold text-slate-400 mb-2">ACOUSTIC BIOMARKERS</div>
              {[
                ["Duration", `${result.duration?.toFixed(2)} s`],
                ["Pause Ratio", result.metrics?.pause_ratio !== undefined ? `${Math.round(result.metrics.pause_ratio * 100)}%` : "N/A"],
                ["Jitter (Instability)", result.metrics?.jitter !== undefined ? `${(result.metrics.jitter * 100).toFixed(2)}%` : "N/A"],
                ["Shimmer (APQ)", result.metrics?.shimmer !== undefined ? `${(result.metrics.shimmer * 100).toFixed(1)}%` : "N/A"],
                ["F0 Mean", `${result.metrics?.f0_mean?.toFixed(1)} Hz`],
                ["Centroid", `${result.metrics?.spectral_centroid?.toFixed(0)} Hz`],
                ["ZCR", `${result.metrics?.zcr?.toFixed(4)}`]
              ].map(([k,v]) => (
                <div key={k} className="flex justify-between py-1 border-b border-slate-100 text-xs last:border-0">
                  <span className="text-slate-400">{k}</span>
                  <span className="font-semibold text-slate-700">{v}</span>
                </div>
              ))}
            </div>

            {audioUrl && (
              <div className="bg-slate-50 border border-slate-100 rounded-xl p-3">
                <div className="text-[10px] font-bold text-slate-400 mb-1">RECORDED AUDIO</div>
                <audio src={audioUrl} controls className="w-full" />
              </div>
            )}
          </div>

          {/* Right: Final Speech Output */}
          {showPipeline && (
            <div className="flex-1 min-w-[250px] bg-slate-50 border border-slate-100 rounded-xl p-5 flex flex-col justify-center">
              <div className="flex items-center gap-2 text-[11px] font-bold text-emerald-600 uppercase tracking-widest mb-3">
                <Zap size={13} /> Final Reconstructed Speech
              </div>
              
              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 mb-4 shadow-sm shadow-emerald-100">
                <p className="m-0 text-[15px] font-bold text-emerald-800 leading-relaxed text-center">"{result.s4_final}"</p>
              </div>
              
              <button onClick={() => { window.speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(result.s4_final); u.rate=0.8; window.speechSynthesis.speak(u); }}
                className="mx-auto inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 border-2 border-emerald-200 bg-white rounded-full px-5 py-2 hover:bg-emerald-50 hover:-translate-y-0.5 transition shadow-sm">
                <Volume2 size={14} /> Hear Reconstructed Speech
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

/* ════════════════════════════════════════════════
   REHAB STUDIO  (all original logic kept)
════════════════════════════════════════════════ */
function RehabStudio({ user, words, rehabData, onRefresh }) {
  const [idx, setIdx]             = useState(0);
  const [phase, setPhase]         = useState("idle");
  const [result, setResult]       = useState(null);
  const [wordScore, setWordScore] = useState(null);
  const [error, setError]         = useState("");
  const [animCls, setAnimCls]     = useState("slide-in");
  const [recSec, setRecSec]       = useState(0);
  const recRef    = useRef(null);
  const chunksRef = useRef([]);
  const timerRef  = useRef(null);
  const word = words[idx] || null;

  const speakWord = w => { window.speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(w); u.rate=0.8; u.pitch=1; window.speechSynthesis.speak(u); };

  const startRec = async () => {
    setError(""); setResult(null); setWordScore(null); setRecSec(0);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio:{ echoCancellation:true, noiseSuppression:true } });
      const mimeType = ["audio/webm;codecs=opus","audio/webm","audio/ogg"].find(t => MediaRecorder.isTypeSupported(t)) || "";
      const rec = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      recRef.current = rec; chunksRef.current = [];
      rec.ondataavailable = e => { if (e.data?.size > 0) chunksRef.current.push(e.data); };
      rec.onstop = () => {
        stream.getTracks().forEach(t => t.stop()); clearInterval(timerRef.current);
        if (!chunksRef.current.length) { setError("No audio captured."); setPhase("idle"); return; }
        submitRec(new Blob(chunksRef.current, { type: mimeType || "audio/webm" }));
      };
      rec.start(200); setPhase("recording");
      timerRef.current = setInterval(() => setRecSec(s => s + 1), 1000);
    } catch { setError("Microphone access denied."); }
  };

  const stopRec = () => { if (recRef.current?.state !== "inactive") recRef.current.stop(); setPhase("processing"); };

  const submitRec = async blob => {
    const fd = new FormData();
    fd.append("file", new File([blob], "rec.webm", { type: blob.type || "audio/webm" }));
    fd.append("patient_id", String(user.id));
    try {
      const res = await axios.post(`${API}/api/analyze-utterance`, fd, { timeout: 180000 });
      const d = res.data; setResult(d);
      const spoken = (d.s4_final || "").toLowerCase();
      const tgt = word ? word.word.toLowerCase() : "";
      const matched = spoken.includes(tgt);
      let score = 40;
      if (matched) score = d.severity==="Normal"?100:d.severity==="Mild"?85:d.severity==="Moderate"?65:50;
      setWordScore({ score, matched, severity: d.severity });
      if (word) await axios.post(`${API}/api/rehab/score`, { patient_id: user.id, word_id: word.id, score });
      setPhase("result"); onRefresh();
    } catch (err) { setError(`Analysis failed: ${err.response?.data?.detail || err.message}`); setPhase("idle"); }
  };

  const goNext = () => {
    setAnimCls("slide-out");
    setTimeout(() => { setIdx(p => (p+1)%Math.max(words.length,1)); setPhase("idle"); setResult(null); setWordScore(null); setError(""); setAnimCls("slide-in"); }, 280);
  };

  const summary = words.map(w => { const s = rehabData.find(r => r.word===w.word); return { ...w, score:s?.score||0, attempts:s?.attempts||0 }; });

  return (
    <div className="flex flex-col gap-4">

      {/* Word Progress Grid */}
      <Card>
        <SectionHeader Icon={Star} title="Word Progress" />
        <div className="grid gap-2.5" style={{ gridTemplateColumns:"repeat(auto-fill,minmax(120px,1fr))" }}>
          {summary.map((w, i) => {
            const isActive   = w.id === word?.id;
            const isMastered = w.score >= 80;
            return (
              <div key={w.id}
                onClick={() => { setIdx(i); setPhase("idle"); setResult(null); setWordScore(null); setAnimCls("slide-in"); }}
                className={`rounded-xl p-3 cursor-pointer transition-all
                  ${isActive   ? "bg-sky-50 border-2 border-sky-400 ring-2 ring-sky-100"
                  : isMastered ? "bg-emerald-50 border-2 border-emerald-200"
                  :              "bg-slate-50 border-2 border-slate-100 hover:border-sky-200 hover:bg-sky-50"}`}>
                <div className="flex justify-between items-start mb-1">
                  <span className={`font-bold text-sm ${isActive?"text-sky-700":"text-slate-800"}`}>{w.word}</span>
                  {isMastered && <CheckCircle size={13} className="text-emerald-500 flex-shrink-0" />}
                </div>
                <div className="text-[11px] text-slate-400">{w.attempts} attempts</div>
                <div className={`text-[13px] font-bold mt-0.5 ${w.score>=80?"text-emerald-600":w.score>=60?"text-amber-500":"text-slate-400"}`}>
                  {w.score}%
                </div>
              </div>
            );
          })}
          {words.length === 0 && <p className="text-slate-400 text-sm col-span-full">No words assigned yet.</p>}
        </div>
      </Card>

      {/* Practice Zone */}
      {word && (
        <Card className="text-center">
          <SectionHeader Icon={Mic} title="Practice Zone" sub="Pronounce the target word clearly, then stop recording" />

          {/* Progress dots */}
          <div className="flex gap-1.5 justify-center mb-6">
            {words.map((_,i) => (
              <div key={i} className={`h-1.5 rounded-full transition-all duration-300 ${i===idx?"w-6 bg-sky-500":i<idx?"w-1.5 bg-sky-200":"w-1.5 bg-slate-200"}`} />
            ))}
          </div>

          {/* Word card */}
          <div className={`${animCls} mb-5`}>
            <div className="inline-block bg-gradient-to-br from-sky-50 to-blue-100 border-2 border-sky-200 rounded-2xl px-14 py-7 mb-3">
              <div className="text-5xl font-black tracking-tight text-sky-600">{word.word}</div>
            </div>
            <br />
            <button onClick={() => speakWord(word.word)}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-sky-600 border border-sky-200 rounded-full px-4 py-1.5 hover:bg-sky-50 transition">
              <Volume2 size={13} /> Hear it
            </button>
          </div>

          {error && <div className="bg-red-50 border border-red-200 text-red-600 text-sm rounded-xl px-4 py-2.5 mb-4">{error}</div>}

          {phase==="idle" && (
            <button onClick={startRec}
              className="inline-flex items-center gap-2 bg-gradient-to-r from-sky-500 to-cyan-500 text-white font-bold text-sm rounded-full px-8 py-3 shadow-md shadow-sky-200 hover:-translate-y-0.5 hover:shadow-lg transition">
              <Mic size={17} /> Start Recording
            </button>
          )}

          {phase==="recording" && (
            <div className="flex flex-col items-center gap-3">
              <div className="flex items-center gap-2 text-red-500 font-semibold text-sm">
                <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                Recording… {recSec}s — speak clearly now
              </div>
              <button onClick={stopRec}
                className="recording inline-flex items-center gap-2 bg-gradient-to-r from-red-500 to-rose-500 text-white font-bold text-sm rounded-full px-7 py-2.5 shadow-md shadow-red-200">
                <Square size={15} /> Stop &amp; Analyse
              </button>
            </div>
          )}

          {phase==="processing" && (
            <div className="flex items-center justify-center gap-2.5 text-sky-500 font-semibold text-sm">
              <Activity size={18} className="spinner" /> AI pipeline running…
            </div>
          )}

          {phase==="result" && result && wordScore && (
            <div className="pop-in flex flex-col items-center gap-4">
              {wordScore.matched ? (
                <div className={`rounded-full px-7 py-2.5 text-lg font-black border-2
                  ${wordScore.score>=80?"bg-emerald-50 border-emerald-300 text-emerald-700"
                  :wordScore.score>=60?"bg-amber-50 border-amber-300 text-amber-700"
                  :"bg-red-50 border-red-300 text-red-700"}`}>
                  {wordScore.score>=80?"🎉":wordScore.score>=60?"👍":"🔄"} {wordScore.score}% — {wordScore.severity}
                </div>
              ) : (
                <div className="rounded-full px-7 py-2.5 text-lg font-black border-2 bg-red-50 border-red-300 text-red-700">
                  ❌ Wrong Word — Try Again!
                </div>
              )}
              
              <div className="bg-slate-50 border border-slate-200 rounded-xl px-5 py-3.5 text-left max-w-sm w-full">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">You said:</div>
                <p className="text-base font-bold text-slate-800">"{result.s4_final}"</p>
              </div>

              <div className="flex gap-2.5">
                <button onClick={() => { setPhase("idle"); setResult(null); setWordScore(null); }}
                  className={`flex items-center gap-1.5 text-xs font-semibold rounded-full px-6 py-2 transition hover:-translate-y-0.5 ${!wordScore.matched ? "bg-gradient-to-r from-red-500 to-rose-500 text-white shadow-md shadow-red-200" : "bg-white text-slate-500 border border-slate-200 shadow-sm hover:bg-slate-50"}`}>
                  🔄 Retry
                </button>
                {wordScore.matched && (
                  <button onClick={goNext}
                    className="flex items-center gap-1.5 text-xs font-semibold text-white bg-gradient-to-r from-sky-500 to-cyan-500 rounded-full px-6 py-2 shadow-md shadow-sky-200 hover:-translate-y-0.5 transition">
                    Next Word <ChevronRight size={14} />
                  </button>
                )}
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}

/* ════════════════════════════════════════════════
   CLINICIAN DASHBOARD  (all original logic kept)
════════════════════════════════════════════════ */
function ClinicianDashboard({ user }) {
  const [patients, setPatients] = useState([]);
  const [words, setWords]       = useState([]);
  const [newWord, setNewWord]   = useState("");
  const [tab, setTab]           = useState("roster");

  const fetchAll = useCallback(() => {
    axios.get(`${API}/api/patients`).then(r => setPatients(r.data)).catch(console.error);
    axios.get(`${API}/api/words`).then(r => setWords(r.data)).catch(console.error);
  }, []);
  useEffect(() => { fetchAll(); }, [fetchAll]);

  const addWord = async e => {
    e.preventDefault(); if (!newWord.trim()) return;
    try { await axios.post(`${API}/api/add-word`, { word: newWord.trim().toLowerCase(), clinician_id: user.id }); setNewWord(""); fetchAll(); } catch {}
  };

  return (
    <div className="flex flex-col gap-4">
      {/* Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-500 text-white px-6 py-4 flex items-center gap-3 shadow-lg shadow-emerald-200">
        <Users size={24} />
        <div>
          <div className="text-lg font-black">Clinician Dashboard</div>
          <div className="text-xs opacity-75">Manage patients, words and verify audio</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2">
        {[{id:"roster",Icon:Users,label:"Patient Roster"},{id:"words",Icon:Plus,label:"Word Bank"},{id:"tester",Icon:Mic,label:"Verify Audio"}].map(t => (
          <TabBtn key={t.id} active={tab===t.id} onClick={() => setTab(t.id)}><t.Icon size={14} /> {t.label}</TabBtn>
        ))}
      </div>

      {tab==="roster" && (
        <Card className="fade-up overflow-hidden">
          <SectionHeader Icon={Users} title="Multi-Patient Roster" sub="Baseline vs current severity tracking" />
          <div className="overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr>{["Patient","Baseline","Current Severity","Sessions","Last Active"].map(h => (
                  <th key={h} className="text-left text-xs font-semibold text-slate-400 px-3 py-2.5 border-b border-slate-100">{h}</th>
                ))}</tr>
              </thead>
              <tbody>
                {patients.length===0 && <tr><td colSpan={5} className="text-center text-slate-400 py-8">No patients registered yet.</td></tr>}
                {patients.map(p => (
                  <tr key={p.id} className="hover:bg-slate-50 transition">
                    <td className="px-3 py-3 border-b border-slate-50">
                      <div className="flex items-center gap-2.5">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-sky-500 to-cyan-400 flex items-center justify-center text-white text-xs font-black">{p.username[0].toUpperCase()}</div>
                        <span className="font-semibold text-slate-800">{p.username}</span>
                      </div>
                    </td>
                    <td className="px-3 py-3 border-b border-slate-50 text-slate-500 font-medium">{p.baseline_severity}</td>
                    <td className="px-3 py-3 border-b border-slate-50">
                      <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${SEV_CLR[p.latest_severity]?.pill || "bg-slate-100 text-slate-500"}`}>
                        {p.latest_severity || "N/A"}
                      </span>
                    </td>
                    <td className="px-3 py-3 border-b border-slate-50 font-bold text-sky-600">{p.session_count}</td>
                    <td className="px-3 py-3 border-b border-slate-50 text-slate-400 text-xs">
                      {p.last_active !== "Never" ? new Date(p.last_active).toLocaleString() : "Never"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {tab==="words" && (
        <Card className="fade-up">
          <SectionHeader Icon={Plus} title="Word Bank Manager" sub="Add target words for patient rehabilitation sessions" />
          <form onSubmit={addWord} className="flex gap-2.5 mb-4">
            <input value={newWord} onChange={e => setNewWord(e.target.value)} placeholder="Type a word or phrase…"
              className="flex-1 px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-100 transition" />
            <button type="submit"
              className="flex items-center gap-1.5 text-xs font-semibold text-white bg-gradient-to-r from-sky-500 to-cyan-500 rounded-xl px-4 py-2.5 shadow-md shadow-sky-200 hover:-translate-y-0.5 transition">
              <Plus size={14} /> Add Word
            </button>
          </form>
          <div className="flex flex-wrap gap-2">
            {words.map(w => (
              <span key={w.id} className="bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm font-semibold rounded-full px-4 py-1.5">
                {w.word}
              </span>
            ))}
          </div>
        </Card>
      )}

      {tab==="tester" && (
        <Card className="fade-up">
          <SectionHeader Icon={Mic} title="Acoustic Verification Tester" sub="Test phrases yourself — confirm they register as Normal before assigning" />
          <AudioAnalyzer patientId={null} showPipeline={true} />
        </Card>
      )}
    </div>
  );
}
