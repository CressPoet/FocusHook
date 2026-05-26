import tkinter as tk
from tkinter import messagebox
import random
import threading
import time
import winsound

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("随机提示音程序")
        self.root.geometry("320x200")
        self.running = False
        self.timer_thread = None

        tk.Label(root, text="最小间隔（分钟）:").pack()
        self.min_entry = tk.Entry(root)
        self.min_entry.insert(0, "3")
        self.min_entry.pack()

        tk.Label(root, text="最大间隔（分钟）:").pack()
        self.max_entry = tk.Entry(root)
        self.max_entry.insert(0, "5")
        self.max_entry.pack()

        self.status_label = tk.Label(root, text="状态：未启动")
        self.status_label.pack(pady=10)

        self.time_left_label = tk.Label(root, text="剩余时间：--:--")
        self.time_left_label.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        self.start_btn = tk.Button(btn_frame, text="开始", command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = tk.Button(btn_frame, text="停止", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

    def beep(self):
        # 响提示音
        winsound.Beep(1000, 500)

    def timer_loop(self, min_minute, max_minute):
        while self.running:
            wait_minutes = random.uniform(min_minute, max_minute)
            wait_seconds = int(wait_minutes * 60)
            self.update_status(f"状态：计时中（{wait_minutes:.2f}分钟）")
            for left in range(wait_seconds, -1, -1):
                if not self.running:
                    self.update_time_left("--:--")
                    return
                mins, secs = divmod(left, 60)
                self.update_time_left(f"{mins:02}:{secs:02}")
                time.sleep(1)
            self.beep()
            self.update_status(f"状态：已响铃，重新计时...")

    def start(self):
        try:
            min_minute = float(self.min_entry.get())
            max_minute = float(self.max_entry.get())
            assert 0 < min_minute <= max_minute
        except Exception:
            messagebox.showerror("输入错误", "请输入有效的数值，且最小值不大于最大值")
            return

        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.timer_thread = threading.Thread(
            target=self.timer_loop, args=(min_minute, max_minute), daemon=True)
        self.timer_thread.start()

    def stop(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_status("状态：已停止")
        self.update_time_left("--:--")

    def update_status(self, text):
        def update():
            self.status_label.config(text=text)
        self.root.after(0, update)

    def update_time_left(self, text):
        def update():
            self.time_left_label.config(text=f"剩余时间：{text}")
        self.root.after(0, update)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.protocol("WM_DELETE_WINDOW", app.stop)
    root.mainloop()