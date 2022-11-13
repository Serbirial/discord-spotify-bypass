import beautifuldiscord.app as bd
from argparse import ArgumentParser

def main():
  # parse CLI arguments
  parser = ArgumentParser('discord-spotify-bypass')
  parser.add_argument('--revert', action='store_false',
    help='undo script injection, restore original discord app.asar')
  args = parser.parse_args()

  # open discord process
  discord: bd.DiscordProcess
  try:
    discord = bd.discord_process()
  except Exception as e:
    print(e)
    return

  if args.revert:
    bd.revert_changes(discord)
    return

main()