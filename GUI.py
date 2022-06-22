import tkinter as tk
from tkinter import filedialog, messagebox
from Cluster import Cluster


# tk.Text - display multiple lines of text that can be edited
# tk.Entry - is used to accept single-line text strings from a user
# tk.Label - display one or more lines of text that cannot be modified by the user

class GUI:
    def __init__(self, master_window):
        self.master_window = master_window
        master_window.title("K Means Clustering")
        self.master_window.geometry("350x100")
        self.k = -1
        self.runs = 0
        self.Clustermodel = Cluster()

        # Path
        self.path_label = tk.Label(master_window, text="Data Path")
        self.path_label.grid(row=0, column=0)
        self.file_Path = tk.StringVar()
        self.path = tk.Entry(master_window, textvariable=self.file_Path, validate="key",
                             validatecommand=self.IsPathValid)
        self.path.grid(row=0, column=1)
        self.browse_button = tk.Button(master_window, text="Browse", command=self.getFolderPath)
        self.browse_button.grid(row=0, column=2)

        # Number of clusters k
        self.k_label = tk.Label(master_window, text="Number of clusters k")
        self.k_label.grid(row=1, column=0)
        ikv = self.master_window.register(self.IsKValid)
        self.k = tk.Entry(master_window, validate="key", validatecommand=(ikv, '%P'))
        self.k.grid(row=1, column=1)

        # Number of runs
        self.runs_label = tk.Label(master_window, text="Number of runs")
        self.runs_label.grid(row=2, column=0)
        irv = self.master_window.register(self.IsRunsValid)
        self.runs = tk.Entry(master_window, validate="key", validatecommand=(irv, '%P'))
        self.runs.grid(row=2, column=1)

        # Pre_process
        self.pre_process_button = tk.Button(master_window, text="Pre_process", command=self.preprocess)
        self.pre_process_button.grid(row=4, column=1)
        self.pre_process_button["state"] = "disabled"  # can"t press until all previous requirements are fine

        # Cluster
        self.cluster_button = tk.Button(master_window, text="Cluster", command=self.cluster())
        self.cluster_button.grid(row=5, column=1)

    # update file_path after picking one with the browser
    def getFolderPath(self):
        try:
            self.file_Path.set(filedialog.askdirectory())
            self.IsPathValid()
        except ValueError:
            messagebox.showinfo(title="K Means Clustering", message="Path not valid")

    # Checks if path is valid
    def IsPathValid(self):
        try:
            return
        except ValueError:
            tk.messagebox.showinfo(title="K Means Clustering", message="Bad parameters. Please try again")

    # Checks if number of clusters k is valid
    def IsKValid(self, num_input):
        try:
            if num_input == "":
                self.k = ""  # User didn't fill it yet
                return True
            if not num_input:  #
                return False
            self.k = int(num_input)  # convert
            if 0 < self.k < 10:
                return num_input
        except ValueError:
            messagebox.showinfo(title="K Means Clustering", message="Bad parameters")

    # Checks if number of runs is valid
    def IsRunsValid(self, num_input):
        try:
            if num_input == "":
                self.runs = ""  # User didn't fill it yet
                return True
            if not num_input:  # Check if there is any input from user
                return False
            self.runs = int(num_input)  # convert
            if self.runs > 0:
                return num_input
        except ValueError:
            messagebox.showinfo(title="K Means Clustering", message="Bad parameters")

    # Load the file, process it and clean it
    def preprocess(self):
        try:
            if self.k != "" and 0 < self.k < 10 and self.runs > 0:
                self.cluster_button["state"] = "active"
                self.Clustermodel.preprocess(self.file_Path)  # Call the pre-process method
                tk.messagebox.showinfo(title="Pre-Process complete", message="Data was pre-processed")
            else:
                tk.messagebox.showinfo(title="Pre-Process error", message="Bad parameters. Please try again")
        except ValueError:
            tk.messagebox.showinfo(title="Pre-Process error", message="Bad parameters. Please try again")

    # Build K-Means model and make visualization output
    def cluster(self):
        try:
            self.Clustermodel.cluster(self.file_Path, self.k, self.runs)  # Call the cluster method
            tk.messagebox.showinfo(title="Clusters complete", message="K-means model and clusters visualization done")
            self.master_window.destroy()
        except ValueError:
            tk.messagebox.showinfo(title="Clusters error", message="Bad parameters. Please try again")


root = tk.Tk()
my_gui = GUI(root)
root.mainloop()
