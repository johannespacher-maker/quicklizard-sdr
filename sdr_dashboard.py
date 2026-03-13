import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # We need this for the beautiful Target Gauge

# --- PAGE SETUP ---
st.set_page_config(page_title="Quicklizard SDR Dashboard", page_icon="🦎", layout="wide")
st.title("🦎 Quicklizard SDR Performance & Coaching Dashboard")

# --- QUICKLIZARD BRANDING ---
ql_green = "#27ae60"

# --- GOOGLE SHEETS DATA ENGINE ---
@st.cache_data(ttl=600) # This tells the app to fetch fresh data every 10 minutes
def load_data():
    # Replace the text inside the quotes with your copied link!
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=0&single=true&output=csv"
    return pd.read_csv(sheet_url)

df = load_data()

# --- GOOGLE SHEETS HEATMAP ENGINE ---
@st.cache_data(ttl=600)
def load_heatmap_data():
    # Replace with your NEW Heatmap tab CSV link!
    sheet_url_heatmap = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=1688694640&single=true&output=csv"
    df_raw = pd.read_csv(sheet_url_heatmap)
    
    heatmap_data = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    for _, row in df_raw.iterrows():
        sdr = row['SDR']
        week = row['Week']
        
        # Convert "2:00 PM" into integer 14 for the engine
        time_str = str(row['Hour'])
        try:
            hour_int = int(pd.to_datetime(time_str, format='%I:%M %p').strftime('%H'))
        except:
            continue
            
        for day in days:
            cell_val = str(row.get(day, 'nan'))
            if cell_val != 'nan' and '/' in cell_val:
                try:
                    calls, connects = cell_val.split('/')
                    calls = int(calls)
                    connects = int(connects)
                    
                    if calls > 0:
                        conn_rate = round((connects / calls) * 100, 1)
                        # We map the full day names back to 3 letters for the chart
                        heatmap_data.append((sdr, week, day[:3], hour_int, calls, conn_rate))
                except:
                    continue
                    
    df_heat = pd.DataFrame(heatmap_data, columns=["SDR", "Week", "Day", "Hour", "Calls", "Connect %"])
    
    # --- The Auto-Aggregating Magic ---
    # This automatically builds "This Quarter" and "Last Week" on the fly!
    final_heat = []
    
    # 1. Build "This Quarter" (Sums everything for an SDR)
    qtr_agg = df_heat.groupby(['SDR', 'Day', 'Hour']).agg({'Calls':'sum', 'Connect %':'mean'}).reset_index()
    qtr_agg['Timeframe'] = 'This Quarter'
    final_heat.append(qtr_agg)
    
    # 2. Build "Last Week" (Finds the most recent week for each SDR)
    for sdr in df_heat['SDR'].unique():
        sdr_weeks = df_heat[df_heat['SDR'] == sdr]['Week'].unique()
        if len(sdr_weeks) > 0:
            # Assumes the newest week is typed last in the spreadsheet
            latest_week = sdr_weeks[-1] 
            lw_data = df_heat[(df_heat['SDR'] == sdr) & (df_heat['Week'] == latest_week)].copy()
            lw_data['Timeframe'] = 'Last Week'
            final_heat.append(lw_data)
            
    if final_heat:
        return pd.concat(final_heat, ignore_index=True)
    else:
        return pd.DataFrame(columns=["SDR", "Timeframe", "Day", "Hour", "Calls", "Connect %"])

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

# --- GOOGLE SHEETS SPECIAL PROJECTS ENGINE ---
@st.cache_data(ttl=600)
def load_projects_data():
    # Replace with your NEW Special Projects tab CSV link!
    sheet_url_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=1790930146&single=true&output=csv"
    df_proj = pd.read_csv(sheet_url_projects)
    
    projects_dict = {}
    for index, row in df_proj.iterrows():
        # This replaces the <br> tags from Google Sheets with actual Markdown line breaks!
        projects_dict[row['Project Title']] = str(row['Content']).replace("<br>", "\n")
    return projects_dict

projects_data = load_projects_data()

# --- CONFERENCES DATA ENGINE ---
@st.cache_data(ttl=600)
def load_conference_data():
    # Paste your NEW link for the Conferences tab right here between the quotes!
    conf_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=1297186162&single=true&output=csv" 
    return pd.read_csv(conf_url)

conf_df = load_conference_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🦎 Quicklizard Menu")
view = st.sidebar.radio("Go to:", ["🏆 Team Overview & Rankings", "🔍 Individual Deep Dive", "🗣️ 1:1 Coaching Advice", "🚀 Special Projects", "🎟️ Event Targets"])

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

    row3_col1, row3_col2 = st.columns(2)
    with row3_col1: st.plotly_chart(px.line(sdr_data, x="Week", y="Emails Sent", title="Emails Sent 🦎", markers=True, 
color_discrete_sequence=[ql_green]), use_container_width=True)
    with row3_col2: st.plotly_chart(px.line(sdr_data, x="Week", y="Reply %", title="Reply % 🦎", markers=True, 
color_discrete_sequence=[ql_green]), use_container_width=True)

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

        # 1. Custom Connect % Buckets Logic
        def get_connect_tier(val):
            if val <= 5.0: return "0-5%"
            elif val <= 10.0: return "5-10%"
            elif val <= 15.0: return "10-15%"
            elif val <= 20.0: return "15-20%"
            elif val <= 30.0: return "20-30%"
            elif val <= 50.0: return "30-50%"
            else: return "50-100%"

        sdr_heatmap_data["Connect Tier"] = sdr_heatmap_data["Connect %"].apply(get_connect_tier)

        # 2. Custom Color Palette Mapping
        tier_colors = {
            "0-5%": "#e6f4ea",     # Faint mint
            "5-10%": "#a8dab5",    # Light green
            "10-15%": "#6cc08b",   # Soft green
            "15-20%": "#27ae60",   # Quicklizard Brand Green
            "20-30%": "#1e8449",   # Darker green
            "30-50%": "#145a32",   # Deep forest green
            "50-100%": "#082614"   # Almost black-green
        }
        tier_order = ["0-5%", "5-10%", "10-15%", "15-20%", "20-30%", "30-50%", "50-100%"]

        # FORCE MON-FRI Y-AXIS AND 24HR X-AXIS
        all_days = ["Fri", "Thu", "Wed", "Tue", "Mon"] 
        sdr_heatmap_data = sdr_heatmap_data[sdr_heatmap_data["Day"].isin(all_days)]
        
        dummy_data = []
        for d in all_days:
            dummy_data.append({"SDR": selected_sdr, "Timeframe": "This Quarter", "Day": d, "Hour": -10, "Calls": 0, "Connect %": 0, "Connect Tier": "0-5%"})
            dummy_data.append({"SDR": selected_sdr, "Timeframe": "Last Week", "Day": d, "Hour": -10, "Calls": 0, "Connect %": 0, "Connect Tier": "0-5%"})
        sdr_heatmap_data = pd.concat([sdr_heatmap_data, pd.DataFrame(dummy_data)], ignore_index=True)

        heat_col1, heat_col2 = st.columns(2)
        
        q_data = sdr_heatmap_data[sdr_heatmap_data["Timeframe"] == "This Quarter"]
        if not q_data.empty:
            fig_q = px.scatter(
                q_data, x="Hour", y="Day", size="Calls", color="Connect Tier", 
                color_discrete_map=tier_colors, 
                category_orders={"Day": all_days, "Connect Tier": tier_order},
                title=f"This Quarter ({selected_tz.split(' ')[0]})",
                hover_data={"Connect %": True, "Connect Tier": False}
            )
            fig_q.update_xaxes(range=[-0.5, 23.5], tickvals=list(range(24)), ticktext=[f"{h%12 if h%12!=0 else 12} {'AM' if h<12 else 'PM'}" for h in range(24)])
            heat_col1.plotly_chart(fig_q, use_container_width=True)
            
        w_data = sdr_heatmap_data[sdr_heatmap_data["Timeframe"] == "Last Week"]
        if not w_data.empty:
            fig_w = px.scatter(
                w_data, x="Hour", y="Day", size="Calls", color="Connect Tier", 
                color_discrete_map=tier_colors, 
                category_orders={"Day": all_days, "Connect Tier": tier_order},
                title=f"Last Week ({selected_tz.split(' ')[0]})",
                hover_data={"Connect %": True, "Connect Tier": False}
            )
            fig_w.update_xaxes(range=[-0.5, 23.5], tickvals=list(range(24)), ticktext=[f"{h%12 if h%12!=0 else 12} {'AM' if h<12 else 'PM'}" for h in range(24)])
            heat_col2.plotly_chart(fig_w, use_container_width=True)

# --- VIEW 3: 1:1 COACHING ADVICE ---
elif view == "🗣️ 1:1 Coaching Advice":
    st.header("1:1 Coaching Agendas")
    
    if coaching_plans:
        selected_sdr_coach = st.selectbox("Select SDR for 1:1 Prep:", list(coaching_plans.keys()))
        st.subheader(f"Action Plan for {selected_sdr_coach}")
        
        # Grab the text and force double line breaks before the numbers so Markdown renders a clean list!
        raw_text = coaching_plans[selected_sdr_coach]
        formatted_text = raw_text.replace(" 1.", "\n\n1.").replace(" 2.", "\n\n2.").replace(" 3.", "\n\n3.").replace(" 4.", "\n\n4.")
        
        st.markdown(formatted_text)
    else:
        st.info("Coaching data not found. Please check your Google Sheets connection.")

# --- VIEW 4: SPECIAL PROJECTS ---
elif view == "🚀 Special Projects":
    st.header("Strategic Initiatives & Focus Areas")
    
    if projects_data:
        # Dynamically pulls the project titles from your Google Sheet
        project = st.selectbox("Select Project:", list(projects_data.keys()))
        st.markdown(projects_data[project])
    else:
        st.info("Special Projects data not found. Please check your Google Sheets connection.")

# --- VIEW 5: EVENT TARGETS ---
elif view == "🎟️ Event Targets":
    st.header("🎟️ Conference Target Tracker")
    
    # 1. Custom City Themes (Emoji, Bar Color, Background Color)
    city_themes = {
        "NRF New York": {"emoji": "🗽", "color": "#3498db", "bg": "#ebf5fb"},        # Big Apple Blue
        "ShopTalk Las Vegas": {"emoji": "🎰", "color": "#e74c3c", "bg": "#fdedec"},  # Neon Red
        "RetailTech London": {"emoji": "🎡", "color": "#9b59b6", "bg": "#f5eef8"},    # Royal Purple
        "ShopTalk Barcelona": {"emoji": "💃", "color": "#f1c40f", "bg": "#fef9e7"},  # Sunny Yellow
        "K5 Berlin": {"emoji": "🥨", "color": "#e67e22", "bg": "#fdf2e9"}             # Warm Orange
    }
    
    # 2. Select Event & Filter Data
    selected_conf = st.selectbox("Select Conference:", conf_df["Conference"].unique())
    conf_data = conf_df[conf_df["Conference"] == selected_conf]
    
    # Calculate current progress
    total_booked = conf_data["Meetings Booked"].sum()
    target = conf_data["Target"].iloc[0]
    
    # Grab the theme for the selected city (defaults to QL Green if city not in dictionary)
    theme = city_themes.get(selected_conf, {"emoji": "🎯", "color": "#27ae60", "bg": "#eafaf1"})
    
    st.markdown("---")
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # 3. The Customized Target Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_booked,
            number={'suffix': f" / {target}", 'font': {'size': 40}},
            title={'text': f"{theme['emoji']} {selected_conf} Progress", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, target], 'tickwidth': 1},
                'bar': {'color': theme['color']},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, target], 'color': theme['bg']} # Light background based on city
                ],
            }
        ))
        fig_gauge.update_layout(height=380, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with col2:
        # 4. SDR Leaderboard Chart
        # Filter out SDRs with 0 meetings so the chart only shows those who contributed
        leaderboard_data = conf_data[conf_data["Meetings Booked"] > 0].sort_values(by="Meetings Booked", ascending=False)
        
        if not leaderboard_data.empty:
            fig_leader = px.bar(
                leaderboard_data,
                x="SDR",
                y="Meetings Booked",
                title=f"🏆 Top SDR Contributors",
                text_auto=True,
                color="Meetings Booked",
                # The bar chart colors dynamically adapt to the city's theme!
                color_continuous_scale=[theme['bg'], theme['color']] 
            )
            fig_leader.update_layout(xaxis_title="", yaxis_title="Meetings Booked", height=380, showlegend=False)
            st.plotly_chart(fig_leader, use_container_width=True)
        else:
            # Displays if a brand new event has 0 meetings booked
            st.warning(f"No meetings booked yet for {selected_conf}. Time to hit the phones! 📞")