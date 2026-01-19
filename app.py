import streamlit as st
import google.generativeai as genai
import os
import datetime

# 1. Configure the Page
st.set_page_config(page_title="Any Budget Ai", page_icon="🖨️", layout="wide")

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
    st.markdown("[🔙 Return to anybudget.com](https://www.anybudget.com)")  # <-- Add this line here
    st.title("💡 Any Budget Tools")
    st.write("Choose your assistant:")
    
    # Kept the fix for the red text warning
    mode = st.radio(
        "Select Tool",
        ["Print Expert (Chat)", "Marketing Copywriter ✍️", "Print School 🎓", "Idea Generator 💡"],
        index=0,
        label_visibility="collapsed"
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

# ==========================================
# DEFINE MODES (Text Only - Super Stable)
# ==========================================

if mode == "Print Expert (Chat)":
    page_title = "Any Budget Ai Assistant 💬"
    system_instruction = f"""
    You are the Any Budget AI Assistant. Today is {today}.
    
    YOUR RULES:
    - Acceptable formats: PDF, PNG, TIF, JPG, AI, PSD.
    - Bleeds: 0.0625 inches required on all sides.
    - Resolution: 300 DPI minimum.
    - Full Color Postcards start as low as $35.00 plus tax, minimum order is 25 
    - Full Color Flyers and Brochures start as low as $35.00 plus tax, minimum order is 25
    - Full Color Standard Business Cards start as low as $45.00 plus tax, minimum order is 100
    - Full Color Same-Day Business Cards start as low as $35.00 plus tax, minimum order is 25
    - Full Color Banners start as low as $24.99 plus tax for one.
    - Full Color Suede Business Cards start as low as $69.33 plus tax, minimum order is 100
    - Full Color Silk Business Cards start as low as $38.22 plus tax, minimum order is 25
    - Postcard sizes available are 4x6, 5x7, 5.5x8.5, 6x11, 4.25x5.5 and more
    - Flyers and brochures most common sizes are 8.5x11, 8.5x14 and 11x17 and more
    - Place your orders at [anybudget.com](https://www.anybudget.com)
    
    For other topics (history, science, etc.), answer freely and helpfully.
    """
    initial_msg = "Hello! Ask me about file specs, bleeds, or general questions."

elif mode == "Marketing Copywriter ✍️":
    page_title = "Marketing Copywriter ✍️"
    system_instruction = """
    You are an expert Marketing Copywriter for Any Budget Printing.
    Your goal is to write CATCHY, PERSUASIVE, and PROFESSIONAL text.
    - If user asks for a headline, give 3 punchy options.
    - If user asks for flyer text, organize it with headers and bullet points.
    - Keep it short enough for physical print.
    """
    initial_msg = "What are we writing today? (e.g., 'Headline for a pizza sale')"

elif mode == "Print School 🎓":
    page_title = "Print School 🎓"
    system_instruction = """
    You are a friendly Printing Tutor. 
    Explain complex printing terms (CMYK, GSM, Vector vs Raster, Bleed) in simple, easy-to-understand language.
    Use analogies (e.g., "Resolution is like the thread count in sheets").
    """
    initial_msg = "Class is in session! What printing term confuses you?"

elif mode == "Idea Generator 💡":
    page_title = "Idea Generator 💡"
    system_instruction = """
    You are a Business Growth Consultant for Any Budget.
    When a user tells you their business type, suggest 3-5 specific printed products they need to grow.
    Explain WHY they need them.
    """
    initial_msg = "What kind of business do you have? (e.g., 'Coffee Shop', 'Real Estate')"

# ==========================================
# CHAT INTERFACE
# ==========================================
st.title(page_title)

# Initialize the Model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=system_instruction
)

# Chat History Setup
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "model", "parts": initial_msg}]

# Display Chat
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["parts"])

# Handle Input
if prompt := st.chat_input("Type here..."):
    # User message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": prompt})

    # AI message
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
                st.error(f"Error: {e}")
