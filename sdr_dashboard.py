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
    weeks_list = [
        "Oct - W1", "Oct - W2", "Oct - W3", "Oct - W4", "Oct - W5",
        "Nov - W1", "Nov - W2", "Nov - W3", "Nov - W4",
        "Dec - W1", "Dec - W2", "Dec - W3", "Dec - W4", "Dec - W5",
        "Jan - W1", "Jan - W2", "Jan - W3", "Jan - W4",
        "Feb - W1", "Feb - W2", "Feb - W3", "Feb - W4",
        "Mar - W1"
    ]

    raw_data = {
        "Ben": [
            [0,0,0,0,0,0], [0,0,0,0,0,0], [855,245,6.5,193,0.7,0], [847,315,7.3,234,1,1], [1229,405,7,475,0.5,2],
            [962,395,5.1,264,0.9,5], [963,519,1.9,325,0,1], [735,281,2.1,220,0.5,3], [873,307,4.9,314,1.2,5],
            [530,150,2,183,1.3,1], [506,363,7.2,68,0,1], [326,140,2.1,168,0,1], [0,0,0,0,0,0], [0,0,0,0,0,0],
            [842,103,7.8,342,0,3], [761,224,4.9,346,2,3], [727,654,12.1,73,3.1,3], [544,460,2,83,0,5],
            [572,503,5,68,0,2], [426,367,3.3,59,0,4], [417,417,4.8,0,0,3], [438,369,3.8,10,0,1], [290,277,4.3,12,0.0,0]
        ],
        "Feddy": [[0,0,0,0,0,0]] * 8 + [
            [75,31,6.5,19,0,0],
            [269,99,3,114,0,0], [226,81,2.5,64,0,0], [473,161,3.1,169,0.7,0], [271,178,6.2,69,0,0], [351,1,0,155,1.4,0],
            [473,395,2.8,78,4.6,0], [257,51,2,206,2.2,1], [321,120,1.7,95,3.5,4], [558,377,2.9,77,0,1],
            [582,140,3.6,317,1.5,0], [647,245,9,330,0.3,1], [384,260,2.3,74,0,0], [38,0,0,38,3.2,0], [306,152,1.3,70,1.9,0]
        ],
        "Heike": [[0,0,0,0,0,0]] * 9 + [
            [128,85,21.1,24,9.5,0], [201,156,14.7,40,5.9,1], [188,146,11,180,3.5,0], [103,13,15.4,87,0,0], [48,40,5,8,12.5,0],
            [375,215,6,93,3.9,1], [197,137,5.8,37,2.7,0], [385,254,7.1,92,1.4,1], [309,223,6.3,77,3.2,0],
            [252,199,9.5,53,10.4,1], [248,203,3.4,40,11.8,0], [207,148,6.1,55,6.5,1], [157,120,5,37,0,1], [271,214,2.3,52,4.3,0]
        ],
        "Ilana": [[0,0,0,0,0,0]] * 8 + [
            [39,20,20,11,0,0],
            [94,32,28.1,29,11.1,0], [103,39,23.1,29,4,0], [145,25,16,90,4.8,1], [0,0,0,0,0,0], [13,0,0,0,0,0],
            [118,46,17.4,38,3.2,0], [120,30,33.3,68,8.1,0], [116,41,19.5,41,17.5,2], [73,22,9.1,27,8,0],
            [153,44,25,66,3.3,1], [118,32,12.5,55,3.8,0], [7,0,0,2,0,0], [95,35,5.7,33,11.1,0], [49,12,0.0,17,0.0,0]
        ],
        "Jessica": [[0,0,0,0,0,0]] * 3 + [
            [808,174,16.1,387,2.3,2], [698,163,13.5,310,6.4,0],
            [853,221,11.8,376,5,3], [805,292,5.1,366,2.7,3], [833,237,5.5,400,7.2,2], [624,283,5.7,241,6.7,3],
            [555,192,7.3,258,6.3,1], [541,170,5.3,240,4.4,1], [380,109,11,180,3.5,0], [14,8,12.5,6,33.3,0], [33,0,0,0,0,0],
            [216,80,6.3,109,7.7,1], [564,152,7.9,335,1.3,1], [466,158,15.8,207,5.7,1], [375,129,9.3,163,7,0],
            [496,173,11.6,205,8.1,1], [379,114,7,175,4.1,1], [410,108,13.9,214,6.3,1], [495,98,13.3,325,4.8,2], [288,73,11.0,162,3.1,2]
        ],
        "Laura": [
            [681,39,0,319,0,0], [569,61,1.6,172,0,1], [513,30,0,298,0,1], [737,19,10.5,293,1.1,0], [820,50,0,346,0,0],
            [795,57,7,343,1.3,2], [652,49,6.1,294,0,0], [770,102,5.9,311,0,0], [681,173,4.6,207,0,1],
            [600,112,1.8,307,0,0], [699,209,3.8,231,0,0], [758,31,3.2,182,0,1], [607,125,4,278,0.8,0], [315,0,0,177,0,0],
            [170,38,5.3,90,0,0], [30,0,0,1,0,0], [300,36,8.3,256,0,0], [629,44,6.8,294,0,0],
            [714,170,4.1,264,0.4,1], [667,124,5.6,240,0.4,1], [594,140,1.4,224,0,0], [203,0,0,90,0,0], [529,94,4.3,202,0.0,0]
        ],
        "Lea": [
            [108,53,5.7,43,0,0], [0,0,0,0,0,0], [195,44,11.4,84,1.3,0], [459,89,13.5,242,1.8,2], [451,181,7.7,181,3.7,0],
            [594,116,12.1,236,1.4,1], [571,126,13.5,238,1.4,1], [523,218,12.4,148,0.8,2], [575,251,8.4,194,5.1,2],
            [314,111,9.9,116,1.9,0], [254,94,11.7,61,6.8,1], [419,130,7.7,159,3.1,1], [118,54,1.9,32,0,0], [184,3,33.3,76,7.7,1],
            [254,39,17.9,128,7.3,1], [162,91,15.4,58,3.9,2], [336,88,14.8,141,4.4,1], [259,132,23.5,102,3.4,0],
            [478,159,11.3,193,2.4,2], [185,104,17.3,50,8.5,0], [303,89,15.7,144,5.6,0], [342,123,13,131,1.8,1], [236,99,9.1,78,6.5,1]
        ],
        "Rozanne": [
            [235,24,16.7,115,0,0], [360,62,11.3,84,1.3,0], [547,76,3.9,163,0,0], [581,123,5.7,210,0.5,1], [786,164,6.7,225,1,0],
            [806,190,5.3,239,0.9,0], [744,177,4,232,0,1], [718,143,2.1,267,0,1], [404,79,6.3,90,0,0],
            [832,304,5.6,323,0,0], [699,209,3.8,231,0,1], [466,16,6.3,200,0,0], [97,0,0,96,0,0], [177,0,0,127,0,0],
            [283,0,0,201,1.1,0], [182,0,0,182,0.5,0], [127,55,5.5,20,16.7,0], [413,148,10.1,82,2.5,0],
            [470,75,8,166,2.6,1], [611,137,7.3,182,0,0], [595,148,5.4,168,0,0], [62,0,0,6,0,0], [273,70,5.7,83,0.0,0]
        ],
        "Aiko": [
            [355,96,3.1,116,0,0], [255,75,5.3,96,1.3,0], [293,68,0,164,0.7,1], [375,114,1.8,138,0.8,0], [263,83,2.4,125,4.5,0],
            [274,80,3.8,118,0,0], [456,139,10.8,142,0,2], [410,144,3.5,147,0,0], [445,129,7,126,0.9,1],
            [322,109,2.8,77,1.4,2], [420,136,2.9,146,0,0], [395,113,8,111,0,0], [0,0,0,0,0,0], [55,0,0,14,0,0],
            [434,139,4.3,142,2.5,0], [311,117,0.9,79,1.5,0], [510,178,1.7,132,0.9,0], [444,117,1.7,169,1.4,1],
            [477,167,6,126,0.9,0], [399,155,1.9,99,0,0], [417,188,0,119,3,0], [421,156,1.9,84,4.2,0], [365,116,0.9,146,1.7,0]
        ],
        "Max": [[0,0,0,0,0,0]] * 22 + [[560, 73, 0.0, 226, 0.0, 0]]
    }

    data = []
    for sdr, metrics in raw_data.items():
        for i, row in enumerate(metrics):
            data.append({
                "SDR": sdr, "Week": weeks_list[i],
                "Total Activities": row[0], "Calls Logged": row[1],
                "Connect %": row[2], "Emails Sent": row[3],
                "Reply %": row[4], "Meetings Booked": row[5]
            })
            
    return pd.DataFrame(data)

df = load_data()

# --- CONTENT DICTIONARIES ---
sdr_analytics = {
    "Ben": "**The Situation:** Ben ran out of runway on emails due to his D2C TAM limits, but brilliantly pivoted to Nooks to aggressively call his best prospects. This led to a massive 12.1% connect rate in January.\n\n**Strengths:** Highly adaptable, proven closer (14 meetings in Nov, 14 in Jan).\n\n**Action Item:** Review his Nooks strategy. Ensure he has enough fresh, verified data to sustain his high call volume so he doesn't burn through his 'creme de la creme' list too quickly.",
    "Feddy": "**The Situation:** Started in Q4. His erratic channel-switching in late Dec/Jan was caused by shifting his focus to booking NRF conference meetings rather than pure outbound. However, he still managed a mysterious and impressive spike of 4 outbound meetings in Jan Week 3.\n\n**Strengths:** Hustle and persistence in a brutal market. He survived a zero-meeting ramp-up to book 6 in January.\n\n**Action Item:** Dissect his Jan Week 3 outbound spike. Find out what messaging he used. Help him build a consistent, daily multi-channel cadence now that the conference disruptions are over and he has a redefined account list.",
    "Heike": "**The Situation:** Operating with a very limited TAM, she plays the 'sniper.' Her engagement rates are elite (reply rates regularly hitting 10–12%+, connect rates consistently solid).\n\n**Strengths:** World-class personalization and DACH market mastery.\n\n**Action Item:** Do not force her to do mindless volume, as it will ruin her TAM. Instead, ask her to template her most successful hooks and share them with Jessica (who is struggling slightly with volume in DACH B2C).",
    "Ilana": "**The Situation:** Leveraging native language skills to achieve absurdly high conversion metrics (up to 33.3% connect rates and 17.5% reply rates). Her volume, however, is critically low.\n\n**Strengths:** Elite local engagement. When she touches an account, she converts it.\n\n**Action Item:** Focus 100% on workflow optimization. Sit with her to figure out why a single touchpoint takes her so long. If you can help her double her volume (which would still be relatively low), she will easily become your top meeting booker.",
    "Jessica": "**The Situation:** She was a volume machine (700+ activities/week) until her territory was reduced to just B2C. Her volume naturally halved, but she remained perfectly consistent in her execution.\n\n**Strengths:** Discipline. She maintained a true multi-channel approach despite the frustrating drop in meetings.\n\n**Action Item:** Validate her consistency. Facilitate a strategy session between her and Heike to see if Heike's high-converting DACH hooks can be adapted for Jessica's B2C accounts to increase her yield.",
    "Laura": "**The Situation:** Slogged through the US market, attended NRF, took vacation, and is now working with a redefined list. She actively dislikes making calls and defaults to email, but her email reply rate is essentially 0%.\n\n**Strengths:** Willing to put in high overall activity volume (regularly 600–700+ touches/week).\n\n**Action Item:** This is a critical intervention. You must rewrite her US email sequences entirely. Concurrently, use the Nooks parallel dialer to help her overcome her call reluctance. She cannot survive in the US market hiding behind 0% reply rate emails.",
    "Lea": "**The Situation:** A true 'Steady Eddy.' She books 1-2 meetings almost every single week with excellent connect rates (11-17%+). Her low activity in late Dec was due to targeted outreach, and Oct was vacation.\n\n**Strengths:** Reliability and great phone presence.\n\n**Action Item:** Find out what is causing her total activity volume to dip into the 100-300 range recently compared to her 500+ baseline in November. Have her share her UK/Nordics call openers with the team.",
    "Rozanne": "**The Situation:** Had a massive 16.7% reply rate on 20 emails due to brilliant NRF conference follow-up. Proved she can use Nooks (304 calls in Dec), but has a serious red flag: 4 weeks of 0 calls despite not being fully on vacation.\n\n**Strengths:** Capable of high volume, excellent at event follow-up.\n\n**Action Item:** Address the 0-call month immediately. Since she already proved Nooks works for her, mandate its use to ensure she hits a minimum weekly call threshold. Pair her with Laura to rewrite their standard US outbound emails.",
    "Aiko": "**The Situation:** She provides steady, low-risk upside in non-core markets. Under Ben's hybrid leadership, she has successfully grown her call volume from the 80/week range up to 150–180+ calls a week. Her connect rates are low (mostly 0–6%), but this is a known systemic issue with bad data in her regions, not a lack of effort.\n\n**Strengths:** Incredibly consistent, reliable, and highly coachable (proven by her steady volume growth).\n\n**Action Item:** Decouple her connect rates from her performance review until the data issue is fixed. Praise her dialing consistency, and work on standardizing the specific email hooks she used in late February that yielded 3–4.2% reply rates.",
    "Max": "**The Situation:** The newest US SDR, just ramping up.\n\n**Strengths:** Blank slate, ready to learn.\n\n**Action Item:** Start on Nooks Day 1. Set expectations that 50 dials for 2 conversations is normal. Email is a supplement, phone is the primary weapon."
}

coaching_plans = {
    "Ben": "1. Celebrate the Nooks Pivot.\n2. List Health Check: Are we burning through accounts too fast?\n3. Knowledge Share: Have him lead a 10-min session on Nooks setup.",
    "Feddy": "1. Solidify the Ben/Feddy Partnership for dialing accountability.\n2. Establish strict daily schedule to stop channel-switching.\n3. US Reality Check: Set expectations on 2-3% connect rates.",
    "Heike": "1. Praise the 'sniper' quality.\n2. Scale the Magic: Can we automate prospect research to add 5 more prospects a day?\n3. Ask her to mentor Jessica on DACH email hooks.",
    "Ilana": "1. Celebrate her superpower conversion rates.\n2. The 'Double Up' Challenge: Commit to doubling daily output for two weeks.\n3. Workflow Audit: Shadow her to build local-language snippets.",
    "Jessica": "1. Validate the TAM drop and praise her consistency.\n2. Brainstorm adjustments to older, high-converting messaging for B2C.\n3. Check if territory parameters need slight widening.",
    "Laura": "1. The Email Intervention: Pause current sequences and rewrite.\n2. Introduce Nooks immediately to lower mental barrier of dialing.\n3. Mandate multi-channel touch for the new self-built account lists.",
    "Lea": "1. Praise her predictability.\n2. Volume Check-In: Ask what is eating up her time to get baseline back up.\n3. Connect Rate Clinic: Have her outline her phone objection handling.",
    "Rozanne": "1. The Missing Month: Set firm boundary on abandoning channels.\n2. Mandate Nooks to ensure minimum weekly call threshold.\n3. Pair with Laura to completely overhaul cold email sequences.",
    "Aiko": "1. Celebrate steady growth and reliability.\n2. Grace on Connect Rates: Decouple from review due to bad region data.\n3. Email Hook Workshop: Standardize what worked in late Feb.",
    "Max": "1. Make clear: Email is a supplement, phone is the primary weapon.\n2. Start on Nooks Day 1 to build the 100+ dial habit.\n3. Set expectations early: 50 dials for 2 conversations is normal."
}

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🦎 Quicklizard Menu")
view = st.sidebar.radio("Go to:", [
    "🏆 Team Overview & Rankings", 
    "🔍 Individual Deep Dive", 
    "🗣️ 1:1 Coaching Advice", 
    "🚀 Special Projects"
])

# --- TIME FILTER LOGIC HELPERS ---
def get_quarter(month_str):
    q1 = ["Jan", "Feb", "Mar"]
    q2 = ["Apr", "May", "Jun"]
    q3 = ["Jul", "Aug", "Sep"]
    q4 = ["Oct", "Nov", "Dec"]
    if month_str in q1: return "Q1"
    if month_str in q2: return "Q2"
    if month_str in q3: return "Q3"
    if month_str in q4: return "Q4"
    return "Q1"

# --- VIEW 1: TEAM OVERVIEW ---
if view == "🏆 Team Overview & Rankings":
    st.header("Team Leaderboard")
    
    time_filter = st.selectbox(
        "Filter Timeframe:",
        ["This Quarter", "This Month", "This Week", "Last 12 Weeks", "All Time"],
        index=0
    )
    
    all_weeks = df['Week'].unique().tolist()
    latest_week = all_weeks[-1]
    latest_month = latest_week.split(" - ")[0]
    latest_quarter = get_quarter(latest_month)
    
    if time_filter == "All Time":
        filtered_df = df
    elif time_filter == "Last 12 Weeks":
        filtered_df = df[df['Week'].isin(all_weeks[-12:])]
    elif time_filter == "This Month":
        filtered_df = df[df['Week'].str.startswith(latest_month)]
    elif time_filter == "This Week":
        filtered_df = df[df['Week'] == latest_week]
    elif time_filter == "This Quarter":
        filtered_df = df[df['Week'].apply(lambda w: get_quarter(w.split(" - ")[0]) == latest_quarter)]

    team_stats = filtered_df.groupby("SDR").agg({
        "Meetings Booked": "sum", 
        "Total Activities": "sum", 
        "Calls Logged": "sum",
        "Emails Sent": "sum"
    }).reset_index().sort_values(by="Meetings Booked", ascending=False)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f"Total Meetings ({time_filter})", team_stats["Meetings Booked"].sum())
    col2.metric("Total Activities", team_stats["Total Activities"].sum())
    col3.metric("Total Calls", team_stats["Calls Logged"].sum())
    col4.metric("Total Emails", team_stats["Emails Sent"].sum())
    st.markdown("---")
    
    st.subheader("Tier Rankings")
    st.markdown("""
    * **🥇 Tier 1: The Pacesetters** (Ben, Lea) - Top producers and anchors of predictability.
    * **🥈 Tier 2: The High-Efficiency Specialists** (Heike, Jessica, Ilana) - Elite conversion and discipline in limited TAMs.
    * **🥉 Tier 3: The Grinders** (Feddy, Aiko) - Surviving tough markets, steadily increasing volume, providing reliable upside.
    * **⚠️ Tier 4: The Execution Bottlenecks** (Rozanne, Laura) - Need strategic resets on messaging and call reluctance.
    """)
    st.markdown("---")
    
    st.subheader(f"SDR Ranking by Meetings Booked ({time_filter})")
    
    styled_df = team_stats.style.background_gradient(subset=["Meetings Booked"], cmap="Greens")\
        .background_gradient(subset=["Total Activities"], cmap="Blues")\
        .background_gradient(subset=["Calls Logged"], cmap="Oranges")\
        .background_gradient(subset=["Emails Sent"], cmap="Purples")
    
    st.dataframe(styled_df, hide_index=True, column_config={
        "SDR": st.column_config.Column("SDR Name", width="large"),
        "Meetings Booked": st.column_config.Column("Meetings", width="small"),
        "Total Activities": st.column_config.Column("Activities", width="small"),
        "Calls Logged": st.column_config.Column("Calls", width="small"),
        "Emails Sent": st.column_config.Column("Emails", width="small"),
    }, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Team-Wide Trends & Strategic Observations")
    st.markdown("""
    * **The Nooks (Power Dialer) Impact:** The introduction of Nooks is a game-changer. Ben used it to aggressively pivot to calling his "creme de la creme" list, which spiked his results. Rozanne proved it works during the early December POC (hitting 304 calls). **Action:** Nooks adoption should be heavily encouraged for reps struggling with call volume (like Laura and Rozanne) to lower the barrier to dialing.
    * **The US Market "Email Black Hole":** Your US team (Laura, Rozanne) is facing near 0% email reply rates across the board. Outbound email in the US requires a complete teardown and rebuild, likely shifting to highly personalized, shorter messaging, or relying much heavier on the phones.
    * **TAM Constraints are Real:** Ben, Heike, and Jessica have all been visibly restricted by their territory limits (D2C vs. B2C limits in specific regions). This requires them to have much higher conversion rates because they simply cannot brute-force high volume without burning their total addressable market (TAM).
    """)

# --- VIEW 2: INDIVIDUAL DEEP DIVE ---
elif view == "🔍 Individual Deep Dive":
    st.header("SDR Data Deep Dive")
    selected_sdr = st.selectbox("Select SDR:", df["SDR"].unique())
    sdr_data = df[df["SDR"] == selected_sdr]
    
    st.markdown("### 👤 SDR Analytics & Action Plan")
    st.info(sdr_analytics.get(selected_sdr, "No detailed analytics available."))
    st.markdown("---")
    
    st.subheader(f"Recent Trends for {selected_sdr}")
    
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.plotly_chart(px.line(sdr_data, x="Week", y="Total Activities", title="Total Activities 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)
    with row1_col2:
        st.plotly_chart(px.bar(sdr_data, x="Week", y="Meetings Booked", title="Outbound Meetings 🦎", labels={"Meetings Booked": "Outbound Meetings"}, color_discrete_sequence=[ql_green]), use_container_width=True)
        
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.plotly_chart(px.line(sdr_data, x="Week", y="Calls Logged", title="Calls Logged 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)
    with row2_col2:
        st.plotly_chart(px.line(sdr_data, x="Week", y="Connect %", title="Connected Calls % 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)

    row3_col1, row3_col2 = st.columns(2)
    with row3_col1:
        st.plotly_chart(px.line(sdr_data, x="Week", y="Emails Sent", title="Emails Sent 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)
    with row3_col2:
        st.plotly_chart(px.line(sdr_data, x="Week", y="Reply %", title="Reply % 🦎", markers=True, color_discrete_sequence=[ql_green]), use_container_width=True)

# --- VIEW 3: 1:1 COACHING ADVICE ---
elif view == "🗣️ 1:1 Coaching Advice":
    st.header("1:1 Coaching Agendas")
    selected_sdr_coach = st.selectbox("Select SDR for 1:1 Prep:", list(coaching_plans.keys()))
    st.subheader(f"Action Plan for {selected_sdr_coach}")
    st.write(coaching_plans[selected_sdr_coach])

# --- VIEW 4: SPECIAL PROJECTS ---
elif view == "🚀 Special Projects":
    st.header("Strategic Initiatives")
    project = st.selectbox("Select Project:", ["Preparing Max (New US SDR)", "The 'Ben Effect' (Leadership)", "The US 'Bad Lists' Excuse"])
    
    if project == "Preparing Max (New US SDR)":
        st.markdown("""
        ### Onboarding Max to the US Market
        * **Email is a Supplement:** Do not let him hide behind email. US reply rates are too low.
        * **Nooks on Day 1:** Get him comfortable with 100+ dials immediately to prevent call reluctance.
        * **Expectation Setting:** Making 50 dials to get 2 conversations is normal. He must know this so he doesn't get discouraged.
        * **Consistency:** Establish a rigid schedule (e.g., 9-11 AM Nooks block, 1-2 PM personalized emails) to prevent erratic channel hopping.
        """)
    elif project == "The 'Ben Effect' (Leadership)":
        st.markdown("""
        ### Tracking Ben's Leadership Impact
        * **The Data:** Aiko's calls jumped from ~80/week to 150-180+/week. Feddy's calls spiked to 245+ in Feb. Both happened when Ben took over as hybrid lead.
        * **Action:** Explicitly praise Ben's leadership in his 1:1. He is successfully driving volume.
        * **Next Steps:** Solidify the Ben/Feddy partnership to ensure Feddy actually calls his newly built account lists.
        """)
    elif project == "The US 'Bad Lists' Excuse":
        st.markdown("""
        ### Debunking the Account List Excuse (Laura & Rozanne)
        * **The Reality:** Data shows their fundamental execution bottlenecks (0% reply rates, low volume) existed in October, *before* they received the "bad" lists in November.
        * **The Drop-Off:** Performance plummeted in Dec/Jan due to holiday breaks, 0-call weeks, and war-related mental toll—not the territory split.
        * **The Solution:** Letting them build their own lists was the right move. It removes the excuse. Now, we track if engagement improves on accounts *they* hand-picked.
        """)