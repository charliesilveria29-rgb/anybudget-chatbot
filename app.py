import streamlit as st
import google.generativeai as genai
import os
import datetime

# 1. Configure the Page
st.set_page_config(page_title="AnyBudget AI Suite", page_icon="🖨️", layout="wide")

# 2. Connect to the Brain (Gemini)
api_key = os.environ.get("GOOGLE_API_KEY") 
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.info("Please add your GOOGLE_API_KEY to the secrets to continue.")
        st.stop()

genai.configure(api_key=api_key)

# 3. Dynamic Date
today = datetime.date.today()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🖨️ AnyBudget Tools")
    st.write("Choose your assistant:")
    
    # The "Gemini Style" Buttons
    mode = st.radio(
        "",
        ["Print Expert (Chat)", "Marketing Copywriter ✍️", "Print School 🎓", "Idea Generator 💡"],
        index=0
    )
    
    st.markdown("---")
    st.caption(f"Powered by Gemini 2.5 • {today.year}")

# --- APP LOGIC ---

# DEFAULT: Clear history if the user switches modes
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode

if st.session_state.current_mode != mode:
    st.session_state.messages = []
    st.session_state.current_mode = mode

# ==========================================
# DEFINING THE PERSONAS
# ==========================================
if mode == "Print Expert (Chat)":
    st.title("AnyBudget Assistant 💬")
    st.write("I can help with file specs, bleeds, and turnaround times.")
    
    system_instruction = f"""
    You are the AnyBudget AI Assistant. Today is {today}.
    
    YOUR RULES:
    - Acceptable formats: PDF, AI, PSD, JPG.
    - Bleeds: 0.125 inches required.
    - Resolution: 300 DPI.
    
    For other topics (history, science), answer freely and helpfully.
    """
    initial_msg = "Hello! Ask me about file specs, bleeds, or general questions."

elif mode == "Marketing Copywriter ✍️":
    st.title("Marketing Copywriter ✍️")
    st.write("Stuck on what to say? I'll write your headlines, flyers, and card text.")
    
    system_instruction = f"""
    You are an expert Marketing Copywriter for AnyBudget Printing.
    Your goal is to write CATCHY, PERSUASIVE, and PROFESSIONAL text.
    - If user asks for a headline, give 3 punchy options.
    - If user asks for flyer text, organize it with headers and bullet points.
    - Keep it short enough for print.
    """
    initial_msg = "What are we writing today? (e.g., 'Headline for a pizza sale')"

elif mode == "Print School 🎓":
    st.title("Print School 🎓")
    st.write("Confused by paper types or coatings? Ask me!")
    
    system_instruction = f"""
    You are a friendly Printing Tutor. 
    Explain complex printing terms (CMYK, GSM, Bleed) in simple language.
    """
    initial_msg = "Class is in session! What term confuses you?"

elif mode == "Idea Generator 💡":
    st.title("Idea Generator 💡")
    st.write("Tell me your business, and I'll suggest what you should print.")
    
    system_instruction = f"""
    You are a Business Growth Consultant.
    Suggest 3-5 specific printed products for the user's business type.
    """
    initial_msg = "What kind of business do you have?"

# --- SHARED CHAT LOGIC ---
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=system_instruction
)

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "model", "parts": initial_msg}]

for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["parts"])

if prompt := st.chat_input("Type here..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": prompt})

    # Show AI message with Spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["parts"]]} for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "parts": response.text})
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
