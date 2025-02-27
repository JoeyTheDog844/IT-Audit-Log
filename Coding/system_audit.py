import psutil
import socket
import subprocess
import os
import requests

# Function to get public IP
def get_public_ip():
    try:
        return requests.get("https://api64.ipify.org?format=text").text
    except:
        return "Could not retrieve"

# Function to get local IP
def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Could not retrieve"

# Function to list desktop files and count them
def get_desktop_files():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    try:
        files = os.listdir(desktop_path)
        file_count = len(files)
        file_list = "\n".join(files[:10]) if files else "No files found."
        return file_list, file_count
    except:
        return "Could not retrieve desktop files.", 0


# Function to get system info
def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return {
        "Local IP Address": get_local_ip(),
        "Public IP Address": get_public_ip(),
        "CPU Usage": f"{cpu_usage}%",
        "Memory Usage": f"{memory_usage}%"
    }

# Function to get network details
def get_network_details():
    try:
        ip_address = get_local_ip()
        mac_address = None
        for interface, addrs in psutil.net_if_addrs().items():
            if "Wi-Fi" in interface or "Ethernet" in interface:
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:
                        mac_address = addr.address
                        break
            if mac_address:
                break

        return {"MAC Address": mac_address or "Unknown", "IP Address": ip_address}
    except Exception as e:
        return {"Error": str(e)}

# Function to get last Windows update
def get_last_windows_update():
    try:
        command = "wmic qfe get Description,InstalledOn"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.stdout else "No update history found."
    except Exception as e:
        return f"Error: {e}"

# Generate system report
def generate_system_report():
    system_info = get_system_info()
    network_details = get_network_details()
    desktop_files, file_count = get_desktop_files()

    return f"""
🔍 System Audit Report

📌 System Info:
Local IP Address: {system_info["Local IP Address"]}
Public IP Address: {system_info["Public IP Address"]}
CPU Usage: {system_info["CPU Usage"]}
Memory Usage: {system_info["Memory Usage"]}

📌 Network Details:
MAC Address: {network_details["MAC Address"]}
IP Address: {network_details["IP Address"]}

📌 Last Windows Update:
{get_last_windows_update()}

📌 Desktop Files ({file_count} total):
{desktop_files}
"""

if __name__ == "__main__":
    print(generate_system_report())
