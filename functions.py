import os
import shutil
import re

NOTES = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "Fb": 4, "E#": 5, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11, "Cb": 11, "B#": 0}

def split_and_move_files(file, destination_place):
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

    dest_folder = os.path.join(os.getcwd(), destination_place)
    for title in titles:
        shutil.move(os.path.join(os.getcwd(), title), os.path.join(dest_folder, title))


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


def song_transpose(input_filepath, target_note, target_scale, output_filepath=None):
    """
    Transpose a song to a target note and scale pattern.
    Handles octave indicators (2 for below, 4 for above).

    Args:
        input_filepath (str): Path to the input song file
        target_note (str): Target root note (e.g., "Bb", "C#")
        target_scale (str): Target scale pattern ("major", "minor", etc.)
        output_filepath (str): Output file path (optional, defaults to input_file_transposed.txt)
    """
    if output_filepath is None:
        base_name = os.path.splitext(input_filepath)[0]
        # Create filename with format: songname_transposed_to_key_scale.txt
        target_key = f"{target_note}_{target_scale}".replace("#", "sharp").replace("b", "flat").replace(" ", "_")
        output_filepath = f"{base_name}_transposed_to_{target_key}.txt"

    # Detect the current key of the song
    current_key_str = detect_key_signature(input_filepath)
    current_parts = current_key_str.split()
    current_note = current_parts[0]
    current_scale = current_parts[1]

    # Calculate the transposition interval
    current_root_value = NOTES[current_note]
    target_root_value = NOTES[target_note]
    transpose_interval = (target_root_value - current_root_value) % 12

    # Read the original song content
    with open(input_filepath, 'r') as f:
        content = f.read()

    # Function to transpose a single note
    def transpose_note(match):
        note_with_octave = match.group(0)
        note_name = match.group(1)

        # Extract octave indicator if present
        octave_match = re.search(r'(\d+)$', note_with_octave)
        current_octave = int(octave_match.group(1)) if octave_match else 3  # Default to middle octave

        # Get the chromatic value of the original note
        original_value = NOTES[note_name]

        # Calculate the new chromatic value
        new_value = (original_value + transpose_interval) % 12

        # Find the best enharmonic spelling for the new note
        new_note_name = get_best_note_name(new_value, target_note, target_scale)

        # Calculate octave change
        octave_change = 0
        if original_value + transpose_interval >= 12:
            octave_change = (original_value + transpose_interval) // 12
        elif original_value + transpose_interval < 0:
            octave_change = -1

        new_octave = current_octave + octave_change

        # Handle octave indicators
        if new_octave == 2:
            return f"{new_note_name}2"
        elif new_octave == 4:
            return f"{new_note_name}4"
        elif new_octave != 3:  # Only add octave indicator if not middle octave
            return f"{new_note_name}{new_octave}"
        else:
            return new_note_name

    # Pattern to match notes with optional octave indicators
    note_pattern = r'\b([A-G](?:#|b)?)(\d*)\b'

    # Replace all notes in the content
    transposed_content = re.sub(note_pattern, transpose_note, content)

    # Write the transposed content to the output file
    with open(output_filepath, 'w') as f:
        f.write(transposed_content)

    print(f"Song transposed from {current_key_str} to {target_note} {target_scale}")
    print(f"Transposed song saved to: {output_filepath}")

    return output_filepath


def get_best_note_name(chromatic_value, target_root, target_scale):
    """
    Get the best enharmonic spelling for a note based on the target key signature.
    """
    # Common note names for each chromatic value
    note_options = {
        0: ["C", "B#"],
        1: ["C#", "Db"],
        2: ["D"],
        3: ["D#", "Eb"],
        4: ["E", "Fb"],
        5: ["F", "E#"],
        6: ["F#", "Gb"],
        7: ["G"],
        8: ["G#", "Ab"],
        9: ["A"],
        10: ["A#", "Bb"],
        11: ["B", "Cb"]
    }

    # Get possible note names
    possible_names = note_options.get(chromatic_value, [])

    if len(possible_names) == 1:
        return possible_names[0]

    # Prefer spellings that match the key signature context
    target_root_value = NOTES[target_root]

    # For major keys, prefer sharps for sharp keys, flats for flat keys
    if target_scale == "major":
        # Sharp keys: G, D, A, E, B, F#, C#
        if target_root in ["G", "D", "A", "E", "B", "F#", "C#"]:
            # Prefer sharp spellings
            for name in possible_names:
                if "#" in name:
                    return name
        # Flat keys: F, Bb, Eb, Ab, Db, Gb, Cb
        elif target_root in ["F", "Bb", "Eb", "Ab", "Db", "Gb"]:
            # Prefer flat spellings
            for name in possible_names:
                if "b" in name:
                    return name

    # Default to the first option
    return possible_names[0]