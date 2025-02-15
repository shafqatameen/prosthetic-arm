import pygame
import sys
import speech_recognition as sr
import re

# ----------------------------------- Define the valid robotic hand commands -----------------------------------
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
        pattern = r'\b' + r'(\s+\w+)?\s*'.join(re.escape(word) for word in cmd.split()) + r'\b'
        if re.search(pattern, text):
            detected_commands.add(cmd)

    return list(detected_commands)

# ----------------------------------- Initialize Pygame -----------------------------------
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Voice-Controlled Prosthetic Hand")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Arm parameters
arm_base_width = 100
arm_base_height = 200
hand_width = 50
hand_height = 50
finger_width = 10
finger_height = 30

# Initial arm state
hand_open = True
fingers_state = {finger: True for finger in ["thumb", "index", "middle", "ring", "little"]}  # True = Open

# ----------------------------------- Function to process voice commands -----------------------------------
def recognize_voice_command():
    """Recognizes voice commands and updates hand state."""
    global hand_open, fingers_state

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        try:
            audio = recognizer.listen(source, timeout=5)
            transcribed_text = recognizer.recognize_google(audio).lower()
            print("Transcribed:", transcribed_text)

            # Extract commands from speech
            commands = extract_command(transcribed_text)

            if commands:
                print("Detected Commands:", commands)
                for command in commands:
                    if command == "open hand":
                        hand_open = True
                        fingers_state = {finger: True for finger in fingers_state}  # Open all fingers
                    elif command == "close hand":
                        hand_open = False
                        fingers_state = {finger: False for finger in fingers_state}  # Close all fingers
                    elif "open" in command:
                        finger = command.replace("open ", "")
                        if finger in fingers_state:
                            fingers_state[finger] = True
                    elif "close" in command:
                        finger = command.replace("close ", "")
                        if finger in fingers_state:
                            fingers_state[finger] = False

                    # Update hand state based on all fingers
                    hand_open = any(fingers_state.values())
            else:
                print("No valid command detected.")

        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError:
            print("Could not request results, check internet connection.")

# ----------------------------------- Function to draw the arm -----------------------------------
def draw_arm():
    screen.fill(WHITE)  # Clear screen

    # Draw arm base (upper arm)
    pygame.draw.rect(screen, BLUE, (350, 200, arm_base_width, arm_base_height))

    # Draw forearm
    forearm_length = 150
    forearm_x = 350 + arm_base_width // 2
    forearm_y = 200 + arm_base_height
    pygame.draw.rect(screen, BLUE, (forearm_x - arm_base_width // 2, forearm_y, arm_base_width, forearm_length))

    # Draw hand
    hand_x = forearm_x - hand_width // 2
    hand_y = forearm_y + forearm_length - hand_height
    pygame.draw.rect(screen, GREEN if hand_open else RED, (hand_x, hand_y, hand_width, hand_height))

    # Draw fingers
    finger_names = ["thumb", "index", "middle", "ring", "little"]
    for i, finger in enumerate(finger_names):
        finger_x = hand_x + i * (finger_width + 5)
        finger_y = hand_y - finger_height
        pygame.draw.rect(screen, GREEN if fingers_state[finger] else RED, (finger_x, finger_y, finger_width, finger_height))

    pygame.display.flip()

# ----------------------------------- Main loop -----------------------------------
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:  # Press 'V' to activate voice command
                recognize_voice_command()

    # Draw the arm
    draw_arm()

    # Control frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
