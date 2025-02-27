import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from system_audit import generate_system_report, get_system_info, get_network_details, get_last_windows_update, get_desktop_files
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cache_manager import clear_all_caches, clear_recycle_bin, clear_temp_files, clear_dns_cache, clear_windows_update_cache

# Create main application window
root = tb.Window(themename="darkly")
root.title("System Audit Tool")
root.geometry("900x600")
root.resizable(False, False)

# Sidebar navigation frame
sidebar = ttk.Frame(root, padding=10)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

# Main content frame
main_content = ttk.Frame(root, padding=10)
main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a label for the title
title_label = ttk.Label(main_content, text="System Audit Dashboard", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Create a Text widget with a scrollbar
text_widget = tk.Text(main_content, wrap=tk.WORD, font=("Arial", 12), bg="#2b2b2b", fg="white", padx=10, pady=10, relief=tk.FLAT, state=tk.DISABLED)
scrollbar = ttk.Scrollbar(main_content, command=text_widget.yview)
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Matplotlib figure for live monitoring
fig, (ax_cpu, ax_mem) = plt.subplots(2, 1, figsize=(5, 4))
fig.tight_layout(pad=3.0)
canvas = FigureCanvasTkAgg(fig, master=main_content)
canvas_widget = canvas.get_tk_widget()
cpu_usage_data = []
mem_usage_data = []

# Function to update the report
def update_report(section="Home"):
    global text_widget  # Ensure text_widget remains consistent
    
    for widget in main_content.winfo_children():
        widget.pack_forget()
    
    if section == "Live System Monitor":
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        update_graph()
        return
    
    if section == "Clear Cache":
        clear_cache_frame = ttk.Frame(main_content)
        clear_cache_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        tb.Button(clear_cache_frame, text="Clear Recycle Bin", bootstyle="danger", command=clear_recycle_bin).pack(fill=tk.X, pady=5)
        tb.Button(clear_cache_frame, text="Clear Temp Files", bootstyle="danger", command=clear_temp_files).pack(fill=tk.X, pady=5)
        tb.Button(clear_cache_frame, text="Clear DNS Cache", bootstyle="danger", command=clear_dns_cache).pack(fill=tk.X, pady=5)
        tb.Button(clear_cache_frame, text="Clear Windows Update Cache", bootstyle="danger", command=clear_windows_update_cache).pack(fill=tk.X, pady=5)
        tb.Button(clear_cache_frame, text="Clear All Caches", bootstyle="danger", command=clear_all_caches).pack(fill=tk.X, pady=5)
        return
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    
    if section == "Home":
        report = generate_system_report()
    elif section == "System Info":
        report = f"\n📌 System Info:\n" + "\n".join([f"{k}: {v}" for k, v in get_system_info().items()])
    elif section == "Network Details":
        report = f"\n📌 Network Details:\n" + "\n".join([f"{k}: {v}" for k, v in get_network_details().items()])
    elif section == "Windows Updates":
        report = f"\n📌 Last Windows Update:\n{get_last_windows_update()}"
    elif section == "Desktop Files":
        report = f"\n📌 Desktop Files:\n{get_desktop_files()}"
    else:
        report = "Unknown Section"
    
    text_widget.insert(tk.END, report)
    text_widget.config(state=tk.DISABLED)

update_task = None

# Function to update live CPU & Memory graphs
def update_graph():
    global update_task
    cpu_usage_data.append(psutil.cpu_percent())
    mem_usage_data.append(psutil.virtual_memory().percent)

    if len(cpu_usage_data) > 50:
        cpu_usage_data.pop(0)
        mem_usage_data.pop(0)

    ax_cpu.clear()
    ax_mem.clear()

    ax_cpu.plot(cpu_usage_data, label=f"CPU Usage: {cpu_usage_data[-1]}%", color="red")
    ax_mem.plot(mem_usage_data, label=f"Memory Usage: {mem_usage_data[-1]}%", color="blue")

    ax_cpu.set_ylim(0, 100)
    ax_mem.set_ylim(0, 100)

    ax_cpu.set_title("CPU Usage")
    ax_mem.set_title("Memory Usage")

    ax_cpu.legend()
    ax_mem.legend()

    canvas.draw()
    update_task = root.after(1000, update_graph)

# Navigation buttons
def create_nav_button(label):
    return tb.Button(sidebar, text=label, bootstyle="secondary", command=lambda: update_report(label))

buttons = ["Home", "System Info", "Network Details", "Windows Updates", "Desktop Files", "Live System Monitor", "Clear Cache"]
for btn in buttons:
    create_nav_button(btn).pack(fill=tk.X, pady=5)

def on_closing():
    global update_task
    if update_task:
        root.after_cancel(update_task)
    root.quit()
    root.destroy()
    exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
