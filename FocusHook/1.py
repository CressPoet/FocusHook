import os
import platform
import random
import time

def play_beep():
    """根据操作系统播放提示音"""
    system = platform.system()
    try:
        if system == "Windows":
            import winsound
            winsound.MessageBeep(winsound.MB_OK)
        elif system == "Darwin":  # macOS
            os.system('afplay /System/Library/Sounds/Ping.aiff')
        else:  # Linux 和其他类 Unix 系统
            # 尝试使用 'play' 命令（需要安装 sox）
            os.system('play -q -n synth 0.3 sine 800 vol 0.5 2>/dev/null || true')
            # 如果没有 sox，也可以尝试终端响铃（可能无效）
            # print('\a', end='', flush=True)
    except Exception as e:
        print(f"播放提示音时出错: {e}")

def main():
    print("程序启动：每30秒内随机时间播放一次提示音。按 Ctrl+C 停止。")
    while True:
        # 生成 0 到 30 秒之间的随机延迟（浮点数，更自然）
        delay = random.uniform(0, 30)
        print(f"将在 {delay:.2f} 秒后播放提示音...")
        time.sleep(delay)
        play_beep()
        # 等待剩余时间，确保每轮严格控制在30秒内（防止累积误差）
        remaining = 30 - delay
        if remaining > 0:
            time.sleep(remaining)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已停止。")