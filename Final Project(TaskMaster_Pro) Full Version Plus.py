import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import csv
from datetime import datetime
from ttkthemes import ThemedTk

# Initialize main application window
root = ThemedTk(theme="arc")
root.title("TaskMaster Pro")
root.geometry("800x600")

# Global variables
task_data = []

# Function to validate date
def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to add a new task
def add_task():
    task_name = task_name_entry.get()
    due_date = due_date_entry.get()
    priority = priority_combobox.get()

    if not task_name.strip():
        messagebox.showerror("Input Error", "Task name cannot be empty.")
        return
    if not validate_date(due_date):
        messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
        return

    task_list.insert("", "end", values=(task_name, due_date, priority, "Incomplete"))
    task_name_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    priority_combobox.set("Medium")
    task_data.append((task_name, due_date, priority, "Incomplete"))

# Function to edit a task
def edit_task():
    selected_items = task_list.selection()
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select a task to edit.")
        return

    for item in selected_items:
        values = task_list.item(item, "values")
        if len(values) < 4:
            values = (*values, *[""] * (4 - len(values)))

        task_name_entry.delete(0, tk.END)
        task_name_entry.insert(0, values[0])
        due_date_entry.delete(0, tk.END)
        due_date_entry.insert(0, values[1])
        priority_combobox.set(values[2])

        task_list.delete(item)
        try:
            task_data.remove((values[0], values[1], values[2], values[3]))
        except ValueError:
            print(f"Task not found in task_data: {values}")

# Function to mark task as complete
def mark_as_complete():
    selected_items = task_list.selection()
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select a task to mark as complete.")
        return

    for item in selected_items:
        values = task_list.item(item, "values")
        task_list.item(item, values=(values[0], values[1], values[2], "Complete"))
        for i, task in enumerate(task_data):
            if task[0] == values[0] and task[1] == values[1]:
                task_data[i] = (task[0], task[1], task[2], "Complete")

# Function to remove a single task
def remove_task():
    selected_items = task_list.selection()
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select a task to remove.")
        return

    for item in selected_items:
        values = task_list.item(item, "values")
        try:
            task_list.delete(item)
            task_data.remove((values[0], values[1], values[2], values[3]))
        except ValueError:
            print(f"Task not found in task_data: {values}")
    messagebox.showinfo("Success", "Selected task(s) removed successfully!")

# Function to clear all tasks
def clear_tasks():
    task_list.delete(*task_list.get_children())
    task_data.clear()

# Function to export tasks to CSV
def export_to_csv():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "tasks.csv")
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Task Name", "Due Date", "Priority", "Status"])
            for item in task_list.get_children():
                writer.writerow(task_list.item(item, "values"))
        messagebox.showinfo("Export Successful", f"Tasks exported to {filename} successfully!")
    except Exception as e:
        print(f"Export Error: {e}")
        messagebox.showerror("Export Error", "An error occurred while exporting.")

# Function to open About window
def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("About TaskMaster Pro")
    about_window.geometry("400x200")
    about_label = tk.Label(
        about_window, 
        text="TaskMaster Pro v1.0\nA simple task management tool.\nCreated by Sean Alsup.",
        font=("Arial", 12)
    )
    about_label.pack(pady=20)
    close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack()

# Function to open Help window
def open_help_window():
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.geometry("500x300")
    help_label = tk.Label(
        help_window, 
        text=(
            "TaskMaster Pro User Manual\n\n"
            "- Introduction:\n"
            "  TaskMaster Pro is a user-friendly task management tool designed to help you organize and prioritize your daily tasks.\n\n"
            "- Getting Started:\n"
            "  Input Task Name, Due Date (in YYYY-MM-DD format), and click 'Add Task' to save the task.\n\n"
            "- Features:\n"
            "  • Edit Tasks: Select a task and click 'Edit' to modify it.\n"
            "  • Mark as Complete: Select a task and click 'Mark as Complete'.\n"
            "  • Delete Task: Select a task and click 'Clear Task'.\n"
            "  • Export to CSV: Save your tasks as a CSV file on the desktop.\n"
            "  • User Manual & About: Use the respective buttons for guidance or information."
        ),
        font=("Arial", 12), 
        justify="left"
    )
    help_label.pack(pady=10)

# Widgets
header_label = tk.Label(root, text="TaskMaster Pro", font=("Arial", 24))
header_label.pack(pady=10)

task_frame = tk.Frame(root)
task_frame.pack(pady=5)

# Task entry widgets
task_name_label = tk.Label(task_frame, text="Task Name:")
task_name_label.grid(row=0, column=0, padx=5, pady=5)
task_name_entry = tk.Entry(task_frame, width=40)
task_name_entry.grid(row=0, column=1, padx=5, pady=5)

due_date_label = tk.Label(task_frame, text="Due Date (YYYY-MM-DD):")
due_date_label.grid(row=1, column=0, padx=5, pady=5)
due_date_entry = tk.Entry(task_frame, width=40)
due_date_entry.grid(row=1, column=1, padx=5, pady=5)

priority_label = tk.Label(task_frame, text="Priority:")
priority_label.grid(row=2, column=0, padx=5, pady=5)
priority_combobox = ttk.Combobox(task_frame, values=["High", "Medium", "Low"], state="readonly")
priority_combobox.set("Medium")
priority_combobox.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(task_frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

# Task list
task_list = ttk.Treeview(root, columns=("Task Name", "Due Date", "Priority", "Status"), show="headings")
task_list.heading("Task Name", text="Task Name")
task_list.heading("Due Date", text="Due Date")
task_list.heading("Priority", text="Priority")
task_list.heading("Status", text="Status")
task_list.pack(pady=10, fill=tk.BOTH, expand=True)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

edit_button = tk.Button(button_frame, text="Edit", command=edit_task)
edit_button.grid(row=0, column=0, padx=5)

complete_button = tk.Button(button_frame, text="Mark as Complete", command=mark_as_complete)
complete_button.grid(row=0, column=1, padx=5)

remove_button = tk.Button(button_frame, text="Clear Task", command=remove_task)
remove_button.grid(row=0, column=2, padx=5)

clear_button = tk.Button(button_frame, text="Clear All Tasks", command=clear_tasks)
clear_button.grid(row=0, column=3, padx=5)

export_button = tk.Button(button_frame, text="Export to CSV", command=export_to_csv)
export_button.grid(row=0, column=4, padx=5)

about_button = tk.Button(button_frame, text="About", command=open_about_window)
about_button.grid(row=0, column=5, padx=5)

help_button = tk.Button(button_frame, text="User Manual", command=open_help_window)
help_button.grid(row=0, column=6, padx=5)

# Run the application
root.mainloop()
