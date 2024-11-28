import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import csv

def validate_input(task_name, due_date):
    """
    Validates user input for task name and due date.
    Ensures both fields are not empty.
    """
    if not task_name.strip():
        return "Task name cannot be empty."
    if not due_date.strip():
        return "Due date cannot be empty."
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

def mark_as_complete():
    """
    Marks the selected task's status as 'Complete'.
    """
    selected_item = task_list.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a task to mark as complete.")
        return

    for item in selected_item:
        task_list.item(item, values=(task_list.item(item, "values")[0],  # Task Name
                                     task_list.item(item, "values")[1],  # Due Date
                                     "Complete"))  # Update status to Complete
    messagebox.showinfo("Success", "Task marked as complete!")

def clear_tasks():
    """
    Clears all tasks from the task list.
    """
    for item in task_list.get_children():
        task_list.delete(item)
    messagebox.showinfo("Clear Tasks", "All tasks cleared!")

def export_to_csv():
    """
    Exports the current tasks in the task list to a CSV file on the Desktop.
    """
    tasks = task_list.get_children()
    if not tasks:
        messagebox.showwarning("No Tasks", "No tasks to export!")
        return

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "tasks.csv")

    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Task Name", "Due Date", "Status"])
            for task in tasks:
                writer.writerow(task_list.item(task, "values"))
        messagebox.showinfo("Export Successful", f"Tasks exported to {filename} successfully!")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred while exporting: {e}")

def exit_application():
    """
    Exits the application with a confirmation prompt.
    """
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

def open_about_window():
    """
    Opens a secondary window displaying application information.
    """
    about_window = tk.Toplevel(root)
    about_window.title("About TaskMaster Pro")
    about_window.geometry("400x200")

    info_label = tk.Label(
        about_window, 
        text="TaskMaster Pro v1.0\nA simple task management tool.\nCreated by Sean Alsup.",
        font=("Arial", 12)
    )
    info_label.pack(pady=20)

    close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack(pady=10)

# Main application window
root = tk.Tk()
root.title("TaskMaster Pro")
root.geometry("600x500")

def load_image(filename, size):
    """
    Loads an image and resizes it. Returns None if the file doesn't exist.
    """
    if os.path.exists(filename):
        return ImageTk.PhotoImage(Image.open(filename).resize(size))
    else:
        return None

task_image = load_image("task.png", (50, 50))
exit_image = load_image("exit.png", (50, 50))

header_label = tk.Label(root, text="TaskMaster Pro", font=("Arial", 18))
header_label.pack(pady=10)

task_name_label = tk.Label(root, text="Task Name:", font=("Arial", 12))
task_name_label.pack()
task_name_entry = tk.Entry(root, width=30)
task_name_entry.pack()

due_date_label = tk.Label(root, text="Due Date (YYYY-MM-DD):", font=("Arial", 12))
due_date_label.pack()
due_date_entry = tk.Entry(root, width=30)
due_date_entry.pack()

task_list = ttk.Treeview(root, columns=("Task Name", "Due Date", "Status"), show="headings")
task_list.heading("Task Name", text="Task Name")
task_list.heading("Due Date", text="Due Date")
task_list.heading("Status", text="Status")
task_list.pack(pady=10, fill=tk.BOTH, expand=True)

add_button = tk.Button(root, text="Add Task", image=task_image, compound=tk.LEFT if task_image else None, command=add_task)
add_button.pack(side=tk.LEFT, padx=10)

complete_button = tk.Button(root, text="Mark as Complete", command=mark_as_complete)
complete_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(root, text="Clear Tasks", command=clear_tasks)
clear_button.pack(side=tk.LEFT, padx=10)

export_button = tk.Button(root, text="Export to CSV", command=export_to_csv)
export_button.pack(side=tk.LEFT, padx=10)

about_button = tk.Button(root, text="About", command=open_about_window)
about_button.pack(side=tk.RIGHT, padx=10)

exit_button = tk.Button(root, text="Exit", image=exit_image, compound=tk.LEFT if exit_image else None, command=exit_application)
exit_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()
