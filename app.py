from flask import Flask, render_template, request,jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")  # OpenWeatherMap API key
base_url = "http://api.openweathermap.org/data/2.5/weather"

# Gemini API configuration
gemini_api_key = os.getenv("gemini_api_key")

app = Flask(__name__)

# Store chat history and weather data in memory
chat_history = []
last_weather_data = None


@app.route('/', methods=['GET', 'POST'])
def home():
    global last_weather_data
    weather_data = None
    
    if request.method == 'POST' and 'city' in request.form:
        city = request.form.get('city')
        complete_url = f"{base_url}?q={city}&appid={api_key}&units=metric"
        response = requests.get(complete_url)

        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather_data = {
                'city': city,
                'temperature': main['temp'],
                'feels_like': main['feels_like'],
                'humidity': main['humidity'],
                'wind_speed': data['wind']['speed'],
                'country': data['sys']['country'],
                'description': data['weather'][0]['description']
            }
            # Store weather data for AI context
            last_weather_data = weather_data
        else:
            weather_data = {'error': 'City Not Found'}

    return render_template('index.html', weather_data=weather_data, chat_history=chat_history)


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message')
    
    if user_input:
        chat_history.append({'content': user_input, 'is_user': True})
        
        # Get weather context and pass to AI
        weather_context = get_weather_context()
        ai_response = call_gemini(user_input, weather_context)
        
        chat_history.append({'content': ai_response, 'is_user': False})
        
        return jsonify({
            'success': True,
            'ai_response': ai_response
        })
    else:
        return jsonify({
            'success': False,
            'error': 'No message provided'
        }), 400


def get_weather_context():
    #get last fetched weather data to provide context to Gemini
    global last_weather_data
    if last_weather_data and 'error' not in last_weather_data:
        return f"""
Current weather information available:
- Location: {last_weather_data.get('city', 'Unknown')}, {last_weather_data.get('country', '')}
- Temperature: {last_weather_data.get('temperature', 'Unknown')}°C
- Condition: {last_weather_data.get('description', 'Unknown')}
- Feels like: {last_weather_data.get('feels_like', 'Unknown')}°C
- Humidity: {last_weather_data.get('humidity', 'Unknown')}%
- Wind Speed: {last_weather_data.get('wind_speed', 'Unknown')} m/s """
    return "No current weather data available.."


def call_gemini(user_input, weather_context=""):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }

    # Build enhanced prompt with weather context
    enhanced_prompt = f"""
You are Sky, a friendly and helpful weather assistant chatbot.

{weather_context}

User question: {user_input}

Instructions for your responses:
- Use the current weather information above to provide accurate and practical answers.
- For questions about rain, umbrellas, or precipitation, consider the weather conditions and humidity to give useful advice.
- For other weather-related questions, use the available data where relevant.
- If no weather data is available, politely explain that real-time information is not accessible.
- Keep responses friendly, conversational, and concise (under 100 words).
- Always provide helpful and practical guidance.
- If you are unsure about a question, respond with "I'm not sure" rather than guessing.
- Avoid repeating the same information multiple times.
- If asked who built you, respond: "This project was built by Ashwell.
-Provide the current weather and practical tips. If the temperature is high, suggest applying sunscreen, wearing a hat, and sunglasses. Include advice on rain, humidity, or other conditions as needed.
- Always end with a friendly note, e.g., "Stay safe and have a great day!
- don't always mention the weather data is not available, only when relevant.
"""
    
    body = {
        "contents": [
            {
                "role": "user", 
                "parts": [{"text": enhanced_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 200,
            "topP": 0.95,
            "topK": 20
        }
    }

    try:
        #for debugging
        response = requests.post(url, headers=headers, json=body, timeout=10)
        print(" Status:", response.status_code)
        print(" Response:", response.text)
        
        if response.status_code == 200:
            result = response.json()
            text = (
                result.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "Sorry, I could not process that.")
            )
            return text
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return f"Sorry, I'm having trouble connecting right now. (Error {response.status_code})"
    except Exception as e:
        print(f"Exception in call_gemini: {str(e)}")
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)