import os

lambda_sorting_key = lambda file_info: file_info["size"]

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
    
def get_items_size_callback(filename='', length=0, current_item=0):
    """ Callback function to bear process of directory change
    """
    print 'Processing "%s" - %s of %s' % (filename, length, current_item)

def get_bytes_size_range(num):
    range_titles = ["b", "kB", "Mb", "Gb", "Tb", "PB", "EB", "ZP", "YB"]
    range_titles_len = len(range_titles)
    i = 1
    prev_value = 0
    new_value = num
    is_iteration = True
    while is_iteration:
        prev_value = new_value
        new_value = num >> ((i << 1) * 5)
        i +=  1
        is_iteration = new_value > 0 and i < range_titles_len
    i -= 2
    return "%.2f%s" % (float(num) / float(1 << ((i << 1) * 5)), range_titles[i])


if __name__ == "__main__" :
    print "Helper functions for file operations"
    print get_bytes_size_range(1024)