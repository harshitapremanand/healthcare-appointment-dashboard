"""
Healthcare Appointment & Service Analysis
Hospital Operations Analytics Dashboard  (Streamlit + Plotly)

NOTE: All data in this dashboard is SYNTHETIC (generated in code).
It contains no real patient information.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------------
# 1. Page setup, colours and styling
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Healthcare Appointment & Service Analysis",
    page_icon="🏥",
    layout="wide",
)

BLUE, TEAL, DARK, MUTED = "#1D6FD8", "#14B8A6", "#0F2A47", "#5B6B7F"
DEPARTMENTS = ["General Medicine", "Cardiology", "Pediatrics", "Orthopedics",
               "Dermatology", "Gynecology", "ENT", "Neurology"]
STATUSES = ["Completed", "Scheduled", "Cancelled", "No-Show"]
STATUS_COLORS = {"Completed": TEAL, "Scheduled": BLUE,
                 "Cancelled": "#94A3B8", "No-Show": "#F59E0B"}
STATUS_ICON = {"Completed": "🟢", "Scheduled": "🔵", "Cancelled": "⚪", "No-Show": "🟠"}
PAGES = ["📊 Overview", "📋 Appointment Details", "🔍 Data Quality & Insights"]

st.markdown(
    """
    <style>
    /* ---------- page ---------- */
    .stApp {background: #F7FAFE;}
    [data-testid="stHeader"] {background: transparent;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1280px;}

    /* ---------- sidebar ---------- */
    [data-testid="stSidebar"] {background: linear-gradient(180deg, #FFFFFF 0%, #EAF3FF 100%);
                               border-right: 1px solid #DCE8F5;}
    [data-testid="stSidebar"] label p {color: #0F2A47;}
    .brand {display: flex; align-items: center; gap: .7rem; padding: .3rem 0 .6rem;}
    .brand .logo {width: 44px; height: 44px; border-radius: 12px; font-size: 1.5rem;
                  background: linear-gradient(135deg, #1D6FD8, #14B8A6);
                  display: flex; align-items: center; justify-content: center;}
    .brand-title {color: #0F2A47; font-weight: 700; font-size: 1.05rem; line-height: 1.2;}
    .brand-sub {color: #5B6B7F; font-size: .8rem;}
    .side-label {font-size: .72rem; letter-spacing: .1em; font-weight: 700; color: #5B6B7F;
                 margin: 1.1rem 0 .4rem;}
    [data-testid="stSidebar"] div[role="radiogroup"] label {padding: .5rem .8rem; border-radius: 10px;
                                                            width: 100%; transition: background .15s;}
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {background: #DCEBFF;}
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {background: #D3E6FF;}
    [data-testid="stSidebar"] .stButton button {width: 100%; border-radius: 10px; border: 1px solid #1D6FD8;
                                                color: #1D6FD8; background: #FFFFFF;}
    [data-testid="stSidebar"] .stButton button:hover {background: #1D6FD8; color: #FFFFFF;}
    span[data-baseweb="tag"] {background-color: #1D6FD8 !important;}
    span[data-baseweb="tag"] span {color: #FFFFFF !important;}

    /* ---------- banner ---------- */
    .banner {position: relative; overflow: hidden; display: flex; justify-content: space-between;
             align-items: center; gap: 1rem; flex-wrap: wrap; padding: 1.7rem 2rem; border-radius: 18px;
             margin-bottom: 1.4rem; box-shadow: 0 8px 24px rgba(29,111,216,.25);
             background: linear-gradient(110deg, #1D6FD8 0%, #1596C9 55%, #14B8A6 100%);}
    .banner::before {content: ""; position: absolute; right: -50px; top: -90px; width: 280px; height: 280px;
                     border-radius: 50%; background: rgba(255,255,255,.10);}
    .banner::after {content: ""; position: absolute; right: 140px; bottom: -110px; width: 200px; height: 200px;
                    border-radius: 50%; background: rgba(255,255,255,.08);}
    .banner-left, .banner-right {position: relative; z-index: 1;}
    .banner h1 {color: #FFFFFF !important; margin: 0; padding: 0; font-size: 2rem; font-weight: 700; line-height: 1.2;}
    .banner p {color: #FFFFFF; margin: .35rem 0 0; font-size: 1.05rem; opacity: .95;}
    .chip {display: inline-block; background: rgba(255,255,255,.22); color: #FFFFFF; border-radius: 20px;
           padding: .2rem .85rem; font-size: .78rem; font-weight: 600; margin: .8rem .4rem 0 0;}
    .period {background: rgba(255,255,255,.18); border: 1px solid rgba(255,255,255,.35); border-radius: 14px;
             padding: .7rem 1.1rem; color: #FFFFFF; text-align: right;}
    .period .p-label {font-size: .7rem; letter-spacing: .1em; opacity: .85; font-weight: 600;}
    .period .p-value {font-size: 1.05rem; font-weight: 700;}

    /* ---------- KPI cards ---------- */
    .kpi {display: flex; align-items: center; gap: 1rem; background: #FFFFFF; border: 1px solid #E1ECF8;
          border-radius: 16px; padding: 1.05rem 1.2rem; box-shadow: 0 2px 10px rgba(15,42,71,.06);
          transition: transform .15s, box-shadow .15s; height: 100%;}
    .kpi:hover {transform: translateY(-3px); box-shadow: 0 8px 20px rgba(29,111,216,.15);}
    .kpi-icon {width: 52px; height: 52px; min-width: 52px; border-radius: 14px; font-size: 1.5rem;
               display: flex; align-items: center; justify-content: center; background: #E8F1FD;}
    .kpi.teal .kpi-icon {background: #DDF5F2;}
    .kpi .label {color: #5B6B7F; font-size: .85rem; font-weight: 600;}
    .kpi .value {color: #0F2A47; font-size: 1.9rem; font-weight: 700; line-height: 1.15;}
    .kpi .note {color: #7A8AA0; font-size: .78rem;}

    /* ---------- section titles, chart cards, insights ---------- */
    .section-title {font-size: 1.15rem; font-weight: 700; color: #0F2A47; margin: 1.5rem 0 .8rem;
                    padding-left: .7rem; border-left: 5px solid #14B8A6;}
    [class*="st-key-card"] {background: #FFFFFF; border: 1px solid #E1ECF8; border-radius: 16px;
                            padding: .6rem .8rem; box-shadow: 0 2px 10px rgba(15,42,71,.06);}
    .insight {background: #FFFFFF; border: 1px solid #E1ECF8; border-top: 4px solid #1D6FD8;
              border-radius: 14px; padding: 1rem 1.2rem; box-shadow: 0 2px 10px rgba(15,42,71,.06);}
    .insight.teal {border-top-color: #14B8A6;}
    .insight.amber {border-top-color: #F59E0B;}
    .insight .i-title {color: #5B6B7F; font-size: .85rem; font-weight: 600;}
    .insight .i-name {color: #0F2A47; font-size: 1.45rem; font-weight: 700; margin: .25rem 0;}
    .insight .i-detail {color: #5B6B7F; font-size: .9rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# 2. Synthetic sample data (clearly labelled, generated with a fixed seed)
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    rng = np.random.default_rng(42)
    n = 600
    today = pd.Timestamp("2026-10-30")

    days = pd.bdate_range("2026-09-01", "2026-11-13").to_numpy()  # weekdays only
    df = pd.DataFrame({
        "appointment_id": [f"APT-{1001 + i}" for i in range(n)],
        "date": pd.to_datetime(rng.choice(days, n)),
        "department": rng.choice(
            DEPARTMENTS, n, p=[0.22, 0.14, 0.12, 0.12, 0.10, 0.10, 0.10, 0.10]),
    })

    # Past appointments get a final status; future ones are "Scheduled"
    outcome = rng.choice(["Completed", "Cancelled", "No-Show"], n, p=[0.72, 0.13, 0.15])
    df["status"] = np.where(df["date"] <= today, outcome, "Scheduled")

    # Waiting time (minutes) is recorded only for completed visits
    avg_wait = {"General Medicine": 32, "Cardiology": 41, "Pediatrics": 24,
                "Orthopedics": 37, "Dermatology": 22, "Gynecology": 28,
                "ENT": 26, "Neurology": 45}
    wait = rng.normal(df["department"].map(avg_wait), 8).clip(5).round()
    df["waiting_time"] = np.where(df["status"] == "Completed", wait, np.nan)

    # Deliberately add a few bad records so the data-quality section has something to show
    picks = rng.choice(df.index[df["status"] == "Completed"], 18, replace=False)
    df.loc[picks[:10], "waiting_time"] = rng.integers(-30, -1, 10)             # negative wait
    df.loc[picks[10:], "department"] = rng.choice(["Cardio", "Unknown", "Ortho"], 8)  # not in master list

    return df.sort_values("date").reset_index(drop=True)


raw = load_data()

# Data-quality rules
invalid = (raw["waiting_time"] < 0) | (raw["waiting_time"] > 240)   # impossible waiting time
unmatched = ~raw["department"].isin(DEPARTMENTS)                    # department not in master list
df = raw[~invalid & ~unmatched]                                     # clean data used by the dashboard


# ------------------------------------------------------------------
# 3. Sidebar: navigation + filters
# ------------------------------------------------------------------
min_d, max_d = df["date"].min().date(), df["date"].max().date()

# Starting values for the filters (also used by the Reset button)
st.session_state.setdefault("f_dates", (min_d, max_d))
st.session_state.setdefault("f_depts", DEPARTMENTS)
st.session_state.setdefault("f_status", STATUSES)


def reset_filters():
    st.session_state["f_dates"] = (min_d, max_d)
    st.session_state["f_depts"] = DEPARTMENTS
    st.session_state["f_status"] = STATUSES


st.sidebar.markdown(
    '<div class="brand"><div class="logo">🏥</div><div><div class="brand-title">Hospital Analytics</div>'
    '<div class="brand-sub">Operations Dashboard</div></div></div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown('<div class="side-label">NAVIGATION</div>', unsafe_allow_html=True)
page = st.sidebar.radio("Navigation", PAGES, label_visibility="collapsed")

st.sidebar.markdown('<div class="side-label">FILTERS</div>', unsafe_allow_html=True)
date_range = st.sidebar.date_input("Date range", min_value=min_d, max_value=max_d, key="f_dates")
depts = st.sidebar.multiselect("Department", DEPARTMENTS, key="f_depts")
statuses = st.sidebar.multiselect("Appointment status", STATUSES, key="f_status")
st.sidebar.button("↺ Reset filters", on_click=reset_filters)
st.sidebar.caption("Data shown is synthetic sample data.")


# ------------------------------------------------------------------
# 4. Header banner
# ------------------------------------------------------------------
if len(date_range) == 2:
    period = f"{date_range[0]:%d %b %Y} – {date_range[1]:%d %b %Y}"
else:
    period = "Select an end date"

st.markdown(
    '<div class="banner"><div class="banner-left">'
    '<h1>Healthcare Appointment &amp; Service Analysis</h1>'
    '<p>Hospital Operations Analytics Dashboard</p>'
    '<span class="chip">🧪 Synthetic sample data</span>'
    '<span class="chip">🏥 8 departments</span>'
    '</div><div class="banner-right"><div class="period">'
    '<div class="p-label">DATA PERIOD</div>'
    f'<div class="p-value">{period}</div></div></div></div>',
    unsafe_allow_html=True,
)

# Apply filters
if len(date_range) != 2:
    st.info("Please select both a start date and an end date in the sidebar.")
    st.stop()

start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
f = df[df["date"].between(start, end) & df["department"].isin(depts) & df["status"].isin(statuses)]

if f.empty:
    st.warning("No appointments match the selected filters. Use **Reset filters** in the sidebar.")
    st.stop()


# ------------------------------------------------------------------
# 5. KPI cards (always visible)
# ------------------------------------------------------------------
def kpi(col, icon, label, value, note, style=""):
    col.markdown(
        f'<div class="kpi {style}"><div class="kpi-icon">{icon}</div><div>'
        f'<div class="label">{label}</div><div class="value">{value}</div>'
        f'<div class="note">{note}</div></div></div>',
        unsafe_allow_html=True,
    )


avg_wait = f["waiting_time"].mean()
n_completed = int((f["status"] == "Completed").sum())
n_noshow = int((f["status"] == "No-Show").sum())
no_show_rate = n_noshow / len(f) * 100
completion_rate = n_completed / len(f) * 100

c1, c2, c3, c4 = st.columns(4)
kpi(c1, "📅", "Total Appointments", f"{len(f):,}", f"Across {f['department'].nunique()} departments")
kpi(c2, "⏱️", "Avg Waiting Time (min)", f"{avg_wait:.1f}" if pd.notna(avg_wait) else "N/A",
    "Completed visits only", "teal")
kpi(c3, "🚫", "No-Show Rate (%)", f"{no_show_rate:.1f}%", f"{n_noshow} missed appointments")
kpi(c4, "✅", "Completion Rate (%)", f"{completion_rate:.1f}%", f"{n_completed} completed visits", "teal")


def tidy(fig, height=370):
    """Apply one clean, readable style to every chart."""
    fig.update_layout(
        template="plotly_white", paper_bgcolor="white", plot_bgcolor="white", height=height,
        font=dict(color=DARK, size=13),
        title=dict(font=dict(size=17, color=DARK), x=0.02, xanchor="left"),
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(font=dict(color=DARK)),
        hoverlabel=dict(bgcolor="white", font_color=DARK),
    )
    axis = dict(gridcolor="#EEF2F7", linecolor="#DCE8F5", tickfont=dict(color=MUTED),
                title_font=dict(color=MUTED))
    fig.update_xaxes(**axis)
    fig.update_yaxes(**axis)
    return fig


def show(fig):
    """Draw a chart without Streamlit's own theme colours and without the toolbar."""
    st.plotly_chart(fig, theme=None, config={"displayModeBar": False})


# ------------------------------------------------------------------
# 6. Pages
# ------------------------------------------------------------------
if page == PAGES[0]:
    st.markdown('<div class="section-title">Appointment Overview</div>', unsafe_allow_html=True)
    left, right = st.columns(2)

    # Chart 1: appointment status distribution
    with left, st.container(key="card_status"):
        status_df = f.groupby("status").size().reset_index(name="count")
        fig = px.pie(status_df, names="status", values="count", hole=0.62, color="status",
                     color_discrete_map=STATUS_COLORS, category_orders={"status": STATUSES},
                     title="Appointment Status Distribution")
        fig.update_traces(textinfo="percent", textfont=dict(color="white", size=13), sort=False,
                          marker=dict(line=dict(color="white", width=3)))
        tidy(fig)
        fig.update_layout(
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.02, font=dict(color=DARK)),
            annotations=[dict(text=f"<b>{len(f):,}</b><br>appointments", x=0.5, y=0.5,
                              showarrow=False, font=dict(size=16, color=DARK))])
        show(fig)

    # Chart 2: department-wise appointments
    with right, st.container(key="card_dept"):
        dept_df = (f.groupby("department").size().reset_index(name="appointments")
                   .sort_values("appointments", ascending=False))
        fig = px.bar(dept_df, x="department", y="appointments", text="appointments",
                     color="appointments", color_continuous_scale=["#BFD9F7", BLUE],
                     title="Department-wise Appointments")
        fig.update_traces(textposition="outside", cliponaxis=False, textfont=dict(color=DARK))
        fig.update_layout(xaxis_title=None, yaxis_title="Appointments", coloraxis_showscale=False)
        fig.update_yaxes(range=[0, dept_df["appointments"].max() * 1.18])
        show(tidy(fig))

    left, right = st.columns(2)

    # Chart 3: average waiting time by department
    with left, st.container(key="card_wait"):
        wait_df = (f.dropna(subset=["waiting_time"]).groupby("department")["waiting_time"]
                   .mean().round(1).reset_index().sort_values("waiting_time", ascending=False))
        if wait_df.empty:
            st.info("No waiting-time data for the selected filters "
                    "(waiting time is recorded for completed visits).")
        else:
            fig = px.bar(wait_df, x="department", y="waiting_time", text="waiting_time",
                         color="waiting_time", color_continuous_scale=["#B7ECE6", TEAL],
                         title="Average Waiting Time by Department")
            fig.update_traces(textposition="outside", cliponaxis=False, textfont=dict(color=DARK))
            fig.add_hline(y=avg_wait, line_dash="dot", line_color=BLUE,
                          annotation_text=f"Overall avg {avg_wait:.1f} min",
                          annotation_position="top right", annotation_font_color=MUTED)
            fig.update_layout(xaxis_title=None, yaxis_title="Minutes", coloraxis_showscale=False)
            fig.update_yaxes(range=[0, wait_df["waiting_time"].max() * 1.25])
            show(tidy(fig))

    # Chart 4: daily appointment trend
    with right, st.container(key="card_trend"):
        daily_df = f.groupby("date").size().reset_index(name="appointments")
        fig = px.line(daily_df, x="date", y="appointments", markers=True,
                      color_discrete_sequence=[BLUE], title="Daily Appointment Trends")
        fig.update_traces(fill="tozeroy", fillcolor="rgba(29,111,216,0.10)",
                          line=dict(width=3), marker=dict(size=7))
        fig.update_layout(xaxis_title=None, yaxis_title="Appointments")
        show(tidy(fig))

elif page == PAGES[1]:
    st.markdown('<div class="section-title">Appointment Details</div>', unsafe_allow_html=True)
    export = f[["appointment_id", "date", "department", "status", "waiting_time"]].copy()
    export["date"] = export["date"].dt.strftime("%Y-%m-%d")
    export.columns = ["Appointment ID", "Date", "Department", "Status", "Waiting Time (min)"]

    top_l, top_r = st.columns([4, 1])
    top_l.caption(f"Showing **{len(export)}** appointments. "
                  "Waiting time is recorded only for completed visits.")
    top_r.download_button("⬇ Download CSV", export.to_csv(index=False),
                          file_name="appointments.csv", mime="text/csv")

    table = export.copy()
    table["Status"] = table["Status"].map(lambda s: f"{STATUS_ICON[s]} {s}")
    st.dataframe(
        table, hide_index=True, height=470,
        column_config={"Waiting Time (min)": st.column_config.ProgressColumn(
            "Waiting Time (min)", min_value=0, max_value=90, format="%d min")},
    )

else:  # Data Quality & Insights
    st.markdown('<div class="section-title">Data Quality</div>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    kpi(q1, "🗂️", "Total Records", f"{len(raw):,}", "Raw synthetic records")
    kpi(q2, "✔️", "Valid Records", f"{len(df):,}", "Used in this dashboard", "teal")
    kpi(q3, "⚠️", "Invalid Records", f"{invalid.sum():,}", "Impossible waiting time")
    kpi(q4, "🔗", "Unmatched Departments", f"{unmatched.sum():,}", "Not in department list", "teal")
    st.write("")

    valid_share = len(df) / len(raw)
    st.progress(valid_share, text=f"{valid_share * 100:.1f}% of records passed all quality checks")
    checks = pd.DataFrame({
        "Check": ["Waiting time between 0 and 240 minutes", "Department exists in department list"],
        "Records failed": [int(invalid.sum()), int(unmatched.sum())],
        "Examples": ["Negative waiting times", ", ".join(sorted(raw.loc[unmatched, "department"].unique()))],
        "Action": ["Excluded from analysis", "Excluded from analysis"],
    })
    st.dataframe(checks, hide_index=True)
    st.caption("Quality counts cover the full dataset and do not change with the sidebar filters.")

    st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)
    by_dept = f.groupby("department").agg(
        appointments=("appointment_id", "count"),
        avg_wait=("waiting_time", "mean"),
        no_show=("status", lambda s: (s == "No-Show").mean() * 100),
    )
    busiest = by_dept["appointments"].idxmax()
    highest_noshow = by_dept["no_show"].idxmax()


    def insight(col, icon, title, name, detail, style=""):
        col.markdown(f'<div class="insight {style}"><div class="i-title">{icon} {title}</div>'
                     f'<div class="i-name">{name}</div><div class="i-detail">{detail}</div></div>',
                     unsafe_allow_html=True)


    i1, i2, i3 = st.columns(3)
    insight(i1, "📈", "Busiest department", busiest,
            f"{by_dept.loc[busiest, 'appointments']} appointments in the selected period")
    if by_dept["avg_wait"].notna().any():
        longest = by_dept["avg_wait"].idxmax()
        insight(i2, "⏱️", "Longest waiting time", longest,
                f"Averages {by_dept.loc[longest, 'avg_wait']:.1f} minutes per visit", "teal")
    else:
        insight(i2, "⏱️", "Longest waiting time", "N/A", "No waiting-time data for these filters", "teal")
    insight(i3, "🚫", "Highest no-show rate", highest_noshow,
            f"{by_dept.loc[highest_noshow, 'no_show']:.1f}% of appointments were missed", "amber")

st.divider()
st.caption("Healthcare Appointment & Service Analysis • College internship project • Synthetic data only")
