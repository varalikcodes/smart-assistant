import datetime
from virtual_assistant import speak, listen, get_weather
from task_manager import set_reminder, get_upcoming_reminders

def suggest_context_aware_task():
    now = datetime.datetime.now()
    hour = now.hour

    # For weather info, we'll ask for a default city or let the user specify.
    default_city = "London"
    weather_info = get_weather(default_city)
    
    # Determine suggestion based on time and weather keywords
    if hour < 10:
        suggestion = "Good morning! Would you like to schedule your morning exercise?"
    elif hour >= 18 and hour < 22:
        suggestion = "It's evening. Would you like to set a reminder to review your tasks?"
    elif "rain" in weather_info.lower():
        suggestion = "It seems to be raining. Would you like to postpone your outdoor activities?"
    else:
        suggestion = "Would you like to check your upcoming reminders?"

    speak(suggestion)
    response = listen()
    
    if response and "yes" in response.lower():
        speak("Great! Please tell me the task details.")
        task_details = listen()
        if not task_details:
            speak("I didn't catch that. Let's try again later.")
            return
        
        speak("Please tell me the time for this reminder. For example, 'tomorrow at 9 AM'.")
        time_info = listen()
        if not time_info:
            speak("I didn't catch the time. Please try again later.")
            return

        confirmation = set_reminder(task_details, time_info)
        speak(confirmation)
    else:
        speak("No problem. Let me know if you need anything else.")

def main():
    speak("Hello! I am your integrated virtual assistant.")
    while True:
        speak("Please say a command: 'suggest tasks', 'weather', 'upcoming reminders', or 'exit'.")
        command = listen()
        if not command:
            continue

        command = command.lower()
        if "exit" in command:
            speak("Goodbye!")
            break
        elif "suggest" in command or "task" in command:
            suggest_context_aware_task()
        elif "weather" in command:
            speak("Please tell me the city name.")
            city = listen()
            if city:
                weather_info = get_weather(city)
                speak(weather_info)
            else:
                speak("I didn't catch that.")
        elif "upcoming" in command or "reminder" in command:
            upcoming = get_upcoming_reminders()
            speak("Here are your upcoming reminders.")
            speak(upcoming)
        else:
            speak("I'm not sure how to help with that. Please try a different command.")

if __name__ == "__main__":
    main()
