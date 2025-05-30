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

### Changed
- Chat interface now only appears after profile completion
- Added profile completion status tracking in session state
- Enhanced sidebar with profile reset option alongside existing delete history button
- Improved user experience with clear section headers and form organization

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
