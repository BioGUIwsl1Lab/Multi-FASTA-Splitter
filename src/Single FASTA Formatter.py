import os
import glob
import textwrap
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_pipeline(input_dir, fasta_width, progress_bar):
    try:
        # Start the progress bar
        progress_bar.start()

        # Change to the input directory
        os.chdir(input_dir)

        # list files in the dir
        files = glob.glob("*.fa")

        if fasta_width > 0:
            def fasta_reformat(fasta):
                # Insert fasta file
                file = open(fasta, 'r')
                # Stripe leading and trailing characters in each line
                lines = list(map(lambda line: str(line).strip(), file))
                # Close the file
                file.close()
                # Retrieve the header
                header = lines[0]
                # Retrieve the sequence
                seq = "".join(lines[1:])
                # Wrap by fasta width
                wrapped_seq = textwrap.fill(seq,width=fasta_width)
                # Export to fasta
                with open(fasta,'w') as f:
                    f.writelines(f"{header}\n{wrapped_seq}\n")
        else:
            def fasta_reformat(fasta):    
                # Insert fasta file
                file = open(fasta, 'r')
                # Stripe leading and trailing characters in each line
                lines = list(map(lambda line: str(line).strip(), file))
                # Close the file
                file.close()
                # Retrieve the header
                header = lines[0]
                # Retrieve the sequence
                seq = "".join(lines[1:])
                # Export to fasta
                with open(fasta,'w') as f:
                    f.writelines(f"{header}\n{seq}\n")
        
        # Iterate over each file
        for file in files:
            fasta_reformat(file)

        progress_bar.stop()
        messagebox.showinfo("Success", f"FASTA files reformatted successfully.")

    except Exception as e:
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
width_var = tk.IntVar(value=80)
width_options = [0, 60, 70, 80]
width_dropdown = tk.OptionMenu(app, width_var, *width_options)
width_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")


# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=3, column=1, padx=10, pady=20)

app.mainloop()
