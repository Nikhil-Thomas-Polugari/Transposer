import os
import re
from functions import split_and_move_files, detect_key_signature, song_transpose

def get_target_key():
    NOTES = {
        'C': 0, 'C#': 1, 'Db': 1,
        'D': 2, 'D#': 3, 'Eb': 3,
        'E': 4, 'Fb': 4, 'E#': 5,
        'F': 5, 'F#': 6, 'Gb': 6,
        'G': 7, 'G#': 8, 'Ab': 8,
        'A': 9, 'A#': 10, 'Bb': 10,
        'B': 11, 'Cb': 11, 'B#': 0,
    }

    while True:
        target_key_input = input("Enter the key to transpose to (e.g., C major, D# minor): ").strip()
        parts = target_key_input.split()
        if len(parts) != 2:
            print("Please enter the key in the format: NOTE major/minor (e.g., C major)")
            continue

        note, key_type = parts[0], parts[1].lower()
        if note not in NOTES:
            print(f"Unrecognized note: {note}. Try again.")
            continue
        if key_type not in ["major", "minor", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "harmonic minor", "melodic minor"]:
            print(f"Invalid key type: {key_type}. Supported types: major, minor, dorian, phrygian, lydian, mixolydian, aeolian, harmonic minor, melodic minor")
            continue

        return note, key_type

def list_songs(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.txt') and 'transposed' not in f]
    return files

def list_transposed_songs(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.txt') and 'transposed' in f]
    return files

def display_song(filepath):
    with open(filepath, 'r') as f:
        print(f.read())

def analyze_song_key(filepath):
    """Analyze and display detailed key signature information"""
    detected_key = detect_key_signature(filepath)
    print(f"\nDetected Key Signature: {detected_key}")
    
    # Show note frequencies for analysis
    with open(filepath, 'r') as f:
        content = f.read()
        note_pattern = r'\b([A-G](?:#|b)?)(\d*)\b'
        matches = re.findall(note_pattern, content)
        
        note_counts = {}
        for note, octave in matches:
            full_note = note + octave if octave else note
            note_counts[full_note] = note_counts.get(full_note, 0) + 1
        
        if note_counts:
            print("\nNote frequency analysis:")
            sorted_notes = sorted(note_counts.items(), key=lambda x: x[1], reverse=True)
            for note, count in sorted_notes:
                print(f"  {note}: {count} times")

def main_menu():
    music_file = "Music_File.txt"
    music_folder = "Music_Notes"

    if not os.path.exists(music_folder):
        os.makedirs(music_folder)

    if os.path.exists(music_file):
        split_and_move_files(music_file, music_folder)

    while True:
        print("\n" + "="*50)
        print("MUSIC ANALYSIS & TRANSPOSITION TOOL")
        print("="*50)
        print("1. Refresh song list from Music_File.txt")
        print("2. Display a song")
        print("3. Analyze song key signature")
        print("4. Transpose a song")
        print("5. View transposed songs")
        print("6. Compare original and transposed versions")
        print("7. Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            if os.path.exists(music_file):
                split_and_move_files(music_file, music_folder)
                print("✓ Song list refreshed from Music_File.txt!")
            else:
                print("❌ Music_File.txt not found!")

        elif choice == '2':
            songs = list_songs(music_folder)
            if not songs:
                print("❌ No songs available.")
                continue

            print(f"\nAvailable songs ({len(songs)} total):")
            for idx, song in enumerate(songs, 1):
                print(f"{idx:2d}. {song}")

            song_choice = input("\nEnter the number of the song to display: ")
            if song_choice.isdigit() and 1 <= int(song_choice) <= len(songs):
                selected_song = songs[int(song_choice) - 1]
                filepath = os.path.join(music_folder, selected_song)
                
                print(f"\n{'='*60}")
                print(f"DISPLAYING: {selected_song}")
                print(f"{'='*60}")
                display_song(filepath)
                print(f"{'='*60}")
            else:
                print("❌ Invalid choice.")

        elif choice == '3':
            songs = list_songs(music_folder)
            if not songs:
                print("❌ No songs available to analyze.")
                continue

            print(f"\nAvailable songs ({len(songs)} total):")
            for idx, song in enumerate(songs, 1):
                print(f"{idx:2d}. {song}")

            song_choice = input("\nEnter the number of the song to analyze: ")
            if song_choice.isdigit() and 1 <= int(song_choice) <= len(songs):
                selected_song = songs[int(song_choice) - 1]
                filepath = os.path.join(music_folder, selected_song)
                
                print(f"\n{'='*60}")
                print(f"ANALYZING: {selected_song}")
                print(f"{'='*60}")
                analyze_song_key(filepath)
            else:
                print("❌ Invalid choice.")

        elif choice == '4':
            songs = list_songs(music_folder)
            if not songs:
                print("❌ No songs available to transpose.")
                continue

            print(f"\nAvailable songs ({len(songs)} total):")
            for idx, song in enumerate(songs, 1):
                print(f"{idx:2d}. {song}")

            song_choice = input("\nEnter the number of the song to transpose: ")
            if song_choice.isdigit() and 1 <= int(song_choice) <= len(songs):
                selected_song = songs[int(song_choice) - 1]
                filepath = os.path.join(music_folder, selected_song)

                print(f"\n{'='*60}")
                print(f"TRANSPOSING: {selected_song}")
                print(f"{'='*60}")

                # Get current key signature
                current_key = detect_key_signature(filepath)
                print(f"Current key: {current_key}")

                # Get target key
                note, key_type = get_target_key()
                
                # Use the song_transpose function
                output_file = song_transpose(filepath, note, key_type)
                print(f"\n✓ Successfully transposed!")
                print(f"Original: {selected_song}")
                print(f"Transposed: {os.path.basename(output_file)}")
            else:
                print("❌ Invalid choice.")

        elif choice == '5':
            transposed_songs = list_transposed_songs(music_folder)
            if not transposed_songs:
                print("❌ No transposed songs available.")
                continue

            print(f"\nTransposed songs ({len(transposed_songs)} total):")
            for idx, song in enumerate(transposed_songs, 1):
                print(f"{idx:2d}. {song}")

            song_choice = input("\nEnter the number of the transposed song to display: ")
            if song_choice.isdigit() and 1 <= int(song_choice) <= len(transposed_songs):
                selected_song = transposed_songs[int(song_choice) - 1]
                filepath = os.path.join(music_folder, selected_song)
                
                print(f"\n{'='*60}")
                print(f"DISPLAYING TRANSPOSED: {selected_song}")
                print(f"{'='*60}")
                display_song(filepath)
                
                # Also show key analysis
                analyze_song_key(filepath)
                print(f"{'='*60}")
            else:
                print("❌ Invalid choice.")

        elif choice == '6':
            # Compare original and transposed versions
            original_songs = list_songs(music_folder)
            transposed_songs = list_transposed_songs(music_folder)
            
            if not original_songs or not transposed_songs:
                print("❌ Need both original and transposed songs for comparison.")
                continue

            print(f"\nOriginal songs ({len(original_songs)} total):")
            for idx, song in enumerate(original_songs, 1):
                print(f"{idx:2d}. {song}")

            original_choice = input("\nSelect original song: ")
            if not (original_choice.isdigit() and 1 <= int(original_choice) <= len(original_songs)):
                print("❌ Invalid choice.")
                continue

            print(f"\nTransposed songs ({len(transposed_songs)} total):")
            for idx, song in enumerate(transposed_songs, 1):
                print(f"{idx:2d}. {song}")

            transposed_choice = input("\nSelect transposed song: ")
            if not (transposed_choice.isdigit() and 1 <= int(transposed_choice) <= len(transposed_songs)):
                print("❌ Invalid choice.")
                continue

            original_song = original_songs[int(original_choice) - 1]
            transposed_song = transposed_songs[int(transposed_choice) - 1]
            
            original_path = os.path.join(music_folder, original_song)
            transposed_path = os.path.join(music_folder, transposed_song)

            print(f"\n{'='*80}")
            print(f"COMPARISON: {original_song} vs {transposed_song}")
            print(f"{'='*80}")
            
            print(f"\nORIGINAL ({original_song}):")
            print("-" * 40)
            current_key = detect_key_signature(original_path)
            print(f"Key: {current_key}")
            display_song(original_path)
            
            print(f"\nTRANSPOSED ({transposed_song}):")
            print("-" * 40)
            transposed_key = detect_key_signature(transposed_path)
            print(f"Key: {transposed_key}")
            display_song(transposed_path)
            
            print(f"{'='*80}")

        elif choice == '7':
            print("\n👋 Thank you for using the Music Analysis & Transposition Tool!")
            print("Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main_menu()
