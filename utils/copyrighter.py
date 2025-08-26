

import os
import sys
import fnmatch
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox


# Defaults, can be changed in GUI
AUTHOR = "Lachlan Mckenna"
githubuser = "mrtibbz2"
YEAR = datetime.now().year

def get_default_comment():
    return f"Copyright (c) {YEAR} {AUTHOR}\nAll rights reserved."

def make_header_lines(style, comment_text):
    lines = comment_text.strip('\n').splitlines()
    if style in ['py', 'cmake']:
        prefix = '# '
    elif style in ['c', 'cpp', 'h', 'hpp', 'js']:
        prefix = '// '
    else:
        prefix = '# '
    header_lines = []
    for line in lines:
        if line.strip() == '':
            header_lines.append('')  # True blank line
        else:
            header_lines.append(prefix + line)
    return header_lines

def get_comment_style(filename):
    ext = os.path.splitext(filename)[1].lower()
    if filename.lower().startswith("cmakelists") or ext == ".cmake":
        return 'cmake'
    if ext == ".py":
        return 'py'
    if ext in [".c", ".h"]:
        return 'c'
    if ext in [".cpp", ".hpp"]:
        return 'cpp'
    if ext == ".js" or ext == ".jsx":
        return 'js'
    return None

def has_header(lines, style, comment_text):
    # Only check for the first line of the generated header
    header_lines = make_header_lines(style, comment_text)
    if not header_lines:
        return False
    return any(header_lines[0] in line for line in lines[:3])


import subprocess

def is_authored_by_me_git(filepath, author, githubuser):
    """
    Returns True if the most recent git author of the file matches author or githubuser.
    """
    try:
        # Get the last commit author for the file
        result = subprocess.run([
            'git', 'log', '-1', '--pretty=format:%an|%ae', '--', filepath
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        author_info = result.stdout.strip().lower()
        # Check both name and github username/email
        if author.lower() in author_info or githubuser.lower() in author_info:
            return True
    except Exception:
        pass
    return False

def process_file(filepath, comment_text, author, githubuser):
    style = get_comment_style(os.path.basename(filepath))
    if not style:
        return
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return
    if has_header(lines, style, comment_text):
        return
    if not is_authored_by_me_git(filepath, author, githubuser):
        return
    header = make_header_lines(style, comment_text)
    # Insert a single blank line after the header if not already present
    if header and header[-1] != '':
        header.append('')
    new_lines = [h + '\n' if h != '' else '\n' for h in header] + lines
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Header added: {filepath}")

def find_files(root, patterns):
    matches = []
    for dirpath, _, filenames in os.walk(root):
        for pattern in patterns:
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(dirpath, filename))
    return matches


def gui_main():
    root = tk.Tk()
    root.title("Copyrighter - Directory Selector")
    root.geometry("500x300")
    dirs = []

    def add_dir():
        dir_selected = filedialog.askdirectory()
        if dir_selected and dir_selected not in dirs:
            dirs.append(dir_selected)
            listbox.insert(tk.END, dir_selected)

    def remove_selected():
        selected = listbox.curselection()
        for i in reversed(selected):
            dirs.pop(i)
            listbox.delete(i)


    def run_copyrighter():
        if not dirs:
            messagebox.showwarning("No directories", "Please add at least one directory.")
            return
        author = author_entry.get().strip()
        github = github_entry.get().strip()
        comment_text = comment_textbox.get("1.0", tk.END).strip()
        if not comment_text:
            messagebox.showwarning("No comment", "Please enter a copyright comment.")
            return
        # Collect selected file types
        patterns = []
        if var_py.get(): patterns.append("*.py")
        if var_c.get(): patterns.extend(["*.c", "*.h"])
        if var_cpp.get(): patterns.extend(["*.cpp", "*.hpp"])
        if var_js.get(): patterns.append("*.js")
        if var_jsx.get(): patterns.append("*.jsx")
        if var_cmake.get(): patterns.extend(["CMakeLists.txt", "*.cmake"])
        if not patterns:
            messagebox.showwarning("No file types", "Please select at least one file type.")
            return
        count = 0
        for directory in dirs:
            if not os.path.isdir(directory):
                continue
            files = find_files(directory, patterns)
            for file in files:
                process_file(file, comment_text, author, github)
                count += 1
        messagebox.showinfo("Done", f"Processed {count} files.")



    # Author fields
    author_frame = tk.Frame(root)
    author_frame.pack(pady=(10,0))
    tk.Label(author_frame, text="Author Name:").grid(row=0, column=0, sticky='e')
    author_entry = tk.Entry(author_frame, width=25)
    author_entry.grid(row=0, column=1, padx=5)
    author_entry.insert(0, AUTHOR)
    tk.Label(author_frame, text="GitHub Username or Email:").grid(row=0, column=2, sticky='e')
    github_entry = tk.Entry(author_frame, width=20)
    github_entry.grid(row=0, column=3, padx=5)
    github_entry.insert(0, githubuser)

    # Comment edit box
    comment_label = tk.Label(root, text="Edit copyright comment (will be auto-formatted):")
    comment_label.pack(pady=(10,0))
    comment_textbox = tk.Text(root, height=4, width=60)
    comment_textbox.pack(pady=(0,10))
    comment_textbox.insert(tk.END, get_default_comment())


    # File type checkboxes
    types_frame = tk.Frame(root)
    types_frame.pack(pady=(5,0))
    var_py = tk.BooleanVar(value=True)
    var_c = tk.BooleanVar(value=True)
    var_cpp = tk.BooleanVar(value=True)
    var_js = tk.BooleanVar(value=True)
    var_jsx = tk.BooleanVar(value=True)
    var_cmake = tk.BooleanVar(value=True)
    tk.Label(types_frame, text="File types:").grid(row=0, column=0, sticky='w')
    tk.Checkbutton(types_frame, text="Python (.py)", variable=var_py).grid(row=0, column=1, sticky='w')
    tk.Checkbutton(types_frame, text="C/C Header (.c/.h)", variable=var_c).grid(row=0, column=2, sticky='w')
    tk.Checkbutton(types_frame, text="C++/Header (.cpp/.hpp)", variable=var_cpp).grid(row=0, column=3, sticky='w')
    tk.Checkbutton(types_frame, text="JavaScript (.js)", variable=var_js).grid(row=0, column=4, sticky='w')
    tk.Checkbutton(types_frame, text="JSX (.jsx)", variable=var_jsx).grid(row=0, column=5, sticky='w')
    tk.Checkbutton(types_frame, text="CMake", variable=var_cmake).grid(row=0, column=6, sticky='w')

    frame = tk.Frame(root)
    frame.pack(pady=10)

    add_btn = tk.Button(frame, text="Add Directory", command=add_dir)
    add_btn.grid(row=0, column=0, padx=5)

    remove_btn = tk.Button(frame, text="Remove Selected", command=remove_selected)
    remove_btn.grid(row=0, column=1, padx=5)

    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=60)
    listbox.pack(pady=10)

    run_btn = tk.Button(root, text="Run Copyrighter", command=run_copyrighter)
    run_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    gui_main()
