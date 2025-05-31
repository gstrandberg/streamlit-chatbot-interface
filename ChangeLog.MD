# Changelog

All notable changes to the Streamlit Chatbot Interface project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- User profile questionnaire system before chat initiation
- 5 comprehensive profile questions for nursing professionals:
  - Role selection (LPN, RN, ANP) with radio buttons
  - Work area description with free text input
  - Highest nursing education level (ADN, BSN, MSN, Non-Nursing Masters) with radio buttons
  - Current grade level (Nurse I-IV) with radio buttons
  - Experience duration in current role with free text input
- Profile completion validation requiring all questions to be answered
- User profile summary display in an expandable section during chat
- Profile reset functionality in sidebar
- Session state management for profile data persistence
- System message integration with user profile for context-aware responses
- Automatic inclusion of user profile information in all chat interactions with the AI bot
- **New:** After profile completion, added Question 7: "What action would you like to perform?" (radio button: Annual evaluation, Promotion contribution, Skills development). This is required before chat interface is shown. User's choice is stored in session state but not included in the profile summary. The user's selection is now echoed as a user message in the chat history.
- **New:** If Question 6 (functional statement upload) is answered 'Yes', the user must upload a file before proceeding to Question 7. The form cannot be submitted until a file is uploaded.

### Changed
- Chat interface now only appears after profile completion **and** action selection (Question 7)
- Added profile completion status tracking in session state
- Enhanced sidebar with profile reset option alongside existing delete history button
- Improved user experience with clear section headers and form organization
- AI bot now receives user profile context for personalized responses based on nursing role, work area, education, grade level, and experience

## [0.1.1] - 5-30-2025
### Changed
- Removed shelve functionality and associated code for chat history persistence
- Chat history is now maintained only during the current session and not persisted between sessions
- Simplified code by removing load_chat_history and save_chat_history functions

## [0.1.0] - YYYY-MM-DD
### Added
- First version of the chatbot interface
- Basic conversation functionality

### Changed
- N/A

### Fixed
- N/A

<!--
Changelog entry types:
- Added: for new features
- Changed: for changes in existing functionality
- Deprecated: for soon-to-be removed features
- Removed: for now removed features
- Fixed: for any bug fixes
- Security: in case of vulnerabilities
-->
