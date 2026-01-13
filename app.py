import streamlit as st
import google.generativeai as genai
import os

st.title("🛠️ AnyBudget System Diagnostic")

# 1. Get the API Key
api_key = os.environ.get("GOOGLE_API_KEY") 
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.error("❌ API Key not found in Secrets!")
        st.stop()

genai.configure(api_key=api_key)

# 2. List Available Models
st.write("Contacting Google to see available models...")

try:
    my_models = []
    # Ask Google for the list of models this key can access
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            my_models.append(m.name)

    if len(my_models) > 0:
        st.success(f"✅ Success! Your key has access to {len(my_models)} models.")
        st.write("Here are the valid names:")
        st.code(my_models)
        
        # Test the first one found
        test_model_name = my_models[0]
        st.write(f"Testing the first one: `{test_model_name}`...")
        model = genai.GenerativeModel(test_model_name)
        response = model.generate_content("Say hello!")
        st.info(f"Response: {response.text}")
    else:
        st.error("⚠️ Your key works, but Google returned 0 models. This usually means the API has not been enabled for this project yet.")

except Exception as e:
    st.error(f"❌ Connection Error: {e}")
