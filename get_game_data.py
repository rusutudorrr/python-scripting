import os
import json
import shutil
from subprocess import PIPE, run # this will allow us to run any terminal command
import sys # use to get accec to the cmd arguments

GAME_DIR_PATTERN = "game"


def find_game_paths(source):
      games_paths = []

      for root, dirs, files in os.walk(source):
            # os.walk "walks" recursively through the source directory that you pass and returns the root, dirs and files
            for d in dirs:
                  if GAME_DIR_PATTERN in d.lower():
                        game_path = os.path.join(source, d)
                        games_paths.append(game_path)
            break # We only want this func to run once in our case
      return games_paths


def get_name_from_path(paths, remove_from_pathname):
      new_names = []

      for path in paths:
            _, dir_name = os.path.split(path)
            new_dirname = dir_name.replace(remove_from_pathname, '')
            new_names.append(new_dirname) 


def create_target_dir(path):
      if not os.path.exists(path):
            os.mkdir(path)


def main(source, target):
      cwd = os.getcwd()
      source_path = os.path.join(cwd, source)
      # os.path.join() Is great because it will concat your paths depending on your os.
      target_path = os.path.join(cwd, target)

      game_paths = find_game_paths(source_path)
      new_game_dirs = get_name_from_path(game_paths, "_game")
      print(new_game_dirs)

      create_target_dir(target_path)


# This checks if you run the file directly
if __name__ == "__main__":
      args = sys.argv
      if len(args) != 3:
            raise Exception("You must pass a source and a target directory - only")

      source, target = args[1:] # We strip off the name of our file and get the remaining dirs
      main(source, target)
