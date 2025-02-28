from functions import *
import os

def UI():
    song_and_key = {}
    key_signature = ""
    file = "Music_File.txt"
    songs = file_split(file)
    file_move(songs)
    for song_name in songs:
        key_signature = Key_Signeture(os.getcwd() + "/Music_Notes/" + song_name)
        song_and_key[song_name] = key_signature