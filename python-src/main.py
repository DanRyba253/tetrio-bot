import subprocess as sp
from gui import GUI
import sys
import signal

config_path = "config.txt"

bot_process = None

def on_click(bot_started):
    global bot_process
    if (bot_started):
        bot_process = sp.Popen([sys.executable, 'bot.py', config_path])
    else:
        if (bot_process is None): return
        bot_process.send_signal(signal.SIGTERM)
        bot_process.wait()

gui = GUI(on_click, config_path)

gui.mainloop()

