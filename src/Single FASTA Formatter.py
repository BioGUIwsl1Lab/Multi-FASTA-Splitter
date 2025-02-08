import os
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_pipeline(input_dir, fasta_width, progress_bar):

    # Start the progress bar
    progress_bar.start()

    # Change to the input directory
    os.chdir(input_dir)

    # Run command
    command = f'for i in *.fa; do fasta_formatter.py "$i" {fasta_width}; done'
    try:
        subprocess.run(f"wsl bash -c '{command}'", check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    
        progress_bar.stop()
        messagebox.showinfo("Success", f"FASTA files reformatted successfully.")

    except subprocess.CalledProcessError as e:
        progress_bar.stop()
        messagebox.showerror("Error", str(e))
        
def start_thread():
    input_dir = input_dir_var.get()
    fasta_width = width_var.get()

    if not input_dir:
        messagebox.showwarning("Input Error", "Please select an input directory.")
        return
    
    # Start command in a new thread
    thread = threading.Thread(target=run_pipeline, args=(input_dir, fasta_width, progress_bar))
    thread.start()

def select_dir():
    file_path = filedialog.askdirectory()
    input_dir_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("Single FASTA Formatter")

# Input file selection
input_dir_var = tk.StringVar()
tk.Label(app, text="Input directory:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_dir_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_dir).grid(row=0, column=2, padx=10, pady=10)

# Fasta width selection
tk.Label(app, text="FASTA Width:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
width_var = tk.StringVar(value="80")
width_options = ["60", "70", "80"]
width_dropdown = tk.OptionMenu(app, width_var, *width_options)
width_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")


# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=3, column=1, padx=10, pady=20)

app.mainloop()
