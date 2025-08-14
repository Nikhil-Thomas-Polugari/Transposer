import os
import re
from functions import *

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
        if key_type not in ["major", "minor"]:
            print(f"Invalid key type: {key_type}. Use 'major' or 'minor'.")
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

def main_menu():
    music_file = "Music_file.txt"
    music_folder = "Music_Notes"
    songs_and_keys = {}

    if not os.path.exists(music_folder):
        os.makedirs(music_folder)

    if os.path.exists(music_file):
        split_and_move_files(music_file, music_folder)

    while True:
        print("\nMain Menu")
        print("1. Refresh song list")
        print("2. Display a song")
        print("3. Transpose a song")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            split_and_move_files(music_file)
            print("Song list refreshed!")

        elif choice == '2':
            songs = list_songs(music_folder)
            if not songs:
                print("No songs available.")
                continue

            print("\nAvailable songs:")
            for idx, song in enumerate(songs, 1):
                print(f"{idx}. {song}")

            song_choice = input("Enter the number of the song to display: ")
            if song_choice.isdigit() and 1 <= int(song_choice) <= len(songs):
                selected_song = songs[int(song_choice) - 1]
                filepath = os.path.join(music_folder, selected_song)

                with open(filepath, 'r') as f:
                    print(f"\nContents of {selected_song}:\n")
                    print(f.read())
            else:
                print("Invalid choice.")

        elif choice == '3':
            songs = list_songs(music_folder)
            if not songs:
                print("No songs available to transpose.")
                continue

            print("\nAvailable songs:")
            for idx, song in enumerate(songs, 1):
                print(f"{idx}. {song}")

            song_choice = input("Enter the number of the song to transpose: ")
            if song_choice.isdigit() and 1 <= int(song_choice) <= len(songs):
                selected_song = songs[int(song_choice) - 1]
                filepath = os.path.join(music_folder, selected_song)

                # Get current key signature
                current_key = detect_key_signature(filepath)
                print(f"Current key: {current_key}")

                # Get target key
                note, key_type = get_target_key()
                
                # Use the new song_transpose function
                from functions import song_transpose
                song_transpose(filepath, note, key_type)
            else:
                print("Invalid choice.")

        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")