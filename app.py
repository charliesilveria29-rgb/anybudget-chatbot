import streamlit as st
import google.generativeai as genai
import os
import datetime

# 1. Configure the Page
st.set_page_config(page_title="AnyBudget AI Suite", page_icon="🎨")

# 2. Connect to the Brain (Gemini)
api_key = os.environ.get("GOOGLE_API_KEY") 
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.info("Please add your GOOGLE_API_KEY to the secrets to continue.")
        st.stop()

genai.configure(api_key=api_key)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🤖 AI Tools")
mode = st.sidebar.radio("Select a tool:", ["Print Expert (Chat)", "Image Generator"])

# ==========================================
# MODE 1: THE TEXT CHAT (Fixed: Uses Gemini 2.5)
# ==========================================
if mode == "Print Expert (Chat)":
    st.title("AnyBudget Assistant 💬")
    
    # Get today's date dynamically
    today = datetime.date.today()
    
    # Define Persona with the CURRENT DATE
    system_instruction = f"""
    You are the AnyBudget AI Assistant.
    Today's date is {today}. (You must know this to answer questions about the current year).
    
    You have vast knowledge about history, science, coding, and the world. 
    You are free to answer ANY question the user asks.

    HOWEVER, if asked specifically about **printing services**, strictly follow:
    - Acceptable formats: PDF, AI, PSD, JPG.
    - Bleeds: 0.125 inches.
    - Resolution: 300 DPI minimum.
    """
    
    # --- CRITICAL FIX: Using the model we KNOW works for you ---
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash", 
        system_instruction=system_instruction
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "model", "parts": f"Hello! I am running on Gemini 2.5. I know it is {today.year}. Ask me anything!"}
        ]

    for message in st.session_state.messages:
        role = "user" if message["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message["parts"])

    if prompt := st.chat_input("Ask me anything..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "parts": prompt})

        with st.chat_message("assistant"):
            try:
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["parts"]]} for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "parts": response.text})
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# MODE 2: IMAGE GENERATOR (Fixed: Uses Imagen 3)
# ==========================================
elif mode == "Image Generator":
    st.title("Art Studio 🎨")
    st.write("Generate images using the Standard Imagen model.")

    img_prompt = st.text_area("Describe the image you want:", height=100, placeholder="A futuristic printing press...")

    if st.button("Generate Image ✨"):
        if not img_prompt:
            st.warning("Please describe an image first!")
        else:
            with st.spinner("Painting... (This may take 30 seconds)"):
                try:
                    # Switch to the standard Imagen 3 model (More reliable for free tier)
                    img_model = genai.GenerativeModel("imagen-3.0-generate-001")
                    
                    response = img_model.generate_content(img_prompt)
                    
                    if response.parts:
                        st.image(response.parts[0].image, caption=img_prompt, use_column_width=True)
                    else:
                        st.error("Blocked by safety filters. Try a different prompt.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
