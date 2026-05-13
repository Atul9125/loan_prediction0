import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import time

st.set_page_config(
    page_title="LoanIQ · Smart Credit Engine",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Syne:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:      #04080e;
    --surface: rgba(255,255,255,0.035);
    --border:  rgba(255,255,255,0.08);
    --teal:    #0ae3c8;
    --teal2:   #00b4a6;
    --gold:    #f5c842;
    --blue:    #3b7bff;
    --purple:  #9b5de5;
    --red:     #ff4b6e;
    --green:   #00e5a0;
    --text:    #dde6f0;
    --muted:   #4a5a6e;
    --dim:     #232f3e;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background: var(--bg);
    color: var(--text);
}

.stApp { background: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Streamlit column padding reset */
div[data-testid="column"] { padding: 0 !important; }

/* Fix columns to sit side by side and not wrap */
div[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    gap: 0 !important;
}

/* LEFT column scrollable */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
    overflow-y: auto !important;
    max-height: 100vh !important;
}

/* RIGHT column fixed height, no overflow */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
    position: sticky !important;
    top: 0 !important;
    height: 100vh !important;
    overflow-y: auto !important;
    border-left: 1px solid var(--border) !important;
    background: rgba(5,9,16,0.98) !important;
    flex-shrink: 0 !important;
}

/* ── BACKGROUND ── */
.bg-canvas { position:fixed; inset:0; z-index:0; overflow:hidden; pointer-events:none; }
.mesh { position:absolute; border-radius:50%; filter:blur(100px); opacity:0.12; }
.mesh-1 { width:600px;height:600px; background:radial-gradient(circle,#0ae3c8,transparent); top:-200px;left:-150px; animation:d1 16s ease-in-out infinite; }
.mesh-2 { width:500px;height:500px; background:radial-gradient(circle,#9b5de5,transparent); bottom:-100px;right:400px; animation:d2 20s ease-in-out infinite; }
.mesh-3 { width:300px;height:300px; background:radial-gradient(circle,#f5c842,transparent); top:45%;left:35%; animation:d3 14s ease-in-out infinite; }
.grid-bg { position:absolute;inset:0; background-image:linear-gradient(rgba(255,255,255,0.015) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.015) 1px,transparent 1px); background-size:48px 48px; }
@keyframes d1{0%,100%{transform:translate(0,0)}50%{transform:translate(60px,-80px)}}
@keyframes d2{0%,100%{transform:translate(0,0)}50%{transform:translate(-50px,60px)}}
@keyframes d3{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,-40px)}}

/* ── HEADER ── */
.site-header {
    padding:18px 48px; display:flex; align-items:center; justify-content:space-between;
    border-bottom:1px solid var(--border); background:rgba(4,8,14,0.9);
    backdrop-filter:blur(20px); position:relative; z-index:10;
}
.brand { display:flex; align-items:center; gap:12px; }
.brand-logo { width:36px;height:36px; background:linear-gradient(135deg,var(--teal),var(--blue)); border-radius:10px; font-size:16px; display:flex;align-items:center;justify-content:center; box-shadow:0 0 20px rgba(10,227,200,0.35); }
.brand-name { font-family:'DM Serif Display',serif; font-size:19px; background:linear-gradient(90deg,#fff 40%,var(--teal)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.brand-tag { font-size:9px;font-weight:700;letter-spacing:3px;text-transform:uppercase; color:var(--teal); border:1px solid rgba(10,227,200,0.3); background:rgba(10,227,200,0.07); padding:4px 12px;border-radius:99px; }
.hdr-right { display:flex;gap:10px;align-items:center; }
.sdot { width:7px;height:7px;border-radius:50%; background:var(--green); box-shadow:0 0 8px var(--green); animation:pdot 2s ease-in-out infinite; }
@keyframes pdot{0%,100%{opacity:1}50%{opacity:0.4}}
.stxt { font-size:10px;color:var(--muted);font-weight:600;letter-spacing:1.5px;text-transform:uppercase; }

/* ── HERO ── */
.hero { padding:44px 48px 28px; position:relative;z-index:2; }
.hero-eye { font-size:10px;font-weight:700;letter-spacing:4px;text-transform:uppercase; color:var(--teal); margin-bottom:14px; display:flex;align-items:center;gap:12px; }
.hero-eye::before { content:'';width:32px;height:1px; background:linear-gradient(90deg,transparent,var(--teal)); }
.hero-title { font-family:'DM Serif Display',serif; font-size:48px;line-height:1.08; color:#fff;margin-bottom:14px;letter-spacing:-1px; }
.hero-title em { font-style:italic; background:linear-gradient(90deg,var(--teal),var(--blue),var(--purple)); -webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.hero-desc { font-size:14px;color:var(--muted);line-height:1.9;max-width:420px; }
.hdiv { height:1px; margin:0 48px; background:linear-gradient(90deg,transparent,var(--border),transparent); position:relative;z-index:2; }

/* ── STATS ── */
.topbar { display:flex;gap:10px;padding:18px 48px; position:relative;z-index:2; }
.sc { flex:1;border-radius:14px;background:var(--surface);border:1px solid var(--border);padding:16px 14px;text-align:center;transition:all 0.3s; }
.sc:hover { border-color:rgba(10,227,200,0.3);transform:translateY(-2px); }
.sv { font-family:'DM Serif Display',serif;font-size:24px;display:block; background:linear-gradient(135deg,var(--teal),var(--gold)); -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px; }
.sl { font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--dim); }

/* ── FORM ── */
.form-area { padding:20px 48px 60px; position:relative;z-index:2; }
.sh { display:flex;align-items:center;gap:14px;margin:26px 0 16px; }
.sbadge { width:28px;height:28px; background:linear-gradient(135deg,var(--teal),var(--blue)); border-radius:8px;color:var(--bg);font-size:12px;font-weight:800; display:flex;align-items:center;justify-content:center; box-shadow:0 0 16px rgba(10,227,200,0.4); }
.slabel { font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#536070; }
.srule { flex:1;height:1px;background:var(--border); }

/* ── WIDGET OVERRIDES ── */
div[data-testid="stSelectbox"]>label,
div[data-testid="stNumberInput"]>label,
div[data-testid="stSlider"]>label,
div[data-testid="stRadio"]>label {
    color:#4a6070 !important;font-size:10px !important;font-weight:700 !important;
    letter-spacing:2.5px !important;text-transform:uppercase !important;
    margin-bottom:8px !important;font-family:'Syne',sans-serif !important;
}
.stSelectbox>div>div, input[type="number"] {
    background:rgba(255,255,255,0.04) !important;border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:12px !important;color:var(--text) !important;
    font-family:'Syne',sans-serif !important;font-size:14px !important;
}
.stSelectbox>div>div:hover { border-color:rgba(10,227,200,0.4) !important; }
input[type="number"]:focus { border-color:var(--teal) !important;box-shadow:0 0 0 3px rgba(10,227,200,0.12) !important;outline:none !important; }
div[data-testid="stRadio"]>div { flex-direction:row !important;gap:8px !important;flex-wrap:wrap !important; }
div[data-testid="stRadio"] label {
    background:rgba(255,255,255,0.03) !important;border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:10px !important;padding:8px 18px !important;cursor:pointer !important;
    color:#536070 !important;font-size:12px !important;font-weight:600 !important;
    font-family:'Syne',sans-serif !important;transition:all 0.2s !important;
}
div[data-testid="stRadio"] label:hover { border-color:rgba(10,227,200,0.4) !important;color:var(--teal) !important;background:rgba(10,227,200,0.06) !important; }
div[data-testid="stSlider"]>div>div>div { background:var(--teal) !important; }
div[data-testid="stSlider"]>div>div { background:rgba(255,255,255,0.08) !important; }

/* ── PREDICT BUTTON ── */
div[data-testid="stButton"] > button {
    font-family:'Syne',sans-serif !important;transition:all 0.3s !important;cursor:pointer !important;
}
.stButton > button {
    background:linear-gradient(135deg,var(--teal2),var(--blue)) !important;
    color:#04080e !important;border:none !important;border-radius:14px !important;
    padding:16px 48px !important;font-size:12px !important;font-weight:800 !important;
    letter-spacing:3px !important;text-transform:uppercase !important;
    width:100% !important;margin-top:24px !important;
    box-shadow:0 6px 28px rgba(10,227,200,0.35) !important;
}
.stButton > button:hover {
    transform:translateY(-3px) !important;
    box-shadow:0 14px 40px rgba(10,227,200,0.5) !important;
}

/* ── RESULT PANEL STYLES ── */
.rp { padding:36px 28px; }
.rp-label { font-size:9px;font-weight:700;letter-spacing:3.5px;text-transform:uppercase; color:var(--dim);margin-bottom:28px;display:flex;align-items:center;gap:10px; }
.rp-label::after { content:'';flex:1;height:1px;background:var(--border); }

/* idle */
.idle { display:flex;flex-direction:column;align-items:center;justify-content:center; min-height:70vh;text-align:center;padding:20px; }
.idle-ring { position:relative;width:100px;height:100px;margin:0 auto 26px; }
.idle-ring::before,.idle-ring::after { content:'';position:absolute;border-radius:50%;border:1px dashed;animation:sr 20s linear infinite; }
.idle-ring::before { inset:-10px;border-color:rgba(10,227,200,0.2); }
.idle-ring::after  { inset:-20px;border-color:rgba(245,200,66,0.15);animation-direction:reverse;animation-duration:30s; }
@keyframes sr{to{transform:rotate(360deg)}}
.idle-box { width:100px;height:100px;border-radius:24px;font-size:38px; background:linear-gradient(145deg,rgba(10,227,200,0.08),rgba(59,123,255,0.08)); border:1px solid rgba(10,227,200,0.2); display:flex;align-items:center;justify-content:center; }
.idle-title { font-family:'DM Serif Display',serif;font-size:22px;color:var(--dim);margin-bottom:10px; }
.idle-sub { font-size:13px;color:#2a3a4a;line-height:1.8; }
.idle-sub b { color:#3a5060; }

/* verdict */
.vw { border-radius:20px;padding:28px 20px;text-align:center;margin-bottom:20px;position:relative;overflow:hidden; }
.vw.approved { background:linear-gradient(145deg,rgba(0,229,160,0.1),rgba(0,180,166,0.04));border:1px solid rgba(0,229,160,0.25); }
.vw.rejected { background:linear-gradient(145deg,rgba(255,75,110,0.1),rgba(200,28,60,0.04));border:1px solid rgba(255,75,110,0.25); }
.vglow { position:absolute;top:-80px;left:50%;transform:translateX(-50%);width:200px;height:200px;border-radius:50%;filter:blur(60px);opacity:0.2;pointer-events:none; }
.approved .vglow { background:var(--green); }
.rejected .vglow { background:var(--red); }
.vicon { width:68px;height:68px;border-radius:18px;margin:0 auto 14px;display:flex;align-items:center;justify-content:center;font-size:28px; }
.approved .vicon { background:rgba(0,229,160,0.12);border:1px solid rgba(0,229,160,0.3);box-shadow:0 0 30px rgba(0,229,160,0.2); }
.rejected .vicon { background:rgba(255,75,110,0.12);border:1px solid rgba(255,75,110,0.3);box-shadow:0 0 30px rgba(255,75,110,0.2); }
.vverdict { font-family:'DM Serif Display',serif;font-size:28px;margin-bottom:8px; }
.approved .vverdict { color:var(--green); }
.rejected .vverdict { color:var(--red); }
.vdesc { font-size:12px;color:var(--muted);margin-bottom:14px;line-height:1.6; }
.rbadge { display:inline-flex;align-items:center;gap:6px;padding:5px 14px;border-radius:99px;font-size:9px;font-weight:800;letter-spacing:2px;text-transform:uppercase; }
.rl { background:rgba(0,229,160,0.1);color:var(--green);border:1px solid rgba(0,229,160,0.3); }
.rm { background:rgba(245,200,66,0.1);color:var(--gold);border:1px solid rgba(245,200,66,0.3); }
.rh { background:rgba(255,75,110,0.1);color:var(--red);border:1px solid rgba(255,75,110,0.3); }

/* prob bars */
.pb { margin:20px 0; }
.pi { margin-bottom:14px; }
.pm { display:flex;justify-content:space-between;align-items:baseline;margin-bottom:7px; }
.pl { font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted); }
.pp { font-family:'DM Serif Display',serif;font-size:20px; }
.pp.teal { color:var(--teal); }
.pp.red  { color:var(--red); }
.pbar { height:5px;border-radius:99px;background:rgba(255,255,255,0.05);overflow:hidden; }
.pfill { height:100%;border-radius:99px; }
.ft { background:linear-gradient(90deg,var(--teal2),var(--teal));box-shadow:0 0 10px rgba(10,227,200,0.5); }
.fr { background:linear-gradient(90deg,#c81c3c,var(--red));box-shadow:0 0 10px rgba(255,75,110,0.5); }

/* summary */
.stitle { font-size:9px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--dim);margin:20px 0 12px;display:flex;align-items:center;gap:10px; }
.stitle::after { content:'';flex:1;height:1px;background:var(--border); }
.sgrid { display:grid;grid-template-columns:1fr 1fr;gap:8px; }
.scell { background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px 14px;transition:all 0.2s; }
.scell:hover { border-color:rgba(10,227,200,0.25); }
.sk { font-size:8px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--dim);margin-bottom:4px; }
.sv2 { font-size:13px;font-weight:600;color:#c0cdd8; }

/* new app button in result panel */
.new-btn {
    display:block;width:100%;margin-top:20px;padding:11px;
    background:rgba(255,255,255,0.03);color:var(--muted);
    border:1px solid rgba(255,255,255,0.07);border-radius:10px;
    font-family:'Syne',sans-serif;font-size:10px;font-weight:700;
    letter-spacing:2px;text-transform:uppercase;
    cursor:pointer;transition:all 0.2s;text-align:center;
    text-decoration:none;
}
.new-btn:hover { border-color:rgba(10,227,200,0.3);color:var(--teal); }
</style>
""", unsafe_allow_html=True)

# ── Load Model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = os.path.join(os.path.dirname(__file__), "model_rf.joblib")
    return joblib.load(path)

model = load_model()

SUBGRADE_MAP = {
    'A1':1,'A2':2,'A3':3,'A4':4,'A5':5,
    'B1':6,'B2':7,'B3':8,'B4':9,'B5':10,
    'C1':11,'C2':12,'C3':13,'C4':14,'C5':15,
    'D1':16,'D2':17,'D3':18,'D4':19,'D5':20,
    'E1':21,'E2':22,'E3':23,'E4':24,'E5':25,
    'F1':26,'F2':27,'F3':28,'F4':29,'F5':30,
    'G1':31,'G2':32,'G3':33,'G4':34,'G5':35,
}
VERIF_MAP = {'Not Verified':0,'Verified':1,'Source Verified':2}
TERM_MAP  = {'36 months':36,'60 months':60}

# ── Session State ──────────────────────────────────────────────────────────────
for k, v in [("prediction",None),("probability",None),("input_summary",{})]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Result HTML builder ────────────────────────────────────────────────────────
def result_html():
    if st.session_state.prediction is None:
        return """
<div class="idle">
  <div class="idle-ring"><div class="idle-box">🏦</div></div>
  <div class="idle-title">Awaiting Analysis</div>
  <div class="idle-sub">Fill in the form and click<br><b>Analyze &amp; Predict</b><br>to get your instant AI decision.</div>
</div>"""

    pred  = st.session_state.prediction
    proba = st.session_state.probability
    sm    = st.session_state.input_summary

    approved    = (pred == 0)
    ap          = round(proba[0]*100, 1)
    rp          = round(proba[1]*100, 1)
    vcls        = "approved" if approved else "rejected"
    icon        = "✅" if approved else "❌"
    label       = "APPROVED" if approved else "REJECTED"
    desc        = "Meets all lending criteria." if approved else "Does not meet lending criteria."
    rcls, rtxt  = ("rl","🟢 Low Risk") if ap>=75 else (("rm","🟡 Moderate") if ap>=45 else ("rh","🔴 High Risk"))

    cells = "".join(
        f'<div class="scell"><div class="sk">{k}</div><div class="sv2">{v}</div></div>'
        for k,v in sm.items()
    )

    return f"""
<div class="vw {vcls}">
  <div class="vglow"></div>
  <div class="vicon">{icon}</div>
  <div class="vverdict">{label}</div>
  <div class="vdesc">{desc}</div>
  <span class="rbadge {rcls}">{rtxt}</span>
</div>
<div class="pb">
  <div class="pi">
    <div class="pm"><span class="pl">Approval Probability</span><span class="pp teal">{ap}%</span></div>
    <div class="pbar"><div class="pfill ft" style="width:{ap}%"></div></div>
  </div>
  <div class="pi">
    <div class="pm"><span class="pl">Rejection Probability</span><span class="pp red">{rp}%</span></div>
    <div class="pbar"><div class="pfill fr" style="width:{rp}%"></div></div>
  </div>
</div>
<div class="stitle">Application Summary</div>
<div class="sgrid">{cells}</div>
"""

# ══════════════════════════════════════════════════════════════════════════════
# PAGE RENDER
# ══════════════════════════════════════════════════════════════════════════════

# Background
st.markdown("""
<div class="bg-canvas">
  <div class="grid-bg"></div>
  <div class="mesh mesh-1"></div>
  <div class="mesh mesh-2"></div>
  <div class="mesh mesh-3"></div>
</div>""", unsafe_allow_html=True)

# ── Two column layout ──────────────────────────────────────────────────────────
left, right = st.columns([62, 38])

# ══ RIGHT COLUMN — pure HTML only, no widgets ══════════════════════════════════
with right:
    st.markdown(f"""
<div class="rp">
  <div class="rp-label">Prediction Result</div>
  {result_html()}
</div>""", unsafe_allow_html=True)

# ══ LEFT COLUMN — all the form ════════════════════════════════════════════════
with left:
    # Header
    st.markdown("""
<div class="site-header">
  <div class="brand">
    <div class="brand-logo">💎</div>
    <div class="brand-name">LoanIQ</div>
  </div>
  <div class="hdr-right">
    <div class="sdot"></div>
    <span class="stxt">Model Online</span>
    <div class="brand-tag">AI Credit Engine</div>
  </div>
</div>""", unsafe_allow_html=True)

    # Hero
    st.markdown("""
<div class="hero">
  <div class="hero-eye">Instant Decision &nbsp;·&nbsp; ML Powered &nbsp;·&nbsp; 25 Features</div>
  <div class="hero-title">Will your loan<br>get <em>approved?</em></div>
  <div class="hero-desc">Our Random Forest model analyzes 25 financial signals to predict your loan outcome in under 2 seconds.</div>
</div>
<div class="hdiv"></div>
<div class="topbar">
  <div class="sc"><span class="sv">25</span><span class="sl">Signal Features</span></div>
  <div class="sc"><span class="sv">RF</span><span class="sl">Random Forest</span></div>
  <div class="sc"><span class="sv">A1–G5</span><span class="sl">Grade Range</span></div>
  <div class="sc"><span class="sv">&lt;2s</span><span class="sl">Decision Time</span></div>
</div>
<div class="hdiv"></div>
""", unsafe_allow_html=True)

    # Form
    st.markdown('<div class="form-area">', unsafe_allow_html=True)

    st.markdown('<div class="sh"><div class="sbadge">1</div><div class="slabel">Loan Details</div><div class="srule"></div></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        loan_amnt = st.number_input("Loan Amount ($)", min_value=500, max_value=40000, value=10000, step=500)
    with c2:
        term = st.selectbox("Loan Term", list(TERM_MAP.keys()))
    c3, c4 = st.columns(2)
    with c3:
        sub_grade = st.selectbox("Credit Sub-Grade", list(SUBGRADE_MAP.keys()), index=4)
    with c4:
        purpose = st.selectbox("Loan Purpose", [
            "debt_consolidation","credit_card","home_improvement","other",
            "major_purchase","medical","small_business","car","vacation",
            "moving","house","wedding","renewable_energy"
        ])

    st.markdown('<div class="sh"><div class="sbadge">2</div><div class="slabel">Applicant Profile</div><div class="srule"></div></div>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        emp_length = st.slider("Employment Length (years)", 0, 10, 3)
    with c6:
        home_ownership = st.radio("Home Ownership", ["RENT","MORTGAGE","OWN","OTHER"], horizontal=True)
    verification_status = st.radio("Income Verification", list(VERIF_MAP.keys()), horizontal=True)

    st.markdown('<div class="sh"><div class="sbadge">3</div><div class="slabel">Credit History</div><div class="srule"></div></div>', unsafe_allow_html=True)
    c7, c8, c9, c10 = st.columns(4)
    with c7:
        delinq_2yrs = st.number_input("Delinquencies (2yr)", min_value=0, max_value=30, value=0)
    with c8:
        pub_rec = st.number_input("Public Records", min_value=0, max_value=20, value=0)
    with c9:
        collections_12_mths = st.number_input("Collections (12mo)", min_value=0, max_value=20, value=0)
    with c10:
        acc_now_delinq = st.number_input("Accts Delinquent", min_value=0, max_value=20, value=0)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  Analyze & Predict"):
        with st.spinner("Running AI model..."):
            time.sleep(0.5)
        purpose_cols = ["car","credit_card","debt_consolidation","home_improvement",
                        "house","major_purchase","medical","moving","other",
                        "renewable_energy","small_business","vacation","wedding"]
        features = pd.DataFrame([{
            'loan_amnt': loan_amnt,
            'term': TERM_MAP[term],
            'sub_grade': SUBGRADE_MAP[sub_grade],
            'emp_length': emp_length,
            'verification_status': VERIF_MAP[verification_status],
            'delinq_2yrs': delinq_2yrs,
            'pub_rec': pub_rec,
            'collections_12_mths_ex_med': collections_12_mths,
            'acc_now_delinq': acc_now_delinq,
            'home_ownership_MORTGAGE': 1 if home_ownership=="MORTGAGE" else 0,
            'home_ownership_OWN':      1 if home_ownership=="OWN"      else 0,
            'home_ownership_RENT':     1 if home_ownership=="RENT"     else 0,
            **{f'purpose_{p}':(1 if p==purpose else 0) for p in purpose_cols}
        }])
        pred  = model.predict(features)[0]
        proba = model.predict_proba(features)[0]
        st.session_state.prediction  = int(pred)
        st.session_state.probability = proba.tolist()
        st.session_state.input_summary = {
            "Amount": f"${loan_amnt:,}", "Term": term,
            "Sub-Grade": sub_grade,
            "Purpose": purpose.replace("_"," ").title(),
            "Employment": f"{emp_length} yrs", "Ownership": home_ownership,
        }
        st.rerun()

    if st.session_state.prediction is not None:
        if st.button("↩ New Application"):
            st.session_state.prediction  = None
            st.session_state.probability = None
            st.session_state.input_summary = {}
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
