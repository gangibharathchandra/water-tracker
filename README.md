# 💧 Water Issue Tracker - Civic Complaint Management System


## 📌 Project Overview

Water Issue Tracker is a web-based civic complaint management application developed using Python and Streamlit.

The project helps citizens report water-related issues and allows administrators to monitor, manage, and resolve complaints efficiently.

Citizens can submit complaints with proof files, while administrators can update complaint status from Pending to Resolved with resolution details.


---

# 🚀 Features


## 👤 Citizen Features

- Report water issues online
- Submit personal details
- Select issue category
- Add location information
- Provide issue description
- Upload proof files

Supported proof formats:

Images:
- PNG
- JPG
- JPEG

Videos:
- MP4
- MOV
- AVI

Audio:
- MP3
- WAV


---

## 🛠 Admin Features

- Secure admin login
- View all complaints
- Track complaint status
- Update complaint status

Status workflow:

Pending 🔴

⬇️

Resolved 🟢


Admin can add:

- Resolution description
- Resolution proof files


---

# 🌐 Internationalization (i18n) and Localization (l10n)


This project implements i18n and l10n concepts.

## i18n (Internationalization)

The application is designed to support multiple languages without changing application logic.

All UI text is separated using translation dictionaries.

Example:

```python
T["submit"]
T["dashboard"]
T["report"]
```

This allows dynamic language switching.


## l10n (Localization)

The interface is localized into multiple Indian languages.

Supported Languages:

- English 🇬🇧
- Telugu తెలుగు
- Hindi हिन्दी
- Tamil தமிழ்
- Kannada ಕನ್ನಡ
- Malayalam മലയാളം
- Marathi मराठी
- Bengali বাংলা
- Gujarati ગુજરાતી
- Punjabi ਪੰਜਾਬੀ


Users can select their preferred language using the language switch option.


---

# 🏗️ Technology Stack


## Frontend

- Streamlit


## Backend

- Python


## Database

- MySQL


## Cloud Services

- Aiven MySQL Database
- Streamlit Cloud Deployment


## Version Control

- Git
- GitHub
- GitLab


---

# 📂 Project Structure


```
water-tracker/

│
├── app.py
│
├── database.py
│
├── utils.py
│
├── requirements.txt
│
├── README.md
│
├── SKILL.md
│
├── .env.example
│
├── uploads/
│
└── .specify/
```


---

# ⚙️ Installation


Clone repository:

```bash
git clone <repository-url>

cd water-tracker
```


Install dependencies:


```bash
pip install -r requirements.txt
```


---

# 🔐 Environment Configuration


Create `.env` file:


```env
DB_HOST=your_database_host

DB_PORT=3306

DB_USER=your_database_user

DB_PASSWORD=your_database_password

DB_NAME=your_database_name


ADMIN_PASSWORD=your_password
```


Secrets should never be committed into Git.


---

# ▶️ Run Application


Start Streamlit:


```bash
streamlit run app.py
```


Application opens in browser.


---

# 🗄️ Database


The application automatically creates the required MySQL tables.

Database operations implemented:

- CREATE
- INSERT
- SELECT
- UPDATE


---

# 🔁 Complaint Workflow


Citizen:

```
Report Issue
      |
      ↓
Pending Status 🔴
```


Admin:


```
Review Complaint
      |
      ↓
Add Resolution
      |
      ↓
Mark Resolved 🟢
```


---

# 🧪 Code Quality


Tools used:

- Ruff Formatter
- GitLab CI/CD Pipeline


Run formatter:

```bash
python -m ruff format .
```


---

# 🚀 Deployment


Application deployed using:

- Streamlit Cloud


Database hosted using:

- Aiven MySQL


---

# 🔒 Security Practices


Implemented:

- Environment variables
- Streamlit secrets
- No hardcoded passwords
- Protected database credentials


---

# 📚 Skills Learned


- Python development
- Streamlit application development
- MySQL integration
- Cloud database usage
- File upload handling
- Authentication basics
- i18n implementation
- l10n implementation
- Git workflow
- GitHub deployment
- GitLab CI/CD


---

# 📄 License


This project is released under:

AGPLv3 License


---

# 👨‍💻 Author


Developed by:

Bharath Chandra


---

# 📌 Project Status


✅ Active Development

Implemented:
- Complaint management
- Admin workflow
- Multilingual support
- Cloud deployment

Future improvements:
- User authentication
- SMS notifications
- Advanced analytics dashboard