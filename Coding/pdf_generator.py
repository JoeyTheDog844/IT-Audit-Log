from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from system_audit import get_system_info, get_network_details, get_last_windows_update, get_desktop_files
from log_manager import get_security_logs, get_system_logs, get_application_logs, get_dns_logs, get_usb_logs
from security_logs import get_antivirus_status, get_last_scan_time

def generate_pdf_report():
    filename = "System_Audit_Report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y_position = height - 40  # Start position for text

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y_position, "System Audit Report")
    y_position -= 40

    def add_section(title, content):
        nonlocal y_position
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, title)
        y_position -= 20
        c.setFont("Helvetica", 10)
        for line in content.split("\n"):
            c.drawString(60, y_position, line)
            y_position -= 15
        y_position -= 10  # Space between sections

    # Collect system data
    add_section("System Info", "\n".join([f"{k}: {v}" for k, v in get_system_info().items()]))
    add_section("Network Details", "\n".join([f"{k}: {v}" for k, v in get_network_details().items()]))
    add_section("Last Windows Update", get_last_windows_update())
    desktop_files = get_desktop_files()
    if isinstance(desktop_files, tuple):  # Ensure it's not a tuple
        desktop_files = "\n".join(map(str, desktop_files))  

    add_section("Desktop Files", desktop_files)


    # Collect log data
    add_section("Security Logs", get_security_logs())
    add_section("System Logs", get_system_logs())
    add_section("Application Logs", get_application_logs())
    add_section("DNS Logs", get_dns_logs())
    add_section("USB Logs", get_usb_logs())

    # Antivirus Status
    add_section("Antivirus Status", get_antivirus_status())
    add_section("Last Antivirus Scan Time", get_last_scan_time())

    c.save()
    print(f"PDF Report Generated: {filename}")
