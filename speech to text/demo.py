import pygame
import sys
import speech_recognition as sr
import re

# Initialize Pygame
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
forearm_length = 150

# Initial arm state
hand_open = True
elbow_angle = 0  # Elbow joint angle (0 = straight, 90 = bent)
fingers_state = {finger: True for finger in ["thumb", "index", "middle", "ring", "little"]}  # True = Open
wrist_rotation = 0  # 0 = neutral, -30 = left, 30 = right
wave_motion = False
pointing = False
thumbs_up = False
peace_sign = False
fist_bump = False

# Command processing
command_actions = {
    "open hand": lambda: open_hand(),
    "close hand": lambda: close_hand(),
    "rotate wrist": lambda: rotate_wrist(),
    "wave": lambda: wave_hand(),
    "point": lambda: point_finger(),
    "thumbs up": lambda: thumbs_up_gesture(),
    "peace sign": lambda: peace_sign_gesture(),
    "fist bump": lambda: fist_bump_gesture(),
}


def open_hand():
    global hand_open, fingers_state
    hand_open = True
    fingers_state = {finger: True for finger in fingers_state}


def close_hand():
    global hand_open, fingers_state
    hand_open = False
    fingers_state = {finger: False for finger in fingers_state}


def rotate_wrist():
    global wrist_rotation
    wrist_rotation = 30 if wrist_rotation == 0 else -30 if wrist_rotation == 30 else 0


def wave_hand():
    global wave_motion
    wave_motion = not wave_motion


def point_finger():
    global pointing, fingers_state
    pointing = not pointing
    fingers_state = {finger: False for finger in fingers_state}
    fingers_state["index"] = pointing


def thumbs_up_gesture():
    global thumbs_up, fingers_state
    thumbs_up = not thumbs_up
    fingers_state = {finger: False for finger in fingers_state}
    fingers_state["thumb"] = thumbs_up


def peace_sign_gesture():
    global peace_sign, fingers_state
    peace_sign = not peace_sign
    fingers_state = {finger: False for finger in fingers_state}
    fingers_state["index"] = peace_sign
    fingers_state["middle"] = peace_sign


def fist_bump_gesture():
    global fist_bump, fingers_state
    fist_bump = not fist_bump
    fingers_state = {finger: not fist_bump for finger in fingers_state}


def extract_command(text):
    """Extracts multiple valid commands from transcribed speech."""
    text = text.lower()
    detected_commands = [cmd for cmd in command_actions if cmd in text]
    return detected_commands


def recognize_voice_command():
    """Recognizes voice commands and updates hand state."""
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
                for command in commands:
                    command_actions[command]()
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError:
            print("Could not request results, check internet connection.")


def draw_arm():
    screen.fill(WHITE)

    # Draw upper arm
    pygame.draw.rect(screen, BLUE, (350, 200, arm_base_width, arm_base_height))

    # Rotate forearm based on elbow and wrist rotation
    forearm_x = 350 + arm_base_width // 2
    forearm_y = 200 + arm_base_height
    forearm_surface = pygame.Surface((arm_base_width, forearm_length), pygame.SRCALPHA)
    pygame.draw.rect(forearm_surface, BLUE, (0, 0, arm_base_width, forearm_length))
    rotated_forearm = pygame.transform.rotate(forearm_surface, -elbow_angle - wrist_rotation)
    screen.blit(rotated_forearm, (forearm_x - rotated_forearm.get_width() // 2, forearm_y))

    # Draw hand
    hand_x = forearm_x - hand_width // 2
    hand_y = forearm_y + forearm_length - hand_height
    pygame.draw.rect(screen, GREEN if hand_open else RED, (hand_x, hand_y, hand_width, hand_height))

    # Draw fingers
    finger_names = ["thumb", "index", "middle", "ring", "little"]
    for i, finger in enumerate(finger_names):
        finger_x = hand_x + i * (finger_width + 5)
        finger_y = hand_y - (finger_height if fingers_state[finger] else 10)
        pygame.draw.rect(screen, BLACK if fingers_state[finger] else RED, (finger_x, finger_y, finger_width, finger_height))
    
    pygame.display.flip()

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:  # Press 'V' to activate voice command
                recognize_voice_command()

    draw_arm()
    clock.tick(30)

pygame.quit()
sys.exit()
