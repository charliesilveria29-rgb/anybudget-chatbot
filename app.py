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
    
    mode = st.radio(
        "",
        ["Print Expert (Chat)", "Marketing Copywriter ✍️", "Print School 🎓", "Idea Generator 💡"],
        index=0
    )
    
    st.markdown("---")
    st.caption(f"Powered by Gemini 2.5 • {today.year}")

# --- APP LOGIC ---

# Reset history if mode changes
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode

if st.session_state.current_mode != mode:
    st.session_state.messages = []
    st.session_state.current_mode = mode

# Define Prompts based on Mode
if mode == "Print Expert (Chat)":
    page_title = "AnyBudget Assistant 💬"
    page_helper = "Ask me about file specs, bleeds, or general questions."
    system_instruction = f"""
    You are the AnyBudget AI Assistant. Today is {today}.
    YOUR RULES:
    - Acceptable formats: PDF, AI, PSD, JPG.
    - Bleeds: 0.125 inches required.
    - Resolution: 300 DPI.
    For other topics, answer freely and helpfully.
    """
    initial_msg = "Hello! Ask me about file specs, bleeds, or general questions."

elif mode == "Marketing Copywriter ✍️":
    page_title = "Marketing Copywriter ✍️"
    page_helper = "I'll write your headlines, flyers, and card text."
    system_instruction = f"""
    You are an expert Marketing Copywriter for AnyBudget Printing.
    Write CATCHY, PERSUASIVE text.
    - Give 3 headline options if asked.
    - Keep it short enough for print.
    """
    initial_msg = "What are we writing today? (e.g., 'Headline for a pizza sale')"

elif mode == "Print School 🎓":
    page_title = "Print School 🎓"
    page_helper = "Confused by paper types? Ask me!"
    system_instruction = f"""
    You are a friendly Printing Tutor. 
    Explain complex printing terms (CMYK, GSM, Bleed) in simple language.
    """
    initial_msg = "Class is in session! What term confuses you?"

elif mode == "Idea Generator 💡":
    page_title = "Idea Generator 💡"
    page_helper = "Tell me your business, and I'll suggest products."
    system_instruction = f"""
    You are a Business Growth Consultant.
    Suggest 3-5 specific printed products for the user's business type.
    """
    initial_msg = "What kind of business do you have?"

# --- SHARED GEMINI LOGIC ---
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=system_instruction
)

# Initialize Chat History
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "model", "parts": initial_msg}]

# --- HELPER FUNCTION: Handle the Chat Response ---
def handle_response(user_input):
    # Add user message
    st.session_state.messages.append({"role": "user", "parts": user_input})
    
    # Generate response
    try:
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["parts"]]} for m in st.session_state.messages[:-1]
        ])
        response = chat.send_message(user_input)
        st.session_state.messages.append({"role": "model", "parts": response.text})
    except Exception as e:
        st.error(f"Error: {e}")

# ==========================================
# THE LAYOUT LOGIC (Center vs Bottom)
# ==========================================

# CHECK: Is this the start of the chat? (Only 1 message = the greeting)
if len(st.session_state.messages) == 1:
    # --- PHASE 1: CENTERED "HERO" VIEW ---
    
    # Add some spacer to push it down
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    # Center the Title and Helper Text
    st.markdown(f"<h1 style='text-align: center;'>{page_title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{page_helper}</p>", unsafe_allow_html=True)
    
    # Create 3 columns to center the input box nicely
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # The "Start" Input
        start_input = st.text_input(" ", placeholder="Type here to start...", label_visibility="collapsed")
        
        if start_input:
            # If user types here, handle it and RERUN the app to switch views
            handle_response(start_input)
            st.rerun()

else:
    # --- PHASE 2: STANDARD CHAT VIEW ---
    st.title(page_title)
    
    # Display Chat History
    for message in st.session_state.messages:
        role = "user" if message["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message["parts"])

    # Bottom Input Bar
    if prompt := st.chat_input("Type here..."):
        handle_response(prompt)
        st.rerun()
