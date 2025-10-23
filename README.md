# Python_Jupyter_Codding
Projek Mandiri Python

```{python}
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StatisticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Statistics Data Analysis")
        self.root.geometry("1000x800")
        
        # Variables
        self.value_var = tk.StringVar()
        self.frequency_var = tk.StringVar()
        self.data_list = []
        
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input Frame
        input_frame = ttk.LabelFrame(main_frame, text="Input Data", padding=20)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Input Fields
        ttk.Label(input_frame, text="Nilai:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.value_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Frekuensi:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.frequency_var).grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Tambah Data", command=self.add_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Hitung Statistik", command=self.calculate_statistics).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)

        # Display Frame
        display_frame = ttk.LabelFrame(main_frame, text="Data dan Hasil Analisis", padding=15)
        display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Treeview for data display
        self.tree = ttk.Treeview(display_frame, columns=("Value", "Frequency"), show="headings")
        self.tree.heading("Value", text="Nilai")
        self.tree.heading("Frequency", text="Frekuensi")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Statistics Frame
        stats_frame = ttk.LabelFrame(main_frame, text="Hasil Statistik", padding=15)
        stats_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.stats_text = tk.Text(stats_frame, height=6, width=50)
        self.stats_text.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def add_data(self):
        try:
            value = float(self.value_var.get())
            freq = int(self.frequency_var.get())
            
            if freq <= 0:
                messagebox.showwarning("Warning", "Frekuensi harus lebih dari 0!")
                return
                
            self.tree.insert("", tk.END, values=(value, freq))
            self.data_list.append((value, freq))
            self.clear_inputs()
        except ValueError:
            messagebox.showwarning("Warning", "Masukkan nilai yang valid!")

    def calculate_statistics(self):
        if not self.data_list:
            messagebox.showwarning("Warning", "Tidak ada data untuk dihitung!")
            return

        values = []
        for value, freq in self.data_list:
            values.extend([value] * freq)
        
        values = np.array(values)
        
        mean = np.mean(values)
        median = np.median(values)
        std_dev = np.std(values)
        variance = np.var(values)
        
        stats_text = f"""
Hasil Analisis Statistik:
------------------------
Mean     : {mean:.2f}
Median   : {median:.2f}
Std Dev  : {std_dev:.2f}
Variance : {variance:.2f}
N        : {len(values)}
        """
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats_text)

    def clear_inputs(self):
        self.value_var.set("")
        self.frequency_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = StatisticsApp(root)
    root.mainloop()
```
