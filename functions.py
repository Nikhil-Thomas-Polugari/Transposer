import os
import shutil
'''
def strip_lines(file, file2):
  with open(file, 'r') as f:
    lines = f.readlines()
  with open(file2, 'w') as f:
    for line in lines:
      if line.__contains__('|x2'):
        line = line.replace('|x2', '')
        f.write(line)
      elif line.__contains__('|x2?'):
        line = line.replace('|x2?', '')
        f.write(line)
      elif line.__contains__(']x2?'):
        line = line.replace(']x2?', '')
        f.write(line)
      elif line.__contains__('|'):
        line = line.replace('|', '')
        f.write(line)
      elif line.__contains__(']x2'):
        line = line.replace(']x2', '')
        f.write(line)
      elif line.__contains__(']x4'):
        line = line.replace(']x4', '')
        f.write(line)
      elif line.__contains__('|x4'):
        line = line.replace('|x4', '')
        f.write(line)
      elif line.__contains__('Based on congregation'):
        line = line.replace('Based on congregation', '')
        f.write(line)
      else:
        f.write(line)
'''


def Key_Signeture(file):
  key_sig = {
      'F#': 0,
      'C#': 0,
      'G#': 0,
      'D#': 0,
      'A#': 0,
      'E#': 0,
      'B#': 0,
      'Bb': 0,
      'Eb': 0,
      'Ab': 0,
      'Db': 0,
      'Gb': 0,
      'Cb': 0,
      'Fb': 0,
      'A': 0,
      'B': 0,
      'C': 0,
      'D': 0,
      'E': 0,
      'F': 0,
      'G': 0
  }
  line_split = []
  line_split_temp = []
  #file_name = os.getcwd() + "/Music_Notes/" + file
  with open(file, 'r') as f:
    lines = f.readlines()
    for str in lines:
      if str.__contains__(':'):
        continue
      if str.__contains__('#'):
        str2 = str.strip('\t\n')
        line_split.append(str2.split())
  print(line_split)

  for i in line_split:
    j = list(filter(None, i))
    line_split_temp.append(j)
  line_split = line_split_temp
  for i in line_split:
    print(i)
    for j in i:
      print(j)
      if j[len(line_split) -
           1] == "|x2" or j[len(line_split) - 1] == "|x2?" or j[
               len(line_split) - 1] == "]x2" or j[len(line_split) - 1] == "|":
        continue
      if j.endswith('3'):
        key_sig[j[0:j.find('3')]] += 1
      elif j.endswith('2'):
        key_sig[j[0:j.find('2')]] += 1
  for i in line_split:
    for k in i:
      if k in key_sig:
        key_sig[k] += 1

  sig = sharps_or_flats(key_sig)
  
  return sig


def file_split(file):
  titles_list = []
  song_list = []
  unchanged_song_list = []
  unchanged_song_list_index = []
  with open(file, 'r') as f:
    lines = f.readlines()
    for str in lines:
      if str.__contains__(':'):
        unchanged_song_list.append(str)
        title = str[0:str.find(':')]
        file_name = title + '.txt'
        titles_list.append(file_name)
        song_list.append(title)

  for song in unchanged_song_list:
    unchanged_song_list_index.append(lines.index(song))

  for i in range(len(unchanged_song_list_index)):
    if i == len(unchanged_song_list_index) - 1:
      with open(titles_list[i], 'w') as f:
        for line in lines[unchanged_song_list_index[i]:]:
          f.write(line)
    else:
      with open(titles_list[i], 'w') as f:
        for line in lines[
            unchanged_song_list_index[i]:unchanged_song_list_index[i + 1]]:
          f.write(line)
  return titles_list


def file_move(titles_list):
  for title in titles_list:
    shutil.move(os.getcwd() + "/" + title,
                os.getcwd() + "/Music_Notes/" + title)


def sharps_or_flats(signature):
  sharps = {}
  flats = {}
  naturals = {}
  farthest_sharp = ""
  farthest_flat = ""
  signeture = ""
  for i in signature:
    if i.__contains__("#"):
      sharps[i] = signature.get(i)
    elif i.__contains__("b"):
      flats[i] = signature.get(i)
    else:
      naturals[i] = signature.get(i)

  for note, occurence in sharps.items():
    if occurence > 0:
      farthest_sharp = note

  for note, occurence in flats.items():
    if occurence > 0:
      farthest_flat = note
  if farthest_sharp != "":
    if sharps.get(farthest_sharp) > naturals.get(
        farthest_sharp[0:farthest_sharp.find('#')]):
      if farthest_sharp == "B#":
        signeture = "C#"
      elif farthest_sharp == "E#":
        signeture = "F#"
      elif farthest_sharp == "A#":
        signeture = "B"
      elif farthest_sharp == "D#":
        signeture = "E"
      elif farthest_sharp == "G#":
        signeture = "A"
      elif farthest_sharp == "C#":
        signeture = "D"
      else:
        signeture = "G"
  elif farthest_flat != "":
    if flats.get(farthest_flat) > naturals.get(
        farthest_flat[0:farthest_flat.find('b')]):
      if farthest_flat == "Bb":
        signeture = "F"
      elif farthest_flat == "Eb":
        signeture = "Bb"
      elif farthest_flat == "Ab":
        signeture = "Eb"
      elif farthest_flat == "Db":
        signeture = "Ab"
      elif farthest_flat == "Gb":
        signeture = "Db"
      elif farthest_flat == "Cb":
        signeture = "Bb"
      else:
        signeture = "Cb"
  elif farthest_sharp == "":
    signeture = "C"
  elif farthest_flat == "":
    signeture = "C"
    
  return signeture


NOTES = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11
}

NOTES_REVERSE = {v: k for k, v in NOTES.items()}


def transpose(songs_and_keys, key_sig):
  for song, key in songs_and_keys.items():
    key_num = NOTES[key]
    key_sig_num = NOTES[key_sig]
    
    