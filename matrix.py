import random, shutil, time, sys

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
cols = shutil.get_terminal_size().columns
drops = [0] * cols

try:
    while True:
        print("\033[1;32m", end="")
        for i in range(cols):
            if random.random() > 0.975:
                print(random.choice(chars), end="")
                drops[i] = 0
            elif drops[i] < 5:
                print(" ", end="")
                drops[i] += 1
            else:
                print(random.choice(chars), end="")
        print()
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\033[0m")
    sys.exit()
