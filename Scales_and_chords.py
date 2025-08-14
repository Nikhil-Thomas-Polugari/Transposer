
NOTES = {
    'C': 0, 'C#': 1, 'Db': 1,
    'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'Fb': 4, 'E#': 5,
    'F': 5, 'F#': 6, 'Gb': 6,
    'G': 7, 'G#': 8, 'Ab': 8,
    'A': 9, 'A#': 10, 'Bb': 10,
    'B': 11, 'Cb': 11, 'B#': 0,
}

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


def scale_display(root_note, scale_type):
    """
    Display the notes in a scale pattern.
    
    Args:
        root_note (str): The root note of the scale (e.g., "C", "Bb", "F#")
        scale_type (str): The type of scale ("major", "minor", etc.)
    
    Returns:
        list: List of notes in the scale
    """
    # Scale patterns from detect_key_signature function
    SCALE_PATTERNS = {
        "major": [0, 2, 4, 5, 7, 9, 11],          # 1 2 3 4 5 6 7
        "natural_minor": [0, 2, 3, 5, 7, 8, 10],  # 1 2 b3 4 5 b6 b7
        "minor": [0, 2, 3, 5, 7, 8, 10],          # Alias for natural_minor
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11], # 1 2 b3 4 5 b6 7
        "melodic_minor": [0, 2, 3, 5, 7, 9, 11],  # 1 2 b3 4 5 6 7
        "dorian": [0, 2, 3, 5, 7, 9, 10],         # 1 2 b3 4 5 6 b7
        "phrygian": [0, 1, 3, 5, 7, 8, 10],       # 1 b2 b3 4 5 b6 b7
        "lydian": [0, 2, 4, 6, 7, 9, 11],         # 1 2 3 #4 5 6 7
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],     # 1 2 3 4 5 6 b7
        "aeolian": [0, 2, 3, 5, 7, 8, 10]         # 1 2 b3 4 5 b6 b7
    }
    
    if scale_type not in SCALE_PATTERNS:
        return f"Scale type '{scale_type}' not recognized"
    
    if root_note not in NOTES:
        return f"Root note '{root_note}' not recognized"
    
    root_value = NOTES[root_note]
    pattern = SCALE_PATTERNS[scale_type]
    
    scale_notes = []
    for interval in pattern:
        note_value = (root_value + interval) % 12
        # Get the best enharmonic spelling for this scale
        note_name = get_best_note_name(note_value, root_note, scale_type)
        scale_notes.append(note_name)
    
    return scale_notes


def chord_family(root_note, scale_type):
    """
    Display the chord family for a given scale.
    Shows the triads built on each degree of the scale.
    
    Args:
        root_note (str): The root note of the scale (e.g., "C", "Bb", "F#")
        scale_type (str): The type of scale ("major", "minor", etc.)
    
    Returns:
        dict: Dictionary with chord names and their notes
    """
    # Get the scale notes
    scale_notes = scale_display(root_note, scale_type)
    if isinstance(scale_notes, str):  # Error message
        return scale_notes
    
    # Roman numeral names for each degree
    roman_numerals = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
    
    # For minor and modal scales, adjust roman numerals
    if scale_type in ["minor", "natural_minor", "aeolian"]:
        roman_numerals = ["i", "ii°", "III", "iv", "v", "VI", "VII"]
    elif scale_type == "harmonic_minor":
        roman_numerals = ["i", "ii°", "III+", "iv", "V", "VI", "vii°"]
    elif scale_type == "dorian":
        roman_numerals = ["i", "ii", "III", "IV", "v", "vi°", "VII"]
    elif scale_type == "phrygian":
        roman_numerals = ["i", "II", "III", "iv", "v°", "VI", "vii"]
    elif scale_type == "lydian":
        roman_numerals = ["I", "II", "iii", "iv°", "V", "vi", "vii"]
    elif scale_type == "mixolydian":
        roman_numerals = ["I", "ii", "iii°", "IV", "v", "vi", "VII"]
    
    chord_family_dict = {}
    
    for i in range(len(scale_notes)):
        # Build triad: root, third, fifth (1st, 3rd, 5th degrees)
        root = scale_notes[i]
        third = scale_notes[(i + 2) % len(scale_notes)]
        fifth = scale_notes[(i + 4) % len(scale_notes)]
        
        # Determine chord quality
        root_value = NOTES[root]
        third_value = NOTES[third]
        fifth_value = NOTES[fifth]
        
        # Calculate intervals
        third_interval = (third_value - root_value) % 12
        fifth_interval = (fifth_value - root_value) % 12
        
        # Determine chord type
        if third_interval == 4 and fifth_interval == 7:
            chord_type = "major"
            chord_symbol = ""
        elif third_interval == 3 and fifth_interval == 7:
            chord_type = "minor"
            chord_symbol = "m"
        elif third_interval == 3 and fifth_interval == 6:
            chord_type = "diminished"
            chord_symbol = "°"
        elif third_interval == 4 and fifth_interval == 8:
            chord_type = "augmented"
            chord_symbol = "+"
        else:
            chord_type = "other"
            chord_symbol = "?"
        
        chord_name = f"{root}{chord_symbol}"
        chord_notes = [root, third, fifth]
        
        chord_family_dict[f"{roman_numerals[i]} ({chord_name})"] = {
            "notes": chord_notes,
            "type": chord_type
        }
    
    return chord_family_dict
