<p align="center">
  <img src="pictures/devil_eye.png" alt="Devil's Eye Logo" width="280">
</p>

## 👁️ Devil's Eye - Educational Keylogger
**Devil's Eye** is a Python-based background keylogger for **educational and ethical hacking purposes**.  
It captures keystrokes invisibly, logs them for analysis, and demonstrates how attackers could exploit such tools.  
**Strictly use on your own system or isolated VMs.**


## ⚠️ WARNING: FOR EDUCATIONAL USE ONLY

**This tool captures ALL keystrokes typed on your computer. Use responsibly.**

### ✅ Allowed Use:
- Your own personal computer
- Virtual machines you control
- Systems with explicit written permission

### ❌ Never Use On:
- Others' computers without permission
- Work or school systems
- Public computers
- Any system with sensitive data


## 🚀 QUICK START
### 1. Install Dependencies
pip install -r requirements.txt

### 2. Start the Keylogger
python devils_eye_launcher.py
- Click through 3 warning screens
- Type **"I ACCEPT FULL RESPONSIBILITY"** when asked
- The keylogger runs invisibly in the background

### 3. Check Captured Keystrokes
# Linux / Mac
cat devils_eye_logs/keystrokes.log
# Windows
type devils_eye_logs\keystrokes.log

### 4. Stop the Keylogger
python devils_eye_stop.py

### 5. Delete Logs (After Learning)
rm -rf devils_eye_logs/


## 📁 Project Structure

| File / Folder | Purpose |
|--------------|---------|
| `devils_eye_launcher.py` | Consent-based launcher and user warnings |
| `devils_eye_core.py` | Educational input monitoring logic |
| `devils_eye_stop.py` | Controlled shutdown and statistics |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |
| `pictures/` | Project assets and branding |
| `pictures/devil_eye.png` | Devil’s Eye logo |
| `devils_eye_logs/` | Locally stored lab output |


## 🎓 EDUCATIONAL EXERCISE

### Step 1: Test in Debug Mode
python devils_eye_core.py --debug
- Type some text
- Press **ESC** to stop
- Check `devils_eye_logs/` for captured data

### Step 2: Full Background Test
1. Run:
python devils_eye_launcher.py
2. Complete all consent screens  
3. Type in:
   - Web browser
   - Notepad / Text editor
   - Word processor  
4. Analyze logs:
grep "KEY" devils_eye_logs/keystrokes.log
grep "ANALYSIS" devils_eye_logs/keystrokes.log

### Step 3: Detection Practice
# Linux / Mac
ps aux | grep devils_eye
# Windows
tasklist | findstr python

### Step 4: Analyze Statistics
python devils_eye_stop.py --stats


## ⚖️ ETHICAL GUIDELINES

### ✅ DO:
- Use on your own computers only
- Test in isolated virtual machines
- Delete logs after learning
- Study detection and prevention techniques
- Obtain written permission for testing

### ❌ DO NOT:
- Install on others' computers
- Use in production environments
- Capture real sensitive data
- Use for malicious purposes


## 🧠 LEARNING OBJECTIVES

1. Understand how keyloggers capture keyboard input
2. Identify keylogger indicators on a system
3. Practice detection and removal techniques
4. Learn about keyboard hooks and low-level APIs
5. Build security awareness through hands-on learning


---

**Remember:** This tool exists to help you learn defense by understanding offense.  
Use this knowledge to build better security, never to compromise it.

---


*Educational Use Only | Version: 1.0-EDU*



