import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import KMeans

def load_file():
    global data, headers
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            headers = data[0]
            data = data[1:]
        update_table(data, headers)
        update_column_selection()


def update_table(data, headers):
    table.delete(*table.get_children())
    table["columns"] = headers
    table.configure(show='headings')

    for col in headers:
        table.heading(col, text=col)
        table.column(col, width=150, anchor="center")

    for row in data:
        table.insert("", "end", values=row)


def update_column_selection():
    column_listbox.delete(0, tk.END)
    for col in headers:
        column_listbox.insert(tk.END, col)


def show_correlation_matrix():
    if not data:
        return

    numeric_data = []
    valid_columns = []

    for col_idx in range(len(headers)):
        column_values = []
        for row in data:
            try:
                column_values.append(float(row[col_idx]))
            except ValueError:
                column_values.append(np.nan)

        numeric_data.append(column_values)
        valid_columns.append(headers[col_idx])

    numeric_data = np.array(numeric_data, dtype=np.float64).T

    mask = ~np.isnan(numeric_data).all(axis=0)
    numeric_data = numeric_data[:, mask]
    valid_columns = [valid_columns[i] for i in range(len(mask)) if mask[i]]

    if numeric_data.shape[1] < 2:
        messagebox.showerror("Error", "Too few numeric columns for correlation.")
        return

    correlation_matrix = np.corrcoef(numeric_data, rowvar=False)

    plot_window = tk.Toplevel(window)
    plot_window.title("Correlation Matrix")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", xticklabels=valid_columns, yticklabels=valid_columns)
    ax.set_title("Correlation Matrix")

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()


def show_histogram():
    if not data or not headers:
        return

    selected_indices = column_listbox.curselection()
    if len(selected_indices) != 1:
        messagebox.showinfo("Info", "Please select exactly one column for histogram.")
        return

    col = headers[selected_indices[0]]
    col_idx = headers.index(col)

    try:
        values = [float(row[col_idx]) for row in data]
    except ValueError:
        messagebox.showerror("Error", "Selected column must be numeric.")
        return

    plot_window = tk.Toplevel(window)
    plot_window.title(f"Histogram - {col}")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(values, bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f"Histogram for {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def visualize_data():
    if not data or not headers:
        return

    selected_indices = column_listbox.curselection()
    if len(selected_indices) == 0:
        messagebox.showinfo("Info", "Please select at least one column to visualize.")
        return

    selected_columns = [headers[i] for i in selected_indices]

    plot_window = tk.Toplevel(window)
    plot_window.title("Data Visualization")

    fig, ax = plt.subplots(figsize=(8, 6))

    for col in selected_columns:
        try:
            col_idx = headers.index(col)
            y_values = [float(row[col_idx]) for row in data]
            x_values = list(range(len(y_values)))
            ax.plot(x_values, y_values, label=col, marker='o')
        except ValueError:
            continue

    ax.set_title("Selected Data Visualization")
    ax.set_xlabel("Row Index")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def classify_data():
    if not data or not headers:
        return

    selected_indices = column_listbox.curselection()
    selected_columns = [headers[i] for i in selected_indices]

    if len(selected_columns) < 2:
        messagebox.showerror("Error", "Please select at least 2 numeric columns for classification.")
        return

    try:
        k = int(k_entry.get())
        if k < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for K.")
        return

    numeric_data = []
    for col in selected_columns:
        col_idx = headers.index(col)
        column_values = []
        for row in data:
            try:
                column_values.append(float(row[col_idx]))
            except ValueError:
                column_values.append(np.nan)
        numeric_data.append(column_values)

    numeric_data = np.array(numeric_data, dtype=np.float64).T

    mask = ~np.isnan(numeric_data).all(axis=0)
    numeric_data = numeric_data[:, mask]
    selected_columns = [selected_columns[i] for i in range(len(mask)) if mask[i]]

    if numeric_data.shape[1] < 2:
        messagebox.showerror("Error", "Too few numeric columns available after filtering.")
        return

    numeric_data = numeric_data[~np.isnan(numeric_data).any(axis=1)]

    if len(numeric_data) == 0:
        messagebox.showerror("Error", "No complete rows available after filtering missing data.")
        return

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(numeric_data)

    plot_window = tk.Toplevel(window)
    plot_window.title("K-Means Clustering")

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(numeric_data[:, 0], numeric_data[:, 1], c=labels, cmap="viridis")
    ax.set_xlabel(selected_columns[0])
    ax.set_ylabel(selected_columns[1])
    ax.set_title("K-Means Clustering")
    legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.add_artist(legend1)

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.get_tk_widget().pack()
    canvas.draw()


# Create UI
window = tk.Tk()
window.title("Prediction and Classification App")
window.geometry("1000x750")

data = []
headers = []

# Top Buttons
btn_frame = tk.Frame(window)
btn_frame.pack(pady=10)

btn_load = tk.Button(btn_frame, text="Load CSV", command=load_file)
btn_load.grid(row=0, column=0, padx=5)

btn_correlation = tk.Button(btn_frame, text="Correlation Matrix", command=show_correlation_matrix)
btn_correlation.grid(row=0, column=1, padx=5)

btn_visualize = tk.Button(btn_frame, text="Data Visualization", command=visualize_data)
btn_visualize.grid(row=0, column=2, padx=5)

btn_hist = tk.Button(btn_frame, text="Histogram", command=show_histogram)
btn_hist.grid(row=0, column=3, padx=5)

# Data Table
frame = tk.Frame(window)
frame.pack(expand=True, fill='both', padx=10, pady=5)

scroll_y = tk.Scrollbar(frame, orient="vertical")
scroll_x = tk.Scrollbar(frame, orient="horizontal")

table = ttk.Treeview(frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, show="headings")
scroll_y.config(command=table.yview)
scroll_x.config(command=table.xview)

scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
table.pack(expand=True, fill='both')

# Column Selection & K-Means Controls
selection_frame = tk.Frame(window)
selection_frame.pack(pady=10)

tk.Label(selection_frame, text="Select Columns for Classification:").grid(row=0, column=0, columnspan=2)

listbox_frame = tk.Frame(selection_frame)
listbox_frame.grid(row=1, column=0, columnspan=2, pady=5)

column_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
column_listbox = tk.Listbox(listbox_frame, selectmode="multiple", height=6, exportselection=False,
                            yscrollcommand=column_scrollbar.set, width=40)
column_scrollbar.config(command=column_listbox.yview)
column_listbox.pack(side="left", fill="y")
column_scrollbar.pack(side="right", fill="y")

k_label = tk.Label(selection_frame, text="Number of Clusters (K):")
k_label.grid(row=2, column=0, pady=5)
k_entry = tk.Entry(selection_frame)
k_entry.grid(row=2, column=1, pady=5)
k_entry.insert(0, "3")

btn_classify = tk.Button(selection_frame, text="K-Means Classification", command=classify_data)
btn_classify.grid(row=3, column=0, columnspan=2, pady=5)

window.mainloop()
