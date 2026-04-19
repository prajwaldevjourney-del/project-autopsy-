import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Project Autopsy", layout="wide")

# =========================
# PREMIUM GOLD + BLACK THEME
# =========================
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #000000, #0a0a0a);
    color: #f5f5f5;
    font-family: 'Inter', sans-serif;
}

/* Title */
h1, h2, h3 {
    color: #d4af37;
    letter-spacing: 0.5px;
}

/* Inputs */
textarea, input {
    background-color: #111 !important;
    color: #fff !important;
    border: 1px solid #333 !important;
    border-radius: 12px !important;
    padding: 12px !important;
    transition: all 0.2s ease-in-out;
}

textarea:focus, input:focus {
    border: 1px solid #d4af37 !important;
    box-shadow: 0 0 8px rgba(212,175,55,0.3);
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #d4af37, #b8962e);
    color: black;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    border: none;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 8px 20px rgba(212,175,55,0.3);
}

/* Cards */
.card {
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 20px;
    margin-top: 15px;
    backdrop-filter: blur(12px);
    transition: all 0.25s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0px 12px 30px rgba(0,0,0,0.5);
}

/* Fade-in animation */
.fade-in {
    animation: fadeIn 0.6s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px);}
    to { opacity: 1; transform: translateY(0);}
}

/* Progress bar color */
.stProgress > div > div > div {
    background-color: #d4af37;
}
</style>
""", unsafe_allow_html=True)

# =========================
# ENGINE
# =========================

def score_novelty(text):
    generic = ["ai chatbot", "resume", "todo", "chat app", "blog"]
    score = 10
    for word in generic:
        if word in text.lower():
            score -= 3
    return max(score, 1)


def score_complexity(features):
    if not features:
        return 2
    return min(10, len(features.split(",")) + 2)


def score_defensibility(text):
    keywords = ["data", "engine", "system", "workflow"]
    score = 3
    for word in keywords:
        if word in text.lower():
            score += 2
    return min(score, 10)


def score_saturation(text):
    saturated = ["chatbot", "resume", "portfolio", "todo"]
    score = 7
    for word in saturated:
        if word in text.lower():
            score += 2
    return min(score, 10)


def evaluate(idea, features):
    return {
        "novelty": score_novelty(idea),
        "complexity": score_complexity(features),
        "defensibility": score_defensibility(idea),
        "saturation": score_saturation(idea)
    }


def detect_issues(scores):
    issues = []

    if scores["novelty"] < 4:
        issues.append("Low novelty — overdone idea")

    if scores["saturation"] > 8:
        issues.append("Highly saturated market")

    if scores["defensibility"] < 5:
        issues.append("Weak differentiation")

    if scores["complexity"] < 4:
        issues.append("Too simple to stand out")

    return issues


def verdict(issues):
    if len(issues) >= 3:
        return "🔴 High Risk"
    elif len(issues) == 2:
        return "🟠 Moderate Risk"
    else:
        return "🟢 Promising"


def generate_local_feedback(scores, issues):
    feedback = []

    if scores["novelty"] < 5:
        feedback.append("Your idea lacks uniqueness. Consider narrowing to a niche or adding a strong differentiator.")

    if scores["defensibility"] < 5:
        feedback.append("There is no clear moat. Add a data layer, proprietary system, or workflow advantage.")

    if scores["saturation"] > 7:
        feedback.append("Market is crowded. You need a unique angle or target underserved users.")

    if scores["complexity"] < 5:
        feedback.append("Project is too simple. Add deeper functionality or intelligence.")

    if not feedback:
        feedback.append("This idea is relatively strong. Focus on execution quality and scalability.")

    return feedback


# =========================
# UI
# =========================

st.title("🧠 Project Autopsy")
st.caption("Analyze. Break. Improve.")

st.markdown("### Describe Your Project")

idea = st.text_area("Project Idea", height=150)
features = st.text_input("Key Features (comma separated)")

if st.button("Run Analysis"):

    if not idea.strip():
        st.warning("Enter your idea first.")
        st.stop()

    scores = evaluate(idea, features)
    issues = detect_issues(scores)
    final_verdict = verdict(issues)
    feedback = generate_local_feedback(scores, issues)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.subheader("Scores")
        for k, v in scores.items():
            st.progress(v / 10, text=f"{k.capitalize()}: {v}/10")
        st.markdown(f"### {final_verdict}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.subheader("Issues")
        if issues:
            for i in issues:
                st.error(i)
        else:
            st.success("No major issues detected")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.subheader("Insights")
    for f in feedback:
        st.write(f"• {f}")
    st.markdown('</div>', unsafe_allow_html=True)
