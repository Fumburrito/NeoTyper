import pyperclip
from pynput.keyboard import Key, Controller, Listener
import time
import threading
import sys

terminate_flag = False

def fail_safe_listener():
    def on_press(key):
        global terminate_flag
        try:
            if key.char == '`':
                print("Fail-safe triggered. Exiting...")
                terminate_flag = True
                # Stop listener
                return False
        except AttributeError:
            pass

    with Listener(on_press=on_press) as listener:
        listener.join()

def type_from_clipboard():
    keyboard = Controller()
    text = pyperclip.paste()
    clean_lines = [line.strip() for line in text.splitlines() if line.strip()]
    text = "\n".join(clean_lines)

    print("Switch to the target window within 3 seconds...")
    time.sleep(3)

    for line in text.split("\n"):
        if terminate_flag:
            print("Terminated by fail-safe.")
            sys.exit(0)
        keyboard.type(line)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.2)

if __name__ == "__main__":
    # Start fail-safe listener in a separate thread
    listener_thread = threading.Thread(target=fail_safe_listener, daemon=True)
    listener_thread.start()
    type_from_clipboard()