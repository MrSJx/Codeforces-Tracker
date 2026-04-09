import streamlit as st
import requests
import json
import os
import threading
import time
from datetime import datetime, timedelta

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CF Contest Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

/* Hero Header */
.hero-header {
    background: linear-gradient(135deg, #0a0a0f 0%, #0d0d1a 50%, #0a0a0f 100%);
    border: 1px solid #1e1e3a;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 30% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 50%, rgba(236, 72, 153, 0.06) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a5b4fc, #818cf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -1px;
}
.hero-sub {
    color: #6b7280;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    margin-top: 0.5rem;
    letter-spacing: 0.05em;
}
.live-badge {
    display: inline-block;
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.3);
    border-radius: 20px;
    padding: 0.2rem 0.9rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    margin-top: 0.8rem;
}
.live-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #4ade80;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Stats Row */
.stat-card {
    background: #0d0d1a;
    border: 1px solid #1e1e3a;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.stat-num {
    font-size: 2.2rem;
    font-weight: 800;
    color: #818cf8;
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #6b7280;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

/* Contest Card */
.contest-card {
    background: #0d0d1a;
    border: 1px solid #1e1e3a;
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s ease, transform 0.2s ease;
    position: relative;
    overflow: hidden;
}
.contest-card:hover {
    border-color: #4338ca;
    transform: translateY(-2px);
}
.contest-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #818cf8, #ec4899);
    border-radius: 3px 0 0 3px;
}
.contest-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8e8f0;
    margin-bottom: 0.5rem;
}
.contest-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #6b7280;
}
.tag {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    margin-right: 0.4rem;
}
.tag-div1 { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); }
.tag-div2 { background: rgba(251, 146, 60, 0.15); color: #fb923c; border: 1px solid rgba(251, 146, 60, 0.3); }
.tag-div3 { background: rgba(250, 204, 21, 0.15); color: #facc15; border: 1px solid rgba(250, 204, 21, 0.3); }
.tag-div4 { background: rgba(74, 222, 128, 0.15); color: #4ade80; border: 1px solid rgba(74, 222, 128, 0.3); }
.tag-other { background: rgba(129, 140, 248, 0.15); color: #a5b4fc; border: 1px solid rgba(165, 180, 252, 0.3); }
.tag-edu { background: rgba(34, 211, 238, 0.15); color: #22d3ee; border: 1px solid rgba(34, 211, 238, 0.3); }

/* Countdown */
.countdown {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: #a5b4fc;
}
.countdown-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Reminder Panel */
.reminder-panel {
    background: #0d0d1a;
    border: 1px solid #1e1e3a;
    border-radius: 14px;
    padding: 1.5rem;
}
.reminder-item {
    background: #111127;
    border: 1px solid #1e1e3a;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.reminder-icon {
    font-size: 1.4rem;
}
.reminder-name {
    font-weight: 700;
    font-size: 0.9rem;
    color: #e8e8f0;
}
.reminder-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #6b7280;
    margin-top: 0.2rem;
}

/* Filter bar */
.filter-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #6b7280;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}

/* Section header */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #a5b4fc;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
    border-bottom: 1px solid #1e1e3a;
    padding-bottom: 0.6rem;
    margin-bottom: 1.2rem;
}

/* Streamlit overrides */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #4338ca, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 1.2rem !important;
    transition: opacity 0.2s ease !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.85 !important;
}
div[data-testid="stSelectbox"] > div {
    background: #111127 !important;
    border-color: #1e1e3a !important;
    color: #e8e8f0 !important;
    border-radius: 8px !important;
}
.stAlert {
    border-radius: 10px !important;
}
div[data-testid="stMetricValue"] {
    color: #818cf8 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ───────────────────────────────────────────────────────────────
REMINDERS_FILE = "reminders.json"
CF_API = "https://codeforces.com/api/contest.list"

# ─── Data Layer ──────────────────────────────────────────────────────────────
def load_reminders() -> dict:
    if os.path.exists(REMINDERS_FILE):
        try:
            with open(REMINDERS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_reminders(reminders: dict):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)

def fetch_contests() -> list:
    try:
        resp = requests.get(CF_API, timeout=10)
        data = resp.json()
        if data["status"] != "OK":
            return []
        contests = [c for c in data["result"] if c["phase"] == "BEFORE"]
        contests.sort(key=lambda x: x["startTimeSeconds"])
        return contests
    except Exception:
        return []

# ─── Helpers ─────────────────────────────────────────────────────────────────
def format_time(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime("%a, %d %b %Y  %H:%M")

def format_duration(secs: int) -> str:
    h = secs // 3600
    m = (secs % 3600) // 60
    return f"{h}h {m}m" if m else f"{h}h"

def countdown(ts: int) -> str:
    diff = ts - time.time()
    if diff <= 0:
        return "Starting now!"
    d = int(diff // 86400)
    h = int((diff % 86400) // 3600)
    m = int((diff % 3600) // 60)
    if d > 0:
        return f"{d}d {h}h {m}m"
    if h > 0:
        return f"{h}h {m}m"
    return f"{m}m"

def get_division_tag(name: str) -> str:
    n = name.lower()
    if "educational" in n:
        return "edu"
    if "div. 1" in n and "div. 2" not in n:
        return "div1"
    if "div. 1 + div. 2" in n or ("div. 1" in n and "div. 2" in n):
        return "div12"
    if "div. 2" in n:
        return "div2"
    if "div. 3" in n:
        return "div3"
    if "div. 4" in n:
        return "div4"
    return "other"

DIV_LABELS = {
    "edu": ("Educational", "tag-edu"),
    "div1": ("Div. 1", "tag-div1"),
    "div12": ("Div. 1+2", "tag-div1"),
    "div2": ("Div. 2", "tag-div2"),
    "div3": ("Div. 3", "tag-div3"),
    "div4": ("Div. 4", "tag-div4"),
    "other": ("Other", "tag-other"),
}

def send_notification(title: str, message: str):
    """Send a system notification using plyer."""
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name="CF Tracker",
            timeout=10,
        )
    except Exception:
        pass  # plyer may not work in all environments

# ─── Background Notification Thread ──────────────────────────────────────────
def notification_loop():
    while True:
        reminders = load_reminders()
        now = datetime.now()
        to_remove = []
        for contest_id, info in reminders.items():
            remind_at = datetime.fromisoformat(info["remind_at"])
            if now >= remind_at and not info.get("fired", False):
                send_notification(
                    "⚡ Contest Reminder",
                    f"{info['name']} starts in {info['minutes_before']} minutes!",
                )
                info["fired"] = True
                to_remove.append(contest_id)
        if to_remove:
            for k in to_remove:
                reminders[k]["fired"] = True
            save_reminders(reminders)
        time.sleep(60)

# Start background thread once per session
if "notif_thread_started" not in st.session_state:
    t = threading.Thread(target=notification_loop, daemon=True)
    t.start()
    st.session_state["notif_thread_started"] = True

# ─── Session State ────────────────────────────────────────────────────────────
if "contests" not in st.session_state:
    st.session_state.contests = []
if "last_fetch" not in st.session_state:
    st.session_state.last_fetch = None

# ─── Hero Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-title">⚡ CF Contest Tracker</div>
    <div class="hero-sub">// codeforces.com/api · real-time contest intelligence</div>
    <div class="live-badge">
        <span class="live-dot"></span>LIVE DATA
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Fetch / Refresh ─────────────────────────────────────────────────────────
col_refresh, col_spacer = st.columns([1, 5])
with col_refresh:
    if st.button("🔄 Refresh Contests"):
        st.session_state.contests = fetch_contests()
        st.session_state.last_fetch = datetime.now().strftime("%H:%M:%S")
        st.rerun()

if not st.session_state.contests:
    with st.spinner("Fetching contests from Codeforces..."):
        st.session_state.contests = fetch_contests()
        st.session_state.last_fetch = datetime.now().strftime("%H:%M:%S")

contests = st.session_state.contests
reminders = load_reminders()

# ─── Stats Row ───────────────────────────────────────────────────────────────
upcoming_7d = [c for c in contests if c["startTimeSeconds"] - time.time() < 7 * 86400]
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-num">{len(contests)}</div>
        <div class="stat-label">UPCOMING CONTESTS</div>
    </div>""", unsafe_allow_html=True)
with s2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-num">{len(upcoming_7d)}</div>
        <div class="stat-label">THIS WEEK</div>
    </div>""", unsafe_allow_html=True)
with s3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-num">{len(reminders)}</div>
        <div class="stat-label">REMINDERS SET</div>
    </div>""", unsafe_allow_html=True)
with s4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-num">{st.session_state.last_fetch or "—"}</div>
        <div class="stat-label">LAST UPDATED</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Main Layout: Contests + Sidebar ─────────────────────────────────────────
main_col, side_col = st.columns([2.2, 1], gap="large")

with main_col:
    # Filter Bar
    st.markdown('<div class="filter-label">// FILTER BY DIVISION</div>', unsafe_allow_html=True)
    div_options = ["All", "Div. 1", "Div. 2", "Div. 3", "Div. 4", "Educational", "Other"]
    selected_div = st.selectbox("Division", div_options, label_visibility="collapsed")

    st.markdown('<div class="section-header">UPCOMING CONTESTS</div>', unsafe_allow_html=True)

    if not contests:
        st.warning("⚠️ Could not fetch contests. Check your internet connection.")
    else:
        # Apply filter
        filtered = []
        for c in contests:
            tag = get_division_tag(c["name"])
            if selected_div == "All":
                filtered.append(c)
            elif selected_div == "Div. 1" and tag in ("div1", "div12"):
                filtered.append(c)
            elif selected_div == "Div. 2" and tag in ("div2", "div12"):
                filtered.append(c)
            elif selected_div == "Div. 3" and tag == "div3":
                filtered.append(c)
            elif selected_div == "Div. 4" and tag == "div4":
                filtered.append(c)
            elif selected_div == "Educational" and tag == "edu":
                filtered.append(c)
            elif selected_div == "Other" and tag == "other":
                filtered.append(c)

        st.markdown(f'<div class="contest-meta" style="margin-bottom:1rem;">Showing {len(filtered)} contests</div>', unsafe_allow_html=True)

        for contest in filtered[:20]:  # Show up to 20
            cid = str(contest["id"])
            tag = get_division_tag(contest["name"])
            label, css_class = DIV_LABELS[tag]
            already_set = cid in reminders
            cd = countdown(contest["startTimeSeconds"])
            dur = format_duration(contest["durationSeconds"])
            start = format_time(contest["startTimeSeconds"])

            st.markdown(f"""
            <div class="contest-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">
                    <div style="flex:1; min-width:200px;">
                        <div class="contest-name">{contest['name']}</div>
                        <div style="margin: 0.4rem 0;">
                            <span class="tag {css_class}">{label}</span>
                        </div>
                        <div class="contest-meta">🗓 {start} &nbsp;·&nbsp; ⏱ {dur}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="countdown-label">STARTS IN</div>
                        <div class="countdown">{cd}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Reminder Controls
            r_col1, r_col2, r_col3 = st.columns([2, 2, 1])
            with r_col1:
                minutes_before = st.selectbox(
                    "Remind me",
                    [15, 30, 60, 120],
                    format_func=lambda x: f"{x} min before",
                    key=f"sel_{cid}",
                    label_visibility="collapsed",
                )
            with r_col2:
                if not already_set:
                    if st.button("🔔 Set Reminder", key=f"set_{cid}"):
                        remind_at = datetime.fromtimestamp(contest["startTimeSeconds"]) - timedelta(minutes=minutes_before)
                        reminders[cid] = {
                            "name": contest["name"],
                            "start": contest["startTimeSeconds"],
                            "remind_at": remind_at.isoformat(),
                            "minutes_before": minutes_before,
                            "fired": False,
                        }
                        save_reminders(reminders)
                        st.success(f"✅ Reminder set for {minutes_before} min before!")
                        st.rerun()
                else:
                    if st.button("🗑 Remove Reminder", key=f"rm_{cid}"):
                        del reminders[cid]
                        save_reminders(reminders)
                        st.rerun()
            with r_col3:
                if already_set:
                    st.markdown('<span style="color:#4ade80; font-size:1.3rem;" title="Reminder active">✅</span>', unsafe_allow_html=True)

with side_col:
    st.markdown('<div class="section-header">🔔 MY REMINDERS</div>', unsafe_allow_html=True)

    reminders = load_reminders()
    if not reminders:
        st.markdown("""
        <div style="
            background: #0d0d1a;
            border: 1px dashed #1e1e3a;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            color: #4b5563;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        ">
            No reminders set.<br>
            Click 🔔 on a contest<br>to add one.
        </div>
        """, unsafe_allow_html=True)
    else:
        active = {k: v for k, v in reminders.items() if not v.get("fired", False)}
        fired = {k: v for k, v in reminders.items() if v.get("fired", False)}

        if active:
            st.markdown('<div class="contest-meta" style="margin-bottom:0.7rem;">ACTIVE</div>', unsafe_allow_html=True)
            for cid, info in active.items():
                remind_dt = datetime.fromisoformat(info["remind_at"])
                st.markdown(f"""
                <div class="reminder-item">
                    <div class="reminder-icon">🔔</div>
                    <div>
                        <div class="reminder-name">{info['name'][:35]}{'…' if len(info['name'])>35 else ''}</div>
                        <div class="reminder-time">Alert at {remind_dt.strftime('%d %b, %H:%M')}</div>
                        <div class="reminder-time">{info['minutes_before']} min before start</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if fired:
            st.markdown('<div class="contest-meta" style="margin-bottom:0.7rem; margin-top:1rem;">SENT</div>', unsafe_allow_html=True)
            for cid, info in fired.items():
                st.markdown(f"""
                <div class="reminder-item" style="opacity:0.45;">
                    <div class="reminder-icon">✅</div>
                    <div>
                        <div class="reminder-name">{info['name'][:35]}{'…' if len(info['name'])>35 else ''}</div>
                        <div class="reminder-time">Notification sent</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if st.button("🗑 Clear All Reminders"):
            save_reminders({})
            st.rerun()

    # Quick tips
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background: #0d0d1a;
        border: 1px solid #1e1e3a;
        border-radius: 12px;
        padding: 1.2rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #6b7280;
        line-height: 1.8;
    ">
        <div style="color:#a5b4fc; margin-bottom:0.5rem; font-weight:700;">// HOW IT WORKS</div>
        ① Contests auto-fetched from CF API<br>
        ② Pick a contest + reminder lead time<br>
        ③ Click 🔔 to save locally<br>
        ④ Background thread watches time<br>
        ⑤ System alert fires before start
    </div>
    """, unsafe_allow_html=True)
