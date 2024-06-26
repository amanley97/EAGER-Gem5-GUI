# ----------------------------------------------------------------------------
# NOTICE: This code is the exclusive property of University of Kansas
#         Architecture Research and is strictly confidential.
#
#         Unauthorized distribution, reproduction, or use of this code, in
#         whole or in part, is strictly prohibited. This includes, but is
#         not limited to, any form of public or private distribution,
#         publication, or replication.
#
# For inquiries or access requests, please contact:
#         Alex Manley (amanley97@ku.edu)
#         Mahmudul Hasan (m.hasan@ku.edu)
# ----------------------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, Menu, Menubutton, messagebox
import subprocess
from printdebug import printdebug

def save_as_file(text, file_info):
    file_info['file_path'] = None
    file_info['compile_path'] = None
    printdebug(f"[ide] save file as")
    save_file(text, file_info)

def save_file(text, file_info):
    if 'file_path' in file_info and file_info['file_path']:  # Check if there is a previously saved file
        printdebug(f"[ide] saving file: {file_info['file_path']}")
        with open(file_info['file_path'], "w") as file:
            text_content = text.get("1.0", "end-1c")
            file.write(text_content)
    else:
        file_path = filedialog.asksaveasfilename(defaultextension=".c", filetypes=[("C Program Files", "*.c"), ("All files", "*.*")], initialdir="./workloads")
        printdebug(f"[ide] saving file: {file_path}")
        if file_path:
            with open(file_path, "w") as file:
                text_content = text.get("1.0", "end-1c")
                file.write(text_content)
            file_info['file_path'] = file_path  # Store the new file path        

def open_file(text, file_info, func):
    file_path = filedialog.askopenfilename(defaultextension=".c", filetypes=[("C Program Files", "*.c"), ("All files", "*.*")], initialdir="./workloads")
    printdebug(f"[ide] opening file: {file_path}")
    if file_path:
        with open(file_path, "r") as file:
            file_content = file.read()
            text.delete("1.0", "end")
            text.insert("1.0", file_content)
        file_info['file_path'] = file_path  # Update the file path
        func()

def compile(file_info):
    printdebug("[ide] compiling user program")

    if (file_info["file_path"] == None):
        messagebox.showerror("Error", "File must be saved before compiling!")
    elif (file_info["compile_path"] == None):
        messagebox.showerror("Error", "Please specify executable path!")
        file_info["compile_path"] = filedialog.asksaveasfilename(defaultextension="", filetypes=[("C Binary", "*.out")], initialdir="./workloads", title="Save Binary As")
    
        srcname = file_info["file_path"]
        execpath = file_info["compile_path"]
        cmd = ["gcc", "-O2", srcname, "-o", execpath]
        p = subprocess.Popen(cmd)
        p.wait()
        messagebox.showinfo("Information", "Workload Compiled Successfully!")

def code_window(tab):
    file_info = {'file_path': None,
                 'compile_path': None}
    header_label = tk.Label(tab, text="Simulation Workload Editor", font=('TkDefaultFont', 16, 'bold'), bg="gray", fg="black")
    header_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

    filebutton = Menubutton(tab, text="File", relief=tk.RAISED)
    filebutton.grid(row=0, column=0, padx=10, pady=10)

    filemenu = Menu(filebutton, tearoff=0)
    filebutton['menu'] = filemenu
    
    filemenu.add_command(label="Open", command=lambda: open_file(text, file_info, update_line_numbers))
    filemenu.add_command(label="Save", command=lambda: save_file(text, file_info))
    filemenu.add_command(label="Save As", command=lambda: save_as_file(text, file_info))

    text = tk.Text(tab, 
                   width=80, 
                   height=15, 
                   font="Courier", 
                   cursor="arrow", 
                   bg="lightgray", 
                   fg="black", 
                   wrap="none")
    text.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)

    def update_line_numbers(event=None):
        lines = text.get("1.0", "end").count("\n")
        line_numbers.config(state="normal")
        line_numbers.delete("1.0", "end")
        for i in range(1, lines + 1):
            line_numbers.insert("end", f"{i}\n")
        line_numbers.config(state="disabled")

    text.bind("<MouseWheel>", update_line_numbers)
    text.bind("<Button-4>", update_line_numbers)
    text.bind("<Button-5>", update_line_numbers)
    text.bind("<Key>", update_line_numbers)

    line_numbers = tk.Text(tab, width=4, padx=2, borderwidth=0, highlightthickness=0, background="gray", foreground="white", state=tk.DISABLED)
    line_numbers.grid(row=1, column=0, sticky="ns", padx=(0, 20))

    compile_button = tk.Button(tab, text="Compile", command=lambda: compile(file_info), width=60)
    compile_button.grid(row=3, column=1, padx=10, pady=5, sticky=tk.E)
