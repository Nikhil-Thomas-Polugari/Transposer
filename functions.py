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
    # Scale patterns from comments above
    MAJOR_PATTERN = [0, 2, 4, 5, 7, 9, 11]  # 1 2 3 4 5 6 7
    NATURAL_MINOR_PATTERN = [0, 2, 3, 5, 7, 8, 10]  # 1 2 b3 4 5 b6 b7
    HARMONIC_MINOR_PATTERN = [0, 2, 3, 5, 7, 8, 11]  # 1 2 b3 4 5 b6 7
    MELODIC_MINOR_PATTERN = [0, 2, 3, 5, 7, 9, 11]  # 1 2 b3 4 5 6 7
    DORIAN_PATTERN = [0, 2, 3, 5, 7, 9, 10]  # 1 2 b3 4 5 6 b7
    PHRYGIAN_PATTERN = [0, 1, 3, 5, 7, 8, 10]  # 1 b2 b3 4 5 b6 b7
    LYDIAN_PATTERN = [0, 2, 4, 6, 7, 9, 11]  # 1 2 3 #4 5 6 7
    MIXOLYDIAN_PATTERN = [0, 2, 4, 5, 7, 9, 10]  # 1 2 3 4 5 6 b7
    
    # Count note occurrences
    note_counts = {}
    
    with open(filepath, 'r') as f:
        content = f.read()
        
        # Extract all notes from the content
        note_pattern = r'\b([A-G](?:#|b)?)\d*\b'
        matches = re.findall(note_pattern, content)
        
        for note in matches:
            if note in NOTES:
                if note not in note_counts:
                    note_counts[note] = 0
                note_counts[note] += 1
    
    if not note_counts:
        return "C major"  # Default if no notes found
    
    # Find the most likely key by testing each root note with different patterns
    best_match = ("C", "major", 0)
    
    for root_note in NOTES:
        root_value = NOTES[root_note]
        
        # Test major pattern
        major_score = calculate_pattern_score(note_counts, root_value, MAJOR_PATTERN)
        if major_score > best_match[2]:
            best_match = (root_note, "major", major_score)
        
        # Test natural minor pattern
        minor_score = calculate_pattern_score(note_counts, root_value, NATURAL_MINOR_PATTERN)
        if minor_score > best_match[2]:
            best_match = (root_note, "minor", minor_score)
    
    return f"{best_match[0]} {best_match[1]}"

def calculate_pattern_score(note_counts, root_value, pattern):
    """Calculate how well the note counts match a given scale pattern"""
    score = 0
    total_notes = sum(note_counts.values())
    
    if total_notes == 0:
        return 0
    
    for interval in pattern:
        target_note_value = (root_value + interval) % 12
        # Find the note name that matches this value
        for note_name, note_value in NOTES.items():
            if note_value == target_note_value and note_name in note_counts:
                # Weight the score by how frequently this note appears
                score += note_counts[note_name]
                break
    
    return score / total_notes
    
