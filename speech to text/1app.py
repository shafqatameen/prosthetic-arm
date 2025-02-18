# filepath: /c:/xampp/htdocs/my_projects/arm/speech/app.py
from flask import Flask, jsonify, render_template, request
import speech_recognition as sr

app = Flask(__name__)
recognizer = sr.Recognizer()
command_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/microphone', methods=['GET'])
def transcribe_from_microphone():
    try:
        with sr.Microphone() as source:
            print("Speak now...")
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source)
            transcript = recognizer.recognize_google(audio_data)
            return jsonify({"transcript": transcript}), 200

    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand the audio."}), 400

    except sr.RequestError as e:
        return jsonify({"error": f"Could not request results; {e}"}), 500

@app.route('/control', methods=['POST'])
def control_robot_hand():
    data = request.get_json()
    command = data.get('command', '').lower()
    command_history.append(command)

    if 'open hand' in command:
        print("Opening hand")
        # Add code to open the robot's hand
    elif 'close hand' in command:
        print("Closing hand")
        # Add code to close the robot's hand
    else:
        print("Unknown command")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)