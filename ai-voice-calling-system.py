import speech_recognition as sr
import datetime
import sys
import re
import pyttsx3
import json
import os
from dateutil import parser

# ================= CONFIG =================
BOOKING_FILE = "bookings.json"

# ================= INIT =================
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
mic = sr.Microphone()

# ================= SESSION =================
session = {
    "state": "GREETING",
    "service": None,
    "name": None,
    "checkin": None,
    "checkout": None,
    "guests": None
}

# ================= TTS =================
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    print("AI Caller Assistant:", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# ================= UTILITIES =================
def save_booking(data):
    if os.path.exists(BOOKING_FILE):
        with open(BOOKING_FILE, "r") as f:
            bookings = json.load(f)
    else:
        bookings = []

    bookings.append(data)

    with open(BOOKING_FILE, "w") as f:
        json.dump(bookings, f, indent=4)

def is_valid_domain(text):
    keywords = ["room", "hotel", "hall", "conference"]
    return any(k in text for k in keywords)

def extract_date(text):
    try:
        parsed_date = parser.parse(text, fuzzy=True)
        return parsed_date.date()
    except:
        if "tomorrow" in text:
            return datetime.date.today() + datetime.timedelta(days=1)
        return None

def is_valid_booking_date(date_obj):
    today = datetime.date.today()
    max_date = today + datetime.timedelta(days=240)  # 8 months

    if date_obj < today:
        return False, "You cannot book for past dates."
    if date_obj > max_date:
        return False, "Booking is allowed only within the next 8 months."
    return True, None

def extract_guests(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return None

# ================= MAIN LOGIC =================
def handle_input(text):
    global session

    text = text.replace(".", "").strip()

    # EXIT
    if any(word in text for word in ["exit", "quit", "stop", "bye"]):
        speak("Thank you for using the booking assistant. Goodbye.")
        sys.exit()

    # GREETING
    if session["state"] == "GREETING":
        if not is_valid_domain(text):
            speak("I can only assist with hotel room or event hall bookings.")
            return

        if "room" in text:
            session["service"] = "room"
        elif "hall" in text:
            session["service"] = "event hall"

        session["state"] = "ASK_NAME"
        speak("Please tell me the booking name.")
        return

    # ASK NAME
    if session["state"] == "ASK_NAME":
        session["name"] = text.title()
        session["state"] = "ASK_CHECKIN"
        speak("Please tell me the check in date.")
        return

    # ASK CHECKIN
    if session["state"] == "ASK_CHECKIN":
        checkin = extract_date(text)
        if not checkin:
            speak("Please provide a valid check in date.")
            return

        valid, message = is_valid_booking_date(checkin)
        if not valid:
            speak(message)
            return

        session["checkin"] = checkin
        session["state"] = "ASK_CHECKOUT"
        speak("Please tell me the check out date.")
        return

    # ASK CHECKOUT
    if session["state"] == "ASK_CHECKOUT":
        checkout = extract_date(text)
        if not checkout:
            speak("Please provide a valid check out date.")
            return

        if checkout <= session["checkin"]:
            speak("Check out date must be after check in date.")
            return

        valid, message = is_valid_booking_date(checkout)
        if not valid:
            speak(message)
            return

        session["checkout"] = checkout
        session["state"] = "ASK_GUESTS"
        speak("How many guests will be staying?")
        return

    # ASK GUESTS
    if session["state"] == "ASK_GUESTS":
        guests = extract_guests(text)
        if not guests:
            speak("Please tell me the number of guests.")
            return

        session["guests"] = guests
        session["state"] = "CONFIRM"

        speak(
            f"Please confirm your booking details. "
            f"Name: {session['name']}. "
            f"Service: {session['service']}. "
            f"Check in: {session['checkin']}. "
            f"Check out: {session['checkout']}. "
            f"Guests: {session['guests']}. "
            f"Say yes or correct to confirm. "
            f"If you want to change date say change date."
        )
        return

    # CONFIRM
    if session["state"] == "CONFIRM":

        if any(word in text for word in ["change date", "change the date"]):
            session["state"] = "ASK_CHECKIN"
            speak("Please provide the new check in date.")
            return

        if any(word in text for word in ["yes", "correct", "confirm"]):

            booking_data = {
                "name": session["name"],
                "service": session["service"],
                "checkin": str(session["checkin"]),
                "checkout": str(session["checkout"]),
                "guests": session["guests"],
                "timestamp": str(datetime.datetime.now())
            }

            save_booking(booking_data)
            speak("Your booking has been confirmed successfully. Thank you.")
            sys.exit()

        speak("Please say yes to confirm or say change date to modify your booking.")
        return

# ================= AUDIO CALLBACK =================
def audio_callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio)
        text = text.lower().strip()

        if not text:
            return

        print("User:", text)
        handle_input(text)

    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Speech recognition error:", e)

def start_background_listening():
    print("Listening continuously...")
    stop_listening = recognizer.listen_in_background(mic, audio_callback)
    return stop_listening

# ================= START =================
def main():
    intro = (
        "Hello. I am an AI assistant for hotel room booking, "
        "event hall booking and conference hall booking. "
        "How can I assist you today?"
    )
    speak(intro)

    stop_listener = start_background_listening()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        stop_listener(wait_for_stop=False)
        print("Assistant stopped.")

if __name__ == "__main__":
    print("Starting AI Voice Booking Assistant...")
    main()