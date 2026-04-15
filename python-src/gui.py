from tkinter import *
from tkinter import ttk
import config
from dataclasses import dataclass

@dataclass
class Translation:
    title: str
    main_label: str
    key_label: str
    move_label: str
    retries_label: str
    fail_label: str
    corners_label: str
    dist_label: str
    ms_label: str
    start_label: str
    stop_label: str

translations = {
    "ru": Translation(
        title="Бот для TETR.IO",
        main_label="Бот для TETR.IO",
        key_label="Выберите клавишу активации бота",
        move_label="Задержка после хода",
        retries_label="Попыток сделать скриншот",
        fail_label="Задержка после вынужденного хода",
        corners_label="Искать углов",
        dist_label="Расстояние между углами",
        ms_label="мс",
        start_label="Запустить",
        stop_label="Остановить",
    ),
    "en": Translation(
        title="Bot for TETR.IO",
        main_label="Bot for TETR.IO",
        key_label="Choose key to activate the bot",
        move_label="Sleep time after move",
        retries_label="Times to retry parsing a screenshot",
        fail_label="Sleep time after failing to parse screenshots",
        corners_label="Number of corners to seek",
        dist_label="Min distance between corners",
        ms_label="ms",
        start_label="Start",
        stop_label="Stop",
    ),
}

class GUI(Tk):
    def __init__(self, btn_callback, config_path):
        conf = config.try_parse_config(config_path)

        super().__init__()
        self.title("Бот для TETR.IO")
    
        self.center = ttk.Frame(self)
        self.center.pack(expand=True)

        self.mainframe = ttk.Frame(self.center, padding=(10, 10, 10, 10))
        self.mainframe.grid(row=1, column=1)

        self.main_label_var = StringVar()
        label = ttk.Label(self.mainframe, textvariable=self.main_label_var, font="Helvetica 30 bold")
        label.grid(column=1, row=1, columnspan=3, pady=(0, 30))

        self.adapter_options = ["Windows x64", "Linux x86_64 (Niri)"]
        self.adapter_combo = ttk.Combobox(self.mainframe, values=self.adapter_options, state="readonly")
        self.adapter_combo.set(conf.adapter)
        self.adapter_combo.grid(column=1, row=2, columnspan=2, sticky="WE", padx=(0, 5))

        def on_key_write(*_):
            value = self.key_var.get().upper()[:1]
            if value and (not value.isalpha() or not value.isascii()):
                value = ""
            self.key_var.set(value)

        self.key_var = StringVar()
        self.key_var.set(conf.activation_key)
        self.key_var.trace_add("write", on_key_write)

        self.key_label_var = StringVar()
        label = ttk.Label(self.mainframe, textvariable=self.key_label_var)
        label.grid(column=1, row=3, sticky="E", padx=(0, 5))

        self.key = ttk.Entry(self.mainframe, width=5, justify="center", textvariable=self.key_var)
        self.key.grid(column=2,row=3, sticky="E", padx=(0, 5))
        
        self.options = ttk.Frame(self.center, padding=(10, 10, 10, 10))
        self.options.grid(row=1, column=2)

        self.ms_label_var = StringVar()
        
        self.move_label_var = StringVar()
        label = ttk.Label(self.options, textvariable=self.move_label_var)
        label.grid(column=1, row=1, sticky="W", padx=(0, 5))
        self.sleep_after_move_var = StringVar()
        self.sleep_after_move_var.set(str(conf.sleep_after_move_ms))
        self.sleep_after_move = ttk.Entry(self.options, width=5, justify="right", textvariable=self.sleep_after_move_var)
        self.sleep_after_move.grid(column=2, row=1, sticky="E", padx=(0, 5), pady=(0, 5))
        label = ttk.Label(self.options, textvariable=self.ms_label_var)
        label.grid(column=3, row=1, sticky="W")
        
        self.retries_label_var = StringVar()
        label = ttk.Label(self.options, textvariable=self.retries_label_var)
        label.grid(column=1, row=2, sticky="W", padx=(0, 5))
        self.retries_var = StringVar()
        self.retries_var.set(str(conf.retry_count))
        self.retries = ttk.Entry(self.options, width=5, justify="right", textvariable=self.retries_var)
        self.retries.grid(column=2, row=2, sticky="E", padx=(0, 5), pady=(0, 5))
        
        self.fail_label_var = StringVar()
        label = ttk.Label(self.options, textvariable=self.fail_label_var)
        label.grid(column=1, row=3, sticky="W", padx=(0, 5))
        self.sleep_after_fail_var = StringVar()
        self.sleep_after_fail_var.set(str(conf.sleep_after_fail_ms))
        self.sleep_after_fail = ttk.Entry(self.options, width=5, justify="right", textvariable=self.sleep_after_fail_var)
        self.sleep_after_fail.grid(column=2, row=3, sticky="E", padx=(0, 5), pady=(0, 5))
        label = ttk.Label(self.options, textvariable=self.ms_label_var)
        label.grid(column=3, row=3, sticky="W")
        
        self.corners_label_var = StringVar()
        label = ttk.Label(self.options, textvariable=self.corners_label_var)
        label.grid(column=1, row=4, sticky="W", padx=(0, 5))
        self.corners_var = StringVar()
        self.corners_var.set(str(conf.corners_count))
        self.corners = ttk.Entry(self.options, width=5, justify="right", textvariable=self.corners_var)
        self.corners.grid(column=2, row=4, sticky="E", padx=(0, 5), pady=(0, 5))
        
        self.dist_label_var = StringVar()
        label = ttk.Label(self.options, textvariable=self.dist_label_var)
        label.grid(column=1, row=5, sticky="W", padx=(0, 5))
        self.dist_var = StringVar()
        self.dist_var.set(str(conf.corners_min_dist))
        self.dist = ttk.Entry(self.options, width=5, justify="right", textvariable=self.dist_var)
        self.dist.grid(column=2, row=5, sticky="E", padx=(0, 5))

        def btn_command():
            if (not self.valid_conf()): return

            self.bot_started = not self.bot_started
            self.update_btn_text()
            if (self.bot_started):
                conf.adapter = self.adapter_combo.get()
                conf.activation_key = self.key_var.get()
                conf.sleep_after_move_ms = int(self.sleep_after_move_var.get())
                conf.retry_count = int(self.retries_var.get())
                conf.sleep_after_fail_ms = int(self.sleep_after_fail_var.get())
                conf.corners_count = int(self.corners_var.get())
                conf.corners_min_dist = int(self.dist_var.get())
                conf.lang = self.lang_combo.get()
                config.save_config(conf, config_path)
            btn_callback(self.bot_started)

        self.btn_text = StringVar()
        self.bot_started = False
        self.btn = ttk.Button(self.mainframe, textvariable=self.btn_text, command=btn_command)
        self.btn.grid(column=3, row=2, sticky="WE")

        self.lang_options = list(translations.keys())
        self.lang_combo = ttk.Combobox(self.mainframe, values=self.lang_options, state="readonly", width=3)
        self.lang_combo.set(conf.lang)
        self.lang_combo.grid(column=3, row=3, sticky="E")

        def on_lang_change(*_):
            t = translations[self.lang_combo.get()]
            self.title(t.title)
            self.main_label_var.set(t.main_label)
            self.key_label_var.set(t.key_label)
            self.move_label_var.set(t.move_label)
            self.retries_label_var.set(t.retries_label)
            self.fail_label_var.set(t.fail_label)
            self.corners_label_var.set(t.corners_label)
            self.dist_label_var.set(t.dist_label)
            self.ms_label_var.set(t.ms_label)
            self.update_btn_text()

        self.lang_combo.bind("<<ComboboxSelected>>", on_lang_change)
        on_lang_change()

    def valid_conf(self):
        if (self.adapter_combo.current() == -1): return False
        if (self.key_var.get() == ""): return
        try:
            int(self.sleep_after_move_var.get())
            int(self.retries_var.get())
            int(self.sleep_after_fail_var.get())
            int(self.corners_var.get())
            int(self.dist_var.get())
        except:
            return False
        return True

    def update_btn_text(self):
        t = translations[self.lang_combo.get()]
        if self.bot_started:
            self.btn_text.set(t.stop_label)
        else:
            self.btn_text.set(t.start_label)




