import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, script_to_run, delay=1):
        self.script_to_run = script_to_run
        self.process = None
        self.delay = delay
        self.last_modified_time = time.time()

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

    def on_file_modified(self, event):
        # Trigger a restart only after the file is saved
        if event.src_path.endswith(".py"):
            current_time = time.time()
            if current_time - self.last_modified_time >= self.delay:
                print(f"File {event.src_path} saved. Restarting...")
                self.restart_script()
            else:
                print(f"File {event.src_path} is being modified... waiting for save.")
            self.last_modified_time = current_time

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.watcher = watcher

    def on_modified(self, event):
        self.watcher.on_file_modified(event)

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
