#!/usr/bin/python
import os
import sys

files = os.listdir(sys.argv[1])
for f in files:
	print f
	os.rename(f, f.replace(' ','_'))
