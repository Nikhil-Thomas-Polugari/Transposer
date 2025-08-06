import os
import shutil
import re

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


def detect_key_signature(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        key_signature = re.search(r'Key Signature: (\w+)', content)
        if key_signature:
            return key_signature.group(1)
        else:
            return None  # or handle the case where key signature is not found
            


def transpose(songs_and_keys, target_note, target_key_type, octave_base=3):
    NOTES = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "Fb": 4, "E#": 5, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11, "Cb": 11, "B#": 0}
    NOTES_LIST = list(NOTES.keys())
    MAJOR_SCALE = [1, 2, 4, 5, 7, 9, 11, 0]
    MINOR_SCALE = [1, 2, 3, 5, 7, 8, 10, 0]
    song_contents = []
    file_extention_addition = f'_transposed_to_{target_note}_{target_key_type}.txt'
    
