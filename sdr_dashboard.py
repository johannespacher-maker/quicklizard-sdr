import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="Quicklizard SDR Dashboard", page_icon="🦎", layout="wide")
st.title("🦎 Quicklizard SDR Performance & Coaching Dashboard")

# --- QUICKLIZARD BRANDING ---
ql_green = "#27ae60"

# --- REAL HISTORICAL DATA (Oct - Mar) ---
@st.cache_data
def load_data():
    weeks_list = ["Oct - W1", "Oct - W2", "Oct - W3", "Oct - W4", "Oct - W5", "Nov - W1", "Nov - W2", "Nov - W3", "Nov - W4", "Dec - W1", "Dec - W2", "Dec - W3", "Dec - W4", "Dec - W5", "Jan - W1", "Jan - W2", "Jan - W3", "Jan - W4", "Feb - W1", "Feb - W2", "Feb - W3", "Feb - W4", "Mar - W1"]

    raw_data = {
        "Ben": [[0,0,0,0,0,0], [0,0,0,0,0,0], [855,245,6.5,193,0.7,0], [847,315,7.3,234,1,1], [1229,405,7,475,0.5,2], [962,395,5.1,264,0.9,5], [963,519,1.9,325,0,1], [735,281,2.1,220,0.5,3], [873,307,4.9,314,1.2,5], [530,150,2,183,1.3,1], [506,363,7.2,68,0,1], [326,140,2.1,168,0,1], [0,0,0,0,0,0], [0,0,0,0,0,0], [842,103,7.8,342,0,3], [761,224,4.9,346,2,3], [727,654,12.1,73,3.1,3], [544,460,2,83,0,5], [572,503,5,68,0,2], [426,367,3.3,59,0,4], [417,417,4.8,0,0,3], [438,369,3.8,10,0,1], [290,277,4.3,12,0.0,0]],
        "Feddy": [[0,0,0,0,0,0]] * 8 + [[75,31,6.5,19,0,0], [269,99,3,114,0,0], [226,81,2.5,64,0,0], [473,161,3.1,169,0.7,0], [271,178,6.2,69,0,0], [351,1,0,155,1.4,0], [473,395,2.8,78,4.6,0], [257,51,2,206,2.2,1], [321,120,1.7,95,3.5,4], [558,377,2.9,77,0,1], [582,140,3.6,317,1.5,0], [647,245,9,330,0.3,1], [384,260,2.3,74,0,0], [38,0,0,38,3.2,0], [306,152,1.3,70,1.9,0]],
        "Heike": [[0,0,0,0,0,0]] * 9 + [[128,85,21.1,24,9.5,0], [201,156,14.7,40,5.9,1], [188,146,11,180,3.5,0], [103,13,15.4,87,0,0], [48,40,5,8,12.5,0], [375,215,6,93,3.9,1], [197,137,5.8,37,2.7,0], [385,254,7.1,92,1.4,1], [309,223,6.3,77,3.2,0], [252,199,9.5,53,10.4,1], [248,203,3.4,40,11.8,0], [207,148,6.1,55,6.5,1], [157,120,5,37,0,1], [271,214,2.3,52,4.3,0]],
        "Ilana": [[0,0,0,0,0,0]] * 8 + [[39,20,20,11,0,0], [94,32,28.1,29,11.1,0], [103,39,23.1,29,4,0], [145,25,16,90,4.8,1], [0,0,0,0,0,0], [13,0,0,0,0,0], [118,46,17.4,38,3.2,0], [120,30,33.3,68,8.1,0], [116,41,19.5,41,17.5,2], [73,22,9.1,27,8,0], [153,44,25,66,3.3,1], [118,32,12.5,55,3.8,0], [7,0,0,2,0,0], [95,35,5.7,33,11.1,0], [49,12,0.0,17,0.0,0]],
        "Jessica": [[0,0,0,0,0,0]] * 3 + [[808,174,16.1,387,2.3,2], [698,163,13.5,310,6.4,0], [853,221,11.8,376,5,3], [805,292,5.1,366,2.7,3], [833,237,5.5,400,7.2,2], [624,283,5.7,241,6.7,3], [555,192,7.3,258,6.3,1], [541,170,5.3,240,4.4,1], [380,109,11,180,3.5,0], [14,8,12.5,6,33.3,0], [33,0,0,0,0,0], [216,80,6.3,109,7.7,1], [564,152,7.9,335,1.3,1], [466,158,15.8,207,5.7,1], [375,129,9.3,163,7,0], [496,173,11.6,205,8.1,1], [379,114,7,175,4.1,1], [410,108,13.9,214,6.3,1], [495,98,13.3,325,4.8,2], [288,73,11.0,162,3.1,2]],
        "Laura": [[681,39,0,319,0,0], [569,61,1.6,172,0,1], [513,30,0,298,0,1], [737,19,10.5,293,1.1,0], [820,50,0,346,0,0], [795,57,7,343,1.3,2], [652,49,6.1,294,0,0], [770,102,5.9,311,0,0], [681,173,4.6,207,0,1], [600,112,1.8,307,0,0], [699,209,3.8,231,0,0], [758,31,3.2,182,0,1], [607,125,4,278,0.8,0], [315,0,0,177,0,0], [170,38,5.3,90,0,0], [30,0,0,1,0,0], [300,36,8.3,256,0,0], [629,44,6.8,294,0,0], [714,170,4.1,264,0.4,1], [667,124,5.6,240,0.4,1], [594,140,1.4,224,0,0], [203,0,0,90,0,0], [529,94,4.3,202,0.0,0]],
        "Lea": [[108,53,5.7,43,0,0], [0,0,0,0,0,0], [195,44,11.4,84,1.3,0], [459,89,13.5,242,1.8,2], [451,181,7.7,181,3.7,0], [594,116,12.1,236,1.4,1], [571,126,13.5,238,1.4,1], [523,218,12.4,148,0.8,2], [575,251,8.4,194,5.1,2], [314,111,9.9,116,1.9,0], [254,94,11.7,61,6.8,1], [419,130,7.7,159,3.1,1], [118,54,1.9,32,0,0], [184,3,33.3,76,7.7,1], [254,39,17.9,128,7.3,1], [162,91,15.4,58,3.9,2], [336,88,14.8,141,4.4,1], [259,132,23.5,102,3.4,0], [478,159,11.3,193,2.4,2], [185,104,17.3,50,8.5,0], [303,89,15.7,144,5.6,0], [342,123,13,131,1.8,1], [236,99,9.1,78,6.5,1]],
        "Rozanne": [[235,24,16.7,115,0,0], [360,62,11.3,84,1.3,0], [547,76,3.9,163,0,0], [581,123,5.7,210,0.5,1], [786,164,6.7,225,1,0], [806,190,5.3,239,0.9,0], [744,177,4,232,0,1], [718,143,2.1,267,0,1], [404,79,6.3,90,0,0], [832,304,5.6,323,0,0], [699,209,3.8,231,0,1], [466,16,6.3,200,0,0], [97,0,0,96,0,0], [177,0,0,127,0,0], [283,0,0,201,1.1,0], [182,0,0,182,0.5,0], [127,55,5.5,20,16.7,0], [413,148,10.1,82,2.5,0], [470,75,8,166,2.6,1], [611,137,7.3,182,0,0], [595,148,5.4,168,0,0], [62,0,0,6,0,0], [273,70,5.7,83,0.0,0]],
        "Aiko": [[355,96,3.1,116,0,0], [255,75,5.3,96,1.3,0], [293,68,0,164,0.7,1], [375,114,1.8,138,0.8,0], [263,83,2.4,125,4.5,0], [274,80,3.8,118,0,0], [456,139,10.8,142,0,2], [410,144,3.5,147,0,0], [445,129,7,126,0.9,1], [322,109,2.8,77,1.4,2], [420,136,2.9,146,0,0], [395,113,8,111,0,0], [0,0,0,0,0,0], [55,0,0,14,0,0], [434,139,4.3,142,2.5,0], [311,117,0.9,79,1.5,0], [510,178,1.7,132,0.9,0], [444,117,1.7,169,1.4,1], [477,167,6,126,0.9,0], [399,155,1.9,99,0,0], [417,188,0,119,3,0], [421,156,1.9,84,4.2,0], [365,116,0.9,146,1.7,0]],
        "Max": [[0,0,0,0,0,0]] * 22 + [[560, 73, 0.0, 226, 0.0, 0]]
    }

    data = []
    for sdr, metrics in raw_data.items():
        for i, row in enumerate(metrics):
            data.append({"SDR": sdr, "Week": weeks_list[i], "Total Activities": row[0], "Calls Logged": row[1], "Connect %": row[2], "Emails Sent": row[3], "Reply %": row[4], "Meetings Booked": row[5]})
    return pd.DataFrame(data)

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

# --- CONTENT DICTIONARIES ---
sdr_analytics = {
    "Ben": "**The Situation:** Ben ran out of runway on emails due to his D2C TAM limits, but brilliantly pivoted to Nooks to aggressively call his best prospects.\n\n**Timing Insight:** Dominates the EU/UK hours (6 AM to 3 PM IST). His extreme volume during peak business hours yields incredible connects.\n\n**Action Item:** Ensure he has enough fresh, verified data so he doesn't burn his list too quickly.",
    "Feddy": "**The Situation:** Battling the US market with Nooks. High activity, but very low connect rates.\n\n**Timing Insight:** Calling the US heavily from 2 PM to 10 PM IST. Review if these late blocks are yielding quality connects or just voicemails.\n\n**Action Item:** Dissect his Jan Week 3 outbound spike. Help build a consistent, daily cadence.",
    "Heike": "**The Situation:** Operating with a very limited TAM, she plays the 'sniper.'\n\n**Timing Insight:** Classic DACH hours. Highly effective early mornings (7 AM - 11 AM IST). Keep her focused on these prime windows.\n\n**Action Item:** Do not force mindless volume. Ask her to template her successful hooks and share them.",
    "Ilana": "**The Situation:** Achieving absurdly high conversion metrics, but volume is critically low.\n\n**Timing Insight:** Historical heatmaps are beautiful (8 AM - 4 PM), but 'Last Week' is practically empty. She has stopped dialing.\n\n**Action Item:** Enforce a daily 8 AM - 4 PM block consistency to get her volume up. If she doubles volume, she is the top rep.",
    "Jessica": "**The Situation:** True discipline. Maintained a multi-channel approach despite territory cuts.\n\n**Timing Insight:** Incredibly consistent. Dials solidly between 8 AM and 5 PM IST every single day without fail.\n\n**Action Item:** Facilitate a strategy session with Heike to adapt DACH hooks for B2C.",
    "Laura": "**The Situation:** Slogged through the US market. High activity, but email reply rate is 0%.\n\n**Timing Insight:** Calling heavily in the US blocks. 'This Quarter' shows dense activity Mon/Fri, while 'Last Week' maps perfectly to afternoon/late evening (4 PM - 11 PM IST). Needs strict, repeatable power hours.\n\n**Action Item:** Rewrite US sequences. Use Nooks to lower dialing barrier.",
    "Lea": "**The Situation:** A true 'Steady Eddy.' Books 1-2 meetings almost every week.\n\n**Timing Insight:** Very steady UK/Nordics calling rhythm between 9 AM and 6 PM IST.\n\n**Action Item:** Find out what caused her activity volume to dip into the 100-300 range compared to her 500+ baseline.",
    "Rozanne": "**The Situation:** Capable of high volume, but has a serious red flag: 4 weeks of 0 calls.\n\n**Timing Insight:** US market. Heavily skewed to late evening IST (4 PM - 11 PM), with some midnight spikes.\n\n**Action Item:** Address the 0-call months. Mandate Nooks to ensure she hits a minimum weekly threshold.",
    "Aiko": "**The Situation:** Steady, low-risk upside in non-core markets.\n\n**Timing Insight:** Connects best Tuesday 1-2 AM and Wednesday 8 AM (IST). Focus her efforts on these highly specific windows.\n\n**Action Item:** Decouple connect rates from review until bad data is fixed. Implement iOS Screener Playbook.",
    "Max": "**The Situation:** The newest US SDR, just ramping up. Logged 560 activities in Week 1.\n\n**Timing Insight:** Calling heavily between 2 PM and 9 PM IST. Excellent baseline schedule for the US market.\n\n**Action Item:** Start on Nooks Day 1. Email is a supplement, phone is the primary weapon."
}

coaching_plans = {k: "Discuss timing strategies based on the heatmaps below to optimize connect rates and ensure schedule alignment." for k in sdr_analytics.keys()}

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