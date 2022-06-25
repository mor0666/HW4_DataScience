import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import PhotoImage
from Cluster import Cluster
import pandas as pd


# tk.Text - display multiple lines of text that can be edited
# tk.Entry - is used to accept single-line text strings from a user
# tk.Label - display one or more lines of text that cannot be modified by the user

class GUI:
    def __init__(self, master_window):
        self.master_window = master_window
        master_window.title("K Means Clustering")
        self.master_window.geometry("1300x600")
        self.k = -1
        self.runs = 0
        self.path_ok = False
        self.Clustermodel = Cluster()
        self.preprocessingDone = False
        self.currentDataframe = ""
        self.fig1 = ""
        self.fig2 = ""
        self.img1 = ""
        self.IsClustered = False

        # Path
        self.path_label = tk.Label(master_window, text="Data Path")
        self.path_label.grid(row=0, column=0,sticky='W')
        self.file_Path = tk.StringVar()
        self.path = tk.Entry(self.master_window, textvariable=self.file_Path,state='disabled',bd=2,width=60)
        self.path.grid(row=0, column=1,sticky='we')
        self.browse_button = tk.Button(master_window, text="Browse", command=self.getFilePath)
        self.browse_button.grid(row=0, column=2)

        # Number of clusters k
        self.k_label = tk.Label(self.master_window, text="Number of clusters k")
        self.k_label.grid(row=1, column=0)
        ikv = self.master_window.register(self.IsKValid)
        self.k = tk.Entry(self.master_window, validate="key", validatecommand=(ikv, '%P'))
        self.k.grid(row=1, column=1,sticky='W')

        # Number of runs
        self.runs_label = tk.Label(self.master_window, text="Number of runs")
        self.runs_label.grid(row=2, column=0,sticky='W')
        irv = self.master_window.register(self.IsRunsValid)
        self.runs = tk.Entry(self.master_window, validate="key", validatecommand=(irv, '%P'))
        self.runs.grid(row=2, column=1,sticky='W')

        # Pre_process
        self.pre_process_button = tk.Button(master_window, text="Pre-process", command=self.preprocess)
        self.pre_process_button.grid(row=4, column=1,sticky='we')
        self.pre_process_button["state"] = "disabled"  # can"t press until all previous requirements are fine
        #
        # Cluster
        self.cluster_button = tk.Button(master_window, text="Cluster", command=self.cluster)
        self.cluster_button.grid(row=5, column=1,sticky='we')
        self.cluster_button["state"] = "disabled"  # can"t press until all previous requirements are fine

        self.master_window.grid_rowconfigure(6,weight=1)
        self.master_window.grid_columnconfigure(1, weight=1)
        self.master_window.grid_columnconfigure(3, weight=1)

    # update file_path after picking one with the browser
    def getFilePath(self):
        try:
            self.preprocessingDone = False
            self.currentDataframe = ""
            self.cluster_button["state"] = "disabled"
            self.pre_process_button["state"] = "disabled"
            self.file_Path.set(filedialog.askopenfilename(title="Select Data file", initialdir="/",
                                                          filetypes=[('Excel files', '*.xlsx')]))
            # self.file_Path = filedialog.askopenfilename(title="Select Data file", initialdir="/",
            #                                               filetypes=[('Excel files', '*.xlsx')])
            self.IsPathValid(self.file_Path)
        except ValueError:
            messagebox.showinfo(title="K Means Clustering", message="Path not valid")

    # Checks if path is valid
    def IsPathValid(self, path):
        try:
            self.path_ok = False
            if self.pre_process_button["state"] == "active":
                self.pre_process_button["state"] = "disabled"
            if path.get() == "":
                return False
            df = pd.read_excel(path.get())
            if df.empty:
                tk.messagebox.showinfo(title="K Means Clustering", message=str(path.get()) + " is empty!")
                self.file_Path.set("")
                return False
            self.path_ok = True
            self.pre_process_button["state"] = "active"
        except Exception as e:
            print(e)
            tk.messagebox.showinfo(title="K Means Clustering", message="Bad parameters. Please try again")

    # Checks if number of clusters k is valid
    def IsKValid(self, num_input): #n_clusters
        try:
            if num_input.isdigit(): #if the user filled an integer
                self.k = int(num_input)  # convert
                if self.k <= 0 or self.k > 15:
                    if(self.k <= 0):
                        self.cluster_button["state"] = "disabled"
                    messagebox.showinfo(title="K Means Clustering",message="Bad parameters,enter a number between 1 and 15")
                    return False
                if 0 < self.k <= 15:
                    if isinstance(self.runs, int):
                        if self.preprocessingDone and self.runs >= 1 and self.runs <= 300:
                            self.cluster_button["state"] = "active"
                        else:
                            self.cluster_button["state"] = "disabled"
                    else:
                        self.cluster_button["state"] = "disabled"
                else:
                    self.cluster_button["state"] = "disabled"
                return True
            elif num_input == "": #if the user didnt fill it yet
                self.k = ""  # User didn't fill it yet
                self.cluster_button["state"] = "disabled"
                return True
            else: #if input is not good
                if self.has_numbers(num_input) == False:
                    self.cluster_button["state"] = "disabled"
                messagebox.showinfo(title="K Means Clustering", message="Bad parameters,enter a number between 1 and 15")
                return False
        except ValueError:
            messagebox.showinfo(title="K Means Clustering", message="Bad parameters,enter a number between 1 and 15")

    # Checks if number of runs is valid
    def IsRunsValid(self, num_input): #n_init
        try:
            if num_input.isdigit():  # if the user filled an integer
                self.runs = int(num_input)  # convert
                if self.runs <= 0 or self.runs > 300:
                    if (self.runs <= 0):
                        self.cluster_button["state"] = "disabled"
                    messagebox.showinfo(title="K Means Clustering",message="Error, enter a number between 1 and 300")
                    return False
                if 1 <= self.runs <= 300:
                    if isinstance(self.k, int):
                        if self.preprocessingDone and self.k > 0 and self.k <= 15:
                            self.cluster_button["state"] = "active"
                        else:
                            self.cluster_button["state"] = "disabled"
                    else:
                        self.cluster_button["state"] = "disabled"
                else:
                    self.cluster_button["state"] = "disabled"
                return True
            elif num_input == "":  # if the user didnt fill it yet
                self.runs = ""  # User didn't fill it yet
                self.cluster_button["state"] = "disabled"
                return True
            else:  # if input is not good
                if self.has_numbers(num_input) == False:
                    self.cluster_button["state"] = "disabled"
                messagebox.showinfo(title="K Means Clustering",message="Error,enter a number between 1 and 300")
                return False
        except ValueError:
            messagebox.showinfo(title="K Means Clustering", message="Error,enter a number between 1 and 300")

    #process the file and clean it
    def preprocess(self):
        try:
            self.currentDataframe = self.Clustermodel.preprocess(self.file_Path)  # Call the pre-process method
            tk.messagebox.showinfo(title="K Means Clustering", message="Preprocessing completed successfully!")
            self.preprocessingDone=True
            if isinstance(self.runs, int) and isinstance(self.k, int):
                if self.preprocessingDone and self.runs >= 1 and self.runs <= 300 and self.k > 0 and self.k <= 15:
                    self.cluster_button["state"] = "active"
        except Exception as e:
            tk.messagebox.showinfo(title="K Means Clustering", message="Preprocessing couldn't complete")

    # Build K-Means model and make visualization output
    def cluster(self):
        try:
            self.Clustermodel.cluster(self.currentDataframe, self.k, self.runs)  # Call the cluster method
            self.img1 = PhotoImage(file='plot1.png')
            self.fig1 = tk.Label(self.master_window,image=self.img1)
            self.fig1.grid(row=6, column=3,sticky='wens')
            self.fig2 = tk.Label(self.master_window, image=self.img1)
            self.fig2.grid(row=6, column=1, sticky='wens')
            self.IsClustered = True
            tk.messagebox.showinfo(title="K Means Clustering", message="K-means model and clusters visualization done")
            #self.master_window.destroy()
        except ValueError:
            tk.messagebox.showinfo(title="K Means Clustering", message="Bad parameters. Please try again")

    def has_numbers(self,inputString):
        return any(char.isdigit() for char in inputString)


root = tk.Tk()
my_gui = GUI(root)
root.mainloop()
