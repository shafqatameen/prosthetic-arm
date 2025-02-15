import speech_recognition as sr
import re

# ---------------------------------------------Define the valid robotic hand commands--------------------------------


valid_commands = [
    "close hand", "open hand",
    "open little finger", "close little finger",
    "open ring finger", "close ring finger",
    "open middle finger", "close middle finger",
    "open index finger", "close index finger",
    "open thumb", "close thumb"
]

def extract_command(text):
    """Extracts multiple valid commands from transcribed speech with slight variations."""
    text = text.lower()
    sorted_commands = sorted(valid_commands, key=len, reverse=True)  # Prioritize longer commands

    detected_commands = set()
    for cmd in sorted_commands:
        # Allow extra words (e.g., "the") in between command words
        pattern = r'\b' + r'(\s+\w+)?\s*'.join(re.escape(word) for word in cmd.split()) + r'\b'
        if re.search(pattern, text):
            detected_commands.add(cmd)

    return list(detected_commands)

'''def extract_command(text):
    """Extracts valid commands from transcribed speech."""
    detected_commands = [cmd for cmd in valid_commands if cmd in text.lower()]
    return detected_commands'''

# ----------------------------------------------Initialize the recognizer-----------------------------------------
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Say a command for the robotic hand...")
    recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
    audio = recognizer.listen(source)  # Capture audio

# --------------------------------------Convert speech to text--------------------------------------------------
try:
    transcribed_text = recognizer.recognize_google(audio)  # Use Google's Speech-to-Text
    print("Transcribed Text:", transcribed_text)
    
    # Extract commands from speech
    commands = extract_command(transcribed_text)

    if commands:
        print("Detected Commands:", commands)
    else:
        print("No valid command detected.")

except sr.UnknownValueError:
    print("Sorry, could not understand the audio.")
except sr.RequestError:
    print("Could not request results, check internet connection.")




"""
🔥 Example Outputs
🎙 Input 1:
Text: "Please close the hand and open the little finger."
🔍 Extracted Commands: ["close hand", "open little finger"]

🎙 Input 2:
Text: "Open the index finger and move the thumb."
🔍 Extracted Commands: ["open index finger", "open thumb"]"""