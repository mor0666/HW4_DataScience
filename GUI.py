import tkinter as tk
from tkinter import filedialog, messagebox


#tk.Text - display multiple lines of text that can be edited
#tk.Entry - is used to accept single-line text strings from a user
#tk.Label - display one or more lines of text that cannot be modified by the user

class GUI:
    def __init__(self, master_window):
        self.master_window = master_window
        master_window.title("K Means Clustering")
        self.master_window.geometry("350x100")
        self.k = -1
        self.runs = 0

        # Path
        self.path_label = tk.Label(master_window, text="Data Path")
        self.path_label.grid(row=0, column=0)
        self.file_Path = tk.StringVar()
        self.path = tk.Entry(master_window, textvariable=self.file_Path, validate="key", validatecommand=self.IsPathValid)
        self.path.grid(row=0, column=1)
        self.browse_button = tk.Button(master_window, text="Browse", command= self.getfolderpath)
        self.browse_button.grid(row=0, column=2)

        # Number of clusters k
        self.k_label = tk.Label(master_window, text="Number of clusters k")
        self.k_label.grid(row=1, column=0)
        # ikv = self.master.register(self.IsKValid)
        # validatecommand=(ikv, '%P'))
        self.k = tk.Entry(master_window, validate="key", validatecommand=self.IsKValid)
        self.k.grid(row=1, column=1)

        # Number of runs
        self.runs_label = tk.Label(master_window, text="Number of runs")
        self.runs_label.grid(row=2, column=0)
        # irv = self.master.register(self.IsRunsValid)
        # validatecommand=(irv, '%P'))
        self.runs = tk.Entry(master_window, validate="key", validatecommand=self.IsRunsValid)
        self.runs.grid(row=2, column=1)

        # Pre_process
        self.pre_process_button = tk.Button(master_window, text="Pre_process", command= self.PreProcess)
        self.pre_process_button.grid(row=4, column=1)
        self.pre_process_button["state"] = "disabled" # can"t press until all previous requirements are fine

        # Cluster
        self.cluster_button = tk.Button(master_window, text="Cluster", command=self.Cluster)
        self.cluster_button.grid(row=5, column=1)
        self.cluster_button["state"] = "disabled" # can"t press until all previous requirements are fine

    # Checks if path is valid
    def IsPathValid(self):
        return

    # update file_path after picking one with the browser
    def getfolderpath(self):
        try:
            self.file_Path.set(filedialog.askdirectory())
            self.IsPathValid()
        except ValueError:
            messagebox.showinfo(title="K Means Clustering", message="Path not valid")

    # Checks if number of clusters k is valid
    def IsKValid(self):
        try:
            return
        except ValueError:
            messagebox.showinfo(title="K Means Clustering", message="number of clusters k is not valid")

    # Checks if number of runs is valid
    def IsRunsValid(self):
        return

    # Load the file, process it and clean it
    def PreProcess(self):
        return

    # Build K-Means model and make visualization output
    def Cluster(self):
        return

root = tk.Tk()
my_gui = GUI(root)
root.mainloop()