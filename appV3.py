from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os

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
        "functional_statement_choice": None,
        "functional_statement_content": None,
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
            "functional_statement_choice": None,
            "functional_statement_content": None,
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

        st.markdown("### Question 6")
        functional_statement_choice = st.radio(
            "Would you like to upload or copy and paste your functional statement? If you do, please do so now.",
            options=["Yes", "No"],
            index=None,
            key="functional_statement_radio",
        )

        functional_statement_content = None
        if functional_statement_choice == "Yes":
            st.markdown("#### Upload your functional statement:")
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=["txt", "docx", "pdf"],
                key="functional_statement_file",
            )
            # Require file upload before proceeding
            if uploaded_file is not None:
                try:
                    if uploaded_file.type == "text/plain":
                        functional_statement_content = str(
                            uploaded_file.read(), "utf-8"
                        )
                    elif (
                        uploaded_file.type
                        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    ):
                        st.info(
                            "DOCX file uploaded. Content extraction would require additional libraries (python-docx)."
                        )
                        functional_statement_content = (
                            f"DOCX file uploaded: {uploaded_file.name}"
                        )
                    elif uploaded_file.type == "application/pdf":
                        st.info(
                            "PDF file uploaded. Content extraction would require additional libraries (PyPDF2 or pdfplumber)."
                        )
                        functional_statement_content = (
                            f"PDF file uploaded: {uploaded_file.name}"
                        )
                    else:
                        st.error("Unsupported file type")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
                    functional_statement_content = (
                        f"Error reading file: {uploaded_file.name}"
                    )
            else:
                st.info("Please upload your functional statement before continuing.")

        submitted = st.form_submit_button("Complete Profile")

        if submitted:
            # Validate all fields are filled
            if (
                role
                and work_area
                and education
                and grade
                and experience
                and functional_statement_choice
                and (
                    functional_statement_choice == "No" or functional_statement_content
                )
            ):
                st.session_state.user_profile = {
                    "role": role,
                    "work_area": work_area,
                    "education": education,
                    "grade": grade,
                    "experience": experience,
                    "functional_statement_choice": functional_statement_choice,
                    "functional_statement_content": functional_statement_content,
                }
                st.session_state.profile_complete = True

                # Add initial system message with user profile
                profile_summary = f"User Profile: Role: {role}, Work Area: {work_area}, Education: {education}, Grade: {grade}, Experience: {experience}"
                st.session_state.messages.append(
                    {"role": "system", "content": profile_summary}
                )

                st.success(
                    "Profile completed! Please answer the next question to continue."
                )
                st.session_state.show_action_question = True
                st.rerun()
            else:
                st.error("Please answer all questions before continuing.")

# After profile is complete but before chat interface, ask Question 7
if st.session_state.get("show_action_question", False):
    st.header("Next Step")
    action = st.radio(
        "Question 7: What action would you like to perform?",
        options=["Annual evaluation", "Promotion contribution", "Skills development"],
        index=None,
        key="action_radio",
    )
    if action:
        st.session_state.selected_action = action
        st.session_state.show_action_question = False
        # Echo the user's selection in the chat
        st.session_state.messages.append(
            {"role": "user", "content": f"Selected action: {action}"}
        )
        # --- Load evaluation_bullets.txt and append as system message ---
        try:
            with open(
                os.path.join("data", "evaluation_bullets.txt"),
                "r",
                encoding="utf-8",
            ) as f:
                eval_instructions = f.read()
            st.session_state.messages.append(
                {"role": "system", "content": eval_instructions}
            )
        except Exception as e:
            st.warning(f"Could not load evaluation instructions: {e}")
        # --------------------------------------------------------------

        submitted = False
        if action == "Annual evaluation":
            st.info(
                "Please copy and paste bullets or a paragraph containing your accomplishments. You can also include items that you struggle with."
            )
            with st.form("annual_eval_form"):
                annual_eval = st.text_area(
                    "Accomplishments and/or Struggles",
                    key="annual_eval_accomplishments",
                    height=200,
                    placeholder="Paste your accomplishments and struggles here...",
                )
                submit_btn = st.form_submit_button("Submit")
                if submit_btn:
                    if not annual_eval:
                        st.warning(
                            "Please enter your accomplishments or struggles before submitting."
                        )
                        st.stop()
                    with st.spinner("Uploading..."):
                        st.session_state["annual_eval_accomplishments"] = annual_eval
                        submitted = True
        elif action == "Promotion contribution":
            st.info(
                "Please describe your contributions or achievements that support your promotion request."
            )
            with st.form("promotion_contrib_form"):
                promotion_contrib = st.text_area(
                    "Promotion Contributions",
                    key="promotion_contributions",
                    height=200,
                    placeholder="Describe your promotion contributions here...",
                )
                submit_btn = st.form_submit_button("Submit")
                if submit_btn:
                    if not promotion_contrib:
                        st.warning(
                            "Please enter your promotion contributions before submitting."
                        )
                        st.stop()
                    with st.spinner("Uploading..."):
                        st.session_state["promotion_contributions"] = promotion_contrib
                        submitted = True
        elif action == "Skills development":
            st.info(
                "Please describe the skills you wish to develop or areas where you seek improvement."
            )
            with st.form("skills_dev_form"):
                skills_dev = st.text_area(
                    "Skills Development Goals",
                    key="skills_development",
                    height=200,
                    placeholder="Describe your skills development goals here...",
                )
                submit_btn = st.form_submit_button("Submit")
                if submit_btn:
                    if not skills_dev:
                        st.warning(
                            "Please enter your skills development goals before submitting."
                        )
                        st.stop()
                    with st.spinner("Uploading..."):
                        st.session_state["skills_development"] = skills_dev
                        submitted = True

        if submitted:
            st.success(f"You selected: {action}. You can now start chatting.")
            st.rerun()
        else:
            st.stop()

# Only show chat interface if profile is complete and action is selected
if st.session_state.profile_complete and not st.session_state.get(
    "show_action_question", False
):
    st.header("Chat Interface")

    # Display user profile summary
    with st.expander("Your Profile Summary", expanded=False):
        profile = st.session_state.user_profile
        st.write(f"**Role:** {profile['role']}")
        st.write(f"**Work Area:** {profile['work_area']}")
        st.write(f"**Education:** {profile['education']}")
        st.write(f"**Grade:** {profile['grade']}")
        st.write(f"**Experience:** {profile['experience']}")

    # Display action-specific input as reference
    selected_action = st.session_state.get("selected_action")
    if selected_action == "Annual evaluation":
        accomplishments = st.session_state.get("annual_eval_accomplishments")
        if accomplishments:
            with st.expander("Your Annual Evaluation Input", expanded=True):
                st.markdown(accomplishments)
    elif selected_action == "Promotion contribution":
        promotion_contrib = st.session_state.get("promotion_contributions")
        if promotion_contrib:
            with st.expander("Your Promotion Contributions Input", expanded=True):
                st.markdown(promotion_contrib)
    elif selected_action == "Skills development":
        skills_dev = st.session_state.get("skills_development")
        if skills_dev:
            with st.expander("Your Skills Development Input", expanded=True):
                st.markdown(skills_dev)

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

    # streamlit run appV3.py
