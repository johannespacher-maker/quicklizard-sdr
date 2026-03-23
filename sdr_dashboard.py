import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="Quicklizard SDR Dashboard", page_icon="🦎", layout="wide")
st.title("🦎 Quicklizard SDR Performance & Coaching Dashboard")

# --- QUICKLIZARD BRANDING ---
ql_green = "#27ae60"

# --- 1. SILENT BACKGROUND ENGINE (GOOGLE + SALESLOFT) ---
@st.cache_resource
def get_google_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

try:
    gc = get_google_client()
    # Your Master Google Sheet URL for Auth and Archives
    MASTER_SHEET_URL = "https://docs.google.com/spreadsheets/d/1OySLhZjJk1ArFdbdgtBukO5vKNJTOAZ-A7EM_peXY2g/edit"
    sh = gc.open_by_url(MASTER_SHEET_URL)
    auth_sheet = sh.worksheet("System_Auth")
    
    # Grab current token
    current_refresh_token = auth_sheet.acell('B1').value
    access_token = st.secrets.get("SALESLOFT_ACCESS_TOKEN", "")

    # Silent Token Check
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    test_response = requests.get("https://api.salesloft.com/v2/me", headers=headers)

    if test_response.status_code != 200:
        # Token expired. Silently refresh memory bank...
        payload = {
            "client_id": st.secrets["SALESLOFT_CLIENT_ID"],
            "client_secret": st.secrets["SALESLOFT_CLIENT_SECRET"],
            "grant_type": "refresh_token",
            "refresh_token": current_refresh_token
        }
        refresh_res = requests.post("https://accounts.salesloft.com/oauth/token", data=payload)
        if refresh_res.status_code == 200:
            new_keys = refresh_res.json()
            access_token = new_keys["access_token"]
            auth_sheet.update_acell('B1', new_keys["refresh_token"])
            headers["Authorization"] = f"Bearer {access_token}"
            
except Exception as e:
    st.sidebar.error(f"Background Sync Error: {e}")

# --- 2. GOOGLE SHEETS DATA ENGINES (UNTOUCHED) ---
@st.cache_data(ttl=600)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=0&single=true&output=csv"
    return pd.read_csv(sheet_url)

df = load_data()

@st.cache_data(ttl=600)
def load_heatmap_data():
    sheet_url_heatmap = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=1688694640&single=true&output=csv"
    df_raw = pd.read_csv(sheet_url_heatmap)
    
    heatmap_data = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    for _, row in df_raw.iterrows():
        sdr = row['SDR']
        week = row['Week']
        
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
                        heatmap_data.append((sdr, week, day[:3], hour_int, calls, conn_rate))
                except:
                    continue
                    
    df_heat = pd.DataFrame(heatmap_data, columns=["SDR", "Week", "Day", "Hour", "Calls", "Connect %"])
    
    final_heat = []
    qtr_agg = df_heat.groupby(['SDR', 'Day', 'Hour']).agg({'Calls':'sum', 'Connect %':'mean'}).reset_index()
    qtr_agg['Timeframe'] = 'This Quarter'
    final_heat.append(qtr_agg)
    
    for sdr in df_heat['SDR'].unique():
        sdr_weeks = df_heat[df_heat['SDR'] == sdr]['Week'].unique()
        if len(sdr_weeks) > 0:
            latest_week = sdr_weeks[-1] 
            lw_data = df_heat[(df_heat['SDR'] == sdr) & (df_heat['Week'] == latest_week)].copy()
            lw_data['Timeframe'] = 'Last Week'
            final_heat.append(lw_data)
            
    if final_heat:
        return pd.concat(final_heat, ignore_index=True)
    else:
        return pd.DataFrame(columns=["SDR", "Timeframe", "Day", "Hour", "Calls", "Connect %"])

df_heat = load_heatmap_data()

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

@st.cache_data(ttl=600)
def load_coaching_data():
    sheet_url_coaching = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=1177538336&single=true&output=csv"
    df_coach = pd.read_csv(sheet_url_coaching)
    
    analytics_dict = {}
    plans_dict = {}
    for index, row in df_coach.iterrows():
        sdr_name = row['SDR']
        analytics_dict[sdr_name] = f"**The Situation:** {row['Situation']}\n\n**Strengths:** {row['Strengths']}\n\n**Action Item:** {row['Action Item']}"
        plans_dict[sdr_name] = str(row['Coaching Plan'])
        
    return analytics_dict, plans_dict

sdr_analytics, coaching_plans = load_coaching_data()

@st.cache_data(ttl=600)
def load_projects_data():
    sheet_url_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=1790930146&single=true&output=csv"
    df_proj = pd.read_csv(sheet_url_projects)
    
    projects_dict = {}
    for index, row in df_proj.iterrows():
        projects_dict[row['Project Title']] = str(row['Content']).replace("<br>", "\n")
    return projects_dict

projects_data = load_projects_data()

@st.cache_data(ttl=600)
def load_conference_data():
    conf_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPoua2HZBuFO4OqvrxjB7MOk5B9Sy_nHJKOvMckok97mAKZKFB2nteZPPRv56opZD2i0JpGuJhsQsl/pub?gid=1297186162&single=true&output=csv" 
    return pd.read_csv(conf_url)

conf_df = load_conference_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🦎 Quicklizard Menu")
view = st.sidebar.radio("Go to:", [
    "🏆 Team Overview & Rankings", 
    "🔍 Individual Deep Dive", 
    "🗣️ 1:1 Coaching Advice", 
    "🚀 Special Projects", 
    "🎟️ Event Targets",
    "🔄 Data Sync Center" # <-- NEW ADMIN PAGE
])

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
    with row3_col1: st.plotly_chart(px.line(sdr_data, x="Week", y="Emails Sent", title="Emails Sent 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)
    with row3_col2: st.plotly_chart(px.line(sdr_data, x="Week", y="Reply %", title="Reply % 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)

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

        def get_connect_tier(val):
            if val <= 5.0: return "0-5%"
            elif val <= 10.0: return "5-10%"
            elif val <= 15.0: return "10-15%"
            elif val <= 20.0: return "15-20%"
            elif val <= 30.0: return "20-30%"
            elif val <= 50.0: return "30-50%"
            else: return "50-100%"

        sdr_heatmap_data["Connect Tier"] = sdr_heatmap_data["Connect %"].apply(get_connect_tier)

        tier_colors = {
            "0-5%": "#e6f4ea", "5-10%": "#a8dab5", "10-15%": "#6cc08b", 
            "15-20%": "#27ae60", "20-30%": "#1e8449", "30-50%": "#145a32", "50-100%": "#082614"
        }
        tier_order = ["0-5%", "5-10%", "10-15%", "15-20%", "20-30%", "30-50%", "50-100%"]

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
                color_discrete_map=tier_colors, category_orders={"Day": all_days, "Connect Tier": tier_order},
                title=f"This Quarter ({selected_tz.split(' ')[0]})", hover_data={"Connect %": True, "Connect Tier": False}
            )
            fig_q.update_xaxes(range=[-0.5, 23.5], tickvals=list(range(24)), ticktext=[f"{h%12 if h%12!=0 else 12} {'AM' if h<12 else 'PM'}" for h in range(24)])
            heat_col1.plotly_chart(fig_q, use_container_width=True)
            
        w_data = sdr_heatmap_data[sdr_heatmap_data["Timeframe"] == "Last Week"]
        if not w_data.empty:
            fig_w = px.scatter(
                w_data, x="Hour", y="Day", size="Calls", color="Connect Tier", 
                color_discrete_map=tier_colors, category_orders={"Day": all_days, "Connect Tier": tier_order},
                title=f"Last Week ({selected_tz.split(' ')[0]})", hover_data={"Connect %": True, "Connect Tier": False}
            )
            fig_w.update_xaxes(range=[-0.5, 23.5], tickvals=list(range(24)), ticktext=[f"{h%12 if h%12!=0 else 12} {'AM' if h<12 else 'PM'}" for h in range(24)])
            heat_col2.plotly_chart(fig_w, use_container_width=True)

# --- VIEW 3: 1:1 COACHING ADVICE ---
elif view == "🗣️ 1:1 Coaching Advice":
    st.header("1:1 Coaching Agendas")
    if coaching_plans:
        selected_sdr_coach = st.selectbox("Select SDR for 1:1 Prep:", list(coaching_plans.keys()))
        st.subheader(f"Action Plan for {selected_sdr_coach}")
        raw_text = coaching_plans[selected_sdr_coach]
        formatted_text = raw_text.replace(" 1.", "\n\n1.").replace(" 2.", "\n\n2.").replace(" 3.", "\n\n3.").replace(" 4.", "\n\n4.")
        st.markdown(formatted_text)
    else:
        st.info("Coaching data not found. Please check your Google Sheets connection.")

# --- VIEW 4: SPECIAL PROJECTS ---
elif view == "🚀 Special Projects":
    st.header("Strategic Initiatives & Focus Areas")
    if projects_data:
        project = st.selectbox("Select Project:", list(projects_data.keys()))
        st.markdown(projects_data[project])
    else:
        st.info("Special Projects data not found. Please check your Google Sheets connection.")

# --- VIEW 5: EVENT TARGETS ---
elif view == "🎟️ Event Targets":
    st.header("🎟️ Conference Target Tracker")
    city_themes = {
        "NRF New York": {"emoji": "🗽", "color": "#3498db", "bg": "#ebf5fb"},
        "ShopTalk Las Vegas": {"emoji": "🎰", "color": "#e74c3c", "bg": "#fdedec"},
        "RetailTech London": {"emoji": "🎡", "color": "#9b59b6", "bg": "#f5eef8"},
        "ShopTalk Barcelona": {"emoji": "💃", "color": "#f1c40f", "bg": "#fef9e7"},
        "K5 Berlin": {"emoji": "🥨", "color": "#e67e22", "bg": "#fdf2e9"} 
    }
    
    selected_conf = st.selectbox("Select Conference:", conf_df["Conference"].unique())
    conf_data = conf_df[conf_df["Conference"] == selected_conf]
    
    total_booked = conf_data["Meetings Booked"].sum()
    target = conf_data["Target"].iloc[0]
    theme = city_themes.get(selected_conf, {"emoji": "🎯", "color": "#27ae60", "bg": "#eafaf1"})
    
    st.markdown("---")
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
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
                'steps': [{'range': [0, target], 'color': theme['bg']}],
            }
        ))
        fig_gauge.update_layout(height=380, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with col2:
        leaderboard_data = conf_data[conf_data["Meetings Booked"] > 0].sort_values(by="Meetings Booked", ascending=False)
        if not leaderboard_data.empty:
            fig_leader = px.bar(
                leaderboard_data, x="SDR", y="Meetings Booked", title=f"🏆 Top SDR Contributors",
                text_auto=True, color="Meetings Booked", color_continuous_scale=[theme['bg'], theme['color']] 
            )
            fig_leader.update_layout(xaxis_title="", yaxis_title="Meetings Booked", height=380, showlegend=False)
            st.plotly_chart(fig_leader, use_container_width=True)
        else:
            st.warning(f"No meetings booked yet for {selected_conf}. Time to hit the phones! 📞")

# --- VIEW 6: DATA SYNC CENTER (THE SMART MONDAY PORTAL) ---
elif view == "🔄 Data Sync Center":
    st.header("🔄 Smart Monday Data Sync")
    st.info("This portal safely pulls last week's Salesloft data and preps it for your Data Archive. It protects against duplicates!")
    
    sdr_mapping = {
        125597: "Heike", 125115: "Ilana", 96132: "Aiko", 107027: "Laura",
        130029: "Max", 125114: "Feddy", 73179: "Ben", 118645: "Jessica",
        96130: "Rozanne", 118647: "Lea"
    }
    
    import datetime as dt
    
    # 1. Time Travel: Calculate exactly what "Last Week" was (Monday to Sunday)
    today = dt.date.today()
    last_monday = today - dt.timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + dt.timedelta(days=6)
    
    # Format dates for the API (UTC)
    start_str = last_monday.strftime('%Y-%m-%dT00:00:00Z')
    end_str = last_sunday.strftime('%Y-%m-%dT23:59:59Z')
    
    # Create the "Week" label to match your historic data (e.g., "Mar - W4")
    week_num = (last_monday.day - 1) // 7 + 1
    month_abbr = last_monday.strftime('%b')
    week_label = f"{month_abbr} - W{week_num}"
    
    st.write(f"**Target Sync Window:** {last_monday.strftime('%B %d')} to {last_sunday.strftime('%B %d')} ({week_label})")
    
    if st.button("Fetch Last Week's Data"):
        with st.spinner("Digging through the Salesloft archives..."):
            date_filter = f"?created_at[gte]={start_str}&created_at[lte]={end_str}&per_page=100"
            
            metrics = {name: {"Calls": 0, "Connected": 0, "Emails": 0, "Replies": 0, "Other": 0} for name in sdr_mapping.values()}
            
            # Use the global headers set at the top of the file
            calls_res = requests.get(f"https://api.salesloft.com/v2/activities/calls{date_filter}", headers=headers)
            if calls_res.status_code == 200:
                for call in calls_res.json().get('data', []):
                    if call.get('user') and call['user']['id'] in sdr_mapping:
                        name = sdr_mapping[call['user']['id']]
                        metrics[name]["Calls"] += 1
                        if call.get('disposition') == 'Connected':
                            metrics[name]["Connected"] += 1

            emails_res = requests.get(f"https://api.salesloft.com/v2/activities/emails{date_filter}", headers=headers)
            if emails_res.status_code == 200:
                for email in emails_res.json().get('data', []):
                    if email.get('user') and email['user']['id'] in sdr_mapping:
                        name = sdr_mapping[email['user']['id']]
                        metrics[name]["Emails"] += 1
                        if email.get('counts', {}).get('replies', 0) > 0:
                            metrics[name]["Replies"] += 1

            tasks_res = requests.get(f"https://api.salesloft.com/v2/tasks{date_filter}&current_state=completed", headers=headers)
            if tasks_res.status_code == 200:
                for task in tasks_res.json().get('data', []):
                    if task.get('user') and task['user']['id'] in sdr_mapping:
                        name = sdr_mapping[task['user']['id']]
                        metrics[name]["Other"] += 1

            # Format the data EXACTLY like your Google Sheet
            data_list = []
            for name, m in metrics.items():
                total_activities = m["Calls"] + m["Emails"] + m["Other"]
                conn_pct = f"{round((m['Connected'] / m['Calls'] * 100), 1)}%" if m["Calls"] > 0 else "0.0%"
                reply_pct = f"{round((m['Replies'] / m['Emails'] * 100), 1)}%" if m["Emails"] > 0 else "0.0%"
                
                # Columns: SDR | Week | Total | Calls | Connect% | Emails | Reply% | Meetings Booked (0 by default)
                data_list.append([name, week_label, total_activities, m["Calls"], conn_pct, m["Emails"], reply_pct, 0])

            st.session_state['last_week_df'] = pd.DataFrame(data_list, columns=["SDR", "Week", "Total Activities", "Calls Logged", "Connect %", "Emails Sent", "Reply %", "Meetings Booked"])
            st.session_state['last_week_df'] = st.session_state['last_week_df'].sort_values(by="Total Activities", ascending=False)
            
    if 'last_week_df' in st.session_state:
        st.success("✅ Data Pulled Successfully! Review below before saving.")
        st.dataframe(st.session_state['last_week_df'], hide_index=True, use_container_width=True)
        
        st.markdown("---")
        if st.button("Archive to Google Sheets (Safe Sync)"):
            try:
                archive_sheet = sh.worksheet("Data_Archive")
                
                # DUPLICATION CHECK: Read column B to see if the week_label already exists
                existing_weeks = archive_sheet.col_values(2) 
                
                if week_label in existing_weeks:
                    st.error(f"🚨 Hold up! It looks like data for '{week_label}' is already in the archive. Sync aborted to prevent duplicates.")
                else:
                    archive_sheet.append_rows(st.session_state['last_week_df'].values.tolist())
                    st.success(f"🎉 BOOM! '{week_label}' permanently saved to the Data_Archive tab.")
                    st.balloons()
            except Exception as e:
                st.error(f"Failed to save to Google Sheets: {e}")