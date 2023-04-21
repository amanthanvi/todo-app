import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
import datetime
import csv
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import time


def startup_animation():
    animation_window = tk.Toplevel(root)
    animation_window.overrideredirect(True)
    animation_window.geometry(
        "300x300+{0}+{1}".format(root.winfo_x() + 100, root.winfo_y() + 100))
    canvas = tk.Canvas(animation_window, width=300, height=300, bg="white")
    canvas.pack()

    loading_image = Image.open("loading.png")
    smiley_image = Image.open("smiley.png")
    checkmark_image = Image.open("checkmark.png")

    for _ in range(24):
        loading_image = loading_image.rotate(-15)
        loading_photo = ImageTk.PhotoImage(loading_image)
        canvas.create_image(150, 150, image=loading_photo)
        canvas.update()
        time.sleep(0.1)
        canvas.delete("all")

    smiley_photo = ImageTk.PhotoImage(smiley_image)
    canvas.create_image(150, 150, image=smiley_photo)
    canvas.update()
    time.sleep(1)
    canvas.delete("all")

    checkmark_photo = ImageTk.PhotoImage(checkmark_image)
    canvas.create_image(150, 150, image=checkmark_photo)
    canvas.update()
    time.sleep(1)

    animation_window.destroy()


class PlaceholderEntry(ttk.Entry):
    def __init__(self, master, placeholder, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

    def focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)

    def focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)


class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do Dashboard")

        # Configure the main frame
        self.mainframe = ttk.Frame(master, padding="10")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # Create and configure the listbox
        self.tasks_listbox = tk.Listbox(
            self.mainframe, width=40, height=10, bg="#f0f0f0")
        self.tasks_listbox.grid(
            column=0, row=0, rowspan=4, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create and configure the scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.mainframe, orient=tk.VERTICAL, command=self.tasks_listbox.yview)
        self.scrollbar.grid(column=1, row=0, rowspan=4,
                            sticky=(tk.N, tk.S), pady=5)
        self.tasks_listbox.configure(yscrollcommand=self.scrollbar.set)

        # Create and configure the menu
        self.menubar = tk.Menu(master)
        master.config(menu=self.menubar)

        self.themes_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="Themes", menu=self.themes_menu)

        self.themes = ['arc', 'equilux', 'yaru', 'breeze', 'adapta']

        for theme in self.themes:
            self.themes_menu.add_command(
                label=theme, command=lambda t=theme: self.set_theme(t))

        self.import_export_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(
            label="Import/Export", menu=self.import_export_menu)
        self.import_export_menu.add_command(
            label="Import CSV", command=self.import_csv)
        self.import_export_menu.add_command(
            label="Export CSV", command=self.export_csv)

        # Create and configure the entry widget
        self.task_entry = ttk.Entry(self.mainframe, width=30)
        self.task_entry.grid(column=2, row=0, padx=5,
                             pady=5, sticky=(tk.W, tk.E))

        # Create and configure the priority combobox
        self.priority_var = tk.StringVar()
        self.priority_combobox = ttk.Combobox(
            self.mainframe, textvariable=self.priority_var, values=("Low", "Medium", "High"))
        self.priority_combobox.set("Medium")
        self.priority_combobox.grid(
            column=2, row=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Create and configure the due date entry
        self.due_date_entry = DateEntry(self.mainframe, width=18)
        self.due_date_entry.grid(
            column=2, row=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Create and configure the optional due time entry
        self.due_time_entry = PlaceholderEntry(
            self.mainframe, placeholder="HH:MM (opt)", width=9)
        self.due_time_entry.grid(
            column=2, row=3, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Create and configure the buttons
        self.add_task_button = ttk.Button(
            self.mainframe, text="Add Task", command=self.add_task)
        self.add_task_button.grid(
            column=2, row=4, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.remove_task_button = ttk.Button(
            self.mainframe, text="Remove Task", command=self.remove_task)
        self.remove_task_button.grid(
            column=2, row=5, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Create and configure the live clock and date
        self.clock_label = ttk.Label(self.mainframe, text="")
        self.clock_label.grid(column=0, row=5, padx=5,
                              pady=5, sticky=(tk.W, tk.E))
        self.update_clock()

    def set_theme(self, theme):
        self.master.set_theme(theme)

    def import_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.tasks_listbox.insert(tk.END, " | ".join(row))

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                for task in self.tasks_listbox.get(0, tk.END):
                    writer.writerow(task.split(" | "))

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get()
        due_time = self.due_time_entry.get()

        if task:
            task_details = f"{priority} | {due_date}"
            if due_time != "HH:MM (opt)" or due_time != "":
                task_details += f" {due_time}"
            task_details += f" | {task}"
            self.tasks_listbox.insert(tk.END, task_details)
            self.task_entry.delete(0, tk.END)

    def remove_task(self):
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            self.tasks_listbox.delete(selected_task)

    def update_clock(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.clock_label.config(text=f"{current_time}\n{current_date}")
        self.master.after(1000, self.update_clock)

    def change_theme(self):
        self.style.theme_use(self.selected_theme.get())


if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Set the default theme
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Display the startup animation
    # startup_animation()

    todo_app = TodoApp(root)
    root.mainloop()
