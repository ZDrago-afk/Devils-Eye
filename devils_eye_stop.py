"""
DEVIL'S EYE STOPPER
Safely stop the background keylogger
"""

import os
import sys
import signal
import json
import time
import platform

STATUS_FILE = "devils_eye_logs/status.json"
PID_FILE = "devils_eye_logs/devils_eye.pid"

def print_banner():
    """Print the stop utility banner"""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║         👁️ DEVIL'S EYE STOPPER           ║
    ║      Educational Keylogger Controller     ║
    ╚═══════════════════════════════════════════╝
    """
    print(banner)

def check_running():
    """Check if Devil's Eye is running"""
    if not os.path.exists(PID_FILE):
        return False, None
    
    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        
        # Check if process exists
        if platform.system() == "Windows":
            # Windows method
            import ctypes
            PROCESS_QUERY_INFORMATION = 0x0400
            process = ctypes.windll.kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION, False, pid)
            if process:
                ctypes.windll.kernel32.CloseHandle(process)
                return True, pid
            return False, None
        else:
            # Unix/Linux/Mac method
            os.kill(pid, 0)  # Doesn't kill, just checks if process exists
            return True, pid
    except:
        return False, None

def stop_devils_eye():
    """Stop the running Devil's Eye process"""
    print_banner()
    
    is_running, pid = check_running()
    
    if not is_running:
        print("[!] Devil's Eye is not running")
        
        # Clean up stale files
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
            print("[+] Removed stale PID file")
        
        # Show logs location
        if os.path.exists("devils_eye_logs"):
            print(f"\n[?] Logs are preserved at: devils_eye_logs/")
            print("    To delete logs: Delete the 'devils_eye_logs' folder")
        return
    
    print(f"[*] Found running Devil's Eye (PID: {pid})")
    print("[*] Attempting graceful shutdown...")
    
    try:
        # Send termination signal
        if platform.system() == "Windows":
            import ctypes
            PROCESS_TERMINATE = 0x0001
            handle = ctypes.windll.kernel32.OpenProcess(
                PROCESS_TERMINATE, False, pid)
            ctypes.windll.kernel32.TerminateProcess(handle, 0)
            ctypes.windll.kernel32.CloseHandle(handle)
        else:
            os.kill(pid, signal.SIGTERM)
        
        # Wait for process to terminate
        for i in range(10):
            time.sleep(0.5)
            if not check_running()[0]:
                print("[✓] Devil's Eye stopped successfully")
                break
        else:
            print("[!] Process didn't terminate gracefully")
            print("[*] Attempting force kill...")
            if platform.system() != "Windows":
                os.kill(pid, signal.SIGKILL)
                time.sleep(1)
        
        # Clean up
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        
        # Update status file
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r") as f:
                status = json.load(f)
            status["status"] = "stopped"
            status["stop_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(STATUS_FILE, "w") as f:
                json.dump(status, f, indent=2)
        
        print("\n" + "="*50)
        print("[✓] CLEANUP COMPLETE")
        print("="*50)
        print(f"Logs preserved at: devils_eye_logs/")
        print(f"  - keystrokes.log: Captured keystrokes")
        print(f"  - status.json: Runtime information")
        print("\n⚠️  Remember to delete logs after educational use!")
        print("="*50)
        
    except PermissionError:
        print("[✗] Permission denied. Try running as administrator/root.")
    except Exception as e:
        print(f"[✗] Error stopping Devil's Eye: {str(e)}")

def show_stats():
    """Show statistics from the logs"""
    if not os.path.exists(STATUS_FILE):
        print("[!] No status file found")
        return
    
    try:
        with open(STATUS_FILE, "r") as f:
            status = json.load(f)
        
        print("\n" + "="*50)
        print("DEVIL'S EYE STATISTICS")
        print("="*50)
        
        for key, value in status.items():
            if key not in ["app_name", "version"]:
                print(f"{key.replace('_', ' ').title():20}: {value}")
        
        # Count lines in keystroke log
        log_file = "devils_eye_logs/keystrokes.log"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                lines = len(f.readlines())
            print(f"{'Total Entries':20}: {lines}")
        
        print("="*50)
        
    except Exception as e:
        print(f"[!] Error reading stats: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stats":
            show_stats()
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python devils_eye_stop.py          Stop Devil's Eye")
            print("  python devils_eye_stop.py --stats  Show statistics")
            print("  python devils_eye_stop.py --help   Show this help")
        else:
            stop_devils_eye()
    else:
        stop_devils_eye()