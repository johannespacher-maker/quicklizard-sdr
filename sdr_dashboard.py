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

# --- HEATMAP MOCK DATA ENGINE ---
@st.cache_data
def load_heatmap_data():
    heatmap_raw = []
    
    def generate_blocks(sdr, timeframe, day, start_h, end_h, size, conn):
        for h in range(start_h, end_h + 1):
            heatmap_raw.append((sdr, timeframe, day, h, size, conn))

    # Aiko 
    generate_blocks("Aiko", "This Quarter", "Mon", 1, 7, 15, 2)
    generate_blocks("Aiko", "This Quarter", "Tue", 1, 8, 15, 5)
    generate_blocks("Aiko", "This Quarter", "Wed", 1, 9, 15, 2)
    generate_blocks("Aiko", "This Quarter", "Thu", 1, 7, 15, 3)
    generate_blocks("Aiko", "This Quarter", "Fri", 3, 8, 20, 2)
    generate_blocks("Aiko", "Last Week", "Mon", 5, 6, 15, 2)
    generate_blocks("Aiko", "Last Week", "Tue", 4, 8, 10, 2)
    generate_blocks("Aiko", "Last Week", "Wed", 5, 7, 15, 2)
    generate_blocks("Aiko", "Last Week", "Thu", 4, 6, 10, 2)
    generate_blocks("Aiko", "Last Week", "Fri", 5, 5, 25, 2)

    # Ben 
    generate_blocks("Ben", "This Quarter", "Mon", 6, 17, 30, 8)
    generate_blocks("Ben", "This Quarter", "Tue", 5, 15, 25, 6)
    generate_blocks("Ben", "This Quarter", "Wed", 5, 17, 30, 7)
    generate_blocks("Ben", "This Quarter", "Thu", 8, 15, 25, 6)
    generate_blocks("Ben", "This Quarter", "Fri", 6, 15, 20, 5)
    generate_blocks("Ben", "Last Week", "Mon", 8, 8, 20, 4)
    generate_blocks("Ben", "Last Week", "Tue", 12, 12, 5, 8)
    generate_blocks("Ben", "Last Week", "Tue", 15, 15, 30, 4)
    generate_blocks("Ben", "Last Week", "Wed", 7, 7, 25, 3)
    generate_blocks("Ben", "Last Week", "Wed", 14, 14, 5, 2)
    generate_blocks("Ben", "Last Week", "Fri", 10, 11, 25, 4)

    # Feddy 
    generate_blocks("Feddy", "This Quarter", "Mon", 14, 21, 20, 3)
    generate_blocks("Feddy", "This Quarter", "Tue", 14, 21, 25, 2)
    generate_blocks("Feddy", "This Quarter", "Wed", 19, 22, 20, 4)
    generate_blocks("Feddy", "This Quarter", "Thu", 14, 23, 20, 3)
    generate_blocks("Feddy", "Last Week", "Mon", 19, 19, 25, 3)
    generate_blocks("Feddy", "Last Week", "Tue", 21, 21, 20, 3)
    generate_blocks("Feddy", "Last Week", "Wed", 20, 20, 25, 3)
    generate_blocks("Feddy", "Last Week", "Thu", 23, 23, 20, 3)

    # Heike 
    generate_blocks("Heike", "This Quarter", "Mon", 8, 16, 20, 5)
    generate_blocks("Heike", "This Quarter", "Tue", 8, 15, 25, 6)
    generate_blocks("Heike", "This Quarter", "Wed", 8, 16, 25, 6)
    generate_blocks("Heike", "This Quarter", "Thu", 7, 16, 20, 5)
    generate_blocks("Heike", "This Quarter", "Fri", 7, 15, 25, 6)
    generate_blocks("Heike", "Last Week", "Mon", 8, 13, 15, 4)
    generate_blocks("Heike", "Last Week", "Tue", 9, 9, 25, 6)
    generate_blocks("Heike", "Last Week", "Wed", 9, 12, 20, 4)
    generate_blocks("Heike", "Last Week", "Thu", 8, 12, 15, 5)
    generate_blocks("Heike", "Last Week", "Fri", 8, 13, 30, 3)

    # Ilana 
    generate_blocks("Ilana", "This Quarter", "Mon", 8, 12, 25, 12)
    generate_blocks("Ilana", "This Quarter", "Tue", 9, 15, 25, 10)
    generate_blocks("Ilana", "This Quarter", "Wed", 9, 16, 25, 11)
    generate_blocks("Ilana", "This Quarter", "Thu", 9, 15, 20, 9)
    generate_blocks("Ilana", "This Quarter", "Fri", 11, 11, 15, 4)
    generate_blocks("Ilana", "Last Week", "Wed", 11, 12, 25, 4)

    # Jessica 
    generate_blocks("Jessica", "This Quarter", "Mon", 10, 17, 25, 7)
    generate_blocks("Jessica", "This Quarter", "Tue", 9, 15, 30, 6)
    generate_blocks("Jessica", "This Quarter", "Wed", 9, 17, 25, 7)
    generate_blocks("Jessica", "This Quarter", "Thu", 10, 15, 25, 6)
    generate_blocks("Jessica", "This Quarter", "Fri", 8, 15, 20, 6)
    generate_blocks("Jessica", "Last Week", "Mon", 10, 14, 25, 7)
    generate_blocks("Jessica", "Last Week", "Tue", 10, 13, 30, 4)
    generate_blocks("Jessica", "Last Week", "Wed", 10, 10, 25, 8)
    generate_blocks("Jessica", "Last Week", "Thu", 13, 14, 30, 9)
    generate_blocks("Jessica", "Last Week", "Fri", 11, 14, 20, 4)

    # Laura 
    generate_blocks("Laura", "This Quarter", "Mon", 17, 18, 15, 2)
    generate_blocks("Laura", "This Quarter", "Tue", 0, 0, 15, 2)
    generate_blocks("Laura", "This Quarter", "Wed", 14, 14, 10, 2)
    generate_blocks("Laura", "This Quarter", "Thu", 14, 16, 15, 3)
    generate_blocks("Laura", "This Quarter", "Fri", 17, 23, 20, 4)
    generate_blocks("Laura", "This Quarter", "Sat", 0, 0, 10, 2)
    generate_blocks("Laura", "Last Week", "Tue", 19, 20, 25, 4)
    generate_blocks("Laura", "Last Week", "Thu", 16, 21, 20, 5)
    generate_blocks("Laura", "Last Week", "Fri", 19, 19, 15, 3)

    # Lea 
    generate_blocks("Lea", "This Quarter", "Mon", 9, 17, 25, 8)
    generate_blocks("Lea", "This Quarter", "Tue", 9, 17, 25, 7)
    generate_blocks("Lea", "This Quarter", "Wed", 9, 17, 20, 7)
    generate_blocks("Lea", "This Quarter", "Thu", 10, 18, 20, 6)
    generate_blocks("Lea", "This Quarter", "Fri", 11, 16, 15, 5)
    generate_blocks("Lea", "Last Week", "Mon", 10, 17, 20, 4)
    generate_blocks("Lea", "Last Week", "Tue", 11, 11, 15, 3)
    generate_blocks("Lea", "Last Week", "Wed", 12, 17, 15, 5)
    generate_blocks("Lea", "Last Week", "Thu", 11, 16, 30, 6)
    generate_blocks("Lea", "Last Week", "Fri", 11, 11, 20, 4)

    # Max (First week, identical QTR/Week data)
    for timeframe in ["This Quarter", "Last Week"]:
        generate_blocks("Max", timeframe, "Tue", 19, 19, 25, 3)
        generate_blocks("Max", timeframe, "Wed", 14, 21, 15, 3)
        generate_blocks("Max", timeframe, "Thu", 19, 19, 30, 3)
        generate_blocks("Max", timeframe, "Fri", 18, 18, 25, 3)

    # Rozanne 
    generate_blocks("Rozanne", "This Quarter", "Tue", 16, 18, 25, 5)
    generate_blocks("Rozanne", "This Quarter", "Tue", 22, 23, 15, 8)
    generate_blocks("Rozanne", "This Quarter", "Wed", 11, 11, 15, 3)
    generate_blocks("Rozanne", "This Quarter", "Wed", 16, 23, 20, 6)
    generate_blocks("Rozanne", "This Quarter", "Thu", 0, 0, 10, 7)
    generate_blocks("Rozanne", "This Quarter", "Thu", 14, 23, 20, 5)
    generate_blocks("Rozanne", "Last Week", "Thu", 14, 14, 15, 3)
    generate_blocks("Rozanne", "Last Week", "Thu", 21, 21, 25, 3)
    generate_blocks("Rozanne", "Last Week", "Thu", 23, 23, 30, 5)

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
    "Ben": "**The Situation:** Ben ran out of runway on emails due to his D2C TAM limits, but brilliantly pivoted to Nooks to aggressively call his best prospects. This led to a massive connect rate.\n\n**Strengths:** Highly adaptable, proven closer, unmatched activity volume.\n\n**Timing Insight:** Dominates the EU/UK hours (6 AM to 3 PM IST). His extreme volume during peak business hours yields incredible connects.\n\n**Action Item:** Ensure he has enough fresh, verified data to sustain his high call volume so he doesn't burn through his 'creme de la creme' list too quickly.",
    "Feddy": "**The Situation:** Battling the US market with Nooks. High activity, but very low connect rates.\n\n**Strengths:** Hustle and persistence in a brutal market.\n\n**Timing Insight:** Calling the US heavily from 2 PM to 10 PM IST. We need to review if these late evening IST blocks are yielding quality connections or just voicemails.\n\n**Action Item:** Dissect his Jan Week 3 outbound spike. Help him build a consistent, daily multi-channel cadence now that conference disruptions are over.",
    "Heike": "**The Situation:** Operating with a very limited TAM, she plays the 'sniper.' Her engagement rates are elite.\n\n**Strengths:** World-class personalization and DACH market mastery.\n\n**Timing Insight:** Classic DACH hours. Highly effective early mornings (7 AM - 11 AM IST). Keep her focused on these prime windows.\n\n**Action Item:** Do not force her to do mindless volume, as it will ruin her TAM. Instead, ask her to template her most successful hooks and share them.",
    "Ilana": "**The Situation:** Achieving absurdly high conversion metrics, but her volume is critically low (often under 50 calls a week).\n\n**Strengths:** Elite local engagement. When she touches an account, she converts it.\n\n**Timing Insight:** Her historical heatmaps are beautiful (8 AM - 4 PM), but her 'Last Week' heatmap is practically empty. She has stopped dialing.\n\n**Action Item:** Focus 100% on workflow optimization. Enforce a daily 8 AM - 4 PM block consistency to get her volume up. If she doubles volume, she is the top rep.",
    "Jessica": "**The Situation:** She was a volume machine until her territory was reduced to B2C. Volume naturally halved, but she remained consistent.\n\n**Strengths:** True discipline. Maintained a multi-channel approach despite frustrating drops in meetings.\n\n**Timing Insight:** Incredibly consistent. Dials solidly between 8 AM and 5 PM IST every single day without fail.\n\n**Action Item:** Validate her consistency. Facilitate a strategy session with Heike to adapt DACH hooks for B2C.",
    "Laura": "**The Situation:** Slogged through the US market. Dislikes making calls and defaults to email, but her email reply rate is essentially 0%.\n\n**Strengths:** Willing to put in high overall activity volume (600+ touches/week).\n\n**Timing Insight:** Her dialing times are erratic (some midnight calls, scattered late afternoons). She needs structured US blocks rather than dialing sporadically when she feels like it.\n\n**Action Item:** Rewrite her US email sequences entirely. Use Nooks to lower the mental barrier of dialing and enforce strict 6 PM - 10 PM IST power hours.",
    "Lea": "**The Situation:** A true 'Steady Eddy.' Books 1-2 meetings almost every week with excellent connect rates.\n\n**Strengths:** Reliability and great phone presence.\n\n**Timing Insight:** Very steady UK/Nordics calling rhythm between 9 AM and 6 PM IST. \n\n**Action Item:** Find out what caused her total activity volume to dip into the 100-300 range recently compared to her 500+ baseline in November.",
    "Rozanne": "**The Situation:** Proved she can use Nooks (300+ calls in Dec), but has a serious red flag: 4 historical weeks of 0 calls.\n\n**Strengths:** Capable of high volume, excellent at event follow-up.\n\n**Timing Insight:** US market. Heavily skewed to late evening IST (4 PM - 11 PM), with some odd midnight spikes. Needs structure to prevent burnout and channel abandoning.\n\n**Action Item:** Address the 0-call months. Mandate Nooks to ensure she hits a minimum weekly call threshold and keep her within reasonable US timezone blocks.",
    "Aiko": "**The Situation:** Provides steady, low-risk upside in non-core markets. Successfully growing call volume under hybrid leadership.\n\n**Strengths:** Incredibly consistent, reliable, and highly coachable.\n\n**Timing Insight:** Connects best Tuesday 1-2 AM and Wednesday 8 AM (IST). Focus her efforts on these highly specific, converting windows.\n\n**Action Item:** Decouple her connect rates from her review until the bad data issue in her region is fixed. Implement the iOS Screener Playbook.",
    "Max": "**The Situation:** The newest US SDR, just ramping up.\n\n**Strengths:** Blank slate, ready to learn. Logged 560 activities in his first week.\n\n**Timing Insight:** Calling heavily between 2 PM and 9 PM IST. Excellent baseline schedule for the US market.\n\n**Action Item:** Start on Nooks Day 1. Set expectations that 50 dials for 2 conversations is normal. Email is a supplement, phone is the primary weapon."
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

    # --- HEATMAP VISUALIZATION ---
    st.markdown("---")
    st.subheader("⏱️ Optimal Calling Windows")
    
    sdr_heatmap_data = df_heat[df_heat["SDR"] == selected_sdr].copy()
    
    if not sdr_heatmap_data.empty:
        # Timezone Selector
        tz_col, _ = st.columns([1, 2])
        with tz_col:
            timezones = {
                "Israel Time (IST) - Default": 0,
                "Central Europe (CET)": -1,
                "UK Time (GMT)": -2,
                "US Eastern Time (EST)": -7,
                "US Pacific Time (PST)": -10,
                "Singapore Time (SGT)": 6,
                "Australian Eastern (AEST)": 8
            }
            selected_tz = st.selectbox("Select Timezone:", list(timezones.keys()))
            tz_offset = timezones[selected_tz]

        # Apply the timezone shift if they changed it
        if tz_offset != 0:
            sdr_heatmap_data[["Day", "Hour"]] = sdr_heatmap_data.apply(lambda r: shift_timezone(r, tz_offset), axis=1)

        heat_col1, heat_col2 = st.columns(2)
        
        # Custom Quicklizard Green color palette
        ql_greens = ["#a1d9b3", "#27ae60", "#0b4a24"] 
        all_days = ["Sun", "Sat", "Fri", "Thu", "Wed", "Tue", "Mon"] 
        
        # Quarter Heatmap
        q_data = sdr_heatmap_data[sdr_heatmap_data["Timeframe"] == "This Quarter"]
        if not q_data.empty:
            fig_q = px.scatter(
                q_data, x="Hour", y="Day", size="Calls", color="Connect %", 
                color_continuous_scale=ql_greens, title=f"This Quarter ({selected_tz.split(' ')[0]})",
                category_orders={"Day": all_days}
            )
            fig_q.update_xaxes(tickvals=list(range(24)), ticktext=[f"{h%12 if h%12!=0 else 12} {'AM' if h<12 else 'PM'}" for h in range(24)], range=[-1, 24])
            heat_col1.plotly_chart(fig_q, use_container_width=True)
            
        # Week Heatmap
        w_data = sdr_heatmap_data[sdr_heatmap_data["Timeframe"] == "Last Week"]
        if not w_data.empty:
            fig_w = px.scatter(
                w_data, x="Hour", y="Day", size="Calls", color="Connect %", 
                color_continuous_scale=ql_greens, title=f"Last Week ({selected_tz.split(' ')[0]})",
                category_orders={"Day": all_days}
            )
            fig_w.update_xaxes(tickvals=list(range(24)), ticktext=[f"{h%12 if h%12!=0 else 12} {'AM' if h<12 else 'PM'}" for h in range(24)], range=[-1, 24])
            heat_col2.plotly_chart(fig_w, use_container_width=True)
    else:
        st.info("No time-mapping data available for this SDR yet.")

# --- VIEW 3: 1:1 COACHING ADVICE ---
elif view == "🗣️ 1:1 Coaching Advice":
    st.header("1:1 Coaching Agendas")
    selected_sdr_coach = st.selectbox("Select SDR for 1:1 Prep:", list(coaching_plans.keys()))
    st.subheader(f"Action Plan for {selected_sdr_coach}")
    st.write(coaching_plans[selected_sdr_coach])

# --- VIEW 4: SPECIAL PROJECTS ---
elif view == "🚀 Special Projects":
    st.header("Strategic Initiatives & Focus Areas")
    project = st.selectbox("Select Project:", [
        "Issues to fix",
        "The iPhone Screener Bypass Playbook",
        "Preparing Max (New US SDR)", 
        "The 'Ben Effect' (Leadership)", 
        "The US 'Bad Lists' Excuse"
    ])
    
    if project == "Issues to fix":
        st.markdown("""
        ### 1. The "Activity Illusion" (Laura vs. Ben)
        High activity does not equal high output on this team. 
        * **Laura:** 12,504 all-time activities, but only 8 meetings.
        * **Ben:** 12,553 all-time activities, but has 44 meetings.
        * **The Why:** Laura is hiding behind email in the US market, and her reply rate is a flat 0.0% for almost the entire 5 months. Ben is heavily leveraging the phones. 
        * **The Fix:** This proves that in your current markets, blind email volume without phone execution is completely dead. We need to reset Laura's workflow to prioritize calls.
        
        ---
        
        ### 2. The Conversion vs. Volume Tragedy (Ilana vs. Feddy)
        A massive mismatch between who has the talent and who is doing the work.
        * **Ilana:** Has absolutely elite conversion skills (connect rates routinely hit 17%, 25%, and 33%, with the best reply rates on the team). But her call volume is almost non-existent (often under 45 calls *a week*). Because she isn't dialing, she only has 3 meetings this quarter.
        * **Feddy:** Grinding in the brutal US market with terrible connect rates (1% to 3%). But because he uses Nooks to push his call volume up into the 200–300+ range, he managed to grind out 7 meetings this quarter.
        * **The Fix:** If you can get Ilana to adopt Feddy's work ethic, or if you can give Feddy Ilana's European market lists, your pipeline would explode.

        ---

        ### 3. The "Key Person" Risk
        Ben is completely carrying the team.
        * **The Risk:** With 44 all-time meetings, he has booked nearly double the next highest rep (Jessica, with 23). If Ben takes a two-week vacation, or if his "creme de la creme" account list runs dry, the entire team's target is in serious jeopardy.
        * **The Fix:** You desperately need to clone Ben's Nooks/Dialer framework and force the bottom half of the leaderboard to adopt it.
        """)
    elif project == "The iPhone Screener Bypass Playbook":
        st.markdown("""
        ### 📱 Bypassing the iOS 17 Call Screeners
        With recent iOS updates, Apple introduced two massive hurdles for outbound sales: **"Silence Unknown Callers"** and **"Live Voicemail"**. Here is the playbook to bypass them:

        **1. The "Live Voicemail" Hack (Optimize for the Transcript)**
        Because iOS 17 users see a live text transcript of your voicemail on their screen in real-time, they use it to decide if they should pick up the call mid-ring.
        * **The Fix:** The split second the voicemail records, drop a hyper-relevant hook. *"Hey John, looking at your Q2 pricing strategy and noticed..."* -> The prospect reads their name and a relevant business problem on their screen and presses the green "Accept Call" button.

        **2. The Siri Signature Trick**
        Apple's "Silence Unknown Callers" blocks numbers it doesn't recognize. However, Siri actually scans a user's Apple Mail app for phone numbers.
        * **The Fix:** Ensure the exact phone number the SDR is dialing from (their Nooks/outbound number) is in their email signature. If they email on Tuesday and call on Thursday, Siri will often bypass the blocker and display **"Maybe: [SDR Name]"** on caller ID instead of "Unknown."

        **3. The "Double Dial" (Use Wisely)**
        Most iPhones have a default "Do Not Disturb" setting called "Repeated Calls." If the same number calls back within 3 minutes, the iPhone pushes the second call through loud and clear.
        * **The Fix:** Double-dial absolute top-tier prospects. Call once, let it go to voicemail (don't leave one), hang up, and immediately call right back. *(Note: Only do this for highly researched, Tier 1 accounts).*

        **4. The "Pre-Call Bump"**
        Combine channels to warm up the number.
        * **The Fix:** Send a LinkedIn voice note or an email 10 minutes before a call block: *"Hey Sarah, going to give you a quick ring from a +61 number in a few minutes regarding [X]. Feel free to screen me if you're busy!"* It disarms the prospect and makes them look at their phone when the unknown number pops up.
        """)
    elif project == "Preparing Max (New US SDR)":
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