import speech_recognition as sr
import re

# ----------------------------------- Define the valid robotic hand commands -----------------------------------
command_map = {
    "open hand": [
        "open hand", "can you open my hand", "please open my hand", "i want to open my hand",
        "unclench my hand", "release my hand", "straighten my hand", "open up my hand",
        "let go of my hand", "relax my hand", "extend my hand", "open my palm",
        "spread my fingers", "make my hand open", "open the hand", "hand open",
        "open the prosthetic hand", "open the robotic hand", "open the artificial hand"
    ],
    "close hand": [
        "close hand", "can you close my hand", "please close my hand", "make my hand close",
        "clench my hand", "grip with my hand", "squeeze my hand", "close up my hand",
        "tighten my hand", "close my fist", "make a fist", "close the hand",
        "close the prosthetic hand", "close the robotic hand", "close the artificial hand",
        "shut my hand", "fold my hand", "contract my hand"
    ],
    "open thumb": [
        "open thumb", "please lift my thumb", "move my thumb up", "raise my thumb",
        "extend my thumb", "straighten my thumb", "uncurl my thumb", "thumb up",
        "lift the thumb", "move the thumb up", "open the thumb", "thumb open",
        "raise the prosthetic thumb", "lift the robotic thumb"
    ],
    "close thumb": [
        "close thumb", "put my thumb down", "lower my thumb", "bring my thumb down",
        "curl my thumb", "fold my thumb", "thumb down", "close the thumb",
        "lower the thumb", "put the thumb down", "close the prosthetic thumb",
        "lower the robotic thumb"
    ],
    "open index finger": [
        "open index finger", "raise my index", "move my pointer finger", "lift my index finger",
        "extend my index finger", "straighten my index finger", "uncurl my index finger",
        "index finger up", "raise the index finger", "move the pointer finger up",
        "open the index finger", "index finger open", "raise the prosthetic index finger",
        "lift the robotic index finger"
    ],
    "close index finger": [
        "close index finger", "put my pointer finger down", "lower my index finger",
        "bring my index finger down", "curl my index finger", "fold my index finger",
        "index finger down", "close the index finger", "lower the index finger",
        "put the pointer finger down", "close the prosthetic index finger",
        "lower the robotic index finger"
    ],
    "open little finger": [
        "open little finger", "raise my pinky", "move my pinky up", "lift my little finger",
        "extend my little finger", "straighten my little finger", "uncurl my little finger",
        "pinky up", "raise the little finger", "move the pinky up", "open the little finger",
        "little finger open", "raise the prosthetic little finger", "lift the robotic little finger"
    ],
    "close little finger": [
        "close little finger", "put my pinky down", "lower my little finger",
        "bring my little finger down", "curl my little finger", "fold my little finger",
        "pinky down", "close the little finger", "lower the little finger",
        "put the pinky down", "close the prosthetic little finger",
        "lower the robotic little finger"
    ],
    "open ring finger": [
        "open ring finger", "raise my ring finger", "lift my ring finger",
        "extend my ring finger", "straighten my ring finger", "uncurl my ring finger",
        "ring finger up", "raise the ring finger", "move the ring finger up",
        "open the ring finger", "ring finger open", "raise the prosthetic ring finger",
        "lift the robotic ring finger"
    ],
    "close ring finger": [
        "close ring finger", "put my ring finger down", "lower my ring finger",
        "bring my ring finger down", "curl my ring finger", "fold my ring finger",
        "ring finger down", "close the ring finger", "lower the ring finger",
        "put the ring finger down", "close the prosthetic ring finger",
        "lower the robotic ring finger"
    ],
    "open middle finger": [
        "open middle finger", "raise my middle finger", "lift my middle finger",
        "extend my middle finger", "straighten my middle finger", "uncurl my middle finger",
        "middle finger up", "raise the middle finger", "move the middle finger up",
        "open the middle finger", "middle finger open", "raise the prosthetic middle finger",
        "lift the robotic middle finger"
    ],
    "close middle finger": [
        "close middle finger", "put my middle finger down", "lower my middle finger",
        "bring my middle finger down", "curl my middle finger", "fold my middle finger",
        "middle finger down", "close the middle finger", "lower the middle finger",
        "put the middle finger down", "close the prosthetic middle finger",
        "lower the robotic middle finger"
    ],
    "wave": [
        "wave", "can you wave", "please wave", "i want to wave", "make a wave",
        "wave my hand", "wave the hand", "wave the prosthetic hand", "wave the robotic hand",
        "perform a wave", "do a wave", "wave gesture", "wave motion"
    ],
    "grab": [
        "grab", "can you grab", "please grab", "i want to grab", "make a grab",
        "grab something", "grab an object", "grab with my hand", "grip something",
        "hold something", "pick up something", "clench to grab", "grab the object",
        "grab the prosthetic hand", "grab the robotic hand"
    ],
    "release": [
        "release", "can you release", "please release", "i want to release", "let go",
        "release my grip", "release the object", "open up to release", "stop holding",
        "unclench to release", "release the prosthetic hand", "release the robotic hand"
    ],
    "rotate wrist": [
        "rotate wrist", "can you rotate my wrist", "please rotate my wrist",
        "i want to rotate my wrist", "turn my wrist", "move my wrist", "twist my wrist",
        "rotate the wrist", "rotate the prosthetic wrist", "rotate the robotic wrist",
        "turn the wrist", "twist the wrist"
    ],
    "flex wrist": [
        "flex wrist", "can you flex my wrist", "please flex my wrist",
        "i want to flex my wrist", "bend my wrist", "move my wrist up", "tilt my wrist",
        "flex the wrist", "flex the prosthetic wrist", "flex the robotic wrist",
        "bend the wrist", "tilt the wrist"
    ],
    "extend wrist": [
        "extend wrist", "can you extend my wrist", "please extend my wrist",
        "i want to extend my wrist", "straighten my wrist", "move my wrist down",
        "extend the wrist", "extend the prosthetic wrist", "extend the robotic wrist",
        "straighten the wrist"
    ],
    "point": [
        "point", "can you point", "please point", "i want to point", "make a point",
        "point with my hand", "point with my index finger", "point the hand",
        "point the prosthetic hand", "point the robotic hand", "point gesture",
        "point motion"
    ],
    "thumbs up": [
        "thumbs up", "can you thumbs up", "please thumbs up", "i want to thumbs up",
        "make a thumbs up", "give a thumbs up", "thumbs up gesture", "thumbs up motion",
        "thumbs up with my hand", "thumbs up the prosthetic hand", "thumbs up the robotic hand"
    ],
    "peace sign": [
        "peace sign", "can you peace sign", "please peace sign", "i want to peace sign",
        "make a peace sign", "give a peace sign", "peace sign gesture", "peace sign motion",
        "peace sign with my hand", "peace sign the prosthetic hand", "peace sign the robotic hand"
    ],
    "fist bump": [
        "fist bump", "can you fist bump", "please fist bump", "i want to fist bump",
        "make a fist bump", "give a fist bump", "fist bump gesture", "fist bump motion",
        "fist bump with my hand", "fist bump the prosthetic hand", "fist bump the robotic hand"
    ],
    "pinch": [
        "pinch", "can you pinch", "please pinch", "i want to pinch", "make a pinch",
        "pinch something", "pinch with my fingers", "pinch gesture", "pinch motion",
        "pinch the prosthetic hand", "pinch the robotic hand"
    ],
}

def extract_command(text):
    """Extracts multiple valid commands from transcribed speech."""
    text = text.lower()
    detected_commands = []
    for cmd, variations in command_map.items():
        for phrase in variations:
            pattern = r'\b' + r'\s*'.join(re.escape(word) for word in phrase.split()) + r'\b'
            if re.search(pattern, text):
                detected_commands.append(cmd)
                break  # Stop checking variations if a match is found
    return detected_commands

def recognize_voice_command():
    """Recognizes voice commands and returns the detected robotic hand actions."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            transcribed_text = recognizer.recognize_google(audio).lower()
            print("Transcribed:", transcribed_text)
            
            commands = extract_command(transcribed_text)
            if commands:
                print("Detected Commands:", commands)
                return commands
            else:
                print("No valid command detected.")
                return []
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError:
            print("Could not request results, check internet connection.")

if __name__ == "__main__":
    commands = recognize_voice_command()
    print("Final Command Output:", commands)
