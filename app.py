import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    # --- HIDE STREAMLIT STYLE ---
st.markdown("""
    <style>
    /* This hides the "Hamburger" menu (the three lines) */
    #MainMenu {visibility: hidden;}
    /* This hides the "Made with Streamlit" footer */
    footer {visibility: hidden;}
    /* This hides the top header bar completely */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    page_title="Job Scam Detector",
    page_icon="🛡️",
    layout="centered"
)

# --- YMCA RED STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    div.stButton > button:first-child {
        background-color: #ED1C24;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        width: 100%;
        padding: 15px 0;
    }
    div.stButton > button:first-child:hover { background-color: #c41219; color: white; }
    h1 { color: #ED1C24; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- API SETUP ---
# This looks for the key in the cloud's secure vault
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API Key missing. Please set it in Streamlit Secrets.")

def analyze_job_text(text):
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = f"""
    You are a cybersecurity expert. Analyze this job text for scams.
    Text: "{text}"
    If safe, start with "SAFE". If suspicious, start with "SUSPICIOUS".
    Provide 3 bullet points explaining why. Keep it simple for youth.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Error connecting to AI."

# --- UI ---
st.title("🛡️ Job Scam Detector")
st.write("Paste a job description or email below to check if it's safe.")

user_input = st.text_area("Paste text here:", height=200)

if st.button("CHECK SAFETY"):
    if not user_input:
        st.warning("Please paste some text first.")
    else:
        with st.spinner("Analyzing..."):
            result = analyze_job_text(user_input)
            if "SUSPICIOUS" in result:
                st.error("🔴 CAUTION: SCAM DETECTED")
                st.write(result.replace("SUSPICIOUS", ""))
            elif "SAFE" in result:
                st.success("🟢 LOOKS STANDARD")
                st.write(result.replace("SAFE", ""))
            else:
                st.write(result)
