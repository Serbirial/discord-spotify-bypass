import beautifuldiscord.app as bd
from argparse import ArgumentParser

# parse CLI arguments
parser = ArgumentParser('discord-spotify-bypass')
parser.add_argument('--revert', action='store_false',
  help='undo script injection, restore original discord app.asar')
args = parser.parse_args()

print(args.revert)

discord: bd.DiscordProcess

try:
  discord = bd.discord_process()
except Exception as e:
  print(e)
  exit(1)
