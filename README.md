# biubiubiu-popups 🎂

一个用 Tkinter 做的「生日 biu biu biu」弹窗小程序：
- 启动后按配置自动**批量弹出**小窗（心跳 ♥ 动画、随机彩色背景与文案）
- **Esc** 一键关闭全部并退出

默认：弹窗 **99** 次、**5ms** 间隔、窗口 **300×150**。

---

## 运行

### 方式 A：直接运行（推荐）
```bash
python -m biubiubiu_popups
```

### 方式B：命令行参数覆盖默认值
```
python -m biubiubiu_popups --count 120 --interval 8 --width 320 --height 160

参数：
--count（int）：弹窗数量，默认 99
--interval（int, ms）：每个弹窗间隔，默认 5
--width（int）：弹窗宽度，默认 300
--height（int）：弹窗高度，默认 150

任意时刻按 Esc：关闭全部并退出。
```
