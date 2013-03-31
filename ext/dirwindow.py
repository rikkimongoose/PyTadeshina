from Tkinter import *
from fileoperations import *

PROGRAM_TITLE = "PyTadeshina"
PROGRAM_VER = "0.1"

class DirWindow:
    """ Window with directory info
    """
    DEFAULT_WINDOW_PARAMS = {"width" : 500, "height" : 500}
    Controls = []
    _is_shown = False

    def __init__(self, path = "."):
        object.__init__(self)
        self.path = path
        self.window = Tk()
        self.window.title(self._gen_title(path))
        self.window.geometry("%sx%s" % (self.DEFAULT_WINDOW_PARAMS["width"], self.DEFAULT_WINDOW_PARAMS["height"]))

        items_data = get_items_size(path, None)
        source_items_sorted = sorted(items_data["items"], key = lambda_sorting_key, reverse = True)
        rects_list = self._tile_with_rects(self.DEFAULT_WINDOW_PARAMS["width"], self.DEFAULT_WINDOW_PARAMS["height"], source_items_sorted, items_data["total_size"], lambda_sorting_key)    
        for rect in rects_list:
            self._create_panel(rect["x"], rect["y"], rect["width"], rect["height"], rect["item"])

    def mainloop(self):
        """ Execute to show the window
        """
        if not self._is_shown:
            self.window.mainloop()
            _is_shown = True

    def _gen_title(self, append_str = None):
        """ Generate the window title according current path
        """
        title_str = "%s v%s" % (PROGRAM_TITLE, PROGRAM_VER)
        if append_str is not None:
            title_str = "%s - %s" % (title_str, append_str)
        return title_str

    def _create_panel(self, pos_x, pos_y, pos_width, pos_height, file_data_item):
        """ Create the visual representation of a 'file_data_item'
        """
        new_panel = Frame(borderwidth=3, bd=1, relief=RIDGE) #Button(MAIN_WINDOW, text=file_data_item["file_name"])
        new_panel.place(x = pos_x, y = pos_y, width = pos_width, height= pos_height)
        self.Controls.append(new_panel)
        new_buttom_label = Label(new_panel, text=file_data_item["file_name"])
        new_buttom_label.pack(expand=YES, fill=BOTH)
        file_data_item["button_item"] = new_panel
        file_data_item["button_item_label"] = new_buttom_label
        return new_panel

    def open_path(self, path):
        new_window = DirWindow(path)
        new_window.mainloop()

    def _tile_with_rects(self, base_width, base_height, source_items, total_size, lambda_sorting_key):
        """ Tile area with rects according to lambda_sorting_key values
        """
        rects_list = []
        source_items_sorted_last = len(source_items) - 1
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
        previous_rect = None
        while i < source_items_sorted_last and lambda_sorting_key(source_items[i]) > 0:
            source_items_sorted_item = source_items[i]
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
            # arrange the previous component
            if previous_rect is not None:
                if old_x != prev_x:
                    previous_rect["width"] = old_x - prev_x
                elif old_y != prev_y:
                    previous_rect["height"] = old_y - prev_y
            previous_rect = {"x" : old_x, "y" : old_y, "width" : first_width - old_x, "height" : first_height - old_y, "item" : source_items_sorted_item}
            rects_list.append(previous_rect)
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

        if previous_rect is not None:
            if old_x != prev_x:
                previous_rect["width"] = old_x - prev_x
            elif old_y != prev_y:
                previous_rect["height"] = old_y - prev_y
        rects_list.append({"x" : old_x, "y" : old_y, "width" : first_width - old_x, "height" : first_height - old_y, "item" : source_items[source_items_sorted_last]})
        return rects_list

if __name__ == "__main__":
    print "DirWindow class module"