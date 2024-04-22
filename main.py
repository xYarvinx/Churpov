import tkinter as tk
import numpy as np
from scipy.stats import chi2_contingency

def calculate_chuprov():
    observed = []
    for i in range(rows):
        row_data = []
        row_sum = 0
        for j in range(cols):
            entry_value = int(data_entries[i][j].get())
            row_data.append(entry_value)
            row_sum += entry_value
        row_data.append(row_sum)
        observed.append(row_data)

    chi2, _, _, _ = chi2_contingency(np.array(observed))
    n = np.sum(observed)
    c = np.sqrt(chi2 / (2 + n))

    result_label.config(text=f"Коэффициент Чупрова: {c}")


    row_sums = np.sum(observed, axis=1)
    col_sums = np.sum(observed, axis=0)

    for i in range(rows):
        data_entries[i][cols].insert(tk.END, row_sums[i])

    for j in range(cols+1):
        col_sum = sum(observed[i][j] for i in range(rows))
        col_sum_entry = tk.Entry(data_frame, width=8)
        col_sum_entry.insert(tk.END, col_sum)
        col_sum_entry.grid(row=rows, column=j)

def on_create_table_click():
    global rows, cols
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())


    for widget in data_frame.winfo_children():
        widget.destroy()

    # Create data entries
    global data_entries
    data_entries = []
    for i in range(rows):
        row_entries = []
        for j in range(cols):
            entry = tk.Entry(data_frame, width=8)
            entry.grid(row=i, column=j)
            row_entries.append(entry)
        row_entries.append(tk.Entry(data_frame, width=8))
        data_entries.append(row_entries)


    col_sum_entries = []
    for j in range(cols):
        col_sum = 0
        for i in range(rows):
            entry = data_entries[i][j]
            col_sum += int(entry.get())
        col_sum_entry = tk.Entry(data_frame, width=8)
        col_sum_entry.insert(tk.END, col_sum)
        col_sum_entry.grid(row=rows, column=j)
        col_sum_entries.append(col_sum_entry)

    # Calculate the overall table sum
    overall_sum = sum(int(entry.get()) for row in data_entries for entry in row[:-1])
    overall_sum_entry = tk.Entry(data_frame, width=8)
    overall_sum_entry.insert(tk.END, overall_sum)
    overall_sum_entry.grid(row=rows, column=cols)

# GUI setup
root = tk.Tk()
root.title("Расчет коэффициента Чупрова")
root.geometry("600x400")

entry_frame = tk.Frame(root)
entry_frame.pack()

rows_label = tk.Label(entry_frame, text="Количество строк:")
rows_label.grid(row=0, column=0)
rows_entry = tk.Entry(entry_frame)
rows_entry.grid(row=0, column=1)

cols_label = tk.Label(entry_frame, text="Количество столбцов:")
cols_label.grid(row=1, column=0)
cols_entry = tk.Entry(entry_frame)
cols_entry.grid(row=1, column=1)

create_table_button = tk.Button(entry_frame, text="Создать таблицу", command=on_create_table_click)
create_table_button.grid(row=2, column=0, columnspan=2)

data_frame = tk.Frame(root)
data_frame.pack()

result_label = tk.Label(root, text="")
result_label.pack()

calculate_button = tk.Button(root, text="Вычислить Чупрова", command=calculate_chuprov)
calculate_button.pack()

data_entries = []

root.mainloop()
