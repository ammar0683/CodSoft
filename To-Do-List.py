import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        self.tasks = []
        self.data_file = "tasks.json"
        self.load_tasks()

        self.setup_ui()
        self.refresh_task_list()

    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#4a90e2", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text=" My To-Do List",
            font=("Arial", 20, "bold"),
            bg="#4a90e2",
            fg="white"
        )
        title_label.pack(pady=15)

        # Input frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0", pady=20)
        input_frame.pack(fill="x", padx=20)

        tk.Label(
            input_frame,
            text="Task:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.task_entry = tk.Entry(input_frame, font=("Arial", 11), width=40)
        self.task_entry.grid(row=0, column=1, padx=10, pady=5)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        tk.Label(
            input_frame,
            text="Priority:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.priority_var = tk.StringVar(value="Medium")
        priority_menu = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=["High", "Medium", "Low"],
            state="readonly",
            width=15
        )
        priority_menu.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Buttons frame
        btn_frame = tk.Frame(input_frame, bg="#f0f0f0")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(
            btn_frame,
            text="Add Task",
            command=self.add_task,
            bg="#4caf50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Delete Selected",
            command=self.delete_task,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Clear All",
            command=self.clear_all,
            bg="#ff9800",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side="left", padx=5)

        # Task list frame
        list_frame = tk.Frame(self.root, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            list_frame,
            text="Tasks:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        ).pack(anchor="w", pady=(0, 10))

        # Scrollbar and listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 10),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            bg="white",
            selectbackground="#4a90e2",
            selectforeground="white",
            height=15
        )
        self.task_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        self.task_listbox.bind("<Double-Button-1>", lambda e: self.toggle_complete())

        # Status bar
        status_frame = tk.Frame(self.root, bg="#e0e0e0", height=30)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="Total tasks: 0 | Completed: 0 | Pending: 0",
            font=("Arial", 9),
            bg="#e0e0e0",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=10)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return

        task = {
            "text": task_text,
            "priority": self.priority_var.get(),
            "completed": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_task_list()

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return

        if messagebox.askyesno("Confirm", "Delete this task?"):
            self.tasks.pop(selection[0])
            self.save_tasks()
            self.refresh_task_list()

    def toggle_complete(self):
        selection = self.task_listbox.curselection()
        if selection:
            idx = selection[0]
            self.tasks[idx]["completed"] = not self.tasks[idx]["completed"]
            self.save_tasks()
            self.refresh_task_list()

    def clear_all(self):
        if not self.tasks:
            messagebox.showinfo("Info", "No tasks to clear!")
            return

        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            self.tasks.clear()
            self.save_tasks()
            self.refresh_task_list()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)

        priority_colors = {
            "High": "🔴",
            "Medium": "🟡",
            "Low": "🟢"
        }

        completed_count = 0
        for task in self.tasks:
            status = "✓" if task["completed"] else "○"
            priority = priority_colors.get(task["priority"], "○")
            display = f"{status} {priority} {task['text']} ({task['created']})"

            self.task_listbox.insert(tk.END, display)

            if task["completed"]:
                completed_count += 1
                self.task_listbox.itemconfig(tk.END, fg="gray")

        total = len(self.tasks)
        pending = total - completed_count
        self.status_label.config(
            text=f"Total tasks: {total} | Completed: {completed_count} | Pending: {pending}"
        )

    def save_tasks(self):
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.tasks = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {e}")
                self.tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


