import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, script_to_run):
        self.script_to_run = script_to_run
        self.process = None

        # Get the Python executable from the virtual environment
        self.python_executable = os.path.join(".venv", "Scripts", "python.exe")
        if not os.path.exists(self.python_executable):
            raise FileNotFoundError(f"Python executable not found at {self.python_executable}")

    def restart_script(self):
        if self.process:
            print("Restarting script...")
            self.process.terminate()
            self.process.wait()
        print(f"Running script using: {self.python_executable}")
        self.process = subprocess.Popen([self.python_executable, self.script_to_run])

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.watcher = watcher

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.watcher.restart_script()

def main():
    script_to_run = "main.py"  # Replace with your script name
    watcher = Watcher(script_to_run)
    watcher.restart_script()

    event_handler = FileChangeHandler(watcher)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)

    print(f"Watching for changes in Python files in the current directory...")
    try:
        observer.start()
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()
    finally:
        observer.join()
        if watcher.process:
            watcher.process.terminate()

if __name__ == "__main__":
    main()
