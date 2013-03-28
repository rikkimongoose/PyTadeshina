#!/usr/bin/env python
import os
import sys
import getopt
import ctypes
from Tkinter import *

def produce_item_info(file_name, full_path, size, is_hidden = False):
	""" Create the file info item for current file
	"""
	return {
		"file_name" : file_name,
		"full_path" : full_path,
		"size" : size,
		"is_hidden" : is_hidden
	}
def get_items_size(path=".", callback_iteration_func = None):
	""" Get list of all of the files and directories in 'path', with their sizes and additional info.

		'callback_iteration_func' is executed every new item checking.
	"""
	result = []
	dir_list = os.listdir(path)
	dir_list_length = len(dir_list)
	i = 0
	for file_name in dir_list:
		if os.path.islink(file_name):
			continue
		
		# Callback function executed every iteration
		if callback_iteration_func is not None:
			i += 1
			callback_iteration_func(file_name, dir_list_length, i)

		file_name_full = os.path.join(path, file_name)
		file_size = 0

		if os.path.isfile(file_name_full):
			file_size = os.stat(file_name_full).st_size
		elif os.path.isdir(file_name_full):
			file_size = get_dir_size(file_name_full)

		result.append(produce_item_info(file_name, file_name_full, file_size, False))

	return result

def get_dir_size(path=".", callback_iteration_func = None):
	""" Get size of the directory in 'path'.

		'callback_iteration_func' is executed every new subdirectory checking.
	"""
	total_size = 0
	seen = {}
	for dir_path, dir_name, file_names in os.walk(path):
		for file_name in file_names:
			file_name_full = os.path.join(dir_path, file_name)
			
			# Callback function executed every iteration
			if callback_iteration_func is not None:
				callback_iteration_func(file_name_full, total_size)

			if not os.path.exists(file_name_full):
				continue
			file_stat = os.stat(file_name_full)
			
			file_id = file_stat.st_ino != 0 and (file_stat.st_ino) or file_name_full
			
			if os.path.islink(file_name_full) or file_id in seen:
			    continue
			else:
			    seen[file_id] = True
			total_size += file_stat.st_size
	return total_size
	
try:
	OPTS, ARGS = getopt.getopt(sys.argv[1:], "doh", ["directory=", "output", "help"])
except getopt.GetoptError as err:
	sys.stderr.write("%s\n" % str(err))
	sys.exit(2)

def get_items_size_callback(filename='', length=0, current_item=0):
	""" Callback function to bear process of directory change
	"""
	print 'Processing "%s" - %s of %s' % (filename, length, current_item)

def create_panel(main_window, pos_x, pos_y, pos_width, pos_height, file_data_item):
	new_button = Button(main_window, text=file_data_item["file_name"]).place(x = pos_x, y = pos_y, width = pos_width, height= pos_height)
	file_data_item["button_item"] = new_button

# Main code


OPTS = dict(OPTS)
SETTINGS = {}

if '--help' in OPTS:
	print """Tadeshina 0.1 alpha

	Get size of files in a directory. Usage

	python tadeshina.py %directory_name% %params%

	-h, --help - show help

	--o, --output - show output

	[%directory_name%] - show sizes in a directory
	"""
	sys.exit(0)

if '--directory' in OPTS:
	SETTINGS["path_to_load"] = OPTS['--directory']
elif len(ARGS) > 0:
	SETTINGS["path_to_load"] = ARGS[0]
else:
	SETTINGS["path_to_load"] = "."
if not os.path.exists(SETTINGS["path_to_load"]):
	print 'Directory "%s" is not existing.' % SETTINGS["path_to_load"]
	sys.exit(2)

SETTINGS["debug_output"] = "--output" in OPTS

PANELS = []

items_data = get_items_size(SETTINGS["path_to_load"], SETTINGS["debug_output"] and get_items_size_callback or None)
items_data_sorted = sorted(items_data, key = lambda file_info: file_info["size"], reverse = True)

print items_data_sorted
main_window = Tk()
create_panel(main_window, 0, 0, 20, 20, items_data_sorted[0])

main_window.mainloop()