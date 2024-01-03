import tkinter as tk
from tkinter import ttk
import subprocess

def start_analysis():
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading")

    label_loading = ttk.Label(loading_window, text="Analyzing...")
    label_loading.pack()

    analysis_process = subprocess.Popen(["python", "analysis_gui.py"])

    def close_windows():
        loading_window.destroy()
        root.destroy()

    loading_window.after(10000, close_windows)

def main():
    global root
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("300x200")  # Set a uniform size

    btn_analyze = tk.Button(root, text="Start Analysis", command=start_analysis)
    btn_analyze.pack()

    def exit_app():
        root.destroy()

    btn_exit = tk.Button(root, text="Exit", command=exit_app)
    btn_exit.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
