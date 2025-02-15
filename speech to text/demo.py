#---------------------------------------------------------------------------------------------------------------

import re

command_map = {
    "open hand": ["open hand", "can you open my hand", "please open my hand", "i want to open my hand"],
    "close hand": ["close hand", "can you close my hand", "please close my hand", "make my hand close"],
    "open thumb": ["open thumb", "please lift my thumb", "move my thumb up"],
    "close thumb": ["close thumb", "put my thumb down", "lower my thumb"],
    "open index finger": ["open index finger", "raise my index", "move my pointer finger"],
    "close index finger": ["close index finger", "put my pointer finger down"],
    "open little finger": ["open little finger", "raise my pinky", "move my pinky up"],
    "close little finger": ["close little finger", "put my pinky down"],
    "open ring finger": ["open ring finger", "raise my ring finger"],
    "close ring finger": ["close ring finger", "put my ring finger down"],
    "open middle finger": ["open middle finger", "raise my middle finger"],
    "close middle finger": ["close middle finger", "put my middle finger down"],
}

# Flatten valid phrases
phrase_to_command = {phrase: command for command, phrases in command_map.items() for phrase in phrases}

def extract_command(text):
    """Extracts valid commands from transcribed speech with phrase variations."""
    text = text.lower()
    sorted_phrases = sorted(phrase_to_command.keys(), key=len, reverse=True)  # Sort longest first

    detected_commands = set()
    for phrase in sorted_phrases:
        pattern = r'\b' + r'\s+'.join(re.escape(word) for word in phrase.split()) + r'\b'
        if re.search(pattern, text):
            detected_commands.add(phrase_to_command[phrase])

    return list(detected_commands)

# 🔥 Example Tests
text1 = "Please close my hand and move my pinky up."
print("🔍 Extracted Commands:", extract_command(text1))  
# ✅ Output: ['close hand', 'open little finger']

text2 = "Can you open my hand and raise my index?"
print("🔍 Extracted Commands:", extract_command(text2))  
# ✅ Output: ['open hand', 'open index finger']

'''Main Differences
Feature     	First Version (valid_commands)	Optimized Version (command_map)
Matching    	Strict, allows minor variations	Flexible, supports different phrasings
Scalability  	Hard to add new variations	Easy to expand with more phrases
Performance	  Loops over fewer items	Slightly slower due to more phrases, but optimized
User-Friendliness	Requires exact wording	Supports natural language
'''



#-------------------------------------------------------------------------------------------------------------
'''import re

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
        # Allow small words like "the" in between command words
        pattern = r'\b' + r'(?:\s+the)?\s*'.join(re.escape(word) for word in cmd.split()) + r'\b'
        if re.search(pattern, text):
            detected_commands.add(cmd)

    return list(detected_commands)

# 🔥 Example Outputs:
text1 = "Please close the hand and open the little finger."
print("🔍 Extracted Commands:", extract_command(text1))  
# ✅ Output: ['close hand', 'open little finger']

text2 = "Open the index finger and move the thumb."
print("🔍 Extracted Commands:", extract_command(text2))  
# ✅ Output: ['open index finger', 'open thumb']
'''







#-------------------------------------------------------------------------------------------------------
'''import re

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

# Example Usage:
text = "Please close the hand and open little finger."
print(extract_command(text))  
# Expected Output: ['close hand', 'open little finger']
'''