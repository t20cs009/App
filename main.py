import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

def open_analysis():
    loading_screen = tk.Toplevel(root)
    loading_screen.title("Loading...")

    loading_label = tk.Label(loading_screen, text="Loading analysis, please wait...")
    loading_label.pack()

    analysis_thread = threading.Thread(target=start_analysis)
    analysis_thread.start()

    loading_screen.after(1000, check_analysis_window, loading_screen)

def start_analysis():
    subprocess.Popen(["python", "analysis_gui.py"])

def check_analysis_window(loading_screen):
    analysis_window = tk.Toplevel(root)
    analysis_window.title("FER Analysis")
    analysis_window.withdraw()  # Hide the window initially

    if any(window.winfo_exists() for window in tk.Toplevel.winfo_children(tk.Tk())):
        loading_screen.after(1000, check_analysis_window, loading_screen)
    else:
        loading_screen.destroy()
        analysis_window.deiconify()  # Show the analysis window

def main():
    root = tk.Tk()
    root.title("Main Window")

    btn_analyze = tk.Button(root, text="Start Analysis", command=open_analysis)
    btn_analyze.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
