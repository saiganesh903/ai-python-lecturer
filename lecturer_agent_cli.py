# lecturer_agent_cli_openrouter.py
# ---------------------------------------------------
# Prof. Reddy – AI Python Lecturer (via OpenRouter API with Memory)
# ---------------------------------------------------

import os, json, requests

# ----------  CONFIGURATION  ----------
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL   = "openai/gpt-4o-mini"   # working OpenRouter model
MEMORY_FILE = "prof_reddy_memory.json"   # to store last chat history
# ------------------------------------

SYSTEM_PROMPT = """You are "Prof. Reddy", a warm, humorous Python lecturer with 36 years of teaching experience.
Your goal: teach clearly, make the student smile, and keep them relaxed.

Guidelines:
- Begin every lesson with a TL;DR objective and a short explanation.
- Use friendly conversational tone — add small light-hearted jokes, teacher humour, or puns every few messages.
- The jokes must always be safe-for-work, positive, and related to the topic if possible
  (e.g., "Why did the Python developer go broke? Because his code lost all its cache!").
- If the student seems confused, calm them down with empathy and a tiny joke before explaining again.
- Show one short code example (≤ 12 lines).
- Give 2 exercises (one quick, one slightly harder).
- When student submits code, analyze and respond with:
  1) the issue or success,
  2) corrected code if needed,
  3) reason for fix,
  4) a quick cheerful remark or mini-joke.
- Encourage and celebrate small wins ("Nice work, you deserve a chai break!").
- Keep everything concise, friendly, and motivating.
"""

# ----------  API CALL FUNCTION ----------
def call_openrouter(messages, model=MODEL, temperature=0.2, max_tokens=600):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Python Lecturer",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    r = requests.post(API_URL, headers=headers, json=payload)
    if r.status_code != 200:
        print(f"\nError {r.status_code}: {r.text}")
        return None
    data = r.json()
    return data["choices"][0]["message"]["content"]
# ---------------------------------------

# ----------  MEMORY HANDLERS ----------
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def save_memory(messages):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages[-20:], f, indent=2)
# -------------------------------------

def main():
    print("Welcome back to Prof. Reddy — your Python Lecturer 🤓")
    print("(Type 'quit' to exit, 'forget' to clear memory.)\n")

    msgs = load_memory()
    if len(msgs) == 1:
        # Fresh start
        msgs.append({"role": "user", "content": "Start a short beginner lesson on Python variables and types."})
        reply = call_openrouter(msgs)
        if not reply:
            print("Failed to get response. Check key or internet connection.")
            return
        print("\nProf. Reddy:\n", reply)
        msgs.append({"role": "assistant", "content": reply})
        save_memory(msgs)
    else:
        print("📚 Loaded previous session memory. Continuing where we left off...\n")

    while True:
        user = input("\nYou> ")
        if user.lower() == "quit":
            save_memory(msgs)
            print("Session saved. See you next time! 👋")
            break
        if user.lower() == "forget":
            if os.path.exists(MEMORY_FILE):
                os.remove(MEMORY_FILE)
                print("🧹 Memory cleared! Starting fresh next time.")
            continue

        msgs.append({"role": "user", "content": user})
        reply = call_openrouter(msgs)
        if not reply:
            print("Error fetching reply — check your key or quota.")
            continue
        print("\nProf. Reddy:\n", reply)
        msgs.append({"role": "assistant", "content": reply})
        save_memory(msgs)

if __name__ == "__main__":
    main()
