from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

# List of valid commands
valid_commands = [
    "close hand", "open hand",
    "open little finger", "close little finger",
    "open ring finger", "close ring finger",
    "open middle finger", "close middle finger",
    "open index finger", "close index finger",
    "open thumb", "close thumb"
]

def extract_command(text):
    """Extracts valid commands from the transcribed text."""
    detected_commands = [cmd for cmd in valid_commands if cmd in text.lower()]
    return detected_commands

@app.route("/process_audio", methods=["POST"])
def process_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        transcribed_text = recognizer.recognize_google(audio_data)
        detected_commands = extract_command(transcribed_text)
        return jsonify({"transcribed_text": transcribed_text, "commands": detected_commands})
    
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand the audio"})
    except sr.RequestError:
        return jsonify({"error": "Speech recognition service unavailable"})

if __name__ == "__main__":
    app.run(debug=True)
