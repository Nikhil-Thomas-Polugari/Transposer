#import fnmatch
import UI
import functions
import os

def main():
  #UI.main_menu()
  functions.split_and_move_files("Music_File.txt")
  dest_folder = os.path.join(os.getcwd(), "Music_Notes")
  dest_file = os.path.join(dest_folder, "Jeinchvarini konipova.txt")
  print(functions.detect_key_signature(dest_file))

if __name__ == '__main__':
  main()
