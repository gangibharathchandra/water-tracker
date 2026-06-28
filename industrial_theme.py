"""
High-Fidelity Claymorphism Theme for Streamlit
===============================================
Design tokens, CSS injections, and component helpers for the
Digital Clay aesthetic — celebrating soft tactility, candy colors,
and premium physicality. Every element feels like soft-touch silicone.
"""

import streamlit as st

# ═══════════════════════════════════════════════════════════════════════════════
# 1. THEME CSS
# ═══════════════════════════════════════════════════════════════════════════════

THEME_CSS = r"""
/* ══════════════════════════════════════════════════════
   HIGH-FIDELITY CLAYMORPHISM — Complete Theme
   ══════════════════════════════════════════════════════ */

/* ── 1. Font Import ──────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=DM+Sans:wght@400;500;700&display=swap');

/* ── 2. CSS Custom Properties ────────────────────────── */
:root {
  --clay-canvas: #F4F1FA;
  --clay-foreground: #332F3A;
  --clay-muted: #635F69;
  --clay-accent: #7C3AED;
  --clay-accent-alt: #DB2777;
  --clay-tertiary: #0EA5E9;
  --clay-success: #10B981;
  --clay-warning: #F59E0B;
  --clay-card-bg: rgba(255, 255, 255, 0.6);
  --clay-glass-edge: rgba(255, 255, 255, 0.8);
  --font-heading: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --radius-sm: 20px;
  --radius-md: 24px;
  --radius-lg: 32px;
  --radius-xl: 48px;
  --radius-full: 9999px;
  --shadow-clay-deep:
    30px 30px 60px #cdc6d9,
    -30px -30px 60px #ffffff,
    inset 10px 10px 20px rgba(139, 92, 246, 0.05),
    inset -10px -10px 20px rgba(255, 255, 255, 0.8);
  --shadow-clay-card:
    16px 16px 32px rgba(160, 150, 180, 0.2),
    -10px -10px 24px rgba(255, 255, 255, 0.9),
    inset 6px 6px 12px rgba(139, 92, 246, 0.03),
    inset -6px -6px 12px rgba(255, 255, 255, 1);
  --shadow-clay-card-hover:
    20px 20px 40px rgba(160, 150, 180, 0.25),
    -14px -14px 30px rgba(255, 255, 255, 1),
    inset 6px 6px 12px rgba(139, 92, 246, 0.03),
    inset -6px -6px 12px rgba(255, 255, 255, 1);
  --shadow-clay-button:
    12px 12px 24px rgba(139, 92, 246, 0.3),
    -8px -8px 16px rgba(255, 255, 255, 0.4),
    inset 4px 4px 8px rgba(255, 255, 255, 0.4),
    inset -4px -4px 8px rgba(0, 0, 0, 0.1);
  --shadow-clay-button-hover:
    16px 16px 28px rgba(139, 92, 246, 0.35),
    -10px -10px 20px rgba(255, 255, 255, 0.5),
    inset 4px 4px 8px rgba(255, 255, 255, 0.4),
    inset -4px -4px 8px rgba(0, 0, 0, 0.1);
  --shadow-clay-pressed:
    inset 10px 10px 20px #d9d4e3,
    inset -10px -10px 20px #ffffff;
  --shadow-clay-orb:
    8px 8px 16px rgba(139, 92, 246, 0.25),
    -6px -6px 12px rgba(255, 255, 255, 0.6),
    inset 2px 2px 6px rgba(255, 255, 255, 0.5),
    inset -2px -2px 6px rgba(0, 0, 0, 0.05);
  --shadow-clay-orb-hover:
    12px 12px 24px rgba(139, 92, 246, 0.3),
    -8px -8px 16px rgba(255, 255, 255, 0.7),
    inset 2px 2px 6px rgba(255, 255, 255, 0.5),
    inset -2px -2px 6px rgba(0, 0, 0, 0.05);
}

/* ── 3. Base & Reset ─────────────────────────────────── */
.stApp {
  background: var(--clay-canvas) !important;
  font-family: var(--font-body);
  color: var(--clay-foreground);
}

.stApp > header {
  background: transparent !important;
}

.block-container {
  max-width: 72rem !important;
  padding: 2rem 1.5rem !important;
}

@media (min-width: 1024px) {
  .block-container {
    padding: 2rem 3rem !important;
  }
}

/* ── 4. Animated Background Blobs ────────────────────── */
.clay-blobs-container {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: -1;
}

.clay-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.12;
}

.clay-blob-1 {
  width: 65vh;
  height: 65vh;
  background: #7C3AED;
  top: -15%;
  left: -10%;
  animation: clay-float 8s ease-in-out infinite;
}

.clay-blob-2 {
  width: 55vh;
  height: 55vh;
  background: #DB2777;
  top: 40%;
  right: -10%;
  animation: clay-float-delayed 10s ease-in-out infinite;
}

.clay-blob-3 {
  width: 45vh;
  height: 45vh;
  background: #0EA5E9;
  bottom: -10%;
  left: 20%;
  animation: clay-float-slow 12s ease-in-out infinite;
}

/* ── 5. Typography ────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading) !important;
  color: var(--clay-foreground) !important;
}

h1 {
  font-weight: 900 !important;
  font-size: 2.5rem !important;
  line-height: 1.1 !important;
  letter-spacing: -0.02em;
}

@media (min-width: 1024px) {
  h1 { font-size: 3.5rem !important; }
}

h2 { font-weight: 800 !important; font-size: 1.75rem !important; }
h3 { font-weight: 800 !important; font-size: 1.35rem !important; }

p, li, .stMarkdown, div:not([class*="mono"]):not([class*="metric"]) {
  color: var(--clay-foreground);
  font-family: var(--font-body);
  line-height: 1.625;
}

/* Captions and labels */
.stCaption, caption {
  font-family: var(--font-heading) !important;
  font-size: 0.75rem !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  color: var(--clay-muted) !important;
}

/* ── 6. Sidebar ──────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.55) !important;
  backdrop-filter: blur(24px) !important;
  border-right: 1px solid rgba(255, 255, 255, 0.5) !important;
  box-shadow: var(--shadow-clay-card) !important;
}

[data-testid="stSidebar"] * {
  color: var(--clay-foreground) !important;
  font-family: var(--font-body);
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3,
[data-testid="stSidebar"] .stMarkdown h4 {
  color: var(--clay-foreground) !important;
  font-family: var(--font-heading) !important;
}

/* Sidebar header (clay pill) */
.clay-sidebar-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin: 8px 12px 16px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.08), rgba(219, 39, 119, 0.06));
  box-shadow: inset 2px 2px 4px rgba(255,255,255,0.8), inset -2px -2px 4px rgba(0,0,0,0.04);
}

.clay-sidebar-header .logo-mark {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, #A78BFA, #7C3AED);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-weight: 900;
  font-size: 1.1rem;
  color: white;
  box-shadow: var(--shadow-clay-orb);
  flex-shrink: 0;
}

.clay-sidebar-header .brand {
  font-family: var(--font-heading);
  font-weight: 800;
  font-size: 1rem;
  color: var(--clay-foreground);
  line-height: 1.2;
}

.clay-sidebar-header .brand small {
  display: block;
  font-family: var(--font-body);
  font-weight: 500;
  font-size: 0.7rem;
  color: var(--clay-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* ── 7. Navigation Radio Buttons ──────────────────────── */
[data-testid="stSidebar"] .stRadio {
  padding: 0 8px;
}

[data-testid="stSidebar"] .stRadio > div {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

[data-testid="stSidebar"] .stRadio label {
  display: block !important;
  padding: 12px 16px !important;
  border-radius: var(--radius-sm) !important;
  background: transparent !important;
  border: none !important;
  font-family: var(--font-body);
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  transition: all 250ms cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  cursor: pointer;
}

[data-testid="stSidebar"] .stRadio label:hover {
  background: rgba(124, 58, 237, 0.06) !important;
  transform: translateX(4px);
}

[data-testid="stSidebar"] .stRadio input:checked + div,
[data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="true"],
[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.12), rgba(219, 39, 119, 0.08)) !important;
  box-shadow: var(--shadow-clay-pressed) !important;
  font-weight: 700 !important;
  color: var(--clay-accent) !important;
}

[data-testid="stSidebar"] .stRadio input[type="radio"] {
  display: none;
}

[data-testid="stSidebar"] hr {
  border-color: rgba(124, 58, 237, 0.08) !important;
  margin: 12px 16px !important;
}

/* Sidebar selectbox — white bg with white label */
[data-testid="stSidebar"] .stSelectbox label {
  color: #ffffff !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
  background: rgba(255,255,255,0.7) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  color: var(--clay-foreground) !important;
  box-shadow: var(--shadow-clay-pressed) !important;
}

/* ── 8. Buttons ───────────────────────────────────────── */
.stButton button {
  font-family: var(--font-heading) !important;
  font-weight: 800 !important;
  letter-spacing: 0.02em !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: 0 2rem !important;
  min-height: 56px;
  transition: all 200ms cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  box-shadow: var(--shadow-clay-button) !important;
  background: white !important;
  color: var(--clay-foreground) !important;
  cursor: pointer;
}

.stButton button[kind="primary"],
.stButton button[kind="primaryFormSubmit"] {
  background: linear-gradient(135deg, #A78BFA, #7C3AED) !important;
  color: white !important;
  text-shadow: 0 1px 2px rgba(0,0,0,0.15);
}

.stButton button:hover {
  transform: translateY(-2px) !important;
  box-shadow: var(--shadow-clay-button-hover) !important;
}

.stButton button:active {
  transform: scale(0.92) !important;
  box-shadow: var(--shadow-clay-pressed) !important;
}

.stButton button[kind="primary"]:active,
.stButton button[kind="primaryFormSubmit"]:active {
  box-shadow: var(--shadow-clay-pressed) !important;
}

.stButton button[kind="primary"]:hover,
.stButton button[kind="primaryFormSubmit"]:hover {
  filter: brightness(1.05);
}

.stButton button:focus-visible {
  outline: 4px solid rgba(124, 58, 237, 0.2) !important;
  outline-offset: 3px !important;
}

@media (max-width: 640px) {
  .stButton button {
    width: 100% !important;
  }
}

/* ── 9. Input Fields ──────────────────────────────────── */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
  font-family: var(--font-body) !important;
  background: #EFEBF5 !important;
  color: var(--clay-foreground) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: var(--shadow-clay-pressed) !important;
  padding: 1rem 1.5rem !important;
  min-height: 60px;
  font-size: 1rem !important;
  transition: all 250ms cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
  color: var(--clay-muted) !important;
  opacity: 0.6;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
  background: white !important;
  box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.15), var(--shadow-clay-card) !important;
  outline: none !important;
}

/* Select boxes */
.stSelectbox > div > div {
  background: #EFEBF5 !important;
  color: var(--clay-foreground) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: var(--shadow-clay-pressed) !important;
  min-height: 60px;
  font-family: var(--font-body);
}

/* ── 10. Metrics (Clay Orbs) ──────────────────────────── */
[data-testid="stMetric"] {
  background: white !important;
  border: none !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.5rem !important;
  box-shadow: var(--shadow-clay-card) !important;
  transition: all 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  overflow: hidden;
}

[data-testid="stMetric"]:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-clay-card-hover) !important;
}

[data-testid="stMetric"]::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #A78BFA, #7C3AED, #DB2777);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

[data-testid="stMetric"] label,
[data-testid="stMetric"] .stMetricLabel {
  font-family: var(--font-heading) !important;
  font-size: 0.75rem !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  color: var(--clay-muted) !important;
  display: block;
  margin-bottom: 4px;
}

[data-testid="stMetric"] .stMetricValue {
  font-family: var(--font-heading) !important;
  font-size: 2rem !important;
  font-weight: 900 !important;
  color: var(--clay-foreground) !important;
  letter-spacing: -0.03em;
}

/* ── 11. Custom Cards (Glass-Clay) ────────────────────── */
.ai-card {
  background: var(--clay-card-bg) !important;
  backdrop-filter: blur(24px) !important;
  border: 1px solid var(--clay-glass-edge) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.5rem !important;
  margin: 0.75rem 0 !important;
  box-shadow: var(--shadow-clay-card) !important;
  transition: all 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}

.ai-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-clay-card-hover) !important;
}

/* JSON result display */
.json-result {
  background: var(--clay-card-bg) !important;
  backdrop-filter: blur(24px) !important;
  border: 1px solid var(--clay-glass-edge) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.25rem !important;
  margin: 0.75rem 0 !important;
  box-shadow: var(--shadow-clay-card) !important;
  overflow: hidden;
}

.json-result table {
  width: 100%;
  border-collapse: collapse;
}

.json-result td {
  padding: 0.7rem 0.75rem;
  border-bottom: 1px solid rgba(124, 58, 237, 0.08);
  color: var(--clay-foreground);
  font-family: var(--font-body);
  font-size: 0.9rem;
}

.json-result td:first-child {
  font-family: var(--font-heading);
  font-weight: 800;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--clay-muted);
  width: 180px;
}

.json-result tr:last-child td {
  border-bottom: none;
}

/* ── 12. Chat Components ──────────────────────────────── */
.chat-container {
  border: none !important;
  border-radius: var(--radius-lg) !important;
  background: var(--clay-card-bg) !important;
  backdrop-filter: blur(24px) !important;
  box-shadow: var(--shadow-clay-card) !important;
  padding: 1rem !important;
  max-height: 500px;
  overflow-y: auto;
}

.chat-bubble-user {
  background: linear-gradient(135deg, #A78BFA, #7C3AED) !important;
  color: white !important;
  padding: 0.85rem 1.25rem !important;
  border-radius: 24px 24px 4px 24px !important;
  margin: 0.5rem 0 !important;
  max-width: 80% !important;
  margin-left: auto !important;
  box-shadow: 8px 8px 16px rgba(124, 58, 237, 0.2), -4px -4px 8px rgba(255, 255, 255, 0.1) !important;
  word-wrap: break-word;
}

.chat-bubble-ai {
  background: white !important;
  color: var(--clay-foreground) !important;
  padding: 0.85rem 1.25rem !important;
  border-radius: 24px 24px 24px 4px !important;
  margin: 0.5rem 0 !important;
  max-width: 80% !important;
  margin-right: auto !important;
  box-shadow: var(--shadow-clay-card) !important;
  word-wrap: break-word;
}

.chat-avatar-user {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255,255,255,0.3), rgba(255,255,255,0.1));
  color: white;
  font-size: 14px;
  margin-right: 8px;
  vertical-align: middle;
  box-shadow: inset 1px 1px 2px rgba(255,255,255,0.2), inset -1px -1px 2px rgba(0,0,0,0.1);
}

.chat-avatar-ai {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #A78BFA, #7C3AED);
  color: white;
  font-size: 14px;
  margin-right: 8px;
  vertical-align: middle;
  box-shadow: var(--shadow-clay-orb);
}

.chat-timestamp {
  font-family: var(--font-body);
  font-size: 0.7rem;
  opacity: 0.6;
  margin-top: 4px;
  text-align: right;
}

/* ── 13. Status Messages ──────────────────────────────── */
.stAlert {
  border: none !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: var(--shadow-clay-card) !important;
  backdrop-filter: blur(16px) !important;
}

.stSuccess {
  background: rgba(16, 185, 129, 0.1) !important;
  color: #065f46 !important;
  border-left: 4px solid var(--clay-success) !important;
}

.stError {
  background: rgba(219, 39, 119, 0.08) !important;
  color: #831843 !important;
  border-left: 4px solid var(--clay-accent-alt) !important;
}

.stInfo {
  background: rgba(14, 165, 233, 0.1) !important;
  color: #075985 !important;
  border-left: 4px solid var(--clay-tertiary) !important;
}

.stWarning {
  background: rgba(245, 158, 11, 0.1) !important;
  color: #78350f !important;
  border-left: 4px solid var(--clay-warning) !important;
}

/* ── 14. DataFrames ───────────────────────────────────── */
.stDataFrame {
  border-radius: var(--radius-lg) !important;
  overflow: hidden;
  box-shadow: var(--shadow-clay-card) !important;
  backdrop-filter: blur(16px) !important;
}

.stDataFrame table {
  font-family: var(--font-body) !important;
  font-size: 0.85rem !important;
}

.stDataFrame thead tr th {
  background: linear-gradient(135deg, #7C3AED, #A78BFA) !important;
  color: white !important;
  font-family: var(--font-heading) !important;
  font-size: 0.75rem !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  padding: 0.85rem 1rem !important;
}

.stDataFrame tbody tr td {
  padding: 0.75rem 1rem !important;
  border-bottom: 1px solid rgba(124, 58, 237, 0.06) !important;
  color: var(--clay-foreground) !important;
}

.stDataFrame tbody tr:nth-child(even) td {
  background: rgba(124, 58, 237, 0.02) !important;
}

.stDataFrame tbody tr:hover td {
  background: rgba(124, 58, 237, 0.06) !important;
}

/* ── 15. Expanders ────────────────────────────────────── */
.streamlit-expanderHeader {
  background: var(--clay-card-bg) !important;
  backdrop-filter: blur(16px) !important;
  color: var(--clay-foreground) !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: var(--shadow-clay-card) !important;
  font-family: var(--font-heading);
  font-weight: 700 !important;
  padding: 0.85rem 1.25rem !important;
  transition: all 250ms ease;
  border: 1px solid var(--clay-glass-edge) !important;
}

.streamlit-expanderHeader:hover {
  box-shadow: var(--shadow-clay-card-hover) !important;
  transform: translateY(-1px);
}

.streamlit-expanderContent {
  border: none !important;
  background: transparent !important;
  padding: 0.5rem 0 !important;
}

/* ── 16. File Uploader ────────────────────────────────── */
.stFileUploader {
  background: #EFEBF5 !important;
  border: 2px dashed rgba(124, 58, 237, 0.2) !important;
  border-radius: var(--radius-sm) !important;
  padding: 1rem !important;
  box-shadow: var(--shadow-clay-pressed) !important;
  transition: border-color 250ms ease;
}

.stFileUploader:hover {
  border-color: var(--clay-accent) !important;
}

.stFileUploader [data-testid="stFileUploadDropzone"] {
  background: transparent !important;
  border: none !important;
}

/* ── 17. Sliders & Radio Groups ───────────────────────── */
.stSlider label,
.stRadio label {
  color: var(--clay-muted) !important;
  font-family: var(--font-heading) !important;
  font-size: 0.8rem !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

/* ── 18. Spinner ──────────────────────────────────────── */
.stSpinner > div {
  border-color: var(--clay-accent) transparent transparent transparent !important;
  border-width: 4px !important;
}

/* ── 19. Progress ─────────────────────────────────────── */
.stProgress > div > div {
  background: #EFEBF5 !important;
  border-radius: var(--radius-full) !important;
  box-shadow: var(--shadow-clay-pressed) !important;
  height: 10px !important;
}

.stProgress > div > div > div {
  background: linear-gradient(90deg, #A78BFA, #7C3AED) !important;
  border-radius: var(--radius-full) !important;
  box-shadow: 0 0 8px rgba(124, 58, 237, 0.3) !important;
}

/* ── 20. Floating AI Button ───────────────────────────── */
.floating-ai {
  position: fixed;
  right: 1.5rem;
  bottom: 1.5rem;
  z-index: 9999;
  width: 3.75rem;
  height: 3.75rem;
  border-radius: var(--radius-full);
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #A78BFA, #7C3AED);
  color: white;
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 900;
  letter-spacing: 0.02em;
  box-shadow: var(--shadow-clay-button);
  border: 2px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
  user-select: none;
}

.floating-ai:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: var(--shadow-clay-button-hover);
}

.floating-ai:active {
  transform: scale(0.92);
  box-shadow: var(--shadow-clay-pressed);
}

/* ── 21. Clay Stat Orb ────────────────────────────────── */
.clay-orb {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #A78BFA, #7C3AED);
  color: white;
  font-family: var(--font-heading);
  font-weight: 900;
  font-size: 1.2rem;
  box-shadow: var(--shadow-clay-orb);
  transition: all 300ms ease;
}

.clay-orb:hover {
  transform: scale(1.1);
  box-shadow: var(--shadow-clay-orb-hover);
}

/* ── 22. Clay Pill (Benefit/Category Tag) ─────────────── */
.clay-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  border-radius: var(--radius-full);
  background: white;
  box-shadow: var(--shadow-clay-card);
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 0.85rem;
  color: var(--clay-foreground);
  transition: all 250ms ease;
}

.clay-pill:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-clay-card-hover);
}

.clay-pill .pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

/* ── 23. Clay Gradient Text ────────────────────────────── */
.clay-text-gradient {
  background: linear-gradient(135deg, var(--clay-foreground) 20%, var(--clay-accent) 60%, var(--clay-accent-alt));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ── 24. Animations ───────────────────────────────────── */
@keyframes clay-float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(2deg); }
}

@keyframes clay-float-delayed {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(-2deg); }
}

@keyframes clay-float-slow {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(5deg); }
}

@keyframes clay-breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

@keyframes clay-squish {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(0.92); }
}

/* ── 25. Responsive ───────────────────────────────────── */
@media (max-width: 640px) {
  .block-container {
    padding: 1rem 1rem !important;
  }

  h1 { font-size: 2rem !important; }
  h2 { font-size: 1.5rem !important; }

  [data-testid="stMetric"] {
    padding: 1.25rem !important;
  }

  [data-testid="stMetric"] .stMetricValue {
    font-size: 1.5rem !important;
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  [data-testid="stMetric"] .stMetricValue {
    font-size: 1.75rem !important;
  }
}

/* ── 26. Reduced Motion ───────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .clay-blob-1,
  .clay-blob-2,
  .clay-blob-3 {
    animation: none !important;
  }

  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ── 27. Tabs ─────────────────────────────────────────── */
.stTabs [role="tablist"] {
  gap: 6px;
  background: #EFEBF5;
  padding: 6px;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-clay-pressed);
}

.stTabs [role="tab"] {
  background: transparent !important;
  color: var(--clay-muted) !important;
  border: none !important;
  border-radius: 16px !important;
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 0.85rem;
  padding: 0.5rem 1.25rem !important;
  transition: all 200ms ease;
}

.stTabs [role="tab"][aria-selected="true"] {
  background: white !important;
  color: var(--clay-accent) !important;
  box-shadow: var(--shadow-clay-card) !important;
}

.stTabs [role="tab"]:hover {
  color: var(--clay-accent) !important;
}

/* ── 28. Image hover (gentle lift) ────────────────────── */
.clay-image {
  border-radius: var(--radius-md);
  transition: all 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.clay-image:hover {
  transform: scale(1.02) translateY(-4px);
  box-shadow: var(--shadow-clay-card-hover);
}

/* ── 29. Groq link ────────────────────────────────────── */
.groq-link {
  display: inline-block;
  margin-top: 0.25rem;
  font-size: 0.85rem;
}

.groq-link a {
  font-family: var(--font-body);
  color: var(--clay-accent) !important;
  text-decoration: underline;
  text-underline-offset: 2px;
  font-weight: 500;
  transition: opacity 200ms ease;
}

.groq-link a:hover {
  opacity: 0.8;
}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# 2. DECORATIVE HELPERS
# ═══════════════════════════════════════════════════════════════════════════════


def blob_background() -> str:
    """Render the animated clay blobs."""
    return (
        '<div class="clay-blobs-container">'
        '<div class="clay-blob clay-blob-1"></div>'
        '<div class="clay-blob clay-blob-2"></div>'
        '<div class="clay-blob clay-blob-3"></div>'
        '</div>'
    )


def sidebar_header() -> str:
    """Clay-style sidebar header with gradient mark."""
    return (
        '<div class="clay-sidebar-header">'
        '<div class="logo-mark">WT</div>'
        '<div class="brand">'
        'Water Tracker'
        '<small>Civic Platform</small>'
        '</div>'
        '</div>'
    )


def clay_pill(label: str = 'ACTIVE', color: str = '#7C3AED') -> str:
    """Render a clay pill/tag with colored dot."""
    return (
        f'<span class="clay-pill">'
        f'<span class="pill-dot" style="background:{color};box-shadow:0 0 6px {color}40;"></span>'
        f'{label}'
        f'</span>'
    )


def clay_orb(letter: str = 'W', gradient: str = '135deg, #A78BFA, #7C3AED') -> str:
    """Render a clay stat orb with gradient."""
    return f'<span class="clay-orb" style="background:linear-gradient({gradient});">{letter}</span>'


def apply_theme(show_floating_ai: bool = True) -> None:
    """Inject the complete Claymorphism theme."""
    parts = [
        f'<style>{THEME_CSS}</style>',
        blob_background(),
    ]
    if show_floating_ai:
        parts.append('<div class="floating-ai" title="AI Assistant">AI</div>')
    st.markdown('\n'.join(parts), unsafe_allow_html=True)
