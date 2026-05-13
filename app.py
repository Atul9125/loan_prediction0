import streamlit as st
import numpy as np
import joblib
import os

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LoanIQ · Loan Status Predictor",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Reset & Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0a0f1e;
    color: #e2e8f0;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding: 0 !important; max-width: 100% !important;}

/* ── Hero Banner ── */
.hero {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1a3a 50%, #091529 100%);
    border-bottom: 1px solid rgba(99,179,237,0.15);
    padding: 48px 60px 36px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(66,153,225,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(237,100,166,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.logo-text {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 16px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 42px;
    font-weight: 800;
    color: #fff;
    line-height: 1.15;
    margin: 0 0 12px;
}
.hero-title span { color: #63b3ed; }
.hero-subtitle {
    font-size: 16px;
    color: #94a3b8;
    font-weight: 300;
    max-width: 520px;
    line-height: 1.7;
}

/* ── Main Layout ── */
.main-grid {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 0;
    min-height: calc(100vh - 200px);
}
.form-panel {
    padding: 40px 60px;
    border-right: 1px solid rgba(99,179,237,0.1);
}
.result-panel {
    padding: 40px 32px;
    background: rgba(15,23,42,0.6);
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
}

/* ── Section Headers ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #63b3ed;
    margin: 32px 0 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(99,179,237,0.2);
}

/* ── Streamlit Widget Overrides ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stSlider {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

div[data-testid="stSelectbox"] > label,
div[data-testid="stNumberInput"] > label,
div[data-testid="stSlider"] > label,
div[data-testid="stRadio"] > label {
    color: #94a3b8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
    margin-bottom: 4px !important;
}

/* Radio buttons */
div[data-testid="stRadio"] > div {
    flex-direction: row !important;
    gap: 8px !important;
    flex-wrap: wrap !important;
}
div[data-testid="stRadio"] label {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    color: #94a3b8 !important;
    font-size: 13px !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: #63b3ed !important;
    color: #63b3ed !important;
}

/* Slider track */
div[data-testid="stSlider"] > div > div > div {
    background: #63b3ed !important;
}

/* Number input */
input[type="number"] {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 15px !important;
}

/* ── Predict Button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #3182ce, #63b3ed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 40px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    width: 100% !important;
    margin-top: 20px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 24px rgba(49,130,206,0.35) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(49,130,206,0.5) !important;
}

/* ── Result Cards ── */
.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 24px;
}
.verdict-card {
    border-radius: 16px;
    padding: 28px 24px;
    margin-bottom: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.verdict-card.approved {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.08));
    border: 1px solid rgba(16,185,129,0.3);
}
.verdict-card.rejected {
    background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(185,28,28,0.08));
    border: 1px solid rgba(239,68,68,0.3);
}
.verdict-icon { font-size: 42px; margin-bottom: 10px; }
.verdict-label {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 6px;
}
.verdict-label.approved { color: #34d399; }
.verdict-label.rejected { color: #f87171; }
.verdict-sub {
    font-size: 13px;
    color: #64748b;
    line-height: 1.5;
}

.prob-bar-wrap { margin: 20px 0; }
.prob-label {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #64748b;
    margin-bottom: 6px;
}
.prob-bar-bg {
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    height: 8px;
    overflow: hidden;
}
.prob-bar-fill-g {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #34d399, #10b981);
    transition: width 0.8s ease;
}
.prob-bar-fill-r {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #f87171, #ef4444);
    transition: width 0.8s ease;
}

/* Feature summary cards */
.summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 16px;
}
.summary-chip {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(99,179,237,0.12);
    border-radius: 10px;
    padding: 10px 12px;
}
.chip-key {
    font-size: 10px;
    color: #475569;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 3px;
}
.chip-val {
    font-size: 14px;
    color: #cbd5e1;
    font-weight: 500;
}

/* Idle state */
.idle-state {
    text-align: center;
    padding: 60px 20px;
    color: #334155;
}
.idle-icon { font-size: 56px; margin-bottom: 16px; opacity: 0.5; }
.idle-text {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    color: #475569;
    line-height: 1.6;
}

/* Risk badge */
.risk-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 8px;
}
.risk-low { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.risk-mid { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.risk-high { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

/* Column padding fix */
div[data-testid="column"] { padding: 0 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "loan_model.pkl")
    return joblib.load(model_path)

model = load_model()

# ── Sub-grade mapping ─────────────────────────────────────────────────────────
SUBGRADE_MAP = {
    'A1':1,'A2':2,'A3':3,'A4':4,'A5':5,
    'B1':6,'B2':7,'B3':8,'B4':9,'B5':10,
    'C1':11,'C2':12,'C3':13,'C4':14,'C5':15,
    'D1':16,'D2':17,'D3':18,'D4':19,'D5':20,
    'E1':21,'E2':22,'E3':23,'E4':24,'E5':25,
    'F1':26,'F2':27,'F3':28,'F4':29,'F5':30,
    'G1':31,'G2':32,'G3':33,'G4':34,'G5':35,
}
VERIF_MAP = {'Not Verified': 0, 'Verified': 1, 'Source Verified': 2}
TERM_MAP = {'36 months': 36, '60 months': 60}

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="logo-text">LoanIQ · AI Decision Engine</div>
    <div class="hero-title">Will your loan get<br><span>approved?</span></div>
    <div class="hero-subtitle">
        Powered by a Random Forest model trained on real lending data.
        Fill in your details and get an instant, data-driven prediction.
    </div>
</div>
""", unsafe_allow_html=True)

# ── State ─────────────────────────────────────────────────────────────────────
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "probability" not in st.session_state:
    st.session_state.probability = None
if "input_summary" not in st.session_state:
    st.session_state.input_summary = {}

# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([2, 1], gap="large")

with left:
    st.markdown('<div style="padding: 8px 0 0;">', unsafe_allow_html=True)

    # ── Section 1: Loan Details ──
    st.markdown('<div class="section-label">① Loan Details</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        loan_amnt = st.number_input("Loan Amount ($)", min_value=500, max_value=40000,
                                     value=10000, step=500,
                                     help="Requested loan amount in USD")
    with c2:
        term = st.selectbox("Loan Term", options=list(TERM_MAP.keys()),
                             help="Duration of the loan")

    c3, c4 = st.columns(2)
    with c3:
        sub_grade = st.selectbox("Credit Sub-Grade",
                                  options=list(SUBGRADE_MAP.keys()),
                                  index=4,
                                  help="Lending club assigned sub-grade (A1=best, G5=worst)")
    with c4:
        purpose = st.selectbox("Loan Purpose", options=[
            "debt_consolidation", "credit_card", "home_improvement",
            "other", "major_purchase", "medical", "small_business",
            "car", "vacation", "moving", "house", "wedding",
            "renewable_energy"
        ], help="Reason for the loan")

    # ── Section 2: Applicant Profile ──
    st.markdown('<div class="section-label">② Applicant Profile</div>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        emp_length = st.slider("Employment Length (years)", 0, 10, 3,
                                help="Years at current employer (10 = 10+ years)")
    with c6:
        home_ownership = st.radio("Home Ownership",
                                   options=["RENT", "MORTGAGE", "OWN", "OTHER"],
                                   horizontal=True)

    verification_status = st.radio("Income Verification Status",
                                    options=list(VERIF_MAP.keys()),
                                    horizontal=True)

    # ── Section 3: Credit History ──
    st.markdown('<div class="section-label">③ Credit History</div>', unsafe_allow_html=True)
    c7, c8, c9, c10 = st.columns(4)
    with c7:
        delinq_2yrs = st.number_input("Delinquencies (2yrs)", min_value=0, max_value=30,
                                       value=0, help="Number of 30+ day delinquencies in past 2 years")
    with c8:
        pub_rec = st.number_input("Public Records", min_value=0, max_value=20,
                                   value=0, help="Number of derogatory public records")
    with c9:
        collections_12_mths = st.number_input("Collections (12mo)", min_value=0, max_value=20,
                                               value=0, help="Collections in last 12 months excl. medical")
    with c10:
        acc_now_delinq = st.number_input("Accounts Delinquent", min_value=0, max_value=20,
                                          value=0, help="Number of accounts currently delinquent")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Predict Button ──
    if st.button("🔍  Run Prediction"):
        # Build feature vector
        purpose_cols = ["car","credit_card","debt_consolidation","home_improvement",
                        "house","major_purchase","medical","moving","other",
                        "renewable_energy","small_business","vacation","wedding"]

        home_mortgage = 1 if home_ownership == "MORTGAGE" else 0
        home_other    = 1 if home_ownership == "OTHER" else 0
        home_own      = 1 if home_ownership == "OWN" else 0
        home_rent     = 1 if home_ownership == "RENT" else 0

        purpose_vec = [1 if f"purpose_{p}" == f"purpose_{purpose}" else 0 for p in purpose_cols]

        features = np.array([[
            loan_amnt,
            TERM_MAP[term],
            SUBGRADE_MAP[sub_grade],
            emp_length,
            VERIF_MAP[verification_status],
            delinq_2yrs,
            pub_rec,
            collections_12_mths,
            acc_now_delinq,
            home_mortgage, home_other, home_own, home_rent,
            *purpose_vec
        ]])

        pred = model.predict(features)[0]
        proba = model.predict_proba(features)[0]

        st.session_state.prediction = int(pred)
        st.session_state.probability = proba.tolist()
        st.session_state.input_summary = {
            "Amount": f"${loan_amnt:,}",
            "Term": term,
            "Sub-Grade": sub_grade,
            "Purpose": purpose.replace("_", " ").title(),
            "Employment": f"{emp_length} yrs",
            "Ownership": home_ownership,
        }

    st.markdown('</div>', unsafe_allow_html=True)

# ── Right Panel: Results ──────────────────────────────────────────────────────
with right:
    st.markdown('<div class="result-title">Prediction Result</div>', unsafe_allow_html=True)

    if st.session_state.prediction is None:
        st.markdown("""
        <div class="idle-state">
            <div class="idle-icon">🏦</div>
            <div class="idle-text">
                Complete the form and click<br><strong>Run Prediction</strong><br>to see your result
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        pred = st.session_state.prediction
        proba = st.session_state.probability
        approved = pred == 1
        approve_pct = round(proba[1] * 100, 1) if len(proba) > 1 else round(proba[0] * 100, 1)
        reject_pct = round(100 - approve_pct, 1)

        # Determine class indices — model may output [0,1] mapped differently
        # If pred==1 means approved, proba[1]=approved probability
        if approved:
            verdict_cls = "approved"
            icon = "✅"
            label = "APPROVED"
            sub = "This application meets the model's lending criteria."
        else:
            verdict_cls = "rejected"
            icon = "❌"
            label = "REJECTED"
            sub = "This application does not meet the model's criteria."

        # Risk badge
        if approve_pct >= 75:
            risk_class = "risk-low"
            risk_text = "LOW RISK"
        elif approve_pct >= 45:
            risk_class = "risk-mid"
            risk_text = "MODERATE RISK"
        else:
            risk_class = "risk-high"
            risk_text = "HIGH RISK"

        st.markdown(f"""
        <div class="verdict-card {verdict_cls}">
            <div class="verdict-icon">{icon}</div>
            <div class="verdict-label {verdict_cls}">{label}</div>
            <div class="verdict-sub">{sub}</div>
            <div><span class="risk-badge {risk_class}">{risk_text}</span></div>
        </div>

        <div class="prob-bar-wrap">
            <div class="prob-label"><span>Approval Probability</span><span>{approve_pct}%</span></div>
            <div class="prob-bar-bg"><div class="prob-bar-fill-g" style="width:{approve_pct}%"></div></div>
        </div>
        <div class="prob-bar-wrap">
            <div class="prob-label"><span>Rejection Probability</span><span>{reject_pct}%</span></div>
            <div class="prob-bar-bg"><div class="prob-bar-fill-r" style="width:{reject_pct}%"></div></div>
        </div>

        <div style="margin-top:24px; font-family:'Syne',sans-serif; font-size:11px; letter-spacing:2px; text-transform:uppercase; color:#475569; margin-bottom:10px;">Application Summary</div>
        <div class="summary-grid">
        """, unsafe_allow_html=True)

        for k, v in st.session_state.input_summary.items():
            st.markdown(f"""
            <div class="summary-chip">
                <div class="chip-key">{k}</div>
                <div class="chip-val">{v}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Reset
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 New Application"):
            st.session_state.prediction = None
            st.session_state.probability = None
            st.session_state.input_summary = {}
            st.rerun()
