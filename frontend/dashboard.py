import curses
import time
import os
from datetime import datetime
from typing import Optional


LOG_FILE = "/Users/vikrorkhanin/Ludice/frontend/bot_start_log.txt"
PID_FILE = "/Users/vikrorkhanin/Ludice/frontend/bot.pid"


def read_logs(max_lines=20):
    """Читаем последние max_lines строк из файла лога."""
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    return [line.strip() for line in lines[-max_lines:]]


def read_pid():
    """Читаем PID из файла."""
    if not os.path.exists(PID_FILE):
        return None
    try:
        with open(PID_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except Exception:
        return None


def is_process_alive(pid: Optional[int]) -> bool:
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
    


def draw_dashboard(stdscr):
    curses.curs_set(0)  # скрыть курсор
    stdscr.nodelay(True)  # не блокировать getch

    while True:
        stdscr.clear()

        height, width = stdscr.getmaxyx()

        # Заголовок
        title = " BOT ASCII DASHBOARD "
        stdscr.addstr(0, max(0, (width - len(title)) // 2), title, curses.A_REVERSE)

        # Текущее время
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stdscr.addstr(2, 2, f"Now: {now}")

        # Статус бота
        pid = read_pid()
        alive = is_process_alive(pid)
        status = "RUNNING" if alive else "STOPPED"
        status_color = curses.color_pair(1 if alive else 2)

        stdscr.addstr(4, 2, f"Bot PID: {pid if pid is not None else 'N/A'}")
        stdscr.addstr(5, 2, "Status: ")
        stdscr.addstr(5, 10, status, status_color)

        # Подсказка управления
        stdscr.addstr(7, 2, "Press 'q' to quit")

        # Логи запусков
        stdscr.addstr(9, 2, "Last starts:")
        logs = read_logs(max_lines=height - 11)
        for i, line in enumerate(reversed(logs)):  # новые сверху
            if 11 + i >= height:
                break
            stdscr.addstr(11 + i, 4, line[: width - 8])

        stdscr.refresh()

        # Обработка клавиш
        try:
            key = stdscr.getch()
            if key == ord("q"):
                break
        except Exception:
            pass

        time.sleep(0.5)


def main():
    curses.wrapper(init)


def init(stdscr):
    # Инициализируем цвета
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # RUNNING
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # STOPPED

    draw_dashboard(stdscr)


if __name__ == "__main__":
    main()
