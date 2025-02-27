import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from system_audit import generate_system_report, get_system_info, get_network_details, get_last_windows_update, get_desktop_files

# Create main application window
root = tb.Window(themename="darkly")
root.title("System Audit Tool")
root.geometry("800x600")
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

# Function to update the report
def update_report(section="Home"):
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

update_report()  # Load initial report

# Navigation buttons
def create_nav_button(label):
    return tb.Button(sidebar, text=label, bootstyle="secondary", command=lambda: update_report(label))

buttons = ["Home", "System Info", "Network Details", "Windows Updates", "Desktop Files"]
for btn in buttons:
    create_nav_button(btn).pack(fill=tk.X, pady=5)

# Refresh button
refresh_button = tb.Button(root, text="Refresh Report", bootstyle="primary", command=lambda: update_report())
refresh_button.pack(pady=10)

# Run the application
root.mainloop()
