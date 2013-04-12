from Tkinter import *
from diroperations import *
from tkMessageBox import *
from math import fabs

PROGRAM_TITLE = "PyTadeshina"
PROGRAM_VER = "0.2"

SETTINGS = {}

VIEW_SETTIGNS = { "selection-color" : "red" }

class DirWindow:
    """ Window with directory info
    """
    DEFAULT_WINDOW_PARAMS = {"width" : 500, "height" : 500}
    controls = []
    _is_shown = False

    def __init__(self, path = "."):
        object.__init__(self)

        self.selected_items = []
        self.path = path

        self.window = Tk()
        self.window.app_item = self
        self.default_width = self.DEFAULT_WINDOW_PARAMS["width"]
        self.default_height = self.DEFAULT_WINDOW_PARAMS["height"]
        self.window.geometry("%sx%s" % (self.default_width, self.default_height))
        self.items_count = self.load_dir(path)

        # create a menu
        self.popup = Menu(self.window, tearoff=0)
        self.popup.add_command(label="Delete", command=self.do_delete)
        self.popup.add_command(label="Delete to Recycle", command=self.do_recycle)
        self.popup.add_separator()
        self.popup.add_command(label="About", command=self.show_about)
        self.window.bind("<Button-3>", lambda e: self.do_popup(e))

    def mainloop(self):
        """ Execute to show the window
        """
        if not self._is_shown:
            self.window.bind("<Configure>", lambda e: self._update_elements_size())
            self.window.mainloop()
            _is_shown = True

    def load_dir(self, path = None):
        """ Load a directory to the current window
        """
        import thread

        if path is not None:
            self.path = path

        def iteration_callback(file_name, dir_list_length, i):
            """ Callback function used to update the window title during the enumeration of directories.
            """
            info_title = "Processing %s" % file_name
            self.window.title(self._gen_title(info_title))

        def result_callback(items_data):
            self.update_window_title()
            source_items_sorted = sorted(items_data["items"], key = DirOperations.get_lambda_sorting_key(), reverse = True)
            rects_list = self._tile_with_rects(self.DEFAULT_WINDOW_PARAMS["width"], self.DEFAULT_WINDOW_PARAMS["height"], source_items_sorted, items_data["total_size"], DirOperations.get_lambda_sorting_key())
            for rect in rects_list:
                self._create_panel(rect["x"], rect["y"], rect["width"], rect["height"], rect["item"])
            return len(source_items_sorted)

        thread.start_new_thread(DirOperations.get_items_size, (self.path, iteration_callback, result_callback))


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
        new_panel = DirPanel(self.window, pos_x, pos_y, pos_width, pos_height, file_data_item, self.selected_items)
        self.controls.append(new_panel)
        return new_panel

    @staticmethod
    def open_path(path):
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

    def add_to_selected_items(self, item):
        """Add item to selected items of current form
        """
        if item not in self.selected_items:
            self.selected_items.append(item)
            self.update_window_title()

    def remove_from_selected_items(self, item):
        """ Remove item from selected items of current form
        """
        if item in self.selected_items:
            self.selected_items.remove(item)
            self.update_window_title()

    def update_window_title(self):
        """ Update window title with data about selected files and their size
        """
        selected_items_len = len(self.selected_items)
        new_title = ""
        if selected_items_len == 0:
            new_title = self.path
        elif selected_items_len == 1:
            new_title = "%s (%s)" % (self.selected_items[0].title, DirOperations.get_bytes_size_units(self.selected_items[0].file_size))
        else:
            selected_items_size = 0
            for selected_item in self.selected_items:
                selected_items_size += selected_item.file_size
            new_title = ("%s in %s files" % (DirOperations.get_bytes_size_units(selected_items_size), selected_items_len))
        self.window.title(self._gen_title(new_title))

    def _update_elements_size(self):
        """ Update inner items size according to changed size of the window
        """
        width_koeff = float(self.window.winfo_width()) / float(self.default_width)
        height_koeff = float(self.window.winfo_height()) / float(self.default_height)
        if fabs(width_koeff) - 1.0 <= 0.01 and fabs(height_koeff - 1.0) <= 0.01: return
        for control in self.controls:
            control_width = float(control.frame.default_width) * width_koeff
            control_height = float(control.frame.default_height) * height_koeff
            control_x = float(control.frame.default_x) * width_koeff
            control_y = float(control.frame.default_y) * height_koeff
            control.frame.place(x = control_x, y = control_y, width = control_width, height = control_height)

    def do_recycle(self):
        """ Remove selected files to system recycle bin
        """ 
        if not SETTINGS["silent"] and not self.ask_delete("this files"):
            return
        for selected_item in self.selected_items:
            try:
                DirOperations.remove_file_to_trash(selected_item.full_path)
                selected_item.is_exist = False
            except OSError, e:
                sys.stderr.write("%s\n" % str(e))
        self.do_update()


    def do_delete(self):
        """ Remove selected files
        """
        if not SETTINGS["silent"] and not self.ask_delete("this files"):
            return
        for selected_item in self.selected_items:
            try:
                DirOperations.remove_file(selected_item.full_path)
                selected_item.is_exist = False
            except OSError, e:
                sys.stderr.write("%s\n" % str(e))
        self.do_update()

    def do_update(self):
        """ Update data on the form
        """
        self.load_dir()

    def show_about(self):
        """ Show the about box
        """
        showinfo("About %s %s." % (PROGRAM_TITLE, PROGRAM_VER), "%s %s\n\nA cross-platform util for estimating the file size and delete the useless ones.\n\nhttp://github.com/rikkimongoose/PyTadeshina\n\nDeveloped by RikkiMongoose under GNU GPL License." % (PROGRAM_TITLE, PROGRAM_VER))

    def do_popup(self, event):
        """ Display the popup menu
        """
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.popup.grab_release()
        self.do_update()

    def ask_delete(self, file_name):
        """ Ask before deletion
        """
        return askyesno("Deletion", "Are you sure want to delete %s?" % file_name)

class DirPanel:
    """ Panel with directory information.
    """
    def __init__(self, root, pos_x, pos_y, pos_width, pos_height, file_data_item, selected_items_container):
        self.root = root
        self.frame = Frame(root, borderwidth=3, bd=1, relief=RIDGE)

        self.is_exist = True

        lambda_dir_panel_click = lambda e: self._dir_panel_click(e, self.frame, self)
        lambda_dir_panel_dbl_click = lambda e: self._dir_panel_dbl_click(e, self.frame, self)
        lambda_window_popup = lambda e: self.add_to_selected_items() and root.app_item.do_popup(e)

        self.frame.default_color = self.frame["background"]
        self.frame.app_item = self
        self.base_form_selected_items = selected_items_container
        self.frame.place(x = pos_x, y = pos_y, width = pos_width, height = pos_height)
        self.frame.bind("<Button-1>", lambda_dir_panel_click)
        self.frame.bind("<Double-Button-1>", lambda_dir_panel_dbl_click)
        self.frame.bind("<Button-3>", lambda_window_popup)
        self.frame.default_x = pos_x
        self.frame.default_y = pos_y
        self.frame.default_width = pos_width
        self.frame.default_height = pos_height
        self.frame.file_data_item = file_data_item
        self.file_size = 0
        self.title = ""
        self.full_path = ""
        self.frame.is_directory = False
        if file_data_item is not None:
            self.title = file_data_item["file_name"]
            self.full_path = file_data_item["full_path"]
            self.frame.is_directory = file_data_item["is_directory"]
            self.file_size = file_data_item["size"]
        self.label = Label(self.frame, text=self.title)
        self.frame.label = self.label
        self.label.pack(expand=YES, fill=BOTH)
        self.label.bind("<Button-1>", lambda_dir_panel_click)
        self.label.bind("<Double-Button-1>", lambda_dir_panel_dbl_click)
        self.label.bind("<Button-3>", lambda_window_popup)
        self.frame.is_selected = False

    def add_to_selected_items(self):
        """Add current item to selected items of current form
        """
        if self.base_form_selected_items is None: return
        self.root.app_item.add_to_selected_items(self)
        self.frame.is_selected = True
        self.frame["background"] = VIEW_SETTIGNS['selection-color']

    def remove_from_selected_items(self):
        """ Remove current item from selected items of current form
        """
        if self.base_form_selected_items is None: return
        self.root.app_item.remove_from_selected_items(self)
        self.frame.is_selected = False
        self.frame["background"] = self.frame.default_color

    def _dir_panel_click(self, e, selected_frame, frame_item):
        """ One click on a directory panel
        """
        if selected_frame is None: return

        if not selected_frame.is_selected:
            frame_item.add_to_selected_items()
        else:
            frame_item.remove_from_selected_items()
    def _dir_panel_dbl_click(self, e, selected_frame, frame_item):
        """ Double click on a directory panel
        """
        if selected_frame is None: return

        if selected_frame.is_directory:
            DirWindow.open_path(frame_item.full_path)

if __name__ == "__main__":
    print "DirWindow class module"