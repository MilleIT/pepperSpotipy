import sys
import random
import spotipy
import spotipy.util as util
import zerorpc
import pdfkit

import PlaylistLoader as Loader
from node_connector import python_server as Server

import CardGenerator as Generator
import requests
import json

class Main:

    def __init__(self):
        self.target_device = True

    def run(self):

        # user = raw_input("wat is your username?")
        sp = spotipy.Spotify()
        # usrnm = sp.user(user)
        # print usrnm

        # print r.history.headers
        scope = 'user-read-recently-played user-read-currently-playing user-read-playback-state app-remote-control user-modify-playback-state streaming'# playlist-read-private'
        # username = 'fazzh49d3su4s342ivmxbb74m'
        username = '1120296237'
        token = util.prompt_for_user_token(username, scope, client_id='e7c8d90f7d5246089e8e0e1f6274f07b',
                                           client_secret='9dfb0745d7304355b40d8e373d19c1b6',
                                           redirect_uri='http://localhost/')

        if token:
            spotify = spotipy.Spotify(auth=token)
            devices = spotify.devices()
            #print devices
            if self.target_device:
                for device in devices['devices']:
                    if device['name'] == "MILLENLAPTOP": #"DESKTOP-4RSNA5J":
                        deviceID = device['id']
            else:
                deviceID = devices['devices'][0]['id']
            loader = Loader.Loader(username, spotify)
            playlist = loader.load('5gGIKJ3e0uuGr7e4I0TAnY')
            print playlist
            self.createBingocards(playlist)
            pserver = Server.Server(username, spotify, deviceID, playlist)
            server = zerorpc.Server(pserver)
            print "binding server to: tcp://0.0.0.0:4242"
            server.bind("tcp://0.0.0.0:4242")
            print "starting server"
            server.run()
            # player.play(playlist, 5)

        else:
            print "Can't get token for", username


    def createBingocards(self, playlist):
        Terms = open("bingo_terms.txt", "w")
        for track in playlist:
            song = track[0]
            artist = track[1]
            line = song + ":"+ artist + "\n"
            Terms.write(line)
        Terms.close()
        generator = Generator.Generator("bingo_terms.txt" ,"bingo.html", 12)
        #generator.readTerms()
        generator.start()


if __name__ == "__main__":
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        sys.exit(1)
