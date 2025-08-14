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
    
    # Convert all notes to their chromatic values, combining enharmonic equivalents
    chromatic_counts = [0] * 12
    
    with open(filepath, 'r') as f:
        content = f.read()
        
        # Extract notes using regex (matches note names followed by optional # or b)
        note_pattern = r'\b([A-G](?:#|b)?)\d*\b'
        matches = re.findall(note_pattern, content)
        
        for note in matches:
            if note in NOTES:
                chromatic_value = NOTES[note]
                chromatic_counts[chromatic_value] += 1
    
    if sum(chromatic_counts) == 0:
        return "C major"  # Default if no notes found
    
    # Find the best matching key signature
    best_match = ("C", "major", 0)
    
    # Test each possible root note (only use natural notes and common accidentals)
    test_roots = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]
    
    for root_note in test_roots:
        root_value = NOTES[root_note]
        
        # Test each scale pattern
        for scale_name, pattern in SCALE_PATTERNS.items():
            score = calculate_pattern_score_improved(chromatic_counts, root_value, pattern)
            
            if score > best_match[2]:
                # Convert scale names for output
                display_name = scale_name.replace("natural_", "").replace("_", " ")
                if display_name == "aeolian":
                    display_name = "minor"
                best_match = (root_note, display_name, score)
    
    return f"{best_match[0]} {best_match[1]}"


def calculate_pattern_score_improved(chromatic_counts, root_value, pattern):
    """Calculate how well the chromatic counts match a given scale pattern"""
    total_notes = sum(chromatic_counts)
    
    if total_notes == 0:
        return 0
    
    # Calculate scores for notes in the scale vs notes outside the scale
    in_scale_score = 0
    out_of_scale_score = 0
    
    for chromatic_value in range(12):
        note_count = chromatic_counts[chromatic_value]
        interval_from_root = (chromatic_value - root_value) % 12
        
        if interval_from_root in pattern:
            # This note is in the scale - add to positive score
            # Give extra weight to root, fifth, and third
            weight = 1.0
            if interval_from_root == 0:  # Root
                weight = 3.0
            elif interval_from_root == 7:  # Fifth
                weight = 2.0
            elif interval_from_root in [4, 3]:  # Major/minor third
                weight = 1.5
            
            in_scale_score += note_count * weight
        else:
            # This note is outside the scale - penalize
            out_of_scale_score += note_count * 0.5
    
    # Calculate final score (favor scales with high in-scale notes and low out-of-scale notes)
    if total_notes == 0:
        return 0
    
    # Return a score that rewards in-scale notes and penalizes out-of-scale notes
    return (in_scale_score - out_of_scale_score) / total_notes
    
