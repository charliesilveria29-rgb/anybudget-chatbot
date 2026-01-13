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
    
    # We added 'label_visibility="collapsed"' to hide the name but keep the code happy (fixes red warning)
    mode = st.radio(
        "Select Tool",
        ["Print Expert (Chat)", "Image Generator 🎨", "Marketing Copywriter ✍️", "Print School 🎓", "Idea Generator 💡"],
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
# 1. IMAGE GENERATOR 🎨
# ==========================================
if mode == "Image Generator 🎨":
    st.title("Art Studio 🎨")
    st.write("Generate images for your flyers or business cards.")
    
    img_prompt = st.text_area("Describe the image you want:", height=100, placeholder="A modern coffee shop logo with a cat...")
    
    if st.button("Generate Image ✨"):
        if not img_prompt:
            st.warning("Please describe an image first!")
        else:
            with st.spinner("Painting..."):
                try:
                    # Using the standard Imagen model (best for paid/billing accounts)
                    img_model = genai.GenerativeModel("imagen-3.0-generate-001")
                    response = img_model.generate_content(img_prompt)
                    
                    if response.parts:
                        # This line requires google-generativeai>=0.8.3
                        st.image(response.parts[0].image, caption=img_prompt, use_column_width=True)
                    else:
                        st.error("Blocked by safety filters. Try a different prompt.")
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Tip: If you see 'Unknown field: image', please Reboot the app to update libraries.")
    
    # Stop the script here so the chat bar doesn't appear
    st.stop()

# ==========================================
# 2. TEXT ASSISTANTS (Shared Logic)
# ==========================================

# Define Personas based on Mode
if mode == "Print Expert (Chat)":
    page_title = "AnyBudget Assistant 💬"
    system_instruction = f"""
    You are the AnyBudget AI Assistant. Today is {today}.
    RULES:
    - Acceptable formats: PDF, AI, PSD, JPG.
    - Bleeds: 0.125 inches required.
    - Resolution: 300 DPI.
    For other topics, answer freely.
    """
    initial_msg = "Hello! Ask me about file specs, bleeds, or general questions."

elif mode == "Marketing Copywriter ✍️":
    page_title = "Marketing Copywriter ✍️"
    system_instruction = """
    You are an expert Copywriter for AnyBudget Printing.
    Write CATCHY, PERSUASIVE text for flyers, cards, and brochures.
    """
    initial_msg = "What are we writing today? (e.g., 'Headline for a sale')"

elif mode == "Print School 🎓":
    page_title = "Print School 🎓"
    system_instruction = """
    You are a friendly Printing Tutor. 
    Explain terms like CMYK, GSM, and Bleed simply.
    """
    initial_msg = "Class is in session! What term confuses you?"

elif mode == "Idea Generator 💡":
    page_title = "Idea Generator 💡"
    system_instruction = """
    You are a Business Growth Consultant.
    Suggest 3-5 printed products for the user's business.
    """
    initial_msg = "What kind of business do you have?"

# --- CHAT INTERFACE ---
st.title(page_title)

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
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": prompt})

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
