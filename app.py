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

.stApp { background: var(--bg) !important; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }

/* ── BACKGROUND ── */
.bg-canvas { position:fixed; inset:0; z-index:0; overflow:hidden; pointer-events:none; }
.mesh { position:absolute; border-radius:50%; filter:blur(100px); opacity:0.12; }
.mesh-1 { width:600px;height:600px;background:radial-gradient(circle,#0ae3c8,transparent);top:-200px;left:-150px;animation:d1 16s ease-in-out infinite; }
.mesh-2 { width:500px;height:500px;background:radial-gradient(circle,#9b5de5,transparent);bottom:-100px;right:100px;animation:d2 20s ease-in-out infinite; }
.mesh-3 { width:300px;height:300px;background:radial-gradient(circle,#f5c842,transparent);top:45%;left:35%;animation:d3 14s ease-in-out infinite; }
.grid-bg { position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.015) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.015) 1px,transparent 1px);background-size:48px 48px; }
@keyframes d1{0%,100%{transform:translate(0,0)}50%{transform:translate(60px,-80px)}}
@keyframes d2{0%,100%{transform:translate(0,0)}50%{transform:translate(-50px,60px)}}
@keyframes d3{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,-40px)}}

/* ── LEFT PANEL ── */
.left-panel { padding: 0; }

/* ── HEADER ── */
.site-header { padding:18px 32px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border);background:rgba(4,8,14,0.9);backdrop-filter:blur(20px);position:relative;z-index:10; }
.brand { display:flex;align-items:center;gap:12px; }
.brand-logo { width:36px;height:36px;background:linear-gradient(135deg,var(--teal),var(--blue));border-radius:10px;font-size:16px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba(10,227,200,0.35); }
.brand-name { font-family:'DM Serif Display',serif;font-size:19px;background:linear-gradient(90deg,#fff 40%,var(--teal));-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.brand-tag { font-size:9px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--teal);border:1px solid rgba(10,227,200,0.3);background:rgba(10,227,200,0.07);padding:4px 12px;border-radius:99px; }
.hdr-right { display:flex;gap:10px;align-items:center; }
.sdot { width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:pdot 2s ease-in-out infinite; }
@keyframes pdot{0%,100%{opacity:1}50%{opacity:0.4}}
.stxt { font-size:10px;color:var(--muted);font-weight:600;letter-spacing:1.5px;text-transform:uppercase; }

/* ── HERO ── */
.hero { padding:32px 32px 20px;position:relative;z-index:2; }
.hero-eye { font-size:10px;font-weight:700;letter-spacing:4px;text-transform:uppercase;color:var(--teal);margin-bottom:12px;display:flex;align-items:center;gap:12px; }
.hero-eye::before { content:'';width:32px;height:1px;background:linear-gradient(90deg,transparent,var(--teal)); }
.hero-title { font-family:'DM Serif Display',serif;font-size:38px;line-height:1.08;color:#fff;margin-bottom:12px;letter-spacing:-1px; }
.hero-title em { font-style:italic;background:linear-gradient(90deg,var(--teal),var(--blue),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.hero-desc { font-size:13px;color:var(--muted);line-height:1.8; }
.hdiv { height:1px;margin:0 32px;background:linear-gradient(90deg,transparent,var(--border),transparent);position:relative;z-index:2; }

/* ── STATS ── */
.topbar { display:flex;gap:8px;padding:14px 32px;position:relative;z-index:2; }
.sc { flex:1;border-radius:12px;background:var(--surface);border:1px solid var(--border);padding:12px 10px;text-align:center;transition:all 0.3s; }
.sc:hover { border-color:rgba(10,227,200,0.3);transform:translateY(-2px); }
.sv { font-family:'DM Serif Display',serif;font-size:20px;display:block;background:linear-gradient(135deg,var(--teal),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:3px; }
.sl { font-size:8px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--dim); }

/* ── SECTION HEADERS ── */
.sh { display:flex;align-items:center;gap:12px;margin:20px 0 12px;position:relative;z-index:2; }
.sbadge { width:26px;height:26px;background:linear-gradient(135deg,var(--teal),var(--blue));border-radius:8px;color:var(--bg);font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 0 16px rgba(10,227,200,0.4);flex-shrink:0; }
.slabel { font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#536070; }
.srule { flex:1;height:1px;background:var(--border); }

/* ── FORM AREA ── */
.form-area { padding:0 32px 40px;position:relative;z-index:2; }

/* ── WIDGET OVERRIDES ── */
div[data-testid="stSelectbox"]>label,
div[data-testid="stNumberInput"]>label,
div[data-testid="stSlider"]>label,
div[data-testid="stRadio"]>label {
    color:#4a6070 !important;font-size:10px !important;font-weight:700 !important;
    letter-spacing:2.5px !important;text-transform:uppercase !important;
    margin-bottom:6px !important;font-family:'Syne',sans-serif !important;
}
.stSelectbox>div>div, input[type="number"] {
    background:rgba(255,255,255,0.04) !important;border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:12px !important;color:var(--text) !important;
    font-family:'Syne',sans-serif !important;font-size:14px !important;
}
.stSelectbox>div>div:hover { border-color:rgba(10,227,200,0.4) !important; }
div[data-testid="stRadio"]>div { flex-direction:row !important;gap:8px !important;flex-wrap:wrap !important; }
div[data-testid="stRadio"] label {
    background:rgba(255,255,255,0.03) !important;border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:10px !important;padding:7px 16px !important;cursor:pointer !important;
    color:#536070 !important;font-size:12px !important;font-weight:600 !important;transition:all 0.2s !important;
}
div[data-testid="stRadio"] label:hover { border-color:rgba(10,227,200,0.4) !important;color:var(--teal) !important; }
div[data-testid="stSlider"]>div>div>div { background:var(--teal) !important; }
div[data-testid="stSlider"]>div>div { background:rgba(255,255,255,0.08) !important; }

/* ── BUTTON ── */
.stButton > button {
    background:linear-gradient(135deg,var(--teal2),var(--blue)) !important;
    color:#04080e !important;border:none !important;border-radius:14px !important;
    padding:14px 40px !important;font-size:12px !important;font-weight:800 !important;
    letter-spacing:3px !important;text-transform:uppercase !important;
    width:100% !important;margin-top:16px !important;
    box-shadow:0 6px 28px rgba(10,227,200,0.35) !important;transition:all 0.3s !important;
}
.stButton > button:hover { transform:translateY(-3px) !important;box-shadow:0 14px 40px rgba(10,227,200,0.5) !important; }

/* ── RIGHT PANEL ── */
.rp-outer {
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    border-left: 1px solid var(--border);
    background: rgba(4,8,14,0.97);
    backdrop-filter: blur(20px);
    padding: 28px 22px;
}
.rp-label { font-size:9px;font-weight:700;letter-spacing:3.5px;text-transform:uppercase;color:var(--dim);margin-bottom:22px;display:flex;align-items:center;gap:10px; }
.rp-label::after { content:'';flex:1;height:1px;background:var(--border); }

/* idle */
.idle { display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:75vh;text-align:center;padding:16px; }
.idle-ring { position:relative;width:90px;height:90px;margin:0 auto 22px; }
.idle-ring::before,.idle-ring::after { content:'';position:absolute;border-radius:50%;border:1px dashed;animation:sr 20s linear infinite; }
.idle-ring::before { inset:-10px;border-color:rgba(10,227,200,0.2); }
.idle-ring::after  { inset:-20px;border-color:rgba(245,200,66,0.15);animation-direction:reverse;animation-duration:30s; }
@keyframes sr{to{transform:rotate(360deg)}}
.idle-box { width:90px;height:90px;border-radius:22px;font-size:34px;background:linear-gradient(145deg,rgba(10,227,200,0.08),rgba(59,123,255,0.08));border:1px solid rgba(10,227,200,0.2);display:flex;align-items:center;justify-content:center; }
.idle-title { font-family:'DM Serif Display',serif;font-size:20px;color:var(--dim);margin-bottom:8px; }
.idle-sub { font-size:12px;color:#2a3a4a;line-height:1.8; }
.idle-sub b { color:#3a5060; }

/* verdict */
.vw { border-radius:18px;padding:24px 18px;text-align:center;margin-bottom:18px;position:relative;overflow:hidden; }
.vw.approved { background:linear-gradient(145deg,rgba(0,229,160,0.1),rgba(0,180,166,0.04));border:1px solid rgba(0,229,160,0.25); }
.vw.rejected { background:linear-gradient(145deg,rgba(255,75,110,0.1),rgba(200,28,60,0.04));border:1px solid rgba(255,75,110,0.25); }
.vglow { position:absolute;top:-80px;left:50%;transform:translateX(-50%);width:200px;height:200px;border-radius:50%;filter:blur(60px);opacity:0.2;pointer-events:none; }
.approved .vglow { background:var(--green); } .rejected .vglow { background:var(--red); }
.vicon { width:60px;height:60px;border-radius:16px;margin:0 auto 12px;display:flex;align-items:center;justify-content:center;font-size:26px; }
.approved .vicon { background:rgba(0,229,160,0.12);border:1px solid rgba(0,229,160,0.3);box-shadow:0 0 24px rgba(0,229,160,0.2); }
.rejected .vicon { background:rgba(255,75,110,0.12);border:1px solid rgba(255,75,110,0.3);box-shadow:0 0 24px rgba(255,75,110,0.2); }
.vverdict { font-family:'DM Serif Display',serif;font-size:26px;margin-bottom:6px; }
.approved .vverdict { color:var(--green); } .rejected .vverdict { color:var(--red); }
.vdesc { font-size:11px;color:var(--muted);margin-bottom:12px;line-height:1.6; }
.rbadge { display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:99px;font-size:9px;font-weight:800;letter-spacing:2px;text-transform:uppercase; }
.rl { background:rgba(0,229,160,0.1);color:var(--green);border:1px solid rgba(0,229,160,0.3); }
.rm { background:rgba(245,200,66,0.1);color:var(--gold);border:1px solid rgba(245,200,66,0.3); }
.rh { background:rgba(255,75,110,0.1);color:var(--red);border:1px solid rgba(255,75,110,0.3); }

/* prob bars */
.pb { margin:16px 0; }
.pi { margin-bottom:12px; }
.pm { display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px; }
.pl { font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted); }
.pp { font-family:'DM Serif Display',serif;font-size:18px; }
.pp.teal { color:var(--teal); } .pp.red { color:var(--red); }
.pbar { height:4px;border-radius:99px;background:rgba(255,255,255,0.05);overflow:hidden; }
.pfill { height:100%;border-radius:99px; }
.ft { background:linear-gradient(90deg,var(--teal2),var(--teal));box-shadow:0 0 10px rgba(10,227,200,0.5); }
.fr { background:linear-gradient(90deg,#c81c3c,var(--red));box-shadow:0 0 10px rgba(255,75,110,0.5); }

/* summary */
.stitle { font-size:9px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--dim);margin:16px 0 10px;display:flex;align-items:center;gap:10px; }
.stitle::after { content:'';flex:1;height:1px;background:var(--border); }
.sgrid { display:grid;grid-template-columns:1fr 1fr;gap:7px; }
.scell { background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 12px;transition:all 0.2s; }
.scell:hover { border-color:rgba(10,227,200,0.25); }
.sk { font-size:8px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--dim);margin-bottom:3px; }
.sv2 { font-size:12px;font-weight:600;color:#c0cdd8; }

/* CRITICAL: make columns sit side by side, right panel sticky */
div[data-testid="stHorizontalBlock"] {
    align-items: flex-start !important;
    gap: 0 !important;
    flex-wrap: nowrap !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load Model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = os.path.join(os.path.dirname(__file__), "model_rf.joblib")
    if not os.path.exists(path):
        return None
    return joblib.load(path)

model = load_model()

SUBGRADE_MAP = {g+str(n): i*5+n for i,g in enumerate('ABCDEFG') for n in range(1,6)}
VERIF_MAP = {'Not Verified':0,'Verified':1,'Source Verified':2}
TERM_MAP  = {'36 months':36,'60 months':60}

for k, v in [("prediction",None),("probability",None),("input_summary",{})]:
    if k not in st.session_state:
        st.session_state[k] = v

def result_html():
    if st.session_state.prediction is None:
        return """<div class="idle">
  <div class="idle-ring"><div class="idle-box">🏦</div></div>
  <div class="idle-title">Awaiting Analysis</div>
  <div class="idle-sub">Fill in the form and click<br><b>Analyze &amp; Predict</b><br>to get your instant AI decision.</div>
</div>"""
    pred  = st.session_state.prediction
    proba = st.session_state.probability
    sm    = st.session_state.input_summary
    approved = (pred == 0)
    ap = round(proba[0]*100, 1)
    rp = round(proba[1]*100, 1)
    vcls = "approved" if approved else "rejected"
    icon = "✅" if approved else "❌"
    label = "APPROVED" if approved else "REJECTED"
    desc = "Meets all lending criteria." if approved else "Does not meet lending criteria."
    rcls, rtxt = ("rl","🟢 Low Risk") if ap>=75 else (("rm","🟡 Moderate") if ap>=45 else ("rh","🔴 High Risk"))
    cells = "".join(f'<div class="scell"><div class="sk">{k}</div><div class="sv2">{v}</div></div>' for k,v in sm.items())
    return f"""<div class="vw {vcls}">
  <div class="vglow"></div><div class="vicon">{icon}</div>
  <div class="vverdict">{label}</div><div class="vdesc">{desc}</div>
  <span class="rbadge {rcls}">{rtxt}</span>
</div>
<div class="pb">
  <div class="pi"><div class="pm"><span class="pl">Approval Probability</span><span class="pp teal">{ap}%</span></div><div class="pbar"><div class="pfill ft" style="width:{ap}%"></div></div></div>
  <div class="pi"><div class="pm"><span class="pl">Rejection Probability</span><span class="pp red">{rp}%</span></div><div class="pbar"><div class="pfill fr" style="width:{rp}%"></div></div></div>
</div>
<div class="stitle">Application Summary</div>
<div class="sgrid">{cells}</div>"""

# ══════════════════════════════════════════════════════════════════════════════
# BACKGROUND
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="bg-canvas">
  <div class="grid-bg"></div>
  <div class="mesh mesh-1"></div><div class="mesh mesh-2"></div><div class="mesh mesh-3"></div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN 2-COLUMN LAYOUT  (60% left form | 40% right result)
# ══════════════════════════════════════════════════════════════════════════════
left, right = st.columns([60, 40])

# ── RIGHT COLUMN (rendered first so it's sticky at top) ────────────────────
with right:
    st.markdown(f"""
<div class="rp-outer">
  <div class="rp-label">Prediction Result</div>
  {result_html()}
</div>""", unsafe_allow_html=True)

# ── LEFT COLUMN ────────────────────────────────────────────────────────────
with left:
    # Header
    st.markdown("""
<div class="site-header">
  <div class="brand">
    <div class="brand-logo">💎</div>
    <div class="brand-name">LoanIQ</div>
  </div>
  <div class="hdr-right">
    <div class="sdot"></div><span class="stxt">Model Online</span>
    <div class="brand-tag">AI Credit Engine</div>
  </div>
</div>
<div class="hero">
  <div class="hero-eye">Instant Decision · ML Powered · 25 Features</div>
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
<div class="form-area">
  <div class="sh"><div class="sbadge">1</div><div class="slabel">Loan Details</div><div class="srule"></div></div>
</div>""", unsafe_allow_html=True)

    # ── FORM INPUTS ──
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

    st.markdown('<div class="form-area"><div class="sh"><div class="sbadge">2</div><div class="slabel">Applicant Profile</div><div class="srule"></div></div></div>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        emp_length = st.slider("Employment Length (years)", 0, 10, 3)
    with c6:
        home_ownership = st.radio("Home Ownership", ["RENT","MORTGAGE","OWN","OTHER"], horizontal=True)

    verification_status = st.radio("Income Verification", list(VERIF_MAP.keys()), horizontal=True)

    st.markdown('<div class="form-area"><div class="sh"><div class="sbadge">3</div><div class="slabel">Credit History</div><div class="srule"></div></div></div>', unsafe_allow_html=True)

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

    if model is None:
        st.error("⚠️ model_rf.joblib not found. Please add the model file.")
    else:
        if st.button("⚡  Analyze & Predict"):
            with st.spinner("Running AI model..."):
                time.sleep(0.5)
            purpose_cols = ["car","credit_card","debt_consolidation","home_improvement",
                            "house","major_purchase","medical","moving","other",
                            "renewable_energy","small_business","vacation","wedding"]
            features = pd.DataFrame([{
                'loan_amnt': loan_amnt, 'term': TERM_MAP[term],
                'sub_grade': SUBGRADE_MAP[sub_grade], 'emp_length': emp_length,
                'verification_status': VERIF_MAP[verification_status],
                'delinq_2yrs': delinq_2yrs, 'pub_rec': pub_rec,
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

    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
