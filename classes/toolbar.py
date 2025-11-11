import tkinter as  tk
from tkinter import Menu

BOTTOM_MARGIN = 80

class ToolbarCanvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.bind('<Button-3>', self.show_popup_menu)
        self.bind('<Motion>', self.track_mouse)

    def show_popup_menu(self, event):
        menu = Menu(self, tearoff=0)
        menu.add_command(label='Canvas Menu')
        menu.add_command(label='Cancel')
        menu.tk_popup(event.x_root, event.y_root)

    def track_mouse(self, event):
        self.master.statusbar.update_coords(event.x, event.y)

class DraggableToolbar(tk.Frame):
    def __init__(self, master, name, orientation='vertical', button_labels=None):
        super().__init__(master.canvas, bd=1, relief='raised')
        self.master = master
        self.name = name
        self.orientation = orientation
        self.button_labels = button_labels or []
        self.active_button = None
        self.dragging = False
        self.build_toolbar()
        self.bind_events()

    def build_toolbar(self):
        self.buttons = []
        side = tk.LEFT if self.orientation == 'horizontal' else tk.TOP

        drag_btn = tk.Label(self, text='≡', width=2, bg='gray', relief='sunken', cursor='fleur')
        drag_btn.pack(side=side, padx=1, pady=1)
        drag_btn.bind('<ButtonPress-1>', self.start_drag)
        drag_btn.bind('<B1-Motion>', self.do_drag)
        drag_btn.bind('<ButtonRelease-1>', self.stop_drag)

        for label in self.button_labels[:12]:
            btn = tk.Label(self, text=label, width=6, relief='raised', bg='lightgray')
            btn.pack(side=side, padx=1, pady=1)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='orange'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='lightgray' if b != self.active_button else 'green'))
            btn.bind('<Button-1>', lambda e, b=btn: self.toggle_button(b))
            self.buttons.append(btn)

    def toggle_button(self, btn):
        if self.active_button == btn:
            self.deactivate_button()
        else:
            self.master.deactivate_all_toolbars()
            self.active_button = btn
            btn.config(bg='green')
            self.master.canvas.bind('<Escape>', self.deactivate_button)

    def deactivate_button(self, event=None):
        if self.active_button:
            self.active_button.config(bg='lightgray')
            self.active_button = None
        self.master.canvas.unbind('<Escape>')

    def start_drag(self, event):
        self.dragging = True
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def do_drag(self, event):
        if self.dragging:
            dx = event.x_root - self._drag_start_x
            dy = event.y_root - self._drag_start_y
            x = self.winfo_x() + dx
            y = self.winfo_y() + dy
            canvas_width = self.master.canvas.winfo_width()
            canvas_height = self.master.canvas.winfo_height() - BOTTOM_MARGIN
            x = max(0, min(x, canvas_width - self.winfo_width()))
            y = max(0, min(y, canvas_height - self.winfo_height()))
            self.place(x=x, y=y)
            self._drag_start_x = event.x_root
            self._drag_start_y = event.y_root

    def stop_drag(self, event):
        self.dragging = False

    def bind_events(self):
        self.bind('<Button-3>', self.show_context_menu)
        for child in self.winfo_children():
            child.bind('<Button-3>', self.show_context_menu)

    def show_context_menu(self, event):
        menu = Menu(self, tearoff=0)
        menu.add_command(label='Move', command=lambda: print(f"{self.name} move requested"))
        menu.add_command(label='Close', command=lambda: print(f"{self.name} cannot be closed"))
        menu.add_command(label='Cancel')
        menu.tk_popup(event.x_root, event.y_root)