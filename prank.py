import os, time, random, threading, pyautogui
from pynput import keyboard, mouse

stop_flag = threading.Event()
buffer = []
mouse_controller = mouse.Controller()

def mouse_jitter_and_hide():
    while not stop_flag.is_set():
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        mouse_controller.move(dx, dy)
        if random.random() < 0.3:
            pyautogui.FAILSAFE = False
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            pyautogui.moveTo(-100, -100)
            time.sleep(random.uniform(2, 5))
            screen_w, screen_h = pyautogui.size()
            pyautogui.moveTo(random.randint(0, screen_w), random.randint(0, screen_h))
        time.sleep(random.uniform(3, 8))

def random_typing():
    keys = "abcdefghijklmnopqrstuvwxyz0123456789"
    while not stop_flag.is_set():
        time.sleep(random.uniform(10, 30))
        key = random.choice(keys)
        pyautogui.write(key)

def reverse_typing():
    def on_press(key):
        if stop_flag.is_set():
            return False
        try:
            if key == keyboard.Key.enter or key == keyboard.Key.space:
                pyautogui.write(''.join(reversed(buffer)))
                pyautogui.press('enter' if key == keyboard.Key.enter else 'space')
                buffer.clear()
            elif hasattr(key, 'char') and key.char:
                buffer.append(key.char)
        except:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def kill_switch():
    combo = {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode(char='q')}
    pressed = set()

    def on_press(key):
        if stop_flag.is_set():
            return False
        if key in combo:
            pressed.add(key)
            if combo.issubset(pressed):
                stop_flag.set()
                return False

    def on_release(key):
        if key in pressed:
            pressed.remove(key)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

threads = [
    threading.Thread(target=mouse_jitter_and_hide),
    threading.Thread(target=random_typing),
    threading.Thread(target=reverse_typing),
    threading.Thread(target=kill_switch)
]

for t in threads:
    t.daemon = True
    t.start()

while not stop_flag.is_set():
    time.sleep(1)
