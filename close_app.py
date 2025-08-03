import psutil
def close_app(app_name):
    app_process_map = {
        "photos": "Microsoft.Photos.exe",
        "file explorer": "explorer.exe",
        "word": r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
        "excel": r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
        "powerpoint": r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
        "clock": "clock.exe",
        "powerpoint": "POWERPNT.EXE",
        "chrome": "chrome.exe",
        "brave": "brave.exe",
        "edge": "msedge.exe"
    }
    
    app_process = app_process_map.get(app_name.lower(), f"{app_name}.exe").lower()
    process_found = False

    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'].lower().startswith(app_name):
                process.terminate()
                process_found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not process_found:
        print(f"No running process found for {app_name}")
    
    return process_found