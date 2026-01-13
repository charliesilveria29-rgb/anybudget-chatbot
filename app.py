import streamlit as st
import google.generativeai as genai
import os

# 1. Configure the Page
st.set_page_config(page_title="AnyBudget AI", page_icon="💬")
st.title("AnyBudget AI Assistant")

# 2. Connect to the Brain (Gemini)
api_key = os.environ.get("GOOGLE_API_KEY") 
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.info("Please add your GOOGLE_API_KEY to the secrets to continue.")
        st.stop()

genai.configure(api_key=api_key)

# 3. Define the Persona
system_instruction = """
You are the AnyBudget AI Assistant. 
You help customers with file specifications for printing.
- Acceptable formats: PDF, AI, PSD, JPG.
- Bleeds: 0.125 inches required on all sides.
- Resolution: 300 DPI minimum.
- Tone: Professional, helpful, and concise.
"""

# --- THE FIX: Using the standard "gemini-1.5-flash" ---
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# 4. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "parts": "Hello! I can help with file specs, bleed requirements, and turnaround times. What's on your mind?"}
    ]

# 5. Display Chat Messages
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["parts"])

# 6. Handle User Input
if prompt := st.chat_input("Ask about print specs..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": prompt})

    # Generate and show response
    with st.chat_message("assistant"):
        try:
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["parts"]]} for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "parts": response.text})
        except Exception as e:
            st.error(f"An error occurred: {e}")
