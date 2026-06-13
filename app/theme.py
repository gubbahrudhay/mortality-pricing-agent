"""
Shared Theme — QDT-Inspired Alternating White/Dark Sections (Fixed)
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

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
        }

        [data-testid="stAppViewContainer"] {
            background: #ffffff;
        }

        [data-testid="stSidebar"] {
            background: #fafafa;
            border-right: 1px solid #ececec;
        }

        /* Fix: sidebar nav link text visibility */
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNav"] span,
        section[data-testid="stSidebar"] a,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] li {
            color: #16191c !important;
        }
        [data-testid="stSidebarNav"] a:hover,
        section[data-testid="stSidebar"] a:hover {
            color: #14b8a6 !important;
            background: #f0fdfa !important;
        }

        h1, h2, h3 {
            font-family: 'Plus Jakarta Sans', "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
            font-weight: 700;
            letter-spacing: -0.01em;
            color: #16191c;
        }

        /* ================= HERO (dark halftone) ================= */
        .hero-dark {
            position: relative;
            border-radius: 18px;
            padding: 80px 50px;
            margin-bottom: 8px;
            overflow: hidden;
            background:
                radial-gradient(circle at 75% 35%, rgba(94,234,212,0.30) 0%, transparent 45%),
                radial-gradient(circle at 30% 70%, rgba(20,184,166,0.18) 0%, transparent 50%),
                linear-gradient(135deg, #0d1f24 0%, #0a1518 60%);
        }
        .hero-dark::before {
            content: "";
            position: absolute;
            inset: 0;
            background-image: radial-gradient(rgba(94,234,212,0.35) 1px, transparent 1.2px);
            background-size: 9px 9px;
            -webkit-mask-image: radial-gradient(ellipse 70% 60% at 70% 35%, black 0%, transparent 70%);
            mask-image: radial-gradient(ellipse 70% 60% at 70% 35%, black 0%, transparent 70%);
            opacity: 0.5;
        }
        .hero-dark-content {
            position: relative;
            z-index: 2;
        }
        .hero-dark-title {
            font-size: 1.9rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.3;
            white-space: nowrap;
            margin-bottom: 0;
        }
        @media (max-width: 900px) {
            .hero-dark-title {
                font-size: 1.4rem;
                white-space: normal;
            }
        }
        .hero-dark-sub {
            font-size: 1.1rem;
            font-weight: 500;
            color: #cfe8e4;
            margin-top: 6px;
        }

        /* ================= LIGHT SECTION BELOW HERO ================= */
        .hero-light {
            background: #fafafa;
            border: 1px solid #ececec;
            border-radius: 18px;
            padding: 36px 50px;
            margin-bottom: 48px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 32px;
            flex-wrap: wrap;
        }
        .hero-light-title {
            font-size: 1.6rem;
            font-weight: 800;
            color: #16191c;
            line-height: 1.35;
            max-width: 28ch;
        }
        .hero-light-desc {
            font-size: 0.95rem;
            color: #6b7280;
            line-height: 1.7;
            max-width: 40ch;
        }
        .pill-btn {
            display: inline-block;
            background: #16191c;
            color: #ffffff !important;
            font-weight: 600;
            font-size: 0.9rem;
            padding: 12px 26px;
            border-radius: 999px;
            text-decoration: none !important;
            white-space: nowrap;
            transition: background 0.2s ease;
        }
        .pill-btn:hover {
            background: #14b8a6;
        }

        /* ================= SECTION HEADERS ================= */
        .section-tag {
            display: inline-block;
            background: #f0fdfa;
            color: #0d9488;
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
            margin-bottom: 32px;
            flex-wrap: wrap;
        }
        .section-title {
            font-size: 1.9rem;
            font-weight: 800;
            color: #16191c;
            line-height: 1.3;
            max-width: 32ch;
        }

        /* ================= DARK FEATURE CARDS ================= */
        .dark-card {
            position: relative;
            background: #0d1f24;
            border-radius: 16px;
            padding: 28px 24px;
            height: 100%;
            overflow: hidden;
            transition: transform 0.25s ease;
            border: 1px solid #1c3338;
        }
        .dark-card:hover {
            transform: translateY(-4px);
        }
        .dark-card-pattern {
            position: absolute;
            top: -20px; right: -20px;
            width: 140px; height: 140px;
            background-image: radial-gradient(circle, rgba(94,234,212,0.45) 1.3px, transparent 1.6px);
            background-size: 11px 11px;
            -webkit-mask-image: radial-gradient(circle, black 0%, transparent 75%);
            mask-image: radial-gradient(circle, black 0%, transparent 75%);
            opacity: 0.6;
        }
        .dark-card-index {
            font-size: 0.78rem;
            color: #5eead4;
            font-weight: 600;
            letter-spacing: 0.1em;
            margin-bottom: 18px;
        }
        .dark-card-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 10px;
            position: relative;
            z-index: 2;
        }
        .dark-card-text {
            font-size: 0.88rem;
            color: #9fb6b3;
            line-height: 1.65;
            position: relative;
            z-index: 2;
        }

        /* ================= FULL CLICKABLE DARK CARDS ================= */
        div[data-testid="stPageLink"] {
            margin-top: -1px;
        }
        div[data-testid="stPageLink"] a {
            display: block !important;
            background: #0d1f24 !important;
            border: 1px solid #1c3338 !important;
            border-radius: 16px !important;
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
            border-color: #14b8a6 !important;
        }
        /* Title line (bold, first paragraph) */
        div[data-testid="stPageLink"] a strong {
            color: #ffffff !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stPageLink"] a p:first-of-type {
            margin: 0 0 10px 0 !important;
        }
        /* Description line (second paragraph) */
        div[data-testid="stPageLink"] a p:nth-of-type(2) {
            color: #9fb6b3 !important;
            font-size: 0.88rem !important;
            font-weight: 400 !important;
            line-height: 1.65 !important;
            margin: 0 !important;
            white-space: normal !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
        }

        /* ================= STAT CARDS (for calculator pages) ================= */
        .stat-block {
            background: #fafafa;
            border: 1px solid #ececec;
            border-radius: 14px;
            padding: 24px 26px;
        }
        .glass-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 10px;
        }
        .glass-value {
            font-size: 2.4rem;
            font-weight: 800;
            color: #16191c;
            line-height: 1.1;
        }
        .glass-value.coral { color: #d97706; }
        .glass-value.cyan { color: #0d9488; }
        .glass-sub { font-size: 0.85rem; color: #9ca3af; margin-top: 8px; }
        .glass-card { padding: 0; background: none; border: none; }

        /* ================= ARCHITECTURE / TEAM TEXT BLOCKS ================= */
        .arch-block code {
            background: #f0fdfa;
            color: #0d9488;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .arch-block p, .team-block p {
            color: #6b7280;
        }
        .team-block strong {
            color: #16191c;
        }

        /* ================= SIDEBAR widget labels ================= */
        section[data-testid="stSidebar"] .stSlider label,
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stNumberInput label {
            color: #6b7280 !important;
        }

        /* Sidebar headers (e.g. "Control Panel") */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: #16191c !important;
        }

        /* ================= BUTTONS ================= */
        .stButton button, .stDownloadButton button {
            background: #16191c;
            border: none;
            border-radius: 999px;
            color: #ffffff;
            font-weight: 600;
            padding: 10px 24px;
            transition: background 0.2s ease;
        }
        .stButton button:hover, .stDownloadButton button:hover {
            background: #14b8a6;
            color: #ffffff;
        }

        /* ================= DIVIDERS ================= */
        .glass-divider {
            border: none;
            border-top: 1px solid #ececec;
            margin: 48px 0;
        }

        /* ================= FIX: NATIVE WIDGET TEXT VISIBILITY ================= */
        /* Chat messages (AI Assistant page) */
        [data-testid="stChatMessage"],
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] div,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessageContent"],
        [data-testid="stChatMessageContent"] p {
            color: #16191c !important;
        }
        [data-testid="stChatMessage"] {
            background: #fafafa !important;
            border: 1px solid #ececec !important;
            border-radius: 14px !important;
        }

        /* DataFrames / Tables (Pricing Calculator, Scenario pages) */
        [data-testid="stDataFrame"],
        [data-testid="stDataFrame"] *,
        [data-testid="stTable"],
        [data-testid="stTable"] * {
            color: #16191c !important;
        }
        [data-testid="stDataFrame"] {
            background: #ffffff !important;
        }

        /* st.info / st.success / st.warning / st.error boxes */
        [data-testid="stAlert"],
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] div {
            color: #16191c !important;
        }

        /* Text input fields (sidebar, AI Assistant) */
        [data-testid="stTextInput"] input,
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInputContainer"] textarea {
            color: #16191c !important;
            background: #ffffff !important;
        }

        /* Expander headers/content (Tool Execution trace) */
        [data-testid="stExpander"],
        [data-testid="stExpander"] *,
        details, summary {
            color: #16191c !important;
        }
    </style>
    """, unsafe_allow_html=True)


def metric_card(label, value, sub=None, color="dark"):
    """
    Render a stat card.
    color: "dark" (default, charcoal) or "amber"/"teal" accents
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