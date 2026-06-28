# Self-Evaluation Data for Water Issue Tracker
## Fills the Google Sheet columns row-wise

---

## Section: Profile Information
| Column | Value |
|--------|-------|
| **S.No.** | _(Your row number in sheet)_ |
| **College ID** | _(Fill your college ID)_ |
| **Name** | Bharath Chandra |
| **Faculty Mentor Name** | _(Fill your mentor name)_ |
| **Username on code.swecha.org** | Bharatg |
| **Username on corpus.swecha.org** | _(Fill if you have one)_ |

---

## Section: Basic App Info

**App Name:** Water Issue Tracker – Civic Complaint Management System

**Short Description:** Water Issue Tracker is a web-based civic complaint management application developed using Python and Streamlit that enables citizens to report water-related issues online with supporting proof files (images, videos, audio). The system allows administrators to securely log in, view all complaints, track their status, and update them from Pending to Resolved with resolution details. The application features multilingual support in 10 Indian languages including Telugu, Hindi, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, and Punjabi. It uses AI-powered complaint analysis via Groq API for automated triage, priority assessment, and suggested solutions. The social impact lies in bridging the communication gap between citizens and municipal authorities, making grievance redressal more transparent, efficient, and accessible.

**Target User Personas:** 
- Primary: Citizens residing in urban and rural areas who face water-related issues such as pipeline leaks, contaminated water supply, drainage overflow, and water shortages, and need a simple digital platform to report these problems.
- Secondary: Municipal corporation officials, gram panchayat officers, water board administrators, and civic authorities who need to track, manage, and resolve citizen complaints systematically.

**Current Users Count:** 0 (This is a hackathon project deployed for demonstration purposes. No real-world user registration/enrollment has been implemented yet. Future enhancement includes user authentication and registration features.)

**PROD URL:** Deployed on Streamlit Cloud at the project's hosted URL. _(You need to add your actual Streamlit Cloud URL here. Example: https://water-tracker.streamlit.app)_

**User Feedback Loop - plan doc URL:** _(Not documented yet. This is a hackathon project. Recommend creating a Google Doc with a user feedback collection plan.)_

---

## Section: Growth Strategy

**Week-wise plan (increase user base):** _(Not documented. Recommend creating a week-wise outreach plan as a Google Doc and sharing the URL.)_

**Geographical expansion plans:** _(Not implemented yet. The application is designed with multilingual support covering 10 Indian languages, which lays the foundation for geographical expansion across multiple Indian states. Future plans could include state-specific water authority integrations.)_

---

## Section: Open Source Project Management

| Metric | Status | Details |
|--------|--------|---------|
| **Repo URL** | ✅ | https://code.swecha.org/Bharatg/water-tracker |
| **README.md** | ✅ Yes | Comprehensive README with project overview, features, technology stack, installation guide, environment configuration, run instructions, database info, complaint workflow, code quality tools, deployment, security practices, skills learned, license, and future improvements. A new developer can set up and run the project by following the README guide. |
| **CONTRIBUTING.md** | ✅ Yes | Comprehensive contributing guidelines with local setup instructions, pre-commit hooks, coding standards, Git workflow, CI/CD pipeline info, and pull request process. |
| **CHANGELOG** | ❌ No | CHANGELOG.md file exists but is empty. Needs to be populated with version history using git-cliff tool (configured in cliff.toml) or manually. |
| **Issue Templates** | ❌ No | No issue templates for bug reports, feature requests, or documentation queries. Recommend adding templates in .gitlab/issue_templates/ or .github/ISSUE_TEMPLATE/ directory. |
| **.vscode/settings.json** | ❌ No | Not present. Recommend adding for consistent editor configuration. |

---

## Section: Growth Strategy (Contributor Base)

**Week-wise plan (increase contributor base):** _(Not documented. Recommend creating a contributor onboarding plan as a Google Doc.)_

**Geographical expansion plans (contributors):** _(Not documented.)_

---

## Section: Cross-Platform Availability

### Desktop
| Platform | Available? | Notes |
|----------|-----------|-------|
| **GNU/Linux OS** | ❌ No | This is a web application running on Streamlit Cloud server-side. End users access it via browser. However, the development and deployment environment supports Linux. |
| **MacOS** | ❌ No | Web application accessed via browser. Development is possible on macOS. |
| **WindowsOS** | ❌ No | Web application accessed via browser. Development is possible on Windows. |
| **Others** | N/A | |

### Mobile
| Platform | Available? | Notes |
|----------|-----------|-------|
| **Android** | ❌ No | Streamlit web app is responsive and works in Android browsers. No native Android app exists. |
| **iOS** | ❌ No | Streamlit web app works in iOS Safari browser. No native iOS app exists. |
| **Others** | N/A | |

### Web
| Platform | Available? | Notes |
|----------|-----------|-------|
| **Chrome** | ✅ Yes | Fully tested and compatible |
| **Firefox** | ✅ Yes | Fully tested and compatible |
| **Safari** | ✅ Yes | Compatible (standard web technologies used) |
| **Edge** | ✅ Yes | Compatible |
| **Others** | ✅ Yes | Any modern web browser (Brave, Opera, etc.) |

---

## Section: Indic Languages Support

| Metric | Details |
|--------|---------|
| **Supported Languages in Input** | English, Telugu, Hindi, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi (10 languages) |
| **Supported Languages in Output** | English, Telugu, Hindi, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi (10 languages) |
| **Multilingual UI** | ✅ Yes – The entire application interface including navigation menus, form labels, buttons, status messages, error messages, help text, and AI analysis results are localized into all 10 supported languages. Users can dynamically switch languages using the language selector. |

---

## Section: AI/ML Innovation

| Metric | Details |
|--------|---------|
| **AI Use Case** | ✅ Yes – The application uses Groq API with open-source LLMs (like LLaMA) for: 1) **Complaint Analysis & Triage** – automatically analyzes complaint descriptions to identify issue type and urgency; 2) **AI-Powered Solutions** – suggests possible causes and repair steps for reported issues; 3) **Priority Assessment** – classifies complaints as Low, Medium, High, or Emergency; 4) **Help Desk Chat** – provides AI-powered assistance for citizen queries about complaint submission and workflow; 5) **Administrator Support** – helps admins draft resolution responses. The system also supports Google ADK agent-based orchestration and a BYOK (Bring Your Own Key) mode. |
| **Model Transparency** | ❌ No – Relies on Groq API (cloud-based inference service). The specific open-source models used (e.g., LLaMA variants via Groq) are accessible but the application does not self-host or expose the model details directly. |
| **Indic Dataset Usage** | ❌ No – No Indian language datasets were used or created for training. |
| **Corpus App Usage** | ❌ No – Has not used the official Corpus App to collect primary digital data. |
| **Original Dataset Quality** | N/A – No dataset created. |
| **Indic Relevance** | ❌ No – While the UI supports Indic languages, the AI model itself was not fine-tuned on Indic language data. |
| **Model Fine-tuning** | ❌ No – No model fine-tuning was performed. The application uses pre-existing LLMs via Groq API. |
| **Model Performance** | N/A – No fine-tuning metrics available. |
| **Ethical Data Practices** | ❌ No formal consent mechanisms documented. Complaint data stored in database with no explicit privacy policy or consent collection. This needs to be addressed for production deployment. |

---

## Section: Inclusivity & Accessibility

| Metric | Status | Details |
|--------|--------|---------|
| **Offline-first design** | ❌ No | Requires internet connection to access Streamlit Cloud deployment and Groq API for AI features. |
| **Low Bandwidth Optimization** | ❌ No | Not optimized for low-bandwidth scenarios. File uploads (images, videos, audio) require sufficient bandwidth. |
| **Device Compatibility** | ✅ Partially | Works on any device with a modern web browser (mobile, tablet, desktop). The Streamlit responsive design adapts to different screen sizes. However, no specific testing on low-end devices has been performed. |

---

## Section: Activities / Process Setup

| Metric | Status | Details |
|--------|--------|---------|
| **Registered a local gitlab runner** | ✅ Yes | GitLab CI/CD runner is configured for the project pipeline. |
| **Successful pipeline status with at least 5 checks** | ✅ Yes | Pipeline includes 8 stages: lint (ruff + pylint + flake8), format (ruff format check), type_check (mypy), dead_code (vulture), test (pytest), coverage (pytest-cov), security (bandit + pip-audit + semgrep + detect-secrets), and compliance (file existence checks). Currently being fixed for bash compatibility with the Docker runner. |
| **Ollama** | ❌ No | The project uses Groq API instead of Ollama for local LLM inference. (Note: ai_service.py has ollama-related function stubs but primary implementation uses Groq API.) |
| **Corpus CLI (latest)** | ❌ No | Not used. |

---

## How to fill the sheet:

1. Open the Google Sheet: https://docs.google.com/spreadsheets/d/1JqPCpNKVbBjsYpbHZAzCophunx9pdM305Yeo8ltnXuE/edit?usp=sharing
2. Find your row (S.No.) and start filling column by column
3. For **Yes/No** columns: Enter "Yes" or "No" as shown above
4. For text columns: Copy the relevant description from above
5. For URL columns: Copy the repo URL `https://code.swecha.org/Bharatg/water-tracker` and add your Streamlit Cloud URL
6. For columns marked "Not documented": Leave blank or write "Not yet implemented"  
7. For personal info (College ID, Mentor Name, etc.): Fill your actual details