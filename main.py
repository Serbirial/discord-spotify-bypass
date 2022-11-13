import beautifuldiscord.app as bd
from safe_asr import SafeASR
from argparse import ArgumentParser
import os
import shutil
import textwrap

def xhr_script(cwd: str) -> str:
  load_script = open(f'{cwd}/scripts/load-script.js', 'r').read()
  xhr = open(f'{cwd}/scripts/xhr.js').read()
  return load_script.replace('{}',
    '\n' + textwrap.indent(xhr, ' ' * 4))

def inject_script(discord: bd.DiscordProcess, script: str) -> None:
  # TODO: accomplish script injection using text r/w instead of binary
  script_file = open(discord.script_file, 'rb').read()
  # get injection index
  index = script_file.index(b'mainWindow.on(\'blur\'')
  # to quote bd's repo: yikes
  final = script_file[:index] + script.encode('utf-8') + script_file[index:]
  open(discord.script_file, 'wb').write(final)

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

  if args.revert == True:
    SafeASR.restore_backup() 
    discord.launch()
    return

  if not SafeASR.extract_asr():
    discord.launch()
    return

  # inject xhr.js script
  inject_script(discord, xhr_script(cwd))

  # repack app.asar
  bd.repack_asar()

  print('script injection was successful')

  # relaunch discord
  discord.launch()

main()
