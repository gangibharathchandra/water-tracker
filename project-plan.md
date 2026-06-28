# PROJECT-PLAN.md — Water Issue Tracker 💧
**Civic Complaint Management System | Multilingual Water Issue Reporting Platform**
**Author**: Bharath Chandra | IcfaiTech Hyderabad

---

## 1. Project Overview

Water Issue Tracker is an AI-powered multilingual civic complaint management application built for Indian citizens. It enables citizens to report water-related issues online with supporting proof files (images, videos, audio) and allows administrators to track, manage, and resolve complaints efficiently — accessible in Telugu, Hindi, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, and English via web.

**Live URL**: Deployed on Streamlit Cloud
**Repository**: https://code.swecha.org/Bharatg/water-tracker

---

## 2. Current Feature Status

| Feature | Status |
|---|---|
| Multilingual UI (10 Indian languages) | ✅ Done |
| Online Complaint Submission with Proof Files | ✅ Done |
| File Upload Support (Images, Videos, Audio) | ✅ Done |
| Secure Admin Login with Password Authentication | ✅ Done |
| Complaint Status Workflow (Pending → Resolved) | ✅ Done |
| Admin Resolution Details & Proof Upload | ✅ Done |
| AI-Powered Complaint Analysis & Triage (Groq API) | ✅ Done |
| AI-Powered Suggested Solutions for Complaints | ✅ Done |
| AI Help Desk Chat for Citizen Queries | ✅ Done |
| Google ADK Agent-Based Orchestration | ✅ Done |
| BYOK (Bring Your Own Key) Mode for AI | ✅ Done |
| Streamlit Cloud Deployment | ✅ Done |
| Aiven MySQL Cloud Database | ✅ Done |
| GitLab CI/CD Pipeline with 8 Stages | ✅ Done |
| Ruff Formatter & Code Quality Checks | ✅ Done |
| Internationalization (i18n) & Localization (l10n) | ✅ Done |

---

## 3. Plan for Increasing User Base

### 3.1 Awareness & Outreach
- Partner with **municipal corporations, gram panchayats, and water boards** to introduce Water Issue Tracker as an official complaint channel
- Collaborate with **Swecha Telangana and civic tech communities** for pilot deployments in select wards or villages
- Publish demo videos on YouTube and WhatsApp groups in Telugu, Hindi, and Tamil to reach non-English-speaking citizens
- Register on **state government innovation portals** and **smart city project listings** as a listed civic tool for discoverability

### 3.2 Continuous Improvement of Features
- Collect complaint data patterns from the database to identify most common issue types and geographical hotspots
- Monthly sprint to add new complaint categories based on regional water issues (e.g., borewell drying, flood drainage)
- Use ADK FunctionTool usage logs to identify which AI tools are called most and optimise them
- Add feedback button in complaint tracking UI → logs directly as a GitLab issue for triage
- Regular dependency updates (`pyproject.toml`) and Groq model upgrades as newer Llama versions release

### 3.3 Documented Reference
- Streamlit Docs: https://docs.streamlit.io
- Groq API: https://console.groq.com/docs
- Google ADK Docs: https://google.github.io/adk-docs/
- Aiven MySQL: https://aiven.io/mysql
- GitLab CI/CD: https://docs.gitlab.com/ee/ci/

---

## 4. Geographical Expansion — Horizontal Scaling Plan

### Phase 1 — Telangana (Current)
- Telugu language support already live
- Focus areas: Hyderabad, Warangal, rural districts
- Onboarding via Swecha network and local municipal wards

### Phase 2 — South India (Andhra Pradesh, Tamil Nadu, Karnataka, Kerala)
- Tamil, Kannada, Malayalam support already live
- Partner with **state water supply boards** (e.g., TWAD Board in Tamil Nadu, BWSSB in Karnataka, Kerala Water Authority)
- Add region-specific water issue categories (e.g., Cauvery water disputes, borewell regulations)

### Phase 3 — Hindi Belt & North India (UP, MP, Bihar, Rajasthan, Delhi)
- Hindi support already live
- Partner with **urban local bodies (ULBs)** and **AMRUT mission cities**
- Focus on piped water supply, drainage overflow, and water tanker issues

### Phase 4 — West, East & Northeast India (Maharashtra, Gujarat, West Bengal, Assam, Punjab)
- Marathi, Gujarati, Bengali, Punjabi support already live
- Onboard via **State Water & Sanitation Missions (SWSM)** and **Swachh Bharat Mission**
- Focus on flood drainage, waterlogging, and drinking water quality issues

---

## 5. Onboarding Strategy

| Channel | Target Users | Method |
|---|---|---|
| QR code posters in municipal offices | Walk-in citizens | Scan → submit complaint directly |
| WhatsApp share links | Smartphone users | Share complaint link on local groups |
| Municipal website embed | Online citizens | Embedded Streamlit app on civic portals |
| Ward-level awareness camps | Village/ward citizens | Demo + assisted first submission |
| CSC kiosks | Citizens without smartphones | Operator-assisted complaint registration |
| YouTube/Social media | Young citizens | Demo videos in regional languages |

---

## 6. Roadmap

| Timeline | Milestone |
|---|---|
| Month 1–2 | Deploy on Streamlit Cloud, share live link with Swecha partners |
| Month 3 | Add user registration & authentication for citizens |
| Month 4 | SMS/Email notification integration for complaint status updates |
| Month 5 | Advanced analytics dashboard with visualizations and reports |
| Month 6 | Map integration to plot complaints geographically (GeoJSON/Folium) |
| Month 8 | Escalation mechanism for unresolved complaints beyond time threshold |
| Month 12 | Pilot deployment in 5+ municipal wards with active user base |

---

## 7. Tech Scalability Plan

- **Current**: Single Streamlit Cloud instance (free tier), Aiven MySQL
- **Next**: Migrate complaint file uploads to cloud storage (S3/Azure Blob) for scalable media handling
- **Scale**: Containerized deployment (Dockerfile already present) → move to cloud VM (AWS/GCP/Azure) with load balancer
- **Offline-first**: Implement PWA capabilities for basic complaint submission in low-connectivity areas

---

*Water Issue Tracker — Built for Every Citizen 💧*