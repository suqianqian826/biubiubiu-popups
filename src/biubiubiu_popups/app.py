import tkinter as tk
import random
import argparse 

# ====== 顶部默认参数（可被命令行覆盖） ======
DEFAULT_POPUP_COUNT = 99      # 计划创建的弹窗数量
DEFAULT_POPUP_INTERVAL_MS = 5 # 每个弹窗之间的间隔（毫秒）
DEFAULT_POPUP_W = 300         # 弹窗宽
DEFAULT_POPUP_H = 150         # 弹窗高

TIPS = [
    "多喝热水", "记得吃饭", "今天开心吗", "顺顺利利", "生日快乐",
    "早日FIRE", "我也想你啦", "喵喵喵", "长命百岁", "身体倍儿棒",
    "何其有幸,年岁并进", "福寿绵长", "所求皆如愿", "好花常有,好梦长留",
    "(˘͈ᵕ ˘͈❀)Happy birthday✨",
    "山水未老,风也年轻", "万事胜意", "岁月无恙,你我安好", "岁岁常欢愉",
    "顺颂时宜,百事从欢", "愿年年今日,喜长新",
    "日日是好日,时时是好时", "如云如海如山", "自如自有自在",
    "——— 生日快乐！万事顺意！ ———",
    "♡ Happy birthday ♡ ",
    "┏ 🧁 生  日  快  乐  🧁 ┛",
    "祝你灿烂", "恭喜解锁新篇章"
]

BG_COLORS = [
    "mistyrose", "lavenderblush", "seashell", "honeydew", "mintcream",
    "aliceblue", "azure", "snow", "lemonchiffon", "oldlace",
    "lightpink", "lavender", "powderblue", "lightyellow", "peachpuff",
    "thistle", "papayawhip", "linen", "cornsilk", "bisque"
]

# ====== 运行状态 ======
all_popups = []
_created = 0

def create_one_popup(root, w, h):
    """创建一个弹窗（Toplevel），含心跳动画。"""
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    x = random.randrange(0, max(1, screen_w - w))
    y = random.randrange(0, max(1, screen_h - h))

    bg = random.choice(BG_COLORS)
    tip = random.choice(TIPS)

    top = tk.Toplevel(root)
    top.title("东东~")
    top.geometry(f"{w}x{h}+{x}+{y}")
    top.configure(bg=bg)
    top.attributes("-topmost", True)

    # 文案
    lbl = tk.Label(top, text=tip, bg=bg, font=("微软雅黑", 18), width=30, height=1)
    lbl.pack(pady=(10, 2))

    # ♥ 心跳动画
    heart = tk.Label(top, text="♥", bg=bg, fg="red", font=("Segoe UI Symbol", 16))
    heart.pack()

    sizes = [14, 18, 22, 18]
    def beat(i=0):
        if not top.winfo_exists():
            return
        heart.configure(font=("Segoe UI Symbol", sizes[i % len(sizes)]))
        top.after(160, beat, i + 1)
    beat()

    # 弹窗关闭：从列表移除，并尝试自动退出
    def on_destroy(_=None):
        if top in all_popups:
            all_popups.remove(top)
        try_auto_exit(root)
    top.bind("<Destroy>", on_destroy)

    # 弹窗上 Esc：退出程序
    top.bind("<Escape>", lambda e: exit_program(root))

    all_popups.append(top)
    return top

def exit_program(root):
    """关闭所有弹窗并退出"""
    close_all()
    try:
        root.destroy()
    except Exception:
        pass

def close_all():
    """一键关闭所有弹出的窗口。"""
    for w in list(all_popups):
        try:
            if w.winfo_exists():
                w.destroy()
        except Exception:
            pass
    all_popups.clear()

def try_auto_exit(root):
    """当所有计划弹窗都已创建且全部关闭后，自动退出。"""
    global _created
    if _created >= _goal_count and len(all_popups) == 0:
        exit_program(root)

def spawn_many(root, n, interval, w, h):
    """用 after 定时批量创建弹窗（更安全、无需线程）。"""
    global _created, _goal_count
    _created = 0
    _goal_count = n

    def step():
        global _created
        if _created >= n:
            try_auto_exit(root)
            return
        create_one_popup(root, w, h)
        _created += 1
        root.after(interval, step)
    step()

def parse_args():
    p = argparse.ArgumentParser(description="biubiubiu popups (Esc 退出)")
    p.add_argument("--count", type=int, default=DEFAULT_POPUP_COUNT, help="弹窗数量，默认 99")
    p.add_argument("--interval", type=int, default=DEFAULT_POPUP_INTERVAL_MS, help="间隔（毫秒），默认 5")
    p.add_argument("--width", type=int, default=DEFAULT_POPUP_W, help="弹窗宽，默认 300")
    p.add_argument("--height", type=int, default=DEFAULT_POPUP_H, help="弹窗高，默认 150")
    return p.parse_args()

def main():
    args = parse_args()
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗
    # 全局 Esc：无论焦点在哪，都能退出程序
    root.bind_all("<Escape>", lambda e: exit_program(root))
    # 开始批量弹窗
    spawn_many(root, args.count, max(1, args.interval), max(60, args.width), max(60, args.height))
    root.mainloop()

if __name__ == "__main__":
    main()
