import os
import ctypes
import shutil
import subprocess

def clear_recycle_bin():
    """ Clears the Windows Recycle Bin. """
    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1)
        print("Recycle Bin cleared successfully.")
    except Exception as e:
        print(f"Error clearing Recycle Bin: {e}")

def clear_temp_files():
    """ Clears temporary files from the Windows temp folder. """
    temp_path = os.environ.get("TEMP", "C:\\Windows\\Temp")
    try:
        for file in os.listdir(temp_path):
            file_path = os.path.join(temp_path, file)
            if os.path.isfile(file_path) or os.path.isdir(file_path):
                shutil.rmtree(file_path, ignore_errors=True)
        print("Temporary files cleared.")
    except Exception as e:
        print(f"Error clearing temp files: {e}")

def clear_dns_cache():
    """ Clears the DNS cache using ipconfig. """
    try:
        subprocess.run("ipconfig /flushdns", shell=True, check=True)
        print("DNS cache cleared.")
    except Exception as e:
        print(f"Error clearing DNS cache: {e}")

def clear_windows_update_cache():
    """ Clears the Windows Update cache. """
    update_cache_path = "C:\\Windows\\SoftwareDistribution\\Download"
    try:
        shutil.rmtree(update_cache_path, ignore_errors=True)
        os.makedirs(update_cache_path)  # Recreate directory after deletion
        print("Windows Update cache cleared.")
    except Exception as e:
        print(f"Error clearing Windows Update cache: {e}")

def clear_all_caches():
    """ Runs all cache-clearing functions. """
    clear_recycle_bin()
    clear_temp_files()
    clear_dns_cache()
    clear_windows_update_cache()
    print("All caches cleared successfully.")
