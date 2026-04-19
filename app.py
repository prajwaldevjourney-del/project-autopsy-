import streamlit as st

# =========================
# PAGE CONFIG
# = :heart: PREMIUM UI
# =========================
st.set_page_config(page_title="Project Autopsy", layout="wide")

# =========================
# ENHANCED PREMIUM THEME
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

/* Main Background */
.stApp {
    background: radial-gradient(circle at top right, #1a1a1a, #000000);
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}

/* Header & Titles */
h1, h2, h3 {
    color: #d4af37 !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

/* Input Fields */
.stTextArea textarea, .stTextInput input {
    background-color: #0f0f0f !important;
    color: #ffffff !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #d4af37 !important;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.2) !important;
}

/* Premium Button */
div.stButton > button {
    background: linear-gradient(135deg, #d4af37 0%, #aa891f 100%) !important;
    color: #000 !important;
    border: none !important;
    padding: 0.6rem 2rem !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    width: 100%;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 10px 20px rgba(212, 175, 55, 0.3);
}

/* Custom Card Container */
.status-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(212, 175, 55, 0.1);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

/* Progress Bar Color */
div[data-testid="stProgress"] > div > div > div > div {
    background-color: #d4af37 !important;
}

/* Clean Info/Error Messages */
.stAlert {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid #333 !important;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# BACKEND LOGIC
# =========================

def evaluate(idea, features):
    # Logic remains the same, but cleaned up for consistency
    score_novelty = 10 - (3 if any(w in idea.lower() for w in ["ai chatbot", "resume", "todo"]) else 0)
    score_complexity = min(10, len(features.split(",")) + 2) if features else 3
    score_defens = 3 + (sum(2 for w in ["data", "engine", "system", "workflow"] if w in idea.lower()))
    score_sat = 7 + (sum(1 for w in ["chatbot", "resume", "portfolio"] if w in idea.lower()))
    
    return {
        "Novelty": max(score_novelty, 1),
        "Complexity": min(score_complexity, 10),
        "Defensibility": min(score_defens, 10),
        "Saturation": min(score_sat, 10)
    }

def get_feedback(scores):
    issues = []
    if scores["Novelty"] < 5: issues.append("🔴 Low novelty — looks like a 'template' project.")
    if scores["Saturation"] > 8: issues.append("🟠 Highly saturated market — hard to get noticed.")
    if scores["Defensibility"] < 5: issues.append("🟡 Weak moat — easily copied by others.")
    if scores["Complexity"] < 4: issues.append("⚪ Too simple — might be seen as a weekend toy.")
    return issues

# =========================
# UI LAYOUT
# =========================

st.title("🧠 Project Autopsy")
st.markdown("_Deconstruct your project idea before the market does._")
st.write("---")

col_a, col_b = st.columns([1.5, 1])

with col_a:
    idea = st.text_area("What is the core concept?", placeholder="e.g. A decentralized data engine for supply chain tracking...", height=180)
    features = st.text_input("Key technical features", placeholder="comma, separated, list")
    analyze_btn = st.button("Run Forensic Analysis")

if analyze_btn:
    if not idea.strip():
        st.error("Please provide a project description.")
    else:
        scores = evaluate(idea, features)
        issues = get_feedback(scores)
        
        with col_b:
            st.markdown('<div class="status-card">', unsafe_allow_html=True)
            st.subheader("Metric Analysis")
            for label, val in scores.items():
                st.write(f"**{label}**")
                st.progress(val / 10)
            
            risk_color = "🟢" if len(issues) <= 1 else "🟠" if len(issues) == 2 else "🔴"
            st.markdown(f"### Verdict: {risk_color}")
            st.markdown('</div>', unsafe_allow_html=True)

        st.write("---")
        
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown('<div class="status-card">', unsafe_allow_html=True)
            st.subheader("Detected Friction")
            if issues:
                for issue in issues:
                    st.write(issue)
            else:
                st.success("Clean bill of health! No major red flags.")
            st.markdown('</div>', unsafe_allow_html=True)

        with res_col2:
            st.markdown('<div class="status-card">', unsafe_allow_html=True)
            st.subheader("Strategic Insights")
            if scores["Novelty"] < 6:
                st.info("💡 Try pivoting to a specific niche (e.g., instead of 'AI for HR', try 'AI for Nursing Recruitment').")
            elif scores["Defensibility"] < 6:
                st.info("💡 Focus on building a proprietary dataset or a unique integration that's hard to replicate.")
            else:
                st.success("Execution is everything now. This concept has legs.")
            st.markdown('</div>', unsafe_allow_html=True)
