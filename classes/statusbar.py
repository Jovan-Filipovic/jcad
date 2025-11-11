import tkinter as tk

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