import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from system_audit import generate_system_report, get_system_info, get_network_details, get_last_windows_update, get_desktop_files
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cache_manager import clear_all_caches, clear_recycle_bin, clear_temp_files, clear_dns_cache, clear_windows_update_cache
from log_manager import get_security_logs, get_system_logs, get_application_logs, get_dns_logs, get_usb_logs
import threading
import time
from security_logs import get_antivirus_status, get_last_scan_time
import subprocess

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

canvas_widget = None  # Initialize canvas_widget
cpu_label = None  # Label for CPU usage value
mem_label = None  # Label for Memory usage value

def clear_cache_section():
    for widget in main_content.winfo_children():
        widget.destroy()
    
    label = ttk.Label(main_content, text="\U0001F6E0\ufe0f Select Cache to Clear:", font=("Arial", 14, "bold"))
    label.pack(pady=10)
    
    btn_frame = ttk.Frame(main_content)
    btn_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    
    def create_clear_button(text, command):
        btn = tb.Button(btn_frame, text=text, bootstyle="primary", command=command)
        btn.pack(pady=5, fill=tk.X)
    
    create_clear_button("Clear Recycle Bin", clear_recycle_bin)
    create_clear_button("Clear Temp Files", clear_temp_files)
    create_clear_button("Clear DNS Cache", clear_dns_cache)
    create_clear_button("Clear Windows Update Cache", clear_windows_update_cache)
    create_clear_button("Clear All Caches", clear_all_caches)

def antivirus_section():
    for widget in main_content.winfo_children():
        widget.destroy()
    
    label = ttk.Label(main_content, text="\U0001F6E1 Antivirus Status:", font=("Arial", 14, "bold"))
    label.pack(pady=10)

    # Get antivirus details
    antivirus_status = get_antivirus_status()
    scan_time = get_last_scan_time()

    # Display antivirus status
    status_label = ttk.Label(main_content, text=antivirus_status, font=("Arial", 12))
    status_label.pack(pady=5)

    # Display last scan time
    scan_label = ttk.Label(main_content, text=scan_time, font=("Arial", 12))
    scan_label.pack(pady=5)



def update_report(section="Home"):
    global canvas_widget, text_widget, cpu_label, mem_label, fig, ax1, ax2, canvas

    for widget in main_content.winfo_children():
        widget.pack_forget()
    
    if section == "Live System Monitor":
        if canvas_widget is not None:
            canvas_widget.destroy()
            canvas_widget = None
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 4))
        canvas = FigureCanvasTkAgg(fig, master=main_content)
        canvas_widget = canvas.get_tk_widget()
        
        cpu_label = ttk.Label(main_content, text="", font=("Arial", 12, "bold"))
        mem_label = ttk.Label(main_content, text="", font=("Arial", 12, "bold"))
        
        cpu_label.pack(pady=5)
        mem_label.pack(pady=5)
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        threading.Thread(target=update_graph, daemon=True).start()
        return
    
    if section == "Clear Cache":
        clear_cache_section()
        return
    
    if section == "Antivirus Status":
        antivirus_section()  # Call antivirus function directly
        return
    
    if canvas_widget is not None:
        canvas_widget.pack_forget()
        canvas_widget = None
    
    text_widget = tk.Text(main_content, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    reports = {
        "Home": generate_system_report(),
        "System Info": "\n\U0001F4CC System Info:\n" + "\n".join([f"{k}: {v}" for k, v in get_system_info().items()]),
        "Network Details": "\n\U0001F4CC Network Details:\n" + "\n".join([f"{k}: {v}" for k, v in get_network_details().items()]),
        "Windows Updates": f"\n\U0001F4CC Last Windows Update:\n{get_last_windows_update()}",
        "Desktop Files": f"\n\U0001F4CC Desktop Files:\n{get_desktop_files()}",
        "Security Logs": f"\n\U0001F4CC Security Logs:\n{get_security_logs()}",
        "System Logs": f"\n\U0001F4CC System Logs:\n{get_system_logs()}",
        "Application Logs": f"\n\U0001F4CC Application Logs:\n{get_application_logs()}",
        "DNS Logs": f"\n\U0001F4CC DNS Logs:\n{get_dns_logs()}",
        "USB Logs": f"\n\U0001F4CC USB Logs:\n{get_usb_logs()}",
    }
    
    report = reports.get(section, "Unknown Section")
    
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, report)
    text_widget.config(state=tk.DISABLED)

def update_graph():
    cpu_usage = []
    mem_usage = []
    
    while True:
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            
            cpu_usage.append(cpu)
            mem_usage.append(mem)
            
            if len(cpu_usage) > 20:
                cpu_usage.pop(0)
                mem_usage.pop(0)
            
            ax1.clear()
            ax2.clear()
            
            ax1.plot(cpu_usage, label="CPU Usage (%)", color="red")
            ax2.plot(mem_usage, label="Memory Usage (%)", color="blue")
            
            ax1.set_ylim(0, 100)
            ax2.set_ylim(0, 100)
            ax1.legend()
            ax2.legend()
            
            if canvas_widget and canvas_widget.winfo_exists():
                canvas.draw()
            else:
                print("Live System Monitor closed, stopping updates.")
                break
            
            if cpu_label and cpu_label.winfo_exists():
                cpu_label.config(text=f"CPU Usage: {cpu:.2f}%")
            if mem_label and mem_label.winfo_exists():
                mem_label.config(text=f"Memory Usage: {mem:.2f}%")
            
        except Exception as e:
            print(f"Error updating labels: {e}")
            break
        
        time.sleep(1)

def create_nav_button(label):
    return tb.Button(sidebar, text=label, bootstyle="secondary", command=lambda: update_report(label))

buttons = ["Home", "System Info", "Network Details", "Windows Updates", "Desktop Files", "Live System Monitor", "Clear Cache", "Security Logs", "System Logs", "Application Logs", "DNS Logs", "USB Logs","Antivirus Status"]
for btn in buttons:
    tb.Button(sidebar, text=btn, bootstyle="secondary", command=lambda b=btn: update_report(b)).pack(fill=tk.X, pady=5)



def on_closing():
    root.quit()
    root.destroy()
    exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
