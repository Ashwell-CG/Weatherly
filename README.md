# 🌦️ Weatherly

Weatherly is a Flask-based web app where you can:
- Enter a city name to get **real-time weather data** from [OpenWeatherMap](https://openweathermap.org/).
- Chat with **Gemini AI** about the weather using natural language.
- Get friendly and practical responses (like whether you need an umbrella 🌂).

---

## 🚀 Features
- Fetches live weather data (temperature, humidity, wind speed, conditions).
- AI-powered chat assistant that uses current weather as context.
- Simple and interactive web interface.
- Secure handling of API keys using `.env`.

---

## ⚙️ Tech Stack
- **Python** (Flask, Requests)
- **OpenWeatherMap API**
- **Google Gemini API**
- **HTML Templates (Jinja2)**

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/YOUR-USERNAME/weatherly.git
cd weatherly
````

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate    # On Mac/Linux
venv\Scripts\activate       # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root folder and add:

```
weather_API_KEY=your_openweathermap_api_key
GEMINI_API_KEY=your_gemini_api_key
```

⚠️ Never commit your `.env` file — it’s already ignored via `.gitignore`.

---

## ▶️ Run the app

```bash
python app.py
```

App runs on:
👉 `http://127.0.0.1:5000/`

---

## 📸 DEMO

https://github.com/user-attachments/assets/f45f73f1-a268-4082-8785-15be44bbc897



