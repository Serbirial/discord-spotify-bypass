import beautifuldiscord.app as bd
from argparse import ArgumentParser
import os
import shutil

def main():
  # parse CLI arguments
  parser = ArgumentParser('discord-spotify-bypass')
  parser.add_argument('--revert', action='store_true',
    help='undo script injection, restore original discord app.asar')
  args = parser.parse_args()

  # open discord process
  discord: bd.DiscordProcess
  try:
    discord = bd.discord_process()
  except Exception as e:
    print(e)
    return

  # cwd to discord dir
  cwd = os.getcwd()
  os.chdir(discord.script_path)

  # close discord process before making changes
  discord.terminate()

  if not bd.extract_asar():
    discord.launch()
    return

  if args.revert == True:
    bd.revert_changes(discord)
    return
  
  # inject xhr.js script
  load_script = open(f'{cwd}/scripts/load-script.js', 'r').read()
  xhr = open(f'{cwd}/scripts/xhr.js', 'r').read()
  load_xhr = load_script.replace('{}', xhr)
  print(load_xhr)

  # repack app.asar
  bd.repack_asar()

  # relaunch discord
  discord.launch()

  


main()