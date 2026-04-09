# ⚡ Codeforces Contest Tracker

A beginner-friendly Python app that automatically tracks upcoming contests from Codeforces, lets you set reminders, and notifies you before the contest starts.

---

## 🧠 About the Project

This project is built as a learning-based application to understand:

- API usage (Codeforces public API)
- Time handling with `datetime`
- Local system notifications via `plyer`
- Basic app development using Streamlit

It fetches real-time contest data from Codeforces and helps you stay consistent with competitive programming.

---

## ✨ Features

- 📅 Fetch upcoming Codeforces contests automatically
- 🕒 Display contest start time, duration, and countdown
- 🔔 Set reminders before contest starts (15 / 30 / 60 / 120 min)
- ⚡ Local system notification when reminder fires
- 💾 Save reminders persistently via JSON
- 🔍 Filter contests by Division (Div 1, 2, 3, 4, Educational)

---

## 🛠️ Tech Stack

| Tool       | Purpose              |
|------------|----------------------|
| Python     | Core language        |
| Streamlit  | UI framework         |
| Requests   | Codeforces API calls |
| Datetime   | Time handling        |
| Plyer      | System notifications |
| JSON       | Local data storage   |

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/your-username/codeforces-tracker.git

# Go to project folder
cd codeforces-tracker

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 🔁 How It Works

```
User opens app
    → Fetch contests from Codeforces API
    → Display upcoming contests with countdown
    → User selects lead time (15/30/60/120 min)
    → Clicks 🔔 Set Reminder
    → Reminder saved to reminders.json
    → Background thread checks time every 60s
    → System notification fires at reminder time
```

---

## 📂 Project Structure

```
codeforces-tracker/
├── app.py            ← Main Streamlit application
├── reminders.json    ← Local reminder storage (auto-created)
├── requirements.txt  ← Python dependencies
└── README.md         ← You are here
```

---

## 🚧 Future Improvements

- [ ] Dark/Light mode toggle
- [ ] Contest filtering by type (Codeforces, ICPC, etc.)
- [ ] Multiple reminder times per contest
- [ ] Email notifications
- [ ] Calendar (.ics) export
- [ ] Past contest history viewer
- [ ] Rating predictor link

---

## 🎯 Learning Goals

This project covers:
- Making HTTP requests to public APIs
- Parsing and filtering JSON responses
- Converting UNIX timestamps to readable dates
- Building interactive UIs with Streamlit
- Running background threads in Python
- Persisting data with JSON files
- Sending local system notifications

---

## 🤝 Contributing

Feel free to fork this repo and improve it. Suggestions and PRs are always welcome.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📌 Note

This is a beginner project. The focus is on learning and building step-by-step rather than perfection. Start simple, test each phase, and keep improving.

---

## ⭐ Support

If you found this useful, consider giving it a star ⭐ on GitHub!

---

**Built with ⚡ for competitive programmers**
