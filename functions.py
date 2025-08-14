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
    NOTES_SHARP = {"F#" : 0, "C#" : 0, "G#" : 0, "D#" : 0, "A#" : 0, "E#" : 0, "B#" : 0}
    NOTES_FLAT = {"Bb" : 0, "Eb" : 0, "Ab" : 0, "Db" : 0, "Gb" : 0, "Cb" : 0, "Fb" : 0}
    NOTES_NATURAL = {"B" : 0, "E" : 0, "A" : 0, "D" : 0, "G" : 0, "C" : 0, "F" : 0}
    with open(filepath, 'r') as f:
        content = f.read()
        for note in NOTES_SHARP:
            if note in content:
                NOTES_SHARP[note] += 1
        for note in NOTES_FLAT:
            if note in content:
                NOTES_FLAT[note] += 1
        for note in NOTES_NATURAL:
            if note in content:
                NOTES_NATURAL[note] += 1
    
