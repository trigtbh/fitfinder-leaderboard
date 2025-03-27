import blessed
term = blessed.Terminal()

def warning_yn(message):
    try:
        resp = input(term.orange + term.bold + "WARNING" + term.normal + ": " + message.strip() + " (Y/N)\n> " + term.normal + term.orange + term.bold)
    except KeyboardInterrupt:
        print(term.normal)
        exit(0)
    print(term.normal, end="")
    return "y" in resp.lower()

def warning(message):
    print(term.orange + term.bold + "WARNING" + term.normal + ": " + message.strip() + term.normal)

def error(message):
    print(term.red + term.bold + "ERROR" + term.normal + ": " + message.strip() + term.normal)
    exit(1)

def info(message):
    print(term.blue + term.bold + "INFO" + term.normal + ": " + message.strip() + term.normal)

def note(message):
    print(term.bold + "NOTE" + term.normal + ": " + message.strip() + term.normal)

def clear():
    print(term.clear, end="")

def success(message):
    print(term.green + term.bold + "SUCCESS" + term.normal + ": " + message.strip() + term.normal)

def loaded(name):
    if not hasattr(sys.modules[name], "_initialized"):
        success(f"Loaded module {term.bold + term.blue}{name}{term.normal}")
    sys.modules[name]._initialized = True  # Set flag
    

import sys



import traceback

def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)  # Allow Ctrl+C to exit
        return
    
    tb = traceback.extract_tb(exc_traceback)
    file, line, func, text = tb[-1]  # Get last traceback entry

    error(f"An unhandled exception occurred in {term.bold + term.blue}{file}{term.normal} at line {term.bold + term.blue}{line}{term.normal}: {exc_value}")

import warnings

def global_warning_handler(message, category, filename, lineno, file=None, line=None):
    warning(f"An unhandled warning occurred in {term.bold + term.blue}{filename}{term.normal} at line {term.bold + term.blue}{lineno}{term.normal}: {message}")

# Redirect warnings
warnings.showwarning = global_warning_handler

# Set global exception handler
sys.excepthook = global_exception_handler

import atexit

def exit_handler():
    info("Exiting...")

atexit.register(exit_handler)