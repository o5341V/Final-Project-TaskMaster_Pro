import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

def validate_input(task_name, due_date):
    """
    Validates user input for task name and due date.
    Ensures both fields are not empty and due date follows correct format.
    """
    if not task_name.strip():
        return "Task name cannot be empty."
    if not due_date.strip():
        return "Due date cannot be empty."
    # Additional date validation can be added here
    return None

def add_task():
    """
    Handles adding a new task. Validates inputs and updates task list.
    """
    task_name = task_name_entry.get()
    due_date = due_date_entry.get()
    error = validate_input(task_name, due_date)
    if error:
        messagebox.showerror("Input Error", error)
    else:
        task_list.insert("", "end", values=(task_name, due_date, "Incomplete"))
        messagebox.showinfo("Success", "Task added successfully!")
        task_name_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)

def clear_tasks():
    """
    Clears all tasks from the task list.
    """
    for item in task_list.get_children():
        task_list.delete(item)

def exit_application():
    """
    Exits the application with a confirmation prompt.
    """
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# Main application window
root = tk.Tk()
root.title("TaskMaster Pro")
root.geometry("600x400")

# Load images
task_image = ImageTk.PhotoImage(Image.open("task.png").resize((50, 50)))
exit_image = ImageTk.PhotoImage(Image.open("exit.png").resize((50, 50)))

# Main Window Layout
header_label = tk.Label(root, text="TaskMaster Pro", font=("Arial", 18))
header_label.pack(pady=10)

# Labels
task_name_label = tk.Label(root, text="Task Name:", font=("Arial", 12))
task_name_label.pack()
task_name_entry = tk.Entry(root, width=30)
task_name_entry.pack()

due_date_label = tk.Label(root, text="Due Date (YYYY-MM-DD):", font=("Arial", 12))
due_date_label.pack()
due_date_entry = tk.Entry(root, width=30)
due_date_entry.pack()

# Task List
task_list = ttk.Treeview(root, columns=("Task Name", "Due Date", "Status"), show="headings")
task_list.heading("Task Name", text="Task Name")
task_list.heading("Due Date", text="Due Date")
task_list.heading("Status", text="Status")
task_list.pack(pady=10, fill=tk.BOTH, expand=True)

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(root, text="Clear Tasks", command=clear_tasks)
clear_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(root, text="Exit", image=exit_image, compound=tk.LEFT, command=exit_application)
exit_button.pack(side=tk.RIGHT, padx=10)

# Secondary Window Functionality
def open_about_window():
    """
    Opens a secondary window displaying application information.
    """
    about_window = tk.Toplevel(root)
    about_window.title("About TaskMaster Pro")
    about_window.geometry("400x200")
    info_label = tk.Label(
        about_window, text="TaskMaster Pro v1.0\nA simple task management tool.", font=("Arial", 12)
    )
    info_label.pack(pady=20)

about_button = tk.Button(root, text="About", command=open_about_window)
about_button.pack(side=tk.RIGHT, padx=10)

# Start the application
root.mainloop()
