import os
import json
import shutil
from subprocess import PIPE, run # this will allow us to run any terminal command
import sys # use to get accec to the cmd arguments

GAME_DIR_PATTERN = "game"

GAME_CODE_EXTENSION = ".go"

COMPILE_COMMAND = ['go', 'build']


def find_game_paths(source):
      game_paths = []

      for root, dirs, files in os.walk(source):
            # os.walk "walks" recursively through the source directory that you pass and returns the root, dirs and files
            for directory in dirs:
                  if GAME_DIR_PATTERN in directory.lower():
                        game_path = os.path.join(source, directory)
                        game_paths.append(game_path)
            break # We only want this func to run once in our case
      return game_paths


def get_name_from_path(paths, remove_from_pathname):
      new_names = []

      for path in paths:
            _, dir_name = os.path.split(path)
            new_dirname = dir_name.replace(remove_from_pathname, '')
            new_names.append(new_dirname) 
      
      return new_names


def create_target_dir(path):
      if not os.path.exists(path):
            os.mkdir(path)


def copy_and_override(source, dest):
      if os.path.exists(dest):
            shutil.rmtree(dest) # rmtree works like a recursive delete
      shutil.copytree(source, dest)


def make_json_metadata_file(path, game_dirs):
      data = {
            "gameNames": game_dirs,
            "numberOfGames": len(game_dirs)
      }

      with open (path, "w") as file:
            json.dump(data, file)


def compile_game_code(path):
    code_file_name = None

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break

        if code_file_name is None:
            return
    
    command = COMPILE_COMMAND + [code_file_name]
    run_command(command, path)


def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("Compile result: ", result)

    os.chdir(cwd)

def main(source, target):
      cwd = os.getcwd()
      source_path = os.path.join(cwd, source)
      # os.path.join() Is great because it will concat your paths depending on your os.
      target_path = os.path.join(cwd, target)

      game_paths = find_game_paths(source_path)
      new_game_dirs = get_name_from_path(game_paths, "_game")

      create_target_dir(target_path)
      
      for src, dest in zip(game_paths, new_game_dirs):
            dest_path = os.path.join(target_path, dest)
            copy_and_override(src, dest_path)
            compile_game_code(dest_path)

      json_path = os.path.join(target_path, "metadata.json")
      make_json_metadata_file(json_path, new_game_dirs)


# This checks if you run the file directly
if __name__ == "__main__":
      args = sys.argv
      if len(args) != 3:
            raise Exception("You must pass a source and a target directory - only")

      source, target = args[1:] # We strip off the name of our file and get the remaining dirs
      main(source, target)
