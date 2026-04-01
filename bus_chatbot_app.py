import os
import streamlit as st
import google.generativeai as genai

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Bus Transport Assistant", page_icon="🚌")

# ─── CONFIG ───────────────────────────────────────────────────────────────────
API_KEY = "YOUR_API_KEY_HERE"   # ← paste your Gemini API key here
MODEL_NAME = "gemini-2.5-flash"

# ─── LOAD KB (reads from the same folder as this script) ──────────────────────
# Just place bus_chatbot_dataset.txt in the same folder as bus_chatbot_app.py
KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bus_chatbot_dataset.txt")

with open(KB_PATH, "r", encoding="utf-8") as f:
    kb = f.read()

# ─── SYSTEM PROMPT (unchanged from original notebook) ─────────────────────────
SYSTEM_PROMPT = f"""
You are a professional and friendly Bus Transport Customer Care Assistant.

Your role is to help users with bus-related services such as:

* Ticket booking
* Ticket cancellation
* Seat availability
* Bus timings
* Fare details
* Live bus tracking
* Refund status
* Rescheduling tickets
* Boarding point details
* Handling complaints and issues

Guidelines:

1. Always be polite, helpful, and concise.
2. Ask for required details when missing (e.g., source, destination, date, booking ID).
3. Never assume information. Always confirm with the user.
4. Provide clear step-by-step assistance.
5. If a request involves booking, cancellation, tracking, or refund → ask for booking ID or travel details.
6. Handle errors and complaints with empathy and apology.
7. If you don't know the answer, say: "I'm sorry, I couldn't find that information. Let me connect you to support."

Conversation Style:

* Friendly and professional tone
* Simple English (easy to understand)
* Short and clear responses

Example Behaviors:

User: I want to book a bus
Assistant: Sure! Please tell me your source, destination, and travel date.

User: Cancel my ticket
Assistant: Please provide your booking ID to proceed with cancellation.

User: Where is my bus
Assistant: Please share your booking ID so I can track your bus.

User: My bus is delayed
Assistant: I'm sorry for the inconvenience. Please provide your booking ID so I can check the status.

User: Driver was rude
Assistant: I apologize for your experience. Please share your booking ID or trip details so we can take action.

Important:

* Always guide the user step by step.
* Never provide irrelevant information.
* Focus only on bus transport services.
If you don't know the answer, say: "I'm sorry, I couldn't find that information. Let me connect you to support."
The user is asking questions — provide answers from the knowledge base only.

{kb}
"""

# ─── INIT GEMINI CHAT (only once per session) ─────────────────────────────────
if "chat" not in st.session_state:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT,
    )
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# ─── MAIN UI ──────────────────────────────────────────────────────────────────
st.title("🚌 Bus Transport Assistant")

# ─── DISPLAY CHAT HISTORY ─────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ─── CHAT INPUT ───────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask me anything about bus services...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        response = st.session_state.chat.send_message(user_input)
        reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
