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
	result = { "items" : [], "total_size" : 0}
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

		result["total_size"] += file_size

		result["items"].append(produce_item_info(file_name, file_name_full, file_size, False))

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
	""" Create the visual representation of a 'file_data_item'
	"""
	new_button = Button(main_window, text=file_data_item["file_name"])
	new_button.place(x = pos_x, y = pos_y, width = pos_width, height= pos_height)
	file_data_item["button_item"] = new_button
	return new_button

def tile_with_buttons(base_width, base_height, source_items, total_size, lambda_sorting_key):
	source_items_sorted = sorted(items_data["items"], key = lambda_sorting_key, reverse = True)
	source_items_sorted_last = len(source_items_sorted)
	i = 0
	new_x = 0
	new_y = 0
	old_x = 0
	old_y = 0
	prev_x = 0
	prev_y = 0
	prev_width = 0
	prev_height = 0
	first_width = base_width
	first_height = base_height
	new_width = base_width
	new_height = base_height
	previous_control = None
	while i < source_items_sorted_last and lambda_sorting_key(source_items_sorted[i]) > 0:
		source_items_sorted_item = source_items_sorted[i]
		print source_items_sorted_item["file_name"]
		current_item_size = lambda_sorting_key(source_items_sorted_item)
		current_item_koeff = float(current_item_size) / float(total_size)
		if old_x < old_y:
			step_size = float(base_width) * current_item_koeff
			new_x += step_size
			new_width -= step_size
		else:
			step_size = float(base_height) * current_item_koeff
			new_y += step_size
			new_height -= step_size
		if previous_control is not None:
			if old_x != prev_x:
				previous_control.place(width = old_x - prev_x)
			elif old_y != prev_y:
				previous_control.place(height = old_y - prev_y)
		previous_control = create_panel(main_window, old_x, old_y, first_width - old_x, first_height - old_y, source_items_sorted_item)
		CONTROLS.append(previous_control)
		prev_x = old_x
		prev_y = old_y
		old_x = new_x
		old_y = new_y
		prev_width = first_width - old_x
		prev_height = first_height - old_y
		base_width = new_width
		base_height = new_height
		total_size -= current_item_size
		i += 1
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
	sys.stderr.write('Directory "%s" is not existing.' % SETTINGS["path_to_load"])
	sys.exit(2)

SETTINGS["debug_output"] = "--output" in OPTS

items_data = get_items_size(SETTINGS["path_to_load"], SETTINGS["debug_output"] and get_items_size_callback or None)

CONTROLS = []

main_window = Tk()
tile_with_buttons(main_window.winfo_reqwidth(), main_window.winfo_reqheight(), items_data["items"], items_data["total_size"], lambda file_info: file_info["size"])
main_window.mainloop()