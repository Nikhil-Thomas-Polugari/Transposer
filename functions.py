import os
import shutil
import re

# This function was commented out, but if you want to use it, it's cleaned too.
# def strip_lines(file_in, file_out):
#     patterns = ['|x2', '|x2?', ']x2?', '|', ']x2', ']x4', '|x4', 'Based on congregation']
#     with open(file_in, 'r') as f_in, open(file_out, 'w') as f_out:
#         for line in f_in:
#             for pattern in patterns:
#                 if pattern in line:
#                     line = line.replace(pattern, '')
#             f_out.write(line)

# Map double sharps to correct simple notes
double_sharp_corrections = {
    'C#': 'D',
    'D#': 'E',
    'E#': 'F#',
    'F#': 'G',
    'G#': 'A',
    'A#': 'B',
    'B#': 'C#'
}
'''
def clean_note(word):
    # Separate the note part and the octave number part
    note_part = ''
    number_part = ''

    for char in word:
        if char.isdigit():
            number_part += char
        else:
            note_part += char

    # If double sharp exists (e.g., C##), fix it
    if '##' in note_part:
        base_note = note_part.replace('##', '#')  # D## → D#
        # Fix the single sharp version if possible
        corrected_note = double_sharp_corrections.get(base_note, base_note)
    else:
        corrected_note = note_part

    return corrected_note + number_part
'''
def clean_transposed_song(song_text):
    cleaned_lines = []
    for line in song_text.splitlines():
        cleaned_line = ' '.join(clean_note(word) for word in line.split())
        cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)


def detect_major_or_minor(detected_key, key_counts, last_note=None):
  relative_minors = {
      'C': 'A', 'G': 'E', 'D': 'B', 'A': 'F#', 'E': 'C#', 'B': 'G#',
      'F#': 'D#', 'C#': 'A#', 
      'F': 'D', 'Bb': 'G', 'Eb': 'C', 'Ab': 'F', 'Db': 'Bb', 'Gb': 'Eb', 'Cb': 'Ab'
  }

  if detected_key not in relative_minors:
      return f"{detected_key} major"  # Default to major if no relative minor is found

  minor_tonic = relative_minors[detected_key]

  major_score = key_counts.get(detected_key, 0)
  minor_score = key_counts.get(minor_tonic, 0)

  # Bonus points if last note matches
  if last_note:
      if last_note == detected_key:
          major_score += 3
      elif last_note == minor_tonic:
          minor_score += 3

  if minor_score > major_score:
      return f"{minor_tonic} minor"
  else:
      return f"{detected_key} major"


def clean_note(note):
    return re.sub(r'\d+', '', note)

def detect_key_signature(file):
  key_counts = {note: 0 for note in [
      'F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#',
      'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 'Fb',
      'A', 'B', 'C', 'D', 'E', 'F', 'G'
  ]}

  parsed_lines = []
  with open(file, 'r') as f:
      for line in f:
          if ':' in line:
              continue
          if '#' in line or 'b' in line:
              parsed_lines.append(line.strip().split())

  for tokens in parsed_lines:
      tokens = list(filter(None, tokens))  # Remove empty strings
      for token in tokens:
          # Skip tokens that end with metadata like |x2, |x4, etc.
          if token.endswith(('|x2', '|x4', ']x2', '|')):
              continue
          # Count notes
          if token.endswith(('4', '2')):
              note = token[:-1]
          else:
              note = token
          if note in key_counts:
              key_counts[note] += 1

  

  # Detect key
  key = choose_key(key_counts)

  # Check and adjust based on last note
  last_note = None
  for tokens in reversed(parsed_lines):
      tokens = list(filter(None, tokens))
      for token in reversed(tokens):
          if token.endswith(('|x2', '|x4', ']x2', '|')):
              continue
          if token.endswith(('4', '2')):
              note = token[:-1]
          else:
              note = token
          if note in key_counts:
              last_note = note
              break
      if last_note:
          break

  # Adjust based on last note and relative minor/major
  final_key = detect_major_or_minor(key, key_counts, last_note)
  return final_key



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

def choose_key(counts):
  sharp_order = ["F#", "C#", "G#", "D#", "A#", "E#", "B#"]
  flat_order = ["Bb", "Eb", "Ab", "Db", "Gb", "Cb", "Fb"]

  sharp_count = sum(1 for note in sharp_order if note in counts)
  flat_count = sum(1 for note in flat_order if note in counts)

  if sharp_count > 0 and flat_count == 0:
      keys_by_sharp = ["G", "D", "A", "E", "B", "F#", "C#"]
      signature = keys_by_sharp[sharp_count - 1]
  elif flat_count > 0 and sharp_count == 0:
      keys_by_flat = ["F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"]
      signature = keys_by_flat[flat_count - 1]
  else:
      signature = "C"

  return signature



NOTES = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
    "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11
}
NOTES_REVERSE = {v: k for k, v in NOTES.items()}


# Valid notes mapping, like before
NOTES = {
    'C': 0, 'C#': 1, 'Db': 1,
    'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'Fb': 4, 'E#': 5,
    'F': 5, 'F#': 6, 'Gb': 6,
    'G': 7, 'G#': 8, 'Ab': 8,
    'A': 9, 'A#': 10, 'Bb': 10,
    'B': 11, 'Cb': 11, 'B#': 0,
}

def sanitize_song_file(filepath):
    print(f"Sanitizing {filepath}...")
    note_pattern = re.compile(r'([A-Ga-g])([#b]{0,2})(\d*)')

    with open(filepath, 'r') as f:
        lines = f.readlines()

    sanitized_lines = []
    warnings = []

    for line in lines:
        new_line = ""
        last_idx = 0
        for match in note_pattern.finditer(line):
            start, end = match.span()
            note, accidental, octave = match.groups()
            full_note = note.upper() + accidental

            # Append text before the match
            new_line += line[last_idx:start]

            if full_note not in NOTES:
                # Warn about unrecognized note
                warnings.append(full_note)
                # Replace with safe guess: just use the root note
                new_line += note.upper() + octave
            else:
                new_line += match.group(0)

            last_idx = end

        # Add the rest of the line
        new_line += line[last_idx:]
        sanitized_lines.append(new_line)

    with open(filepath, 'w') as f:
        f.writelines(sanitized_lines)

    if warnings:
        print("⚠️  The following unrecognized notes were found and sanitized:")
        print("   ", sorted(set(warnings)))
    else:
        print("✅ Song sanitized successfully — no unrecognized notes found.")


def transpose_song_text(song_text, full_key, target_key):
  # Extract root note and key type (major/minor)
  root_note, key_type = full_key.split()[0], " ".join(full_key.split()[1:])

  orig_key_num = NOTES[root_note]
  target_key_num = NOTES[target_key]
  difference = target_key_num - orig_key_num

  # Flip the difference if positive
  if difference > 0:
      difference = -difference

  transposed_lines = []

  # Add a header at the top of the file with the full key name
  transposed_lines.append(f"# Transposed to {target_key} {key_type}\n\n")

  lines = song_text.splitlines()

  for line in lines:
      if ':' in line or difference == 0:
          transposed_lines.append(line)
          continue

      # Replace longer notes first to avoid partial replacements
      for note in sorted(NOTES, key=lambda x: -len(x)):
          if note in line:
              new_note = NOTES_REVERSE[(NOTES[note] + difference) % 12]
              line = line.replace(note, new_note)

      transposed_lines.append(line)

  return "\n".join(transposed_lines)

def transpose(songs_and_keys, target_note, target_key_type):
    for song_file, original_key in songs_and_keys.items():
        # Extract root note from the original key (e.g., "C major" → "C")
        original_note = original_key.split()[0]

        if original_note not in NOTES or target_note not in NOTES:
            print(f"Error: Invalid key - {original_note} or {target_note}")
            continue

        orig_key_num = NOTES[original_note]
        target_key_num = NOTES[target_note]
        semitone_shift = (target_key_num - orig_key_num) % 12

        print(f"Transposing {os.path.basename(song_file)} from {original_note} {target_key_type} to {target_note} {target_key_type}...")

        with open(song_file, 'r') as f:
            lines = f.readlines()

        transposed_lines = [f"# Transposed to {target_note} {target_key_type}\n\n"]

        note_pattern = r"\b([A-Ga-g])([#b]?)(\d?)\b"  # e.g., C, C#, C4, C#4

        def transpose_note(match):
            note, accidental, octave = match.groups()
            note = note.upper()
            full_note = note + accidental

            if full_note not in NOTES:
                return match.group(0)  # leave it unchanged if not a known note

            transposed_index = (NOTES[full_note] + semitone_shift) % 12
            transposed_note = NOTES_REVERSE[transposed_index]
            return transposed_note + octave

        for line in lines:
            if ':' in line or semitone_shift == 0:
                transposed_lines.append(line)
            else:
                transposed_line = re.sub(note_pattern, transpose_note, line)
                transposed_lines.append(transposed_line)

        new_filename = f"{os.path.splitext(song_file)[0]}_transposed_to_{target_note}.txt"
        output_path = os.path.join("Music_Notes", os.path.basename(new_filename))

        with open(output_path, 'w') as f:
            f.writelines(transposed_lines)

        print(f"Saved transposed song to {output_path}")
