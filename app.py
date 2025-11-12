# app.py
# ----------------------------------------------------------
# Prof. Reddy – Streamlit Version for Hugging Face Spaces
# ----------------------------------------------------------
import streamlit as st
import requests, os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL   = "openai/gpt-4o-mini"

SYSTEM_PROMPT = """You are "Prof. Reddy", a humorous Python lecturer with 36 years experience.
Teach only Python-related topics (syntax, loops, OOP, debugging etc.).
If the student asks something else, politely refuse and redirect them to Python.
Keep explanations simple, include short jokes, and motivate students.
"""

st.set_page_config(page_title="Prof. Reddy – AI Python Lecturer", page_icon="🐍")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"assistant","content":"Namaste 👋 I’m Prof. Reddy – your Python lecturer. What topic shall we start with today?"}
    ]

st.title("🐍 Prof. Reddy – AI Python Lecturer")
st.caption("36 years of teaching wisdom (now digital!)")

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])
    elif msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])

prompt = st.chat_input("Ask Prof. Reddy anything about Python 👇")

def call_openrouter(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Python Lecturer",
        "Content-Type": "application/json"
    }
    payload = {"model": MODEL, "messages": messages, "temperature":0.3, "max_tokens":700}
    r = requests.post(API_URL, headers=headers, json=payload)
    if r.status_code != 200:
        return f"⚠️ Error {r.status_code}: {r.text}"
    return r.json()["choices"][0]["message"]["content"]

PYTHON_KEYWORDS = [
    "python","variable","loop","function","list","tuple","set","dictionary","string","integer",
    "float","if","else","elif","class","object","file","module","package","pip","syntax",
    "error","exception","program","coding","api","json"
]

def is_python_related(text):
    text = text.lower()
    return any(k in text for k in PYTHON_KEYWORDS)

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

    if not is_python_related(prompt):
        reply = "❌ That’s not part of our Python syllabus. Let’s focus on Python, my dear student! 🐍📘"
    else:
        reply = call_openrouter(st.session_state.messages)

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role":"assistant","content":reply})
