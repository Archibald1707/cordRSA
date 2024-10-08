import tkinter as tk
from gui.interface import ChatInterface

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatInterface(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
