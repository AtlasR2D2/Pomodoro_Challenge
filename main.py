import tkinter as tk
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
SECS_IN_A_MIN = 60
TOMATO_ICON = "\U0001F345"
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 224
PAD_AMOUNT = 100
TIMER_FONT = ("DIN", 24, "bold")
STANDARD_FONT = ("Tahoma, 12")
BOLD_FONT = ("Tahoma", "16", "bold")
TIMER_HEADER_FONT = ("Tahoma", 20, "italic")
TICK_ICON = "\U00002713"
PROGRESS_TICKS = ""
SESSIONS = 0
TIMER_ITERATION = 0
UNIT_TIME_MS = 10**3
yoga_position = "🧘"
work_position = "🧑‍💻"
STRWORK = "work"
STRBREAK = "break"
TIMERTYPE = STRWORK
timer_var = None


print(TICK_ICON)

def determine_break(work_session_x):
    """determines break based on work_session variable"""
    if not work_session_x % 4 == 0:
        repaint_bg(RED)
        return SHORT_BREAK_MIN
    else:
        repaint_bg(PINK)
        return LONG_BREAK_MIN


def repaint_bg(color_x):
    window["bg"] = color_x
    canvas["bg"] = color_x
    label_timer["bg"] = color_x
    session_ticks_label["bg"] = color_x


# ---------------------------- TIMER RESET ------------------------------- #
def reset_command():
    global SESSIONS, TIMER_ITERATION, PROGRESS_TICKS
    window.after_cancel(timer_var)
    SESSIONS = 0
    TIMER_ITERATION = 0
    # Update tick label
    PROGRESS_TICKS = ""
    session_ticks_label["text"] = PROGRESS_TICKS
    canvas.itemconfig(timer_text, text="00:00")
    repaint_bg(YELLOW)
    update_timer_label("")
# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global SESSIONS, TIMER_ITERATION, PROGRESS_TICKS, TIMERTYPE
    work_time_amount = WORK_MIN * SECS_IN_A_MIN

    TIMER_ITERATION += 1
    if TIMER_ITERATION % 2 != 0:
        SESSIONS += 1
        PROGRESS_TICKS += TICK_ICON
        TIMERTYPE = STRWORK
        repaint_bg(YELLOW)
        countdown(work_time_amount)
    else:
        break_time_amount = determine_break(SESSIONS) * SECS_IN_A_MIN
        TIMERTYPE = STRBREAK
        countdown(break_time_amount)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(remaining_secs):
    global timer_var
    intmins = int(math.floor(remaining_secs / 60))
    strmins = "{:02d}".format(intmins)
    intsecs = int(remaining_secs % 60)
    strsecs = "{:02d}".format(intsecs)
    strtime = f"{strmins}:{strsecs}"
    canvas.itemconfig(timer_text, text=strtime)
    if remaining_secs > 0:
        timer_var = window.after(UNIT_TIME_MS, countdown, remaining_secs-1)
    else:
        # Output next iteration symbol
        if TIMERTYPE == "work":
            # Update tick label
            session_ticks_label["text"] = PROGRESS_TICKS
            update_timer_label(STRBREAK)
        else:
            update_timer_label(STRWORK)
        # Restart Timer
        start_timer()

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title(f"Pomodoro {TOMATO_ICON}")
window.config(padx=PAD_AMOUNT, pady=PAD_AMOUNT, bg=YELLOW)

# Label Timer
label_timer = tk.Label(text="Timer", fg=GREEN, font=TIMER_HEADER_FONT, bg=YELLOW, highlightthickness=0)
label_timer.grid(row=0, column=1)

def update_timer_label(timer_type):
    if timer_type == "work":
        label_timer["text"] = f"Time to {work_position}"
    elif timer_type == "break":
        label_timer["text"] = f"Time to {yoga_position}"
    else:
        label_timer["text"] = "Timer"

# Tomato Timer
canvas = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(CANVAS_WIDTH/2,CANVAS_HEIGHT/2, image=tomato_img)
timer_text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT*0.60, text="00:00", fill="white", font=TIMER_FONT)
canvas.grid(row=1, column=1)

def start_command():
    update_timer_label(STRWORK)
    start_timer()


# Start Button
button_start = tk.Button(text="Start", command=start_command, font=STANDARD_FONT)
button_start.grid(row=2, column=0)

# Reset Button
button_reset = tk.Button(text="Reset", command=reset_command, font=STANDARD_FONT)
button_reset.grid(row=2, column=2)

# Session Ticks Label
session_ticks_label = tk.Label(text=PROGRESS_TICKS, fg=GREEN, font=BOLD_FONT, bg=YELLOW, highlightthickness=0)
session_ticks_label.grid(row=3, column=1)

window.mainloop()



