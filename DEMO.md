# 🎬 VIDEO WALKTHROUGH: SECURE TODO API

## 0:00 - 0:45 | THE HOOK & THE PROBLEM
* **Action:** Webcam or Browser (FastAPI Swagger UI).
* **Script:** "Hey everyone, I'm Benson. I've been building this TodoApp with FastAPI, but I realized a major flaw: anyone can create or view tasks. Today, I'm going to show you how I implemented JWT Authentication to secure my endpoints."
* **Visual:** Demonstrate a `POST` request succeeding *without* authentication to show the vulnerability.

---

## 0:45 - 2:15 | THE LOGIC (PYCHARM)
* **Action:** Switch to PyCharm (Presentation Mode).
* **Script:** "Here in `auth.py`, I created a `get_current_user` dependency. It's the 'Security Guard' of the app. It takes the token from the header, decodes it, and makes sure the user is valid."
* **Pro Tip:** Use **Alt+7** (Structure Tool) to jump to the `get_current_user` function instantly.

---

## 2:15 - 3:30 | THE WIRING & THE PROOF
* **Action:** Open `todos.py`. Highlight the `user_dependency`.
* **Script:** "By adding this `user_dependency`, FastAPI now requires a valid token before this code even runs. Plus, we use the `user.get('id')` to make sure the task is saved to the right owner."
* **Visual:** Return to Browser. Click the **"Authorize"** lock icon, input the token, and show the green lock status.

---

## 3:30 - 4:00 | THE OUTRO
* **Action:** Show GitHub Profile (`Benson-Adedara/TodoApp`).
* **Script:** "This is just one step in my journey to becoming an Agentic System Engineer. You can find the full source code and documentation on my GitHub. Thanks for watching!"

---

## 🛠️ CAMTASIA REMINDERS (FOR THE EDITOR)
* **The 3-Second Rule:** If I stumble, stay silent for 3 seconds, then restart the sentence. (Easier to cut later).
* **Cursor Highlight:** In editing, add the "Highlight" effect so viewers can follow the mouse through the PyCharm UI.