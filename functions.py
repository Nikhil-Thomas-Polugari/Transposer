import os
import shutil
import re


NOTES = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "Fb": 4, "E#": 5, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11, "Cb": 11, "B#": 0}

NOTES_REVERSED = {v: k for k, v in NOTES.items()}



def split_and_move_files(file):
    titles = []
    songs = []
    song_indices = []

    with open(file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if ':' in line:
            songs.append(line)
            title = line.split(':')[0]
            titles.append(title + '.txt')

    song_indices = [lines.index(song) for song in songs]

    for i, start in enumerate(song_indices):
        end = song_indices[i + 1] if i + 1 < len(song_indices) else None
        with open(titles[i], 'w') as f_out:
            f_out.writelines(lines[start:end])

    dest_folder = os.path.join(os.getcwd(), "Music_Notes")
    for title in titles:
        shutil.move(os.path.join(os.getcwd(), title), os.path.join(dest_folder, title))



# Order of flats (Go to previous note for key signature and lower a half step unless C & F (Go back to B & E (No Flats needed)))
# -->
# BEADGCF
# <--
# Order of sharps (Raise by half step for key signature unless B & E (Go to C & F (No sharps needed)))


#Major patterns
# Major: 1 2 3 4 5 6 7 8
#Minor patterns
# Natural Minor: 1 2 b3 4 5 b6 b7 8
# Harmonic Minor: 1 2 b3 4 5 b6 7 8
# Melodic Minor: 1 2 b3 4 5 6 7 8
#Mode patterns:
# Ionian: 1 2 3 4 5 6 7 8
# Dorian: 1 2 b3 4 5 6 b7 8
# Phrygian: 1 b2 b3 4 5 b6 b7 8
# Lydian: 1 2 3 #4 5 6 7 8
# Mixolydian: 1 2 3 4 5 6 b7 8
# Aeolian: 1 2 b3 4 5 b6 b7 8

#C_MAJOR = [0, 2, 4, 5, 7, 9, 11, 0]
#C_NATURAL_MINOR = [0, 2, 3, 5, 7, 8, 10, 0]
#C_HARMONIC_MINOR = [0, 2, 3, 5, 7, 8, 10, 0]
#C_MELODIC_MINOR = [0, 2, 3, 5, 7, 9, 11, 0]
#C_DORIAN = [0, 2, 3, 5, 7, 9, 10, 0]
#C_PHRYGIAN = [0, 1, 3, 5, 7, 8, 10, 0]
#C_LYDIAN = [0, 2, 4, 6, 7, 9, 11, 0]
#C_MIXOLYDIAN = [0, 2, 4, 5, 7, 9, 10, 0]
#C_AEOLIAN = [0, 2, 3, 5, 7, 8, 10, 0]

def detect_key_signature(filepath):
    # Scale patterns from comments (semitone intervals)
    SCALE_PATTERNS = {
        "major": [0, 2, 4, 5, 7, 9, 11],          # 1 2 3 4 5 6 7
        "natural_minor": [0, 2, 3, 5, 7, 8, 10],  # 1 2 b3 4 5 b6 b7
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11], # 1 2 b3 4 5 b6 7
        "melodic_minor": [0, 2, 3, 5, 7, 9, 11],  # 1 2 b3 4 5 6 7
        "dorian": [0, 2, 3, 5, 7, 9, 10],         # 1 2 b3 4 5 6 b7
        "phrygian": [0, 1, 3, 5, 7, 8, 10],       # 1 b2 b3 4 5 b6 b7
        "lydian": [0, 2, 4, 6, 7, 9, 11],         # 1 2 3 #4 5 6 7
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],     # 1 2 3 4 5 6 b7
        "aeolian": [0, 2, 3, 5, 7, 8, 10]         # 1 2 b3 4 5 b6 b7
    }
    
    # Count all notes in the file
    note_counts = {}
    
    with open(filepath, 'r') as f:
        content = f.read()
        
        # Extract notes using regex (matches note names followed by optional # or b)
        note_pattern = r'\b([A-G](?:#|b)?)\d*\b'
        matches = re.findall(note_pattern, content)
        
        for note in matches:
            if note in NOTES:
                note_counts[note] = note_counts.get(note, 0) + 1
    
    if not note_counts:
        return "C major"  # Default if no notes found
    
    # Find the best matching key signature
    best_match = ("C", "major", 0)
    
    # Test each possible root note
    for root_note in NOTES:
        root_value = NOTES[root_note]
        
        # Test each scale pattern
        for scale_name, pattern in SCALE_PATTERNS.items():
            score = calculate_pattern_score(note_counts, root_value, pattern)
            
            if score > best_match[2]:
                # Convert scale names for output
                display_name = scale_name.replace("natural_", "").replace("_", " ")
                if display_name == "aeolian":
                    display_name = "minor"
                best_match = (root_note, display_name, score)
    
    return f"{best_match[0]} {best_match[1]}"


def calculate_pattern_score(note_counts, root_value, pattern):
    """Calculate how well the note counts match a given scale pattern"""
    score = 0
    total_notes = sum(note_counts.values())
    
    if total_notes == 0:
        return 0
    
    # Check each note in the scale pattern
    for interval in pattern:
        target_note_value = (root_value + interval) % 12
        
        # Find all note names that match this chromatic value
        matching_notes = [note for note, value in NOTES.items() if value == target_note_value]
        
        # Add score for any matching notes found in the song
        for note_name in matching_notes:
            if note_name in note_counts:
                score += note_counts[note_name]
                break  # Only count the first match to avoid double counting
    
    # Return normalized score (0-1)
    return score / total_notes
    
