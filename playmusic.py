#!/usr/bin/python
from os import listdir
from os.path import isfile, join
import sys,random,os,pygame

if __name__ == "__main__":
	onlyfile = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1],f))]
	mp3file = []
	for i in onlyfile:
		mp3file.append(sys.argv[1]+""+i)
	while len(mp3file)> 0:
		file_to_play = random.choice(mp3file)
		print file_to_play
		os.system("omxplayer "+file_to_play)
		mp3file.remove(file_to_play)
