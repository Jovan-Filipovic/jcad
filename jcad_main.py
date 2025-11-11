import tkinter as tk
from tkinter import Menu

TOOLBAR_WIDTH = 80
TOOLBAR_HEIGHT = 140
TOOLBAR_SPACING = 10
BOTTOM_MARGIN = 80

class CommandBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bd=1, relief='sunken')
        self.entry = tk.Entry(self, width=50)
        self.entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry.bind('<Return>', self.process_command)

    def process_command(self, event=None):
        cmd = self.entry.get().strip()
        print(f"Command entered: {cmd}")
        self.entry.delete(0, tk.END)

class StatusBar(tk.Frame):
    def __init__(self, master, labels=None):
        super().__init__(master, bd=1, relief='sunken')
        self.labels = labels or ['SNAP', 'GRID', 'ORTHO', 'LWT', 'DYN']
        self.states = {label: False for label in self.labels}
        self.coord_label = tk.Label(self, text="X:0 Y:0 Z:0", width=15, anchor='e')
        self.build_status_bar()

    def build_status_bar(self):
        for label in self.labels:
            btn = tk.Label(self, text=label, width=6, relief='raised', bg='lightgray')
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            btn.bind('<Button-1>', lambda e, l=label, b=btn: self.toggle(l, b))
        self.coord_label.pack(side=tk.RIGHT, padx=10)

    def toggle(self, label, btn):
        self.states[label] = not self.states[label]
        btn.config(bg='green' if self.states[label] else 'lightgray')
        print(f"{label} toggled {'ON' if self.states[label] else 'OFF'}")

    def update_coords(self, x, y):
        self.coord_label.config(text=f"X:{x} Y:{y} Z:0")

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
        
class ToolbarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Toolbar Layout")
        self.geometry("1000x700")

        self.toolbars = {}
        self.create_menubar()

        self.canvas = ToolbarCanvas(self)
        self.canvas.pack(fill='both', expand=True)

        self.statusbar = StatusBar(self)
        self.statusbar.pack(side='bottom', fill='x')

        self.commandbar = CommandBar(self)
        self.commandbar.pack(side='bottom', fill='x')

        self.create_named_toolbars()

    def deactivate_all_toolbars(self):
        for tb in self.toolbars.values():
            tb.deactivate_button()

    def create_named_toolbars(self):
        horizontal_names = ['Layers', 'ViewH']
        vertical_names = ['Draw', 'Modify', 'Annotate', 'View']

        # Horizontal toolbars in one row
        x_offset = TOOLBAR_SPACING
        for name in horizontal_names:
            tb = DraggableToolbar(self, name, 'horizontal', [f"{name}{j+1}" for j in range(6)])
            tb.place(x=x_offset, y=TOOLBAR_SPACING)
            x_offset += tb.winfo_reqwidth() + TOOLBAR_SPACING
            self.toolbars[name] = tb

        # Vertical toolbars stacked below horizontal row
        y_offset = TOOLBAR_HEIGHT + TOOLBAR_SPACING * 2
        for i, name in enumerate(vertical_names):
            tb = DraggableToolbar(self, name, 'vertical', [f"{name}{j+1}" for j in range(6)])
            x = TOOLBAR_SPACING + i * (TOOLBAR_WIDTH + TOOLBAR_SPACING)
            tb.place(x=x, y=y_offset)
            self.toolbars[name] = tb

    def create_menubar(self):
        menubar = Menu(self)

        # File
        file_menu = Menu(menubar, tearoff=0)
        for item in ['New', 'Open', 'Close']:
            file_menu.add_command(label=item, command=lambda i=item: print(f"File: {i}"))
        menubar.add_cascade(label='File', menu=file_menu)

        # Edit
        edit_menu = Menu(menubar, tearoff=0)
        for item in ['Copy', 'Paste', 'Delete']:
            edit_menu.add_command(label=item, command=lambda i=item: print(f"Edit: {i}"))
        menubar.add_cascade(label='Edit', menu=edit_menu)

        # Draw
        draw_menu = Menu(menubar, tearoff=0)
        for item in ['Point', 'Line', 'hLine', 'vLine', 'pLines', 'rLine', 'Circle', 'Arc', 'Elipse', 'Rect']:
            draw_menu.add_command(label=item, command=lambda i=item: print(f"Draw: {i}"))
        menubar.add_cascade(label='Draw', menu=draw_menu)

        # View
        view_menu = Menu(menubar, tearoff=0)
        toolbar_menu = Menu(view_menu, tearoff=0)
        for name in ['Draw', 'Modify', 'Annotate', 'View', 'Layers', 'ViewH']:
            toolbar_menu.add_checkbutton(label=name, command=lambda n=name: print(f"Toggled {n} toolbar"))
        view_menu.add_cascade(label='Toolbars', menu=toolbar_menu)
        menubar.add_cascade(label='View', menu=view_menu)

        # Layer
        layer_menu = Menu(menubar, tearoff=0)
        for item in ['New', 'Edit', 'Delete']:
            layer_menu.add_command(label=item, command=lambda i=item: print(f"Layer: {i}"))
        menubar.add_cascade(label='Layer', menu=layer_menu)

        # Modify
        modify_menu = Menu(menubar, tearoff=0)
        for item in ['Trim', 'Extend', 'Mirror', 'Offset', 'Explode']:
            modify_menu.add_command(label=item, command=lambda i=item: print(f"Modify: {i}"))
        menubar.add_cascade(label='Modify', menu=modify_menu)

        # Annotate
        annotate_menu = Menu(menubar, tearoff=0)
        for item in ['hAnnotate', 'vAnnotate', 'lAnnotate', 'cAnnotate', 'dAnnotate', 'rAnnotate']:
            annotate_menu.add_command(label=item, command=lambda i=item: print(f"Annotate: {i}"))
        menubar.add_cascade(label='Annotate', menu=annotate_menu)

        # Settings
        settings_menu = Menu(menubar, tearoff=0)
        for item in ['General', 'Display']:
            settings_menu.add_command(label=item, command=lambda i=item: print(f"Settings: {i}"))
        menubar.add_cascade(label='Settings', menu=settings_menu)

        # Help
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='About', command=lambda: print("Help: About"))
        menubar.add_cascade(label='Help', menu=help_menu)

        self.config(menu=menubar)

if __name__ == '__main__':
    ToolbarApp().mainloop()
