from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import time

load_dotenv()

st.title("Gregs Cool Interactive Chatbot")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure openai_model is initialized in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Initialize chat history as empty list
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize user profile completion status
if "profile_complete" not in st.session_state:
    st.session_state.profile_complete = False

# Initialize user profile data
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "role": None,
        "work_area": None,
        "education": None,
        "grade": None,
        "experience": None,
    }

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []

    if st.button("Reset Profile"):
        st.session_state.profile_complete = False
        st.session_state.user_profile = {
            "role": None,
            "work_area": None,
            "education": None,
            "grade": None,
            "experience": None,
        }

# User Profile Questions Section
if not st.session_state.profile_complete:
    st.header("Welcome! Please complete your profile to get started:")

    with st.form("user_profile_form"):
        st.markdown("### Question 1")
        role = st.radio(
            "What is your current role? (Please respond before we continue.)",
            options=["LPN", "RN", "ANP"],
            index=None,
            key="role_radio",
        )

        st.markdown("### Question 2")
        work_area = st.text_input(
            "What area do you work in? (e.g., inpatient mental health, outpatient primary care, surgery, etc.) Please respond before we continue.",
            key="work_area_input",
        )

        st.markdown("### Question 3")
        education = st.radio(
            "What is your highest level of education in nursing? (Please respond before we continue.)",
            options=["ADN", "BSN", "MSN", "Non-Nursing Masters (Approved Field)"],
            index=None,
            key="education_radio",
        )

        st.markdown("### Question 4")
        grade = st.radio(
            "What is your current grade? (Please respond before we continue.)",
            options=["Nurse I", "Nurse II", "Nurse III", "Nurse IV"],
            index=None,
            key="grade_radio",
        )

        st.markdown("### Question 5")
        experience = st.text_input(
            "How long have you been in your current role, in years and months?",
            key="experience_input",
        )

        submitted = st.form_submit_button("Complete Profile")

        if submitted:
            # Validate all fields are filled
            if role and work_area and education and grade and experience:
                st.session_state.user_profile = {
                    "role": role,
                    "work_area": work_area,
                    "education": education,
                    "grade": grade,
                    "experience": experience,
                }
                st.session_state.profile_complete = True

                # Add initial system message with user profile
                profile_summary = f"User Profile: Role: {role}, Work Area: {work_area}, Education: {education}, Grade: {grade}, Experience: {experience}"
                st.session_state.messages.append(
                    {"role": "system", "content": profile_summary}
                )

                st.success("Profile completed! You can now start chatting.")
                st.rerun()
            else:
                st.error("Please answer all questions before continuing.")

# Only show chat interface if profile is complete
if st.session_state.profile_complete:
    st.header("Chat Interface")

    # Display user profile summary
    with st.expander("Your Profile Summary", expanded=False):
        profile = st.session_state.user_profile
        st.write(f"**Role:** {profile['role']}")
        st.write(f"**Work Area:** {profile['work_area']}")
        st.write(f"**Education:** {profile['education']}")
        st.write(f"**Grade:** {profile['grade']}")
        st.write(f"**Experience:** {profile['experience']}")

    # Display chat messages (excluding system messages)
    for message in st.session_state.messages:
        if message["role"] != "system":  # Don't display system messages in chat
            avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])  # Main chat interface
    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state["messages"],
                stream=True,
            ):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "|")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

    # streamlit run appV2.py
