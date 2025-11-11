import tkinter as tk

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