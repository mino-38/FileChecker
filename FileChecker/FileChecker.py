from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver
from PIL import Image
from pystray import Menu, MenuItem, Icon
from tkinter import filedialog
from tkinter import ttk
import tkinter
import datetime as dt
import threading
import pystray
import json
import sys
import os

def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    else:
        return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), path)

class Config(dict):
    def __init__(self):
        try:
            self.file = resource_path("FileCheckerConfig.json")
            with open(self.file, "r") as f:
                option = json.load(f)
        except:
            option = {}
        super().__init__(**option)

    def write(self, **option):
        self.update(option)
        with open(self.file, "w") as f:
            json.dump(self, f)

class TaskTray:
    file = resource_path("FileCheckerIcon.ico")
    def __init__(self, root):
        self.root = root

    def start(self):
        options_map = {"隠す": self.root.withdraw, "表示": self.root.deiconify, "終了": lambda: self.root.after(1, self.quit)}
        items = []
        for option, callback in options_map.items():
            items.append(MenuItem(option, callback, default=True if option == "表示" else False))
        menu = Menu(*items)
        image = Image.open(self.file)
        self.icon = pystray.Icon("FileChecker", image, "FileChecker Icon", menu)
        self.icon.run()

    def quit(self):
       self.icon.stop()
       self.root.quit()

class FileChecker(FileSystemEventHandler):
    def __init__(self, txt):
        self.txt = txt
        self.logfile = None
        self.txt.tag_config("delete", foreground="red", background="yellow")

    def update_log(self, *text, red=False):
        txt = "{}: {}\n".format(dt.datetime.now(), " ".join(text))
        self.txt.configure(state=tkinter.NORMAL)
        if red:
            self.txt.insert(tkinter.END, txt, "delete")
        else:
            self.txt.insert(tkinter.END, txt)
        self.txt.configure(state=tkinter.DISABLED)
        self.txt.see(tkinter.END)
        if config.get("file"):
            if not self.logfile:
                self.logfile = open(config["file"], "a")
            self.logfile.write(txt)

    # ファイル作成時
    def on_created(self, event):
         self.update_log(event.src_path, "が作成されました")

     # ファイル変更時
    def on_modified(self, event):
        self.update_log(event.src_path, "が変更されました")

     # ファイル削除時
    def on_deleted(self, event):
        self.update_log(event.src_path, "が削除されました", red=True)

     # ファイル移動時
    def on_moved(self, event):
        self.update_log(event.src_path, "が", event.dest_path, "に移動しました")

    def close(self):
        if self.logfile:
            self.logfile.close()

def start(path, button, string):
    if os.path.isdir(path):
        observer = PollingObserver()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        button["command"] = lambda: pause(observer, button, string)
        button["text"] = "一時停止"

def pause(observer, button, string):
    observer.stop()
    observer.join()
    button["command"] = lambda: start(string.get(), button, string)
    button["text"] = "スタート"

def select_path(e, directory=False):
    if directory:
        path = filedialog.askdirectory()
    else:
        path = filedialog.askopenfilename()
    if path:
        e.delete(0, tkinter.END)
        e.insert(tkinter.END, path)

def save(path, root):
    if path:
        config.write(file=path)
        root.destroy()

def ask_logfile():
    subroot = tkinter.Toplevel()
    subroot.title("FileCheckerAskLogFile")
    subroot.geometry("300x200")
    label1 = ttk.Label(subroot, text="ログの出力先ファイルパスを指定してください(存在しないファイルを指定した場合は新しく生成されます)")
    label1.grid(column=0, row=0)
    label2 = ttk.Label(subroot, text="現在設定されているパスは{}".format(config.get("file") if "file" in config else "ありません"))
    label2.grid(column=2, row=0)
    path = tkinter.StringVar()
    entry = ttk.Entry(subroot, textvariable=path)
    entry.grid(column=0, row=1)
    button1 = ttk.Button(subroot, text="参照", command=lambda: select_path(entry))
    button1.grid(column=1, row=1)
    button2 = ttk.Button(subroot, text="決定", command=lambda: save(path.get(), subroot))
    button2.grid(column=0, row=2)

def create():
    root = tkinter.Tk()
    root.title("FileChecker")
    root.geometry("800x500")
    menu = tkinter.Menu(root)
    root.config(menu=menu)
    config_menu = tkinter.Menu(root)
    menu.add_cascade(label="設定", menu=config_menu)
    config_menu.add_command(label="ログ", command=ask_logfile)
    label1 = ttk.Label(root, text="監視対象のディレクトリ")
    label1.grid(column=0, row=0)
    st = tkinter.StringVar()
    entry = ttk.Entry(root, textvariable=st)
    entry.grid(column=0, row=1)
    button1 = ttk.Button(root, text="参照", command=lambda: select_path(entry, directory=True))
    button1.grid(column=1, row=1, sticky=tkinter.W)
    button2 = ttk.Button(root, text="スタート")
    button2["command"] = lambda: start(st.get(), button2, st)
    button2.grid(column=0, row=2)
    label2 = ttk.Label(root, text="ログ")
    label2.grid(column=0, row=3)
    canvas = tkinter.Canvas(root, width=280, bg="white", bd=0, height=200, highlightthickness=0)
    canvas.grid(column=0, row=4)
    scrollbar = ttk.Scrollbar(root, orient=tkinter.VERTICAL, command=canvas.yview)
    canvas["yscrollcommand"] = scrollbar.set
    canvas.yview_moveto(0)
    scrollbar.grid(column=1, row=4, sticky=(tkinter.N, tkinter.S))
    frame_canvas = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_canvas, anchor=tkinter.NW, width=canvas.cget("width"))
    frame_canvas.pack()
    log = tkinter.Text(frame_canvas)
    log.pack()
    log.configure(state=tkinter.DISABLED)
    return root, log

def main():
    global event_handler
    global config
    config = Config()
    try:
        root, log = create()
        icon = TaskTray(root)
        threading.Thread(target=icon.start).start()
        event_handler = FileChecker(log)
        root.mainloop()
    finally:
        event_handler.close()
        try:
            icon.icon.stop()
        except:
            pass

if __name__ == "__main__":
    main()