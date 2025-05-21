# Help Center Bot (WhatsApp + Flask + PostgreSQL)

A WhatsApp-based help center bot built using **Flask**, integrated with **Twilio** for message handling, **PostgreSQL** for storing support issues, and **email alerts** via SMTP.

---

## Features

- Multi-step WhatsApp chat flow to collect support issues.
- Stores user queries in a **PostgreSQL** database.
- Sends email notifications to department-specific addresses.
- Hosted on **Render** with Gunicorn for production.

---

## Project Structure

help-center-bot/
├── app.py # Main Flask app
├── requirements.txt # Python dependencies
└── README.md 



---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/help-center-bot.git
cd help-center-bot
```

### 2. Set up a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```


