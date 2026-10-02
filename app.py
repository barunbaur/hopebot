import os
from groq import Groq

# ⚠️ IMPORTANT: Replace the text below with your actual Groq API key (the one starting with gsk_)
client = Groq(api_key="gsk_paste_your_actual_key_here")

try:
 print("🔍 Fetching your available models...\n")
 models = client.models.list()
 print("✅ Here are the models you have access to:")
 for model in models.data:
  print(f"  -> {model.id}")
except Exception as e:
    print(f"❌ Error: {e}")

import streamlit as st

# 1. The "Uplifting" System Prompt (Moved to the top to fix the error)
SYSTEM_PROMPT = """You are HopeBot, a warm, empathetic, and deeply uplifting AI companion. 
Your goal is to support the user's mental wellness. 
- Encourage gratitude and mindfulness.
- Gently reframe negative thoughts into positive, actionable perspectives.
- Always be kind, non-judgmental, and hopeful. 
- Keep responses concise, comforting, and end with a gentle, encouraging question or affirmation."""

# 2. Page Configuration
st.set_page_config(page_title="HopeBot 🌻", page_icon="🌻", layout="centered")

# Custom CSS for a calming, warm aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #FFFDF9; }
    .stChatMessage { background-color: #F4F1EA; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar for API Key
with st.sidebar:
    st.title("🌻 HopeBot")
    st.markdown("Your uplifting AI companion for mental wellness and gratitude.")
    api_key = st.text_input("Enter your Groq API Key:", type="password")
    st.markdown("[Get a free Groq API Key](https://console.groq.com/)")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if not api_key:
    st.info("Please add your Groq API key in the sidebar to begin your journey.")
    st.stop()

# 4. Initialize Groq Client
client = Groq(api_key=api_key)

# 5. Session State (Remembers the conversation)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 6. Display Chat History
for message in st.session_state.messages[1:]: # Skip the system prompt for display
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Chat Input & AI Generation
if prompt := st.chat_input("How are you feeling today? Share your thoughts..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Stream the response for a natural typing effect
        response_stream = client.chat.completions.create(
       model="openai/gpt-oss-120b", 
       messages=st.session_state.messages,
       stream=True,
   )
        
        response_text = ""
        for chunk in response_stream:
            response_text += chunk.choices[0].delta.content or ""
            message_placeholder.markdown(response_text + "▌")
        
        message_placeholder.markdown(response_text)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})