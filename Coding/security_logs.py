import subprocess
import datetime

def get_antivirus_status():
    try:
        cmd = 'powershell -Command "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object -ExpandProperty displayName"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        
        if not output:
            return "No antivirus detected"

        antivirus_list = output.split("\n")  # Handle multiple AVs
        return f"Antivirus: {', '.join(antivirus_list)}"

    except Exception as e:
        return f"Error retrieving antivirus status: {e}"


def get_last_scan_time():
    try:
        cmd = 'powershell -Command "(Get-MpComputerStatus).ScanTime"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

        if not output:
            return "No scan data available (Windows Defender may be disabled or another AV is in use)"

        return output

    except Exception as e:
        return f"Error retrieving last scan time: {e}"


def log_antivirus_status():
    status = get_antivirus_status()
    scan_time = get_last_scan_time()
    
    log_entry = f"""
    📌 [Antivirus Security Log]
    -------------------------------------
    Timestamp: {datetime.datetime.now()}
    {status}

    Last Scan Time:
    {scan_time}
    -------------------------------------
    """
    
    with open("security_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")
    
    print(log_entry)

if __name__ == "__main__":
    log_antivirus_status()
