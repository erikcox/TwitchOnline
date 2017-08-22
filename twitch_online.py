import urllib.request
import urllib.parse
import json
import sys

# Check if the right amount of arguments are passed in
if len(sys.argv) < 2:
    print("Error: Please run the script with the following:")
    print("python3 twitch_online.py TWITCH_USERNAME")
    exit()

user = sys.argv[1]
file = open("twitch_client_id.txt", 'r')
client_id = file.readline().strip()
base_url = "https://api.twitch.tv/kraken/"
follows_url = base_url + "users/" + user + "/follows/channels?sortby=last_broadcast"
follows_request = urllib.request.Request(follows_url)
follows_request.add_header("Client-ID", client_id)


# Colors for command line formatting
class Colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    UNDERLINE = '\033[4m'
    ENDCOLOR = '\033[0m'


# Streamer class
class Streamer(object):
    def __init__(self, name, game, viewers, logo):
        self.name = name
        self.game = game
        self.viewers = str(viewers)
        self.logo = logo

    def print_info(self):
        print(
            Colors.BLUE + self.name + Colors.ENDCOLOR + " is streaming " + Colors.UNDERLINE + self.game + Colors.ENDCOLOR + " for " + Colors.RED + self.viewers + Colors.ENDCOLOR + " viewers")


# Create a json query
def make_query(request):
    resp = urllib.request.urlopen(request)
    data = resp.read().decode('utf-8')
    j_data = json.loads(data)
    return j_data


# Make an array of following streamers
def get_following():
    following = []
    for i in range(len(follows_data['follows'])):
        following.append(follows_data['follows'][i]['channel']['display_name'])
    return following


# Check to see if followed streamers are online
def is_live(data):
    live_streamers = []
    for i in range(len(data['streams'])):
        name = data['streams'][i]['channel']['display_name']
        game = data['streams'][i]['game']
        viewers = data['streams'][i]['viewers']
        logo = data['streams'][i]['channel']['logo']
        live_streamers.append(Streamer(name, game, viewers, logo))

    live_streamers.reverse()
    return live_streamers


# Make a new json query
follows_data = make_query(follows_request)
followed_streamers = get_following()

streams_url = base_url + "streams?channel=" + ",".join(followed_streamers)
streams_request = urllib.request.Request(streams_url)
streams_request.add_header("Client-ID", client_id)
streams_data = make_query(streams_request)

print("These are the live streamers that " + Colors.PURPLE + user + Colors.ENDCOLOR + " is following:")
for streamer in is_live(streams_data):
    streamer.print_info()

# TODO: add check to see if user exists and have 'nobody online' message if no streamers are online
