"""
Shared Theme — Unified Dark UI
Inject this CSS at the top of every page for a consistent look.

Usage:
    from app.theme import inject_theme
    inject_theme()
"""

import streamlit as st


def inject_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        :root {
            --bg-main: #0b1014;
            --bg-panel: #11181d;
            --bg-card: #161f25;
            --bg-card-alt: #1c2730;
            --border: #26323a;
            --text-primary: #eef2f4;
            --text-secondary: #9fb2bb;
            --text-muted: #6f8089;
            --accent: #2dd4bf;
            --accent-strong: #14b8a6;
            --accent-soft: rgba(45, 212, 191, 0.12);
            --amber: #f59e0b;
            --radius: 16px;
        }

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
            color: var(--text-primary);
        }

        /* ================= GLOBAL BACKGROUND ================= */
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        .main {
            background: var(--bg-main) !important;
        }

        [data-testid="stSidebar"] {
            background: var(--bg-panel) !important;
            border-right: 1px solid var(--border);
        }

        /* ================= SIDEBAR NAV ================= */
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNav"] span,
        section[data-testid="stSidebar"] a,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            color: var(--text-secondary) !important;
        }
        [data-testid="stSidebarNav"] a:hover,
        section[data-testid="stSidebar"] a:hover {
            color: var(--accent) !important;
            background: var(--accent-soft) !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            color: var(--accent) !important;
            background: var(--accent-soft) !important;
            border-radius: 8px;
        }

        /* Sidebar headers e.g. "Control Panel" */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: var(--text-primary) !important;
            font-weight: 700;
        }

        /* ================= HEADINGS ================= */
        h1, h2, h3, h4 {
            font-family: 'Plus Jakarta Sans', "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
            font-weight: 700;
            letter-spacing: -0.01em;
            color: var(--text-primary) !important;
        }
        p, span, label, li {
            color: var(--text-secondary);
        }

        /* ================= HERO ================= */
        .hero-dark {
            position: relative;
            border-radius: var(--radius);
            padding: 60px 50px;
            margin-bottom: 28px;
            overflow: hidden;
            background:
                radial-gradient(circle at 75% 35%, rgba(45,212,191,0.22) 0%, transparent 45%),
                radial-gradient(circle at 30% 70%, rgba(20,184,166,0.14) 0%, transparent 50%),
                linear-gradient(135deg, #14232a 0%, #0b1014 70%);
            border: 1px solid var(--border);
        }
        .hero-dark::before {
            content: "";
            position: absolute;
            inset: 0;
            background-image: radial-gradient(rgba(94,234,212,0.30) 1px, transparent 1.2px);
            background-size: 9px 9px;
            -webkit-mask-image: radial-gradient(ellipse 70% 60% at 70% 35%, black 0%, transparent 70%);
            mask-image: radial-gradient(ellipse 70% 60% at 70% 35%, black 0%, transparent 70%);
            opacity: 0.5;
        }
        .hero-dark-content { position: relative; z-index: 2; }
        .hero-dark-title {
            font-size: 1.9rem;
            font-weight: 800;
            color: #ffffff !important;
            line-height: 1.3;
            white-space: nowrap;
            margin-bottom: 0;
        }
        @media (max-width: 900px) {
            .hero-dark-title { font-size: 1.4rem; white-space: normal; }
        }
        .hero-dark-sub {
            font-size: 1.1rem;
            font-weight: 500;
            color: #b9e6df !important;
            margin-top: 6px;
        }

        /* ================= INTRO BAND (dark panel) ================= */
        .hero-light {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 32px 50px;
            margin-bottom: 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 32px;
            flex-wrap: wrap;
        }
        .hero-light-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--text-primary) !important;
            line-height: 1.35;
            max-width: 30ch;
        }
        .hero-light-desc {
            font-size: 0.95rem;
            color: var(--text-secondary) !important;
            line-height: 1.7;
            max-width: 42ch;
        }
        .pill-btn {
            display: inline-block;
            background: var(--accent-strong);
            color: #04201c !important;
            font-weight: 700;
            font-size: 0.9rem;
            padding: 12px 26px;
            border-radius: 999px;
            text-decoration: none !important;
            white-space: nowrap;
            transition: background 0.2s ease;
        }
        .pill-btn:hover { background: var(--accent); }

        /* ================= SECTION HEADERS ================= */
        .section-tag {
            display: inline-block;
            background: var(--accent-soft);
            color: var(--accent) !important;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 6px 14px;
            border-radius: 999px;
            margin-bottom: 16px;
        }
        .section-title-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 24px;
            margin-bottom: 28px;
            flex-wrap: wrap;
        }
        .section-title {
            font-size: 1.9rem;
            font-weight: 800;
            color: var(--text-primary) !important;
            line-height: 1.3;
            max-width: 32ch;
        }

        /* ================= FEATURE / DARK CARDS ================= */
        .dark-card {
            position: relative;
            background: var(--bg-card);
            border-radius: var(--radius);
            padding: 28px 24px;
            height: 100%;
            overflow: hidden;
            transition: transform 0.25s ease, border-color 0.25s ease;
            border: 1px solid var(--border);
        }
        .dark-card:hover { transform: translateY(-4px); border-color: var(--accent-strong); }
        .dark-card-pattern {
            position: absolute;
            top: -20px; right: -20px;
            width: 140px; height: 140px;
            background-image: radial-gradient(circle, rgba(45,212,191,0.35) 1.3px, transparent 1.6px);
            background-size: 11px 11px;
            -webkit-mask-image: radial-gradient(circle, black 0%, transparent 75%);
            mask-image: radial-gradient(circle, black 0%, transparent 75%);
            opacity: 0.6;
        }
        .dark-card-index {
            font-size: 0.78rem;
            color: var(--accent) !important;
            font-weight: 600;
            letter-spacing: 0.1em;
            margin-bottom: 18px;
        }
        .dark-card-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #ffffff !important;
            margin-bottom: 10px;
            position: relative;
            z-index: 2;
        }
        .dark-card-text {
            font-size: 0.88rem;
            color: var(--text-secondary) !important;
            line-height: 1.65;
            position: relative;
            z-index: 2;
        }

        /* ================= CLICKABLE FEATURE CARDS (page links) ================= */
        div[data-testid="stPageLink"] { margin-top: -1px; }
        div[data-testid="stPageLink"] a {
            display: block !important;
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            padding: 28px 24px !important;
            text-decoration: none !important;
            transition: transform 0.25s ease, border-color 0.25s ease;
            white-space: normal !important;
            min-height: 170px;
            overflow: hidden;
            box-sizing: border-box;
            width: 100% !important;
        }
        div[data-testid="stPageLink"] a:hover {
            transform: translateY(-4px);
            border-color: var(--accent-strong) !important;
        }
        div[data-testid="stPageLink"] a strong {
            color: #ffffff !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stPageLink"] a p:first-of-type { margin: 0 0 10px 0 !important; }
        div[data-testid="stPageLink"] a p:nth-of-type(2) {
            color: var(--text-secondary) !important;
            font-size: 0.88rem !important;
            font-weight: 400 !important;
            line-height: 1.65 !important;
            margin: 0 !important;
            white-space: normal !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
        }

        /* ================= STAT / METRIC CARDS ================= */
        .stat-block {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px 26px;
            height: 100%;
        }
        .glass-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-muted) !important;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 10px;
        }
        .glass-value {
            font-size: 2.4rem;
            font-weight: 800;
            color: var(--text-primary) !important;
            line-height: 1.1;
        }
        .glass-value.coral { color: var(--amber) !important; }
        .glass-value.cyan { color: var(--accent) !important; }
        .glass-sub { font-size: 0.85rem; color: var(--text-muted) !important; margin-top: 8px; }
        .glass-card { padding: 0; background: none; border: none; }

        /* ================= ARCHITECTURE / TEAM BLOCKS ================= */
        .arch-block code {
            background: var(--accent-soft);
            color: var(--accent) !important;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .arch-block p, .team-block p { color: var(--text-secondary) !important; }
        .team-block strong { color: var(--text-primary) !important; }

        /* ================= SIDEBAR WIDGET LABELS ================= */
        section[data-testid="stSidebar"] .stSlider label,
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stNumberInput label {
            color: var(--text-secondary) !important;
        }
        /* Slider numeric readouts */
        section[data-testid="stSidebar"] [data-testid="stTickBarMin"],
        section[data-testid="stSidebar"] [data-testid="stTickBarMax"],
        section[data-testid="stSidebar"] [data-baseweb="slider"] div {
            color: var(--text-muted) !important;
        }
        /* Selectbox / number input boxes */
        section[data-testid="stSidebar"] [data-baseweb="select"] > div,
        section[data-testid="stSidebar"] input {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
        }
        section[data-testid="stSidebar"] [data-baseweb="select"] svg {
            fill: var(--text-secondary) !important;
        }

        /* ================= BUTTONS ================= */
        .stButton button, .stDownloadButton button {
            background: var(--accent-strong);
            border: none;
            border-radius: 999px;
            color: #04201c !important;
            font-weight: 700;
            padding: 10px 24px;
            transition: background 0.2s ease;
        }
        .stButton button:hover, .stDownloadButton button:hover {
            background: var(--accent);
            color: #04201c !important;
        }
        /* Sidebar sample-prompt buttons: full width, left aligned text */
        section[data-testid="stSidebar"] .stButton button {
            background: var(--bg-card);
            color: var(--text-secondary) !important;
            border: 1px solid var(--border);
            font-weight: 500;
            text-align: left;
            white-space: normal;
        }
        section[data-testid="stSidebar"] .stButton button:hover {
            background: var(--accent-soft);
            color: var(--accent) !important;
            border-color: var(--accent-strong);
        }

        /* ================= DIVIDERS ================= */
        .glass-divider {
            border: none;
            border-top: 1px solid var(--border);
            margin: 44px 0;
        }

        /* ================= CHAT MESSAGES ================= */
        [data-testid="stChatMessage"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 14px !important;
        }
        [data-testid="stChatMessage"],
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] div,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessageContent"],
        [data-testid="stChatMessageContent"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] code {
            color: var(--text-primary) !important;
        }
        [data-testid="stChatMessage"] code {
            background: var(--bg-card-alt) !important;
        }

        /* Chat input box */
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInputContainer"] textarea,
        [data-testid="stChatInputContainer"] {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
        }
        [data-testid="stChatInput"] button svg { fill: var(--accent) !important; }

        /* ================= DATAFRAMES / TABLES ================= */
        [data-testid="stDataFrame"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }
        [data-testid="stDataFrame"] * {
            color: var(--text-primary) !important;
        }
        [data-testid="stTable"],
        [data-testid="stTable"] * {
            color: var(--text-primary) !important;
            background: var(--bg-card) !important;
        }
        /* glide-data-grid canvas backgrounds used by st.dataframe */
        [data-testid="stDataFrame"] canvas {
            background: var(--bg-card) !important;
        }

        /* ================= ALERTS (info/success/warning/error) ================= */
        [data-testid="stAlert"] {
            border-radius: 12px !important;
            border: 1px solid var(--border) !important;
        }
        [data-testid="stAlert"],
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] div,
        [data-testid="stAlert"] span {
            color: var(--text-primary) !important;
        }
        /* Info box tint */
        div[data-testid="stAlert"]:has(svg[title="Info"]) {
            background: rgba(45,212,191,0.08) !important;
        }

        /* ================= TEXT INPUTS / NUMBER INPUTS (main area) ================= */
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        .stTextInput input,
        .stNumberInput input {
            color: var(--text-primary) !important;
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
        }

        /* ================= EXPANDER ================= */
        [data-testid="stExpander"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }
        [data-testid="stExpander"] *,
        details, summary {
            color: var(--text-primary) !important;
        }
        [data-testid="stExpander"] textarea {
            background: var(--bg-card-alt) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
        }

        /* ================= MARKDOWN CODE BLOCKS ================= */
        code {
            background: var(--bg-card-alt) !important;
            color: var(--accent) !important;
            border-radius: 4px;
        }
        pre {
            background: var(--bg-card-alt) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
        }

        /* ================= HORIZONTAL RULE DEFAULT ================= */
        hr { border-color: var(--border) !important; }

        /* ================= PLOTLY / CHART CONTAINERS ================= */
        .js-plotly-plot, .plot-container {
            background: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)


def metric_card(label, value, sub=None, color="dark"):
    """
    Render a stat card.
    color: "dark" (default), "amber"/"teal" accents
    """
    color_class = "coral" if color == "amber" else ("cyan" if color == "teal" else "")
    sub_html = f'<div class="glass-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="stat-block">
        <div class="glass-label">{label}</div>
        <div class="glass-value {color_class}">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)
