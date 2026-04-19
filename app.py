import streamlit as st
import requests
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Project Autopsy", layout="wide")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================
# STYLES (PREMIUM UI)
# =========================
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #e6e6e6;
}

.block-container {
    padding: 2rem;
}

textarea, input {
    border-radius: 12px !important;
}

.result-card {
    background: rgba(255,255,255,0.03);
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(10px);
    transition: all 0.25s ease;
}

.result-card:hover {
    transform: translateY(-4px);
    box-shadow: 0px 12px 35px rgba(0,0,0,0.4);
}

.section {
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CORE ENGINE
# =========================

def score_novelty(text):
    generic_keywords = ["ai chatbot", "resume", "todo", "chat app", "blog"]
    score = 10

    for word in generic_keywords:
        if word in text.lower():
            score -= 3

    return max(score, 1)


def score_complexity(features):
    if not features:
        return 2
    count = len(features.split(","))
    return min(10, count + 2)


def score_defensibility(text):
    defensible_keywords = ["data", "engine", "workflow", "system"]
    score = 3

    for word in defensible_keywords:
        if word in text.lower():
            score += 2

    return min(score, 10)


def score_saturation(text):
    saturated = ["ai resume", "chatbot", "portfolio", "task manager"]
    score = 8

    for word in saturated:
        if word in text.lower():
            score += 1

    return min(score, 10)


def evaluate_project(idea, features):
    return {
        "novelty": score_novelty(idea),
        "complexity": score_complexity(features),
        "defensibility": score_defensibility(idea),
        "saturation": score_saturation(idea)
    }


def detect_failures(scores):
    issues = []

    if scores["novelty"] < 4:
        issues.append("Low novelty — idea feels overdone")

    if scores["saturation"] > 8:
        issues.append("Highly saturated market")

    if scores["defensibility"] < 5:
        issues.append("No strong moat or differentiation")

    if scores["complexity"] < 4:
        issues.append("Too simple — lacks depth")

    return issues


def get_verdict(issues):
    if len(issues) >= 3:
        return "🔴 High Risk"
    elif len(issues) == 2:
        return "🟠 Moderate Risk"
    else:
        return "🟢 Promising"


# =========================
# LLM LAYER
# =========================

def generate_feedback(idea, scores, issues):
    if not GROQ_API_KEY:
        return "⚠️ No API key found. Set GROQ_API_KEY environment variable."

    prompt = f"""
You are a brutally honest startup evaluator.

Idea:
{idea}

Scores:
{scores}

Issues:
{issues}

Give:
1. Brutal critique
2. Why it will fail
3. How to improve

Keep it sharp, structured, and no fluff.
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating feedback: {e}"


# =========================
# UI
# =========================

st.title("🧠 Project Autopsy")
st.caption("Analyze. Break. Improve.")

st.markdown("### Describe Your Project")

idea = st.text_area("Project Idea", height=150, placeholder="Explain your idea clearly...")
features = st.text_input("Key Features (comma separated)", placeholder="auth, dashboard, AI analysis...")

run = st.button("Run Analysis")

if run:
    if not idea.strip():
        st.warning("Enter your idea first.")
        st.stop()

    scores = evaluate_project(idea, features)
    issues = detect_failures(scores)
    verdict = get_verdict(issues)

    # =========================
    # RESULTS LAYOUT
    # =========================
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Scores")
        for k, v in scores.items():
            st.progress(v / 10, text=f"{k.capitalize()}: {v}/10")

        st.markdown("### Verdict")
        st.success(verdict)

    with col2:
        st.markdown("### Issues Detected")
        if issues:
            for issue in issues:
                st.error(issue)
        else:
            st.success("No major risks detected")

    # =========================
    # AI OUTPUT
    # =========================
    st.markdown("### AI Critique")

    with st.spinner("Running deep analysis..."):
        feedback = generate_feedback(idea, scores, issues)

    st.markdown(
        f'<div class="result-card">{feedback}</div>',
        unsafe_allow_html=True
    )
