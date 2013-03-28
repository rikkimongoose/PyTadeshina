#!/usr/bin/env python
import os
import sys
import getopt
import ctypes

def makeItemInfo(name, fullpath, size, isHidden = False):
	return {
		"name" : name,
		"fullpath" : fullpath,
		"size" : size,
		"isHidden" : isHidden
	}
def getItemsSize(pathRoot="."):
	result = []
	for f in os.listdir(pathRoot):
		if os.path.islink(f):
			continue
		fp = os.path.join(pathRoot, f)
		if os.path.isfile(fp):
			result.append(makeItemInfo(f, fp, os.stat(fp).st_size, False))
		elif os.path.isdir(fp):
			result.append(makeItemInfo(f, fp, getDirSize(fp), False))
	return result

def getDirSize(path=".", callbackIterationFunc = None):
	total_size = 0
	seen = {}
	for dirpath, dirname, filenames in os.walk(path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			
			# Callback function executed every iteration
			if callbackIterationFunc is not None:
				callbackIterationFunc(fp, total_size)

			if not os.path.exists(fp):
				continue
			stat = os.stat(fp)
			if stat.st_ino != 0:
			    fileid = stat.st_ino
			else:
			    fileid = fp
			if os.path.islink(fp) or fileid in seen:
			    continue
			else:
			    seen[fileid] = True
			total_size += stat.st_size
	return total_size
	
try:
	OPTS, ARGS = getopt.getopt(sys.argv[1:], "do:h", ["directory=", "output=", "help"])
except getopt.GetoptError as err:
	sys.stderr.write("%s\n" % str(err))
	sys.exit(2)

OPTS = dict(OPTS)

if '--help' in OPTS:
	print """Tadeshina 0.1 alpha

	Get size of files in a directory. Usage

	python tadeshina.py %directory_name% %params%

	--help - displays help

	[%directory_name%] - show sizes in a directory
	"""
	sys.exit(0)

if '--directory' in OPTS:
	path_to_load = OPTS['--directory']
elif len(ARGS) > 0:
	path_to_load = ARGS[0]
else:
	path_to_load = "."
if not os.path.exists(path_to_load):
	print 'Directory "%s" is not existing.' % path_to_load
	sys.exit(2)

print getItemsSize(path_to_load)