import streamlit as st
import json
import ollama
import pandas as pd

# -----------------------------
# Load Scheme Database
# -----------------------------
with open("schemes.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Government Scheme Assistant",
    page_icon="🏛️",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("🏛️ AI Government Scheme Assistant")

st.write(
    "Find government schemes based on your age, state, occupation, "
    "income and category using AI."
)

st.info(
    "⚠️ This application provides a prototype profile-based matching score. "
    "Always verify final eligibility on the official government website."
)

# -----------------------------
# Statistics
# -----------------------------
st.subheader("📊 Application Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Government Schemes", len(schemes))
c2.metric("Eligibility Factors", "5")
c3.metric("AI Model", "Llama 3.2")
c4.metric("Platform", "Streamlit")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("👤 Your Profile")

name = st.sidebar.text_input("Name", "User")

age = st.sidebar.number_input(
    "Age",
    min_value=1,
    max_value=100,
    value=19
)

state = st.sidebar.text_input(
    "State",
    "Telangana"
)

occupation = st.sidebar.selectbox(
    "Occupation",
    [
        "Student",
        "Employee",
        "Farmer",
        "Business Owner",
        "Unemployed",
        "Other"
    ]
)

income = st.sidebar.number_input(
    "Annual Income (₹)",
    min_value=0,
    max_value=10000000,
    value=100000,
    step=10000
)

category = st.sidebar.selectbox(
    "Category",
    [
        "General",
        "OBC",
        "SC",
        "ST",
        "EWS",
        "DNT",
        "Other"
    ]
)

# -----------------------------
# About Project
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ About Project")

st.sidebar.write(
    "This project uses a verified scheme database, "
    "profile-based eligibility matching and local AI "
    "using Ollama with Llama 3.2."
)

# -----------------------------
# Search
# -----------------------------
st.subheader("🔎 Search Government Schemes")

search = st.text_input(
    "Search by scheme name",
    placeholder="Example: scholarship, farmer, skill..."
)

filtered_schemes = schemes

if search:
    filtered_schemes = [
        scheme
        for scheme in schemes
        if search.lower() in scheme["name"].lower()
    ]

    if not filtered_schemes:
        st.warning("No scheme found. Try another keyword.")

# -----------------------------
# Find Suitable Schemes
# -----------------------------
if st.button("🔍 Find Suitable Schemes", type="primary"):

    all_matches = []

    for scheme in filtered_schemes:

        score = 0
        reasons = []

        # Category
        if category in scheme["category"]:
            score += 20
        else:
            reasons.append("Category not matched")

        # State
        if (
            scheme["state"] == "All India"
            or scheme["state"].lower() == state.lower()
        ):
            score += 20
        else:
            reasons.append("State not matched")

        # Occupation
        if occupation in scheme["occupation"]:
            score += 20
        else:
            reasons.append("Occupation not matched")

        # Age
        if scheme["min_age"] <= age <= scheme["max_age"]:
            score += 20
        else:
            reasons.append("Age not within scheme range")

        # Income
        if income <= scheme["max_income"]:
            score += 20
        else:
            reasons.append("Income exceeds limit")

        all_matches.append(
            {
                "scheme": scheme,
                "score": score,
                "reasons": reasons
            }
        )

    # Sort by score
    all_matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    suitable_schemes = [
        match
        for match in all_matches
        if match["score"] == 100
    ]

    partial_schemes = [
        match
        for match in all_matches
        if 0 < match["score"] < 100
    ]

    # -----------------------------
    # Eligibility Dashboard
    # -----------------------------
    st.markdown("---")
    st.subheader("📊 Eligibility Dashboard")

    d1, d2, d3, d4 = st.columns(4)

    total_schemes = len(all_matches)
    fully_matched = len(suitable_schemes)
    partial_matches = len(partial_schemes)

    not_matched = total_schemes - fully_matched - partial_matches

    if all_matches:
        average_score = int(
            sum(match["score"] for match in all_matches)
            / len(all_matches)
        )
    else:
        average_score = 0

    d1.metric(
        "Total Schemes",
        total_schemes
    )

    d2.metric(
        "Fully Matched",
        fully_matched
    )

    d3.metric(
        "Partial Matches",
        partial_matches
    )

    d4.metric(
        "Average Score",
        f"{average_score}%"
    )

    if all_matches:

        top_match = all_matches[0]

        st.success(
            f"🏆 Top Match: {top_match['scheme']['name']} "
            f"— {top_match['score']}%"
        )

        st.write("Overall Matching Progress")

        st.progress(
            average_score / 100
        )

    # -----------------------------
    # Data Science Chart
    # -----------------------------
    st.markdown("---")
    st.subheader("📈 Scheme Matching Analysis")

    chart_data = pd.DataFrame(
        {
            "Match Type": [
                "Fully Matched",
                "Partial Match",
                "Not Matched"
            ],
            "Number of Schemes": [
                fully_matched,
                partial_matches,
                not_matched
            ]
        }
    )

    st.bar_chart(
        chart_data.set_index("Match Type")
    )

    # -----------------------------
    # Top Recommendations
    # -----------------------------
    st.markdown("---")
    st.subheader("🏆 Top Recommended Schemes")

    top_three = all_matches[:3]

    medals = [
        "🥇",
        "🥈",
        "🥉"
    ]

    for i, match in enumerate(top_three):

        scheme = match["scheme"]

        st.markdown(
            f"### {medals[i]} {scheme['name']}"
        )

        st.progress(
            match["score"] / 100
        )

        st.write(
            f"**Eligibility Match Score:** "
            f"{match['score']}%"
        )

    # -----------------------------
    # Suitable Schemes
    # -----------------------------
    st.markdown("---")
    st.subheader("✅ Suitable Government Schemes")

    if suitable_schemes:

        st.success(
            f"{len(suitable_schemes)} scheme(s) matched all "
            f"5 profile factors."
        )

        for match in suitable_schemes:

            scheme = match["scheme"]

            st.markdown(
                f"## 🎯 {scheme['name']}"
            )

            st.write(
                f"**Match Score:** {match['score']}%"
            )

            st.write(
                f"**Purpose:** {scheme['purpose']}"
            )

            st.write(
                f"**Eligibility:** {scheme['eligibility']}"
            )

            st.write(
                f"**Benefits:** {scheme['benefits']}"
            )

            # Documents
            st.markdown(
                "### 📄 Required Documents"
            )

            for document in scheme["documents"]:
                st.write(
                    f"• {document}"
                )

            # Official Website
            st.markdown(
                "### 🌐 Official Website"
            )

            st.link_button(
                "Visit Official Website",
                scheme["official_source"]
            )

            # AI Explanation
            st.markdown(
                "### 🤖 AI Explanation"
            )

            prompt = f"""
You are explaining a government scheme to a citizen.

Use ONLY the information given below.

Scheme name:
{scheme['name']}

Scheme purpose:
{scheme['purpose']}

Scheme eligibility:
{scheme['eligibility']}

Scheme benefits:
{scheme['benefits']}

User profile:
Age: {age}
State: {state}
Occupation: {occupation}
Annual income: ₹{income}
Category: {category}

Explain the scheme in very simple English.

Important:
- Do not invent eligibility conditions.
- Do not assume the user owns or does not own a house.
- Do not assume urban or rural location.
- Do not claim official eligibility.
- Clearly say that the application should be verified on the official website.
"""

            try:

                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                st.write(
                    response["message"]["content"]
                )

            except Exception:

                st.error(
                    "AI could not generate an explanation. "
                    "Make sure Ollama is running."
                )

            # Scheme Q&A
            st.markdown(
                "### 💬 Ask About This Scheme"
            )

            question = st.text_input(
                f"Ask a question about {scheme['name']}",
                key=f"question_{scheme['name']}"
            )

            if question:

                qa_prompt = f"""
You are a government scheme assistant.

Answer the user's question using ONLY the information provided.

Scheme:
{scheme['name']}

Purpose:
{scheme['purpose']}

Eligibility:
{scheme['eligibility']}

Benefits:
{scheme['benefits']}

Documents:
{scheme['documents']}

Application:
{scheme['apply']}

User question:
{question}

Rules:
- Do not invent information.
- If the answer is not available, say:
  "Please check the official website for this information."
- Use simple English.
"""

                try:

                    qa_response = ollama.chat(
                        model="llama3.2",
                        messages=[
                            {
                                "role": "user",
                                "content": qa_prompt
                            }
                        ]
                    )

                    st.info(
                        qa_response["message"]["content"]
                    )

                except Exception:

                    st.error(
                        "AI Q&A is unavailable. "
                        "Please make sure Ollama is running."
                    )

            st.markdown("---")

    else:

        st.warning(
            "No scheme matched all 5 profile factors."
        )

    # -----------------------------
    # Partial Matches
    # -----------------------------
    st.subheader(
        "🟡 Other Possible Schemes"
    )

    if partial_schemes:

        for match in partial_schemes:

            scheme = match["scheme"]

            with st.expander(
                f"{scheme['name']} — {match['score']}%"
            ):

                st.write(
                    f"**Eligibility Match Score:** "
                    f"{match['score']}%"
                )

                st.write(
                    f"**Purpose:** {scheme['purpose']}"
                )

                if match["reasons"]:

                    st.write(
                        "**Why it is not a full match:**"
                    )

                    for reason in match["reasons"]:

                        st.write(
                            f"• {reason}"
                        )

                st.link_button(
                    "Check Official Website",
                    scheme["official_source"]
                )

    else:

        st.info(
            "No partial matches found."
        )

    # -----------------------------
    # General AI Assistant
    # -----------------------------
    st.markdown("---")
    st.subheader(
        "🤖 General AI Government Scheme Assistant"
    )

    general_question = st.text_input(
        "Ask anything about government schemes"
    )

    if general_question:

        matched_names = [
            match["scheme"]["name"]
            for match in all_matches
            if match["score"] > 0
        ]

        assistant_prompt = f"""
You are an AI Government Scheme Assistant.

User profile:
Name: {name}
Age: {age}
State: {state}
Occupation: {occupation}
Annual income: ₹{income}
Category: {category}

Schemes available in the database:
{[scheme['name'] for scheme in schemes]}

Schemes matching the user's profile:
{matched_names}

User question:
{general_question}

Answer in simple English.

Rules:
- Use only the scheme information available in the database.
- Do not invent government schemes.
- Do not claim guaranteed eligibility.
- If exact information is unavailable, tell the user to check the official website.
"""

        try:

            assistant_response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": assistant_prompt
                    }
                ]
            )

            st.info(
                assistant_response["message"]["content"]
            )

        except Exception:

            st.error(
                "General AI Assistant is unavailable. "
                "Make sure Ollama is running."
            )