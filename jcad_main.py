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
