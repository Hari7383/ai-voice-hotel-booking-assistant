# AI Voice Hotel Booking Assistant 

A voice-driven hotel and event hall booking assistant built using Python.  
This system listens continuously through the microphone, processes speech input, and manages booking workflows using a structured state machine.

---

##  Features

-  Continuous voice recognition (Google Speech API via SpeechRecognition)
-  Offline Text-to-Speech using pyttsx3
-  Supports:
  - Hotel room booking
  - Event hall booking
  - Conference hall booking
-  Intelligent date parsing (e.g., "February 22 2026")
-  Booking allowed only within the next 8 months
-  Prevents past-date booking
-  Collects:
  - Booking name
  - Check-in date
  - Check-out date
  - Number of guests
-  Allows modifying booking before confirmation
-  Stores confirmed bookings in JSON file
-  Auto-exits after successful confirmation

---

##  System Architecture

The assistant follows a structured state machine:
GREETING
→ ASK_NAME
→ ASK_CHECKIN
→ ASK_CHECKOUT
→ ASK_GUESTS
→ CONFIRM
→ SAVE + EXIT

No LLM is used. This is a deterministic voice workflow system.

---

##  Installation

###  Clone Repository

```bash
git clone https://github.com/yourusername/ai-voice-hotel-booking-assistant.git
cd ai-voice-hotel-booking-assistant
```

Install Dependencies
```
pip install -r requirements.txt
```

If PyAudio fails on Windows:
```
pip install pipwin
pipwin install pyaudio
```
Run the Assistant
```
python voice_booking_assistant.py
```
---

## The assistant will:

Greet you

Start listening continuously

Guide you through booking steps

Save confirmed bookings to bookings.json

---

## Project Structure

ai-voice-hotel-booking-assistant/

│

├── voice\_booking\_assistant.py   # Main application

├── bookings.json                 # Stored bookings

├── requirements.txt              # Dependencies

├── README.md

└── .gitignore

---

Example Booking JSON Output:
```
[
  {
    "name": "John Doe",
    "service": "room",
    "checkin": "2026-02-22",
    "checkout": "2026-02-25",
    "guests": 2,
    "timestamp": "2026-02-21 18:45:30"
  }
]
```

---

## Limitations

- Requires internet for Google Speech Recognition
- Uses system-installed voice for TTS
- No wake word detection
- Single-session prototype (auto-exits after booking)

---

## Future Improvements

- Wake-word activation
- Whisper offline STT
- Cloud TTS neural voice
- Booking modification support
- REST API integration
- Telephony integration (Twilio / SIP)
- Database instead of JSON
- Multi-user handling

---

## Tech Stack

- Python
- SpeechRecognition
- PyAudio
- pyttsx3
- python-dateutil
- JSON persistence

---

## License

MIT License
