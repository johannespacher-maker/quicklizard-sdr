import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="Quicklizard SDR Dashboard", page_icon="🦎", layout="wide")
st.title("🦎 Quicklizard SDR Performance & Coaching Dashboard")

# --- QUICKLIZARD BRANDING ---
ql_green = "#27ae60"

# --- GOOGLE SHEETS DATA ENGINE ---
@st.cache_data(ttl=600) # This tells the app to fetch fresh data every 10 minutes
def load_data():
    # Replace the text inside the quotes with your copied link!
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pubhtml?gid=0&single=true"
    return pd.read_csv(sheet_url)

df = load_data()

# --- EXACT SOURCED HEATMAP DATA ---
@st.cache_data
def load_heatmap_data():
    heatmap_raw = []
    
    # Compact format to save space: (SDR, Timeframe, Day, [List of Hours], calls, connect_rate)
    hm_input = [
        # Aiko
        ("Aiko", "This Quarter", "Mon", list(range(1,8)), 15, 2), ("Aiko", "This Quarter", "Tue", list(range(1,9)), 15, 5), ("Aiko", "This Quarter", "Wed", list(range(1,10)), 15, 2), ("Aiko", "This Quarter", "Thu", list(range(1,8)), 15, 3), ("Aiko", "This Quarter", "Fri", list(range(3,9)), 20, 2),
        ("Aiko", "Last Week", "Mon", [5,6], 15, 2), ("Aiko", "Last Week", "Tue", list(range(4,9)), 10, 2), ("Aiko", "Last Week", "Wed", [5,6,7], 15, 2), ("Aiko", "Last Week", "Thu", [4,5,6], 10, 2), ("Aiko", "Last Week", "Fri", [5], 25, 2),
        
        # Ben
        ("Ben", "This Quarter", "Mon", list(range(6,18)), 25, 8), ("Ben", "This Quarter", "Tue", list(range(5,16)), 25, 6), ("Ben", "This Quarter", "Wed", list(range(5,18)), 25, 7), ("Ben", "This Quarter", "Thu", list(range(8,16)), 25, 6), ("Ben", "This Quarter", "Fri", list(range(6,16)), 20, 5),
        ("Ben", "Last Week", "Mon", [8], 20, 4), ("Ben", "Last Week", "Tue", [12, 15], 25, 6), ("Ben", "Last Week", "Wed", [7, 14], 20, 3), ("Ben", "Last Week", "Fri", [10, 11], 25, 4),
        
        # Feddy
        ("Feddy", "This Quarter", "Mon", list(range(14,22)), 20, 3), ("Feddy", "This Quarter", "Tue", list(range(14,22)), 25, 2), ("Feddy", "This Quarter", "Wed", list(range(14,23)), 20, 4), ("Feddy", "This Quarter", "Thu", list(range(14,24)), 20, 3),
        ("Feddy", "Last Week", "Mon", [19], 25, 3), ("Feddy", "Last Week", "Tue", [21], 20, 3), ("Feddy", "Last Week", "Wed", [20], 25, 3), ("Feddy", "Last Week", "Thu", [23], 20, 3),
        
        # Heike
        ("Heike", "This Quarter", "Mon", list(range(7,18)), 20, 5), ("Heike", "This Quarter", "Tue", list(range(8,17)), 25, 6), ("Heike", "This Quarter", "Wed", list(range(8,17)), 25, 6), ("Heike", "This Quarter", "Thu", list(range(7,17)), 20, 5), ("Heike", "This Quarter", "Fri", list(range(7,16)), 25, 6),
        ("Heike", "Last Week", "Mon", [8,9,10,12,14], 15, 4), ("Heike", "Last Week", "Tue", [9,15,16], 25, 6), ("Heike", "Last Week", "Wed", [9,10,11,12], 20, 4), ("Heike", "Last Week", "Thu", [8,10,11,12], 15, 5), ("Heike", "Last Week", "Fri", [8,12,13], 30, 3),
        
        # Ilana
        ("Ilana", "This Quarter", "Mon", list(range(8,13)), 25, 12), ("Ilana", "This Quarter", "Tue", list(range(9,16)), 25, 10), ("Ilana", "This Quarter", "Wed", list(range(9,17)), 25, 11), ("Ilana", "This Quarter", "Thu", list(range(9,16)), 20, 9), ("Ilana", "This Quarter", "Fri", [11], 15, 4),
        ("Ilana", "Last Week", "Wed", [11, 12], 25, 4),
        
        # Jessica
        ("Jessica", "This Quarter", "Mon", list(range(10,18)), 25, 7), ("Jessica", "This Quarter", "Tue", list(range(9,17)), 30, 6), ("Jessica", "This Quarter", "Wed", list(range(9,18)), 25, 7), ("Jessica", "This Quarter", "Thu", list(range(10,16)), 25, 6), ("Jessica", "This Quarter", "Fri", [11, 13, 14, 16], 20, 6),
        ("Jessica", "Last Week", "Mon", [10,11,12,13,14], 25, 7), ("Jessica", "Last Week", "Tue", [10,11,13], 30, 4), ("Jessica", "Last Week", "Wed", [10], 25, 8), ("Jessica", "Last Week", "Thu", [13, 14], 30, 9), ("Jessica", "Last Week", "Fri", [11, 13, 14], 20, 4),
        
        # Laura (Strictly matching requested QTR & Week mapping)
        ("Laura", "This Quarter", "Mon", [10, 11, 17], 20, 2), ("Laura", "This Quarter", "Wed", [7], 20, 2), ("Laura", "This Quarter", "Thu", [7, 8, 9], 20, 3), ("Laura", "This Quarter", "Fri", list(range(10,18)), 25, 4),
        ("Laura", "Last Week", "Tue", [16, 18, 20, 21, 23], 15, 2), ("Laura", "Last Week", "Wed", [11, 16, 18, 20, 21, 23], 10, 2), ("Laura", "Last Week", "Thu", [0, 14, 15, 16, 17, 21, 22, 23], 20, 3), 
        
        # Lea
        ("Lea", "This Quarter", "Mon", list(range(10,18)), 25, 8), ("Lea", "This Quarter", "Tue", list(range(9,18)), 25, 7), ("Lea", "This Quarter", "Wed", list(range(9,18)), 20, 7), ("Lea", "This Quarter", "Thu", list(range(10,19)), 20, 6), ("Lea", "This Quarter", "Fri", list(range(11,17)), 15, 5),
        ("Lea", "Last Week", "Mon", [10, 11, 12, 13, 14, 16, 17], 20, 4), ("Lea", "Last Week", "Tue", [11], 15, 3), ("Lea", "Last Week", "Wed", [12, 13, 17], 15, 5), ("Lea", "Last Week", "Thu", [11, 12, 15, 16], 30, 6), ("Lea", "Last Week", "Fri", [11], 20, 4),
        
        # Max (Identical QTR & Week)
        ("Max", "This Quarter", "Tue", [19], 25, 3), ("Max", "This Quarter", "Wed", [14, 17, 18, 21], 15, 3), ("Max", "This Quarter", "Thu", [19], 30, 3), ("Max", "This Quarter", "Fri", [18], 25, 3),
        ("Max", "Last Week", "Tue", [19], 25, 3), ("Max", "Last Week", "Wed", [14, 17, 18, 21], 15, 3), ("Max", "Last Week", "Thu", [19], 30, 3), ("Max", "Last Week", "Fri", [18], 25, 3),
        
        # Rozanne
        ("Rozanne", "This Quarter", "Tue", [16, 17, 18, 22, 23], 25, 5), ("Rozanne", "This Quarter", "Wed", [11, 16, 17, 18, 19, 20, 23], 20, 6), ("Rozanne", "This Quarter", "Thu", [0, 14, 15, 16, 17, 21, 22, 23], 15, 7),
        ("Rozanne", "Last Week", "Thu", [14, 21, 23], 20, 4)
    ]
    
    for sdr, tf, day, hours, calls, conn in hm_input:
        for h in hours:
            heatmap_raw.append((sdr, tf, day, h, calls, conn))
            
    return pd.DataFrame(heatmap_raw, columns=["SDR", "Timeframe", "Day", "Hour", "Calls", "Connect %"])

df = load_data()
df_heat = load_heatmap_data()

# --- TIMEZONE SHIFT ENGINE ---
def shift_timezone(row, offset):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_idx = days.index(row["Day"])
    hour = row["Hour"]
    
    new_hour = hour + offset
    if new_hour < 0:
        new_hour += 24
        day_idx = (day_idx - 1) % 7
    elif new_hour >= 24:
        new_hour -= 24
        day_idx = (day_idx + 1) % 7
        
    return pd.Series([days[day_idx], new_hour])

# --- GOOGLE SHEETS COACHING & ANALYTICS ENGINE ---
@st.cache_data(ttl=600)
def load_coaching_data():
    # Replace the text inside the quotes with your NEW Coaching tab CSV link!
    sheet_url_coaching = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=1177538336&single=true&output=csv"
    df_coach = pd.read_csv(sheet_url_coaching)
    
    analytics_dict = {}
    plans_dict = {}
    
    # This stitches your spreadsheet columns into nicely formatted dashboard text!
    for index, row in df_coach.iterrows():
        sdr_name = row['SDR']
        analytics_text = f"**The Situation:** {row['Situation']}\n\n**Strengths:** {row['Strengths']}\n\n**Action Item:** {row['Action Item']}"
        
        analytics_dict[sdr_name] = analytics_text
        plans_dict[sdr_name] = str(row['Coaching Plan'])
        
    return analytics_dict, plans_dict

# Load the data and create the dictionaries the dashboard expects
sdr_analytics, coaching_plans = load_coaching_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🦎 Quicklizard Menu")
view = st.sidebar.radio("Go to:", ["🏆 Team Overview & Rankings", "🔍 Individual Deep Dive", "🗣️ 1:1 Coaching Advice", "🚀 Special Projects"])

def get_quarter(month_str):
    if month_str in ["Jan", "Feb", "Mar"]: return "Q1"
    if month_str in ["Apr", "May", "Jun"]: return "Q2"
    if month_str in ["Jul", "Aug", "Sep"]: return "Q3"
    return "Q4"

# --- VIEW 1: TEAM OVERVIEW ---
if view == "🏆 Team Overview & Rankings":
    st.header("Team Leaderboard")
    time_filter = st.selectbox("Filter Timeframe:", ["This Quarter", "This Month", "This Week", "Last 12 Weeks", "All Time"], index=0)
    
    all_weeks = df['Week'].unique().tolist()
    latest_week = all_weeks[-1]
    latest_month = latest_week.split(" - ")[0]
    
    if time_filter == "All Time": filtered_df = df
    elif time_filter == "Last 12 Weeks": filtered_df = df[df['Week'].isin(all_weeks[-12:])]
    elif time_filter == "This Month": filtered_df = df[df['Week'].str.startswith(latest_month)]
    elif time_filter == "This Week": filtered_df = df[df['Week'] == latest_week]
    else: filtered_df = df[df['Week'].apply(lambda w: get_quarter(w.split(" - ")[0]) == get_quarter(latest_month))]

    team_stats = filtered_df.groupby("SDR").agg({"Meetings Booked": "sum", "Total Activities": "sum", "Calls Logged": "sum", "Emails Sent": "sum"}).reset_index().sort_values(by="Meetings Booked", ascending=False)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f"Total Meetings ({time_filter})", team_stats["Meetings Booked"].sum())
    col2.metric("Total Activities", team_stats["Total Activities"].sum())
    col3.metric("Total Calls", team_stats["Calls Logged"].sum())
    col4.metric("Total Emails", team_stats["Emails Sent"].sum())
    st.markdown("---")
    
    styled_df = team_stats.style.background_gradient(subset=["Meetings Booked"], cmap="Greens").background_gradient(subset=["Total Activities"], cmap="Blues").background_gradient(subset=["Calls Logged"], cmap="Oranges").background_gradient(subset=["Emails Sent"], cmap="Purples")
    st.dataframe(styled_df, hide_index=True, use_container_width=True)

# --- VIEW 2: INDIVIDUAL DEEP DIVE ---
elif view == "🔍 Individual Deep Dive":
    st.header("SDR Data Deep Dive")
    selected_sdr = st.selectbox("Select SDR:", df["SDR"].unique())
    sdr_data = df[df["SDR"] == selected_sdr]
    
    st.markdown("### 👤 SDR Analytics & Action Plan")
    st.info(sdr_analytics.get(selected_sdr, "No detailed analytics available."))
    st.markdown("---")
    
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1: st.plotly_chart(px.line(sdr_data, x="Week", y="Total Activities", title="Total Activities 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)
    with row1_col2: st.plotly_chart(px.bar(sdr_data, x="Week", y="Meetings Booked", title="Outbound Meetings 🦎", color_discrete_sequence=[ql_green]), use_container_width=True)
        
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1: st.plotly_chart(px.line(sdr_data, x="Week", y="Calls Logged", title="Calls Logged 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)
    with row2_col2: st.plotly_chart(px.line(sdr_data, x="Week", y="Connect %", title="Connected Calls % 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)

    # --- HEATMAP VISUALIZATION ---
    st.markdown("---")
    st.subheader("⏱️ Optimal Calling Windows (Mon - Fri)")
    
    sdr_heatmap_data = df_heat[df_heat["SDR"] == selected_sdr].copy()
    
    if not sdr_heatmap_data.empty:
        tz_col, _ = st.columns([1, 2])
        with tz_col:
            timezones = {"Israel Time (IST) - Default": 0, "Central Europe (CET)": -1, "UK Time (GMT)": -2, "US Eastern Time (EST)": -7, "US Pacific Time (PST)": -10, "Singapore Time (SGT)": 6, "Australian Eastern (AEST)": 8}
            selected_tz = st.selectbox("Select Timezone:", list(timezones.keys()))
            tz_offset = timezones[selected_tz]

        if tz_offset != 0:
            sdr_heatmap_data[["Day", "Hour"]] = sdr_heatmap_data.apply(lambda r: shift_timezone(r, tz_offset), axis=1)

        # FORCE MON-FRI Y-AXIS AND 24HR X-AXIS
        all_days = ["Fri", "Thu", "Wed", "Tue", "Mon"] 
        sdr_heatmap_data = sdr_heatmap_data[sdr_heatmap_data["Day"].isin(all_days)] # Strip out weekends entirely
        
        dummy_data = []
        for d in all_days:
            dummy_data.append({"SDR": selected_sdr, "Timeframe": "This Quarter", "Day": d, "Hour": -10, "Calls": 0, "Connect %": 0})
            dummy_data.append({"SDR": selected_sdr, "Timeframe": "Last Week", "Day": d, "Hour": -10, "Calls": 0, "Connect %": 0})
        sdr_heatmap_data = pd.concat([sdr_heatmap_data, pd.DataFrame(dummy_data)], ignore_index=True)

        heat_col1, heat_col2 = st.columns(2)
        ql_greens = ["#a1d9b3", "#27ae60", "#0b4a24"] 
        
        q_data = sdr_heatmap_data[sdr_heatmap_data["Timeframe"] == "This Quarter"]
        if not q_data.empty:
            fig_q = px.scatter(q_data, x="Hour", y="Day", size="Calls", color="Connect %", color_continuous_scale=ql_greens, title=f"This Quarter ({selected_tz.split(' ')[0]})", category_orders={"Day": all_days})
            fig_q.update_xaxes(range=[-0.5, 23.5], tickvals=list(range(24)), ticktext=[f"{h%12 if h%12!=0 else 12} {'AM' if h<12 else 'PM'}" for h in range(24)])
            heat_col1.plotly_chart(fig_q, use_container_width=True)
            
        w_data = sdr_heatmap_data[sdr_heatmap_data["Timeframe"] == "Last Week"]
        if not w_data.empty:
            fig_w = px.scatter(w_data, x="Hour", y="Day", size="Calls", color="Connect %", color_continuous_scale=ql_greens, title=f"Last Week ({selected_tz.split(' ')[0]})", category_orders={"Day": all_days})
            fig_w.update_xaxes(range=[-0.5, 23.5], tickvals=list(range(24)), ticktext=[f"{h%12 if h%12!=0 else 12} {'AM' if h<12 else 'PM'}" for h in range(24)])
            heat_col2.plotly_chart(fig_w, use_container_width=True)

# --- VIEW 3: 1:1 COACHING ADVICE ---
elif view == "🗣️ 1:1 Coaching Advice":
    st.header("1:1 Coaching Agendas")
    st.write("Review the individual Deep Dive tabs to go over exact timing strategies with each rep.")

# --- VIEW 4: SPECIAL PROJECTS ---
elif view == "🚀 Special Projects":
    st.header("Strategic Initiatives & Focus Areas")
    project = st.selectbox("Select Project:", ["Issues to fix", "The iPhone Screener Bypass Playbook", "Preparing Max (New US SDR)", "The 'Ben Effect' (Leadership)", "The US 'Bad Lists' Excuse"])
    
    if project == "Issues to fix":
        st.markdown("""
        ### 1. The "Activity Illusion" (Laura vs. Ben)
        High activity does not equal high output on this team. 
        * **The Why:** Laura is hiding behind email in the US market, and her reply rate is a flat 0.0% for almost the entire 5 months. Ben is heavily leveraging the phones. 
        * **The Fix:** This proves that in your current markets, blind email volume without phone execution is completely dead. We need to reset Laura's workflow to prioritize calls.
        
        ### 2. The Conversion vs. Volume Tragedy (Ilana vs. Feddy)
        A massive mismatch between who has the talent and who is doing the work.
        * **Ilana:** Has absolutely elite conversion skills. But her call volume is almost non-existent.
        * **Feddy:** Grinding in the brutal US market with terrible connect rates (1% to 3%). But because he uses Nooks to push volume, he booked 7 meetings.
        * **The Fix:** Get Ilana to adopt Feddy's work ethic.
        """)
    elif project == "The iPhone Screener Bypass Playbook":
        st.markdown("### 📱 Bypassing the iOS 17 Call Screeners\n\n**1. The 'Live Voicemail' Hack**\nDrop a hyper-relevant hook immediately when the voicemail beep sounds so the transcript shows their name.\n\n**2. The Siri Signature Trick**\nEnsure their Nooks number is in their email signature. Siri scans Apple Mail and overrides unknown caller blocks.\n\n**3. The 'Double Dial'**\nCall once, let it ring, hang up, immediately call back to break 'Do Not Disturb' blocks on Tier 1 accounts.\n\n**4. The Pre-Call Bump**\nSend a LinkedIn voice note 10 minutes before dialing.")
    elif project == "Preparing Max (New US SDR)":
        st.markdown("### Onboarding Max\n* **Nooks on Day 1:** Get him comfortable with 100+ dials immediately to prevent call reluctance.\n* **Expectation Setting:** 50 dials for 2 conversations is normal.\n* **Consistency:** Establish a rigid schedule to prevent erratic channel hopping.")
    elif project == "The 'Ben Effect' (Leadership)":
        st.markdown("### Tracking Ben's Leadership Impact\n* **The Data:** Aiko's calls jumped from ~80/week to 150-180+/week. Feddy's calls spiked to 245+ in Feb.\n* **Action:** Explicitly praise Ben's leadership in his 1:1.")
    elif project == "The US 'Bad Lists' Excuse":
        st.markdown("### Debunking the Account List Excuse\n* **The Solution:** Letting them build their own lists was the right move. Now, we track if engagement improves on accounts *they* hand-picked.")