import streamlit as st
import streamlit.components.v1 as components

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Project Autopsy", layout="wide", initial_sidebar_state="collapsed")

# =========================
# PREMIUM INJECTION (HTML/CSS/JS)
# =========================
def apply_premium_theme():
    # 1. CSS for the Visuals
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Global Overrides */
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%) !important;
        color: #f5f5f5 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Remove Streamlit Header/Footer for clean look */
    header, footer {visibility: hidden !important;}

    /* Title & Text */
    h1, h2, h3 {
        color: #d4af37 !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        text-transform: uppercase;
    }

    /* Cards - The "Glass" Effect */
    .premium-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: transform 0.3s ease, border 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(212, 175, 55, 0.5);
    }

    /* Inputs */
    .stTextArea textarea, .stTextInput input {
        background-color: #0d0d0d !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.15) !important;
    }

    /* The Button */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #aa891f 100%) !important;
        color: #000 !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.4) !important;
        transform: scale(1.01) !important;
    }

    /* Progress Bar */
    div[data-testid="stProgress"] > div > div > div > div {
        background-image: linear-gradient(90deg, #8b6b10, #d4af37) !important;
    }

    /* Animation */
    .fade-in {
        animation: fadeIn 0.8s ease-out forwards;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

    # 2. JavaScript to force font rendering on Streamlit's deep DOM
    components.html("""
    <script>
    const labels = window.parent.document.querySelectorAll('p, span, label');
    labels.forEach(el => {
        el.style.fontFamily = "'Inter', sans-serif";
    });
    </script>
    """, height=0)

apply_premium_theme()

# =========================
# LOGIC ENGINE
# =========================

def analyze_project(idea, features):
    # Simplified Scoring Logic
    scores = {
        "Novelty": 10 - (3 if any(x in idea.lower() for x in ["todo", "chatbot", "resume"]) else 0),
        "Complexity": min(10, (len(features.split(',')) * 2) if features else 2),
        "Defensibility": 4 + (2 if "engine" in idea.lower() or "system" in idea.lower() else 0),
        "Market Sat": 5 + (3 if "ai" in idea.lower() else 0)
    }
    
    issues = []
    if scores["Novelty"] < 5: issues.append("🔴 Common Idea: Market may be tired of this concept.")
    if scores["Complexity"] < 4: issues.append("🟠 Low Barrier: Competitors can replicate this in days.")
    if scores["Defensibility"] < 5: issues.append("🟡 No Moat: Consider adding proprietary data logic.")
    
    return scores, issues

# =========================
# MAIN UI
# =========================

st.markdown('<h1 style="text-align: center;">PROJECT AUTOPSY</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888;">Analyze your vision. Identify the rot. Build stronger.</p>', unsafe_allow_html=True)
st.write("---")

col_in, col_spacer, col_out = st.columns([1, 0.1, 1.2])

with col_in:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    idea = st.text_area("The Concept", placeholder="Describe the soul of your project...", height=200)
    feats = st.text_input("Key Features", placeholder="Feature A, Feature B, Feature C")
    trigger = st.button("RUN FORENSICS")
    st.markdown('</div>', unsafe_allow_html=True)

if trigger:
    if not idea:
        st.warning("You cannot autopsy a ghost. Please enter an idea.")
    else:
        scores, issues = analyze_project(idea, feats)
        
        with col_out:
            # Score Section
            st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
            st.subheader("Vital Signs")
            for label, val in scores.items():
                st.write(f"**{label}**")
                st.progress(val / 10)
            st.markdown('</div>', unsafe_allow_html=True)

            # Issues Section
            st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
            st.subheader("Autopsy Findings")
            if issues:
                for issue in issues:
                    st.write(issue)
            else:
                st.success("Concept is robust. No immediate red flags.")
            st.markdown('</div>', unsafe_allow_html=True)

            # Final Advice
            st.markdown('<div class="premium-card fade-in">', unsafe_allow_html=True)
            st.subheader("Surgeon's Notes")
            if len(issues) > 1:
                st.info("💡 Recommendation: Pivot toward a niche application to increase novelty and defensibility.")
            else:
                st.info("💡 Recommendation: Focus on UX and distribution. The core logic is sound.")
            st.markdown('</div>', unsafe_allow_html=True)
