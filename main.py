import tkinter as tk
from tkinter import ttk
import subprocess
import time

def start_analysis():
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading")

    # Start the analysis_gui.py subprocess immediately
    analysis_process = subprocess.Popen(["python", "wc_test.py"])

    label_loading = ttk.Label(loading_window, text="Now loading... Please wait.")
    label_loading.pack()

    # Allow the analysis process to start for a brief moment
    time.sleep(1)  # You can adjust this duration if needed

    root.after(9000, lambda: close_windows(root, loading_window))  # Close windows after 9 seconds

def close_windows(main_window, loading_window):
    loading_window.destroy()
    main_window.destroy()

def main():
    global root
    root = tk.Tk()
    root.title("Main Window")

    btn_analyze = tk.Button(root, text="Start Analysis", command=start_analysis)
    btn_analyze.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
