import subprocess
import os
APP_COMMANDS = {
    "chrome": "chrome.exe",
    "calculator": "calc",
    "clock": "ms-clock",
    "brave": "brave.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "word": r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint": r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
    "photos": "ms-photos",
    "file explorer": "explorer.exe",
    "paint": "mspaint.exe"
}

def open_app(app_name):
    drives = ['C:\\'] 
    search_paths = [
        r"Program Files", 
        r"Program Files (x86)", 
        r"Users\\<Karmveer>\\AppData\\Local\\Programs",
        r"ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"
    ]
    
    app_path = APP_COMMANDS.get(app_name.lower())
    if not app_path:
        print(f"Application '{app_name}' not found in the command list.")
        return None  # Return None if app not found

    if app_name.lower() == "photos":
        subprocess.Popen(["start", "ms-photos:"], shell=True)
        return "ms-photos"
    elif app_name.lower() == "file explorer":
        subprocess.Popen("explorer")
        return "explorer"

    def find_executable_in_path(base_path, executable):
        if os.path.exists(base_path):  # Check if directory exists
            for root, dirs, files in os.walk(base_path):
                if executable in files:
                    return os.path.join(root, executable)
        return None

    try:
        # Attempt to locate the executable in the provided search paths
        for drive in drives:
            for path in search_paths:
                full_path = os.path.join(drive, path)
                executable_path = find_executable_in_path(full_path, app_path)
                if executable_path:
                    subprocess.Popen(executable_path)
                    return executable_path  # Return the full path if found

        # If no path is found, attempt to execute it directly
        if os.path.exists(app_path):  # Ensure app_path exists
            subprocess.Popen(app_path, shell=True)
            return app_path  # Return the direct path/command
        else:
            print(f"Error: Could not locate the application '{app_name}'.")
            return None  # Return None if not found

    except Exception as e:
        print(f"Error opening {app_name}: {str(e)}")
        return None  # Return None on exception
