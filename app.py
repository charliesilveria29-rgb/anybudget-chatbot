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
        ["Print Expert (Chat)", "Image Generator 🎨", "Marketing Copywriter ✍️", "Print School 🎓", "Idea Generator 💡"],
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

# ==========================================
# 1. PRINT EXPERT (Chat)
# ==========================================
if mode == "Print Expert (Chat)":
    st.title("AnyBudget Assistant 💬")
    system_instruction = f"""
    You are the AnyBudget AI Assistant. Today is {today}.
    RULES:
    - Acceptable formats: PDF, AI, PSD, JPG.
    - Bleeds: 0.125 inches.
    - Resolution: 300 DPI.
    For other topics, answer freely.
    """
    initial_msg = "Hello! Ask me about file specs, bleeds, or general questions."

# ==========================================
# 2. IMAGE GENERATOR (Nano Banana Returns!)
# ==========================================
elif mode == "Image Generator 🎨":
    st.title("Art Studio 🎨")
    st.write("Generate images for your flyers or business cards.")
    
    # We don't use the chat loop for this one
    img_prompt = st.text_area("Describe the image you want:", height=100, placeholder="A modern coffee shop logo with a cat...")
    
    if st.button("Generate Image ✨"):
        if not img_prompt:
            st.warning("Please describe an image first!")
        else:
            with st.spinner("Generating..."):
                try:
                    # Using the standard Imagen model (now unlocked for you)
                    img_model = genai.GenerativeModel("imagen-3.0-generate-001")
                    response = img_model.generate_content(img_prompt)
                    
                    if response.parts:
                        st.image(response.parts[0].image, caption=img_prompt, use_column_width=True)
                    else:
                        st.error("Blocked by safety filters.")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Stop the rest of the script so we don't show the chat bar
    st.stop()

# ==========================================
# 3. MARKETING COPYWRITER
# ==========================================
elif mode == "Marketing Copywriter ✍️":
    st.title("Marketing Copywriter ✍️")
    system_instruction = f"""
    You are an expert Copywriter for AnyBudget Printing.
    Write CATCHY, PERSUASIVE text for flyers, cards, and brochures.
    """
    initial_msg = "What are we writing today? (e.g., 'Headline for a sale')"

# ==========================================
# 4. PRINT SCHOOL
# ==========================================
elif mode == "Print School 🎓":
    st.title("Print School 🎓")
    system_instruction = f"""
    You are a friendly Printing Tutor. 
    Explain terms like CMYK, GSM, and Bleed simply.
    """
    initial_msg = "Class is in session! What term confuses you?"

# ==========================================
# 5. IDEA GENERATOR
# ==========================================
elif mode == "Idea Generator 💡":
    st.title("Idea Generator 💡")
    system_instruction = f"""
    You are a Business Growth Consultant.
    Suggest 3-5 printed products for the user's business.
    """
    initial_msg = "What kind of business do you have?"

# --- SHARED CHAT LOGIC (For everything except Images) ---
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
