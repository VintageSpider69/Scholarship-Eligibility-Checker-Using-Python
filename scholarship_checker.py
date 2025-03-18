import tkinter as tk
from tkinter import ttk, messagebox

def add_student():
    """Adds a student to the table and stores their GPA."""
    name = entry_name.get().strip()
    roll_no = entry_roll.get().strip()
    branch = entry_branch.get().strip()
    gpa = entry_gpa.get().strip()

    if not name or not roll_no or not branch or not gpa:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        gpa = float(gpa)
        if gpa < 0 or gpa > 10:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Input Error", "GPA must be a number between 0 and 10.")
        return

    students_gpa[roll_no] = (name, branch, gpa)
    display_all_students()

    # Clear input fields
    entry_name.delete(0, tk.END)
    entry_roll.delete(0, tk.END)
    entry_branch.delete(0, tk.END)
    entry_gpa.delete(0, tk.END)

def check_eligibility():
    """Filters the table to show only students with GPA above the entered minimum."""
    min_gpa = entry_min_gpa.get().strip()
    if not min_gpa:
        messagebox.showwarning("Input Error", "Please enter a minimum GPA.")
        return

    try:
        min_gpa = float(min_gpa)
    except ValueError:
        messagebox.showwarning("Input Error", "Minimum GPA must be a number.")
        return

    # Clear the table
    for item in tree.get_children():
        tree.delete(item)

    # Add only eligible students
    for roll_no, (name, branch, gpa) in students_gpa.items():
        if gpa >= min_gpa:
            tree.insert("", "end", values=(name, roll_no, branch, gpa))

def remove_student():
    """Removes the selected student from the table and dictionary."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a student to remove.")
        return

    for item in selected_item:
        roll_no = tree.item(item, "values")[1]
        del students_gpa[roll_no]
        tree.delete(item)

def display_all_students():
    """Displays all students in the table (resets any filtering)."""
    # Clear the table
    for item in tree.get_children():
        tree.delete(item)

    # Add all students back
    for roll_no, (name, branch, gpa) in students_gpa.items():
        tree.insert("", "end", values=(name, roll_no, branch, gpa))

# Student data dictionary
students_gpa = {}

# Create main window
root = tk.Tk()
root.title("Scholarship Eligibility Checker")
root.geometry("650x550")
root.configure(bg="#F8F9FA")

# **Title**
tk.Label(root, text="Scholarship Eligibility Checker", font=("Helvetica", 16, "bold"), bg="#F8F9FA", fg="#333").pack(pady=10)

# **Input Fields**
frame_inputs = tk.Frame(root, bg="#F8F9FA")
frame_inputs.pack(pady=10)

fields = [("Name", "entry_name"), ("Roll No", "entry_roll"), ("Branch", "entry_branch"), ("GPA", "entry_gpa")]
entries = {}

for i, (label_text, var_name) in enumerate(fields):
    tk.Label(frame_inputs, text=label_text + ":", bg="#F8F9FA", font=("Helvetica", 11)).grid(row=i, column=0, pady=5, padx=5, sticky="w")
    entry = tk.Entry(frame_inputs, font=("Helvetica", 11), relief="solid", bd=1, width=25)
    entry.grid(row=i, column=1, pady=5, padx=5, ipadx=5, ipady=3)
    entry.configure(highlightbackground="#C7C7C7", highlightcolor="#007AFF", highlightthickness=1)
    entries[var_name] = entry

entry_name, entry_roll, entry_branch, entry_gpa = entries.values()

# **Add Student Button**
btn_add = tk.Button(root, text="Add Student", command=add_student, font=("Helvetica", 11, "bold"), bg="#007AFF", fg="white",
                    relief="flat", bd=0, padx=10, pady=5)
btn_add.pack(pady=5)
btn_add.configure(activebackground="#0056b3")

# **Check Eligibility Section**
frame_check = tk.Frame(root, bg="#F8F9FA")
frame_check.pack(pady=10)

tk.Label(frame_check, text="Min GPA for Eligibility:", bg="#F8F9FA", font=("Helvetica", 11)).grid(row=0, column=0, padx=5)
entry_min_gpa = tk.Entry(frame_check, font=("Helvetica", 11), relief="solid", bd=1, width=10)
entry_min_gpa.grid(row=0, column=1, padx=5, ipadx=5, ipady=3)
entry_min_gpa.configure(highlightbackground="#C7C7C7", highlightcolor="#007AFF", highlightthickness=1)

btn_check = tk.Button(frame_check, text="Check", command=check_eligibility, font=("Helvetica", 11, "bold"), bg="#28A745", fg="white",
                      relief="flat", bd=0, padx=10, pady=5)
btn_check.grid(row=0, column=2, padx=5)
btn_check.configure(activebackground="#1e7d34")

# **Student Table**
frame_table = tk.Frame(root, bg="#F8F9FA")
frame_table.pack(pady=10)

columns = ("Name", "Roll No", "Branch", "GPA")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10, style="Custom.Treeview")
tree.pack(side="left")

for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, width=120, anchor="center")

# **Instruction Text**
instruction_label = tk.Label(root, text="☑ Select a student above and click 'Remove' to delete their details.",
                             font=("Helvetica", 10), bg="#F8F9FA", fg="#666")
instruction_label.pack(pady=5)

# **Remove Student Button**
btn_remove = tk.Button(root, text="Remove", command=remove_student, font=("Helvetica", 11, "bold"), bg="#DC3545", fg="white",
                       relief="flat", bd=0, padx=10, pady=5)
btn_remove.pack(pady=5)
btn_remove.configure(activebackground="#a71d2a")

# **Display All Students Button**
btn_display_all = tk.Button(root, text="Show All", command=display_all_students, font=("Helvetica", 11, "bold"), bg="#6C757D", fg="white",
                            relief="flat", bd=0, padx=10, pady=5)
btn_display_all.pack(pady=5)
btn_display_all.configure(activebackground="#545b62")

# **Styling the Table (Treeview)**
style = ttk.Style()
style.configure("Custom.Treeview",
                font=("Helvetica", 11),
                rowheight=25,
                background="#FFFFFF",
                fieldbackground="#FFFFFF")

style.configure("Custom.Treeview.Heading",
                font=("Helvetica", 11, "bold"),
                background="#F1F1F1",
                foreground="#333")

style.map("Custom.Treeview", background=[("selected", "#007AFF")])

# Run app
root.mainloop()
