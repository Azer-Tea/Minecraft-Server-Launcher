from tkinter import *
import subprocess
import threading
import tkinter.font as tkFont
import math
import uuid

tk = Tk()
tk.title("Minecraft Server Launcher")
tk.geometry("1366x768+75+10")
tk.configure(bg="#1e1e1e")
tk.iconbitmap("Minecraft_Launcher.ico")
server_process = None

try:
    custom_font = tkFont.Font(family="Minecraft Rus", size=15)
    custom_font1 = tkFont.Font(family="Minecraft Rus", size=12)
except:
    custom_font = ("Courier", 10)
    custom_font1 = ("Courier", 10)

def get_start_command():
    mem = MEMORY_INPUT.get().strip()
    mem_val = mem if mem.isdigit() else "2048"
    return f"java -Xmx{mem_val}M -Xms{mem_val}M -jar server.jar nogui"

def start_server():
    global server_process
    if server_process is None or server_process.poll() is not None:
        command = get_start_command()
        server_process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True,
            bufsize=1
        )
        threading.Thread(target=read_output, daemon=True).start()
        log_output("Сервер запущен...\n", "info")

def stop_server():
    global server_process
    if server_process and server_process.poll() is None:
        try:
            server_process.stdin.write("stop\n")
            server_process.stdin.flush()
        except Exception as e:
            log_output(f"Ошибка: {e}\n", "error")
        server_process = None
        log_output("Команда на остановку отправлена.\n", "warning")

def read_output():
    while True:
        if server_process is None:
            break
        output = server_process.stdout.readline()
        if output == '' and server_process.poll() is not None:
            break
        if output:
            classify_and_log(output)

def classify_and_log(text):
    text_lower = text.lower()
    if "error" in text_lower:
        log_output(text, "error")
    elif "warn" in text_lower:
        log_output(text, "warning")
    elif "info" in text_lower:
        log_output(text, "info")
    else:
        log_output(text, "default")

def log_output(text, tag="default"):
    OUTPUT.configure(state=NORMAL)
    OUTPUT.insert(END, text, tag)
    OUTPUT.see(END)
    OUTPUT.configure(state=DISABLED)

def send_command():
    if server_process and server_process.poll() is None:
        command = ENTRY_COMMAND.get().strip()
        if command:
            try:
                server_process.stdin.write(command + "\n")
                server_process.stdin.flush()
                log_output(f"> {command}\n", "usercmd")
                ENTRY_COMMAND.delete(0, END)
            except Exception as e:
                log_output(f"Ошибка отправки команды: {e}\n", "error")

OUTPUT_FRAME = Frame(tk)
OUTPUT_FRAME.place(relx=0.05, rely=0.3, relwidth=0.55, relheight=0.65)

scrollbar = Scrollbar(OUTPUT_FRAME)
scrollbar.pack(side=RIGHT, fill=Y)

OUTPUT = Text(
    OUTPUT_FRAME,
    bg="#0d0d0d",
    fg="white",
    font=("Minecraft 1.1", 11),
    yscrollcommand=scrollbar.set,
    state=DISABLED
)
OUTPUT.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar.config(command=OUTPUT.yview)

OUTPUT.tag_config("error", foreground="red")
OUTPUT.tag_config("warning", foreground="yellow")
OUTPUT.tag_config("info", foreground="lime")
OUTPUT.tag_config("usercmd", foreground="cyan")
OUTPUT.tag_config("default", foreground="white")

ENTRY_COMMAND = Entry(tk, font=custom_font)
ENTRY_COMMAND.place(relx=0.05, rely=0.21, relwidth=0.4, relheight=0.07)

SEND = Button(
    tk,
    text="Отправить",
    font=custom_font,
    bg="#3498db",
    activebackground="#2980b9",
    command=send_command
)
SEND.place(relx=0.46, rely=0.2, relwidth=0.14, relheight=0.07)

def on_press_start(event):
    Frame_c.place(relx=0.05, rely=0.01, relwidth=0.3, relheight=0.09)
    Frame_bl.config(bg="#478532")
    Frame_bl.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.89)
    Frame_otxt.config(bg="#5aa641")
    Frame_otxt.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.8)
    Frame_sh.place(relx=0.02, rely=0.8, relwidth=0.96, relheight=0.15)
    Text_label.config(text="ЗАПУСТИЛОСЬ", bg="#335e24")
    start_server()

def on_release_start(event):
    Frame_c.place(relx=0.05, rely=0.001, relwidth=0.3, relheight=0.1)
    Frame_bl.config(bg="#6bc74c")
    Frame_bl.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.9)
    Frame_otxt.config(bg="#5aa641")
    Frame_otxt.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.65)
    Frame_sh.place(relx=0.01, rely=0.8, relwidth=0.98, relheight=0.15)
    Text_label.config(text="ЗАПУСТИТЬ", bg="#5aa641")

Frame_c = Frame(tk, bg="#000000")
Frame_c.place(relx=0.05, rely=0.001, relwidth=0.3, relheight=0.1)
Frame_bl = Frame(Frame_c, bg="#6bc74c")
Frame_bl.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.9)
Frame_sh = Frame(Frame_c, bg="#214f11")
Frame_sh.place(relx=0.01, rely=0.8, relwidth=0.98, relheight=0.15)
Frame_otxt = Frame(Frame_c, bg="#5aa641")
Frame_otxt.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.65)
Text_label = Label(
    Frame_otxt,
    text="ЗАПУСТИТЬ",
    bg="#5aa641",
    fg="White",
    font=("Minecraft Rus", 20)
)
Text_label.place(relx=0, rely=0, relwidth=1.0, relheight=1)

Frame_bl.bind("<ButtonPress-1>", on_press_start)
Frame_bl.bind("<ButtonRelease-1>", on_release_start)
Frame_c.bind("<ButtonPress-1>", on_press_start)
Frame_c.bind("<ButtonRelease-1>", on_release_start)
Frame_otxt.bind("<ButtonPress-1>", on_press_start)
Frame_otxt.bind("<ButtonRelease-1>", on_release_start)
Text_label.bind("<ButtonPress-1>", on_press_start)
Text_label.bind("<ButtonRelease-1>", on_release_start)
Frame_sh.bind("<ButtonPress-1>", on_press_start)
Frame_sh.bind("<ButtonRelease-1>", on_release_start)

def on_press_stop(event):
    Frame_c1.place(relx=0.05, rely=0.11, relwidth=0.3, relheight=0.09)
    Frame_bl1.config(bg="#9c1616")
    Frame_bl1.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.89)
    Frame_otxt1.config(bg="#7d1313")
    Frame_otxt1.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.8)
    Frame_sh1.place(relx=0.02, rely=0.8, relwidth=0.96, relheight=0.15)
    Text1.config(text="СТАПЕ", bg="#7d1313")
    stop_server()

def on_release_stop(event):
    Frame_c1.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.1)
    Frame_bl1.config(bg="#cf1d1d")
    Frame_bl1.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.9)
    Frame_otxt1.config(bg="#b51b1b")
    Frame_otxt1.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.65)
    Frame_sh1.place(relx=0.01, rely=0.8, relwidth=0.98, relheight=0.15)
    Text1.config(text="СТОП", bg="#b51b1b")

Frame_c1 = Frame(tk, bg="#000000")
Frame_c1.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.1)
Frame_bl1 = Frame(Frame_c1, bg="#cf1d1d")
Frame_bl1.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.9)
Frame_sh1 = Frame(Frame_c1, bg="#7a1111")
Frame_sh1.place(relx=0.01, rely=0.8, relwidth=0.98, relheight=0.15)
Frame_otxt1 = Frame(Frame_c1, bg="#b51b1b")
Frame_otxt1.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.65)
Text1 = Label(
    Frame_otxt1,
    text="СТОП",
    bg="#b51b1b",
    fg="White",
    font=("Minecraft Rus", 20)
)
Text1.place(relx=0, rely=0, relwidth=1.0, relheight=1)

Frame_bl1.bind("<ButtonPress-1>", on_press_stop)
Frame_bl1.bind("<ButtonRelease-1>", on_release_stop)
Frame_c1.bind("<ButtonPress-1>", on_press_stop)
Frame_c1.bind("<ButtonRelease-1>", on_release_stop)
Frame_otxt1.bind("<ButtonPress-1>", on_press_stop)
Frame_otxt1.bind("<ButtonRelease-1>", on_release_stop)
Text1.bind("<ButtonPress-1>", on_press_stop)
Text1.bind("<ButtonRelease-1>", on_release_stop)
Frame_sh1.bind("<ButtonPress-1>", on_press_stop)
Frame_sh1.bind("<ButtonRelease-1>", on_release_stop)

MEMORY_INPUT = Entry(tk, font=custom_font)
MEMORY_INPUT.insert(0, "2048")
MEMORY_INPUT.place(relx=0.5, rely=0.05, relwidth=0.1, relheight=0.075)

MEM_LABEL = Label(tk, text="RAM (MB)", bg="#1e1e1e", fg="white", font=custom_font)
MEM_LABEL.place(relx=0.5, rely=0.01)

var_inventory = IntVar()
var_autosave = IntVar()
var_commandblocks = IntVar()

def create_checkbox(variable, x, y, text, command_true, command_false):
    switch_state = [variable.get() == 1]

    MAIN_SWITCH = Frame(tk, bg="#1e1e1e")
    MAIN_SWITCH.place(relx=x, rely=y, relwidth=0.06, relheight=0.065)

    CONTUR = Frame(MAIN_SWITCH, bg="#000000")
    CONTUR.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

    BLESk = Frame(CONTUR, bg="#97989B")
    BLESk.place(relx=0.04, rely=0.1, relwidth=0.91, relheight=0.8)

    BLESF = Frame(CONTUR, bg="#3C8527" if switch_state[0] else "#8C8D90")
    BLESF.place(relx=0.04, rely=0.1, relwidth=0.91, relheight=0.8)

    BUTUN_CONTUR = Frame(MAIN_SWITCH, bg="#000000")
    BUTUN_CONTUR.place(relx=0.5 if switch_state[0] else 0, rely=0.1, relwidth=0.5, relheight=1)

    BUTUN_BLESK = Frame(BUTUN_CONTUR, bg="#ECEDEE")
    BUTUN_BLESK.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.5)

    BUTUN_CENTR = Frame(BUTUN_BLESK, bg="#D0D1D4")
    BUTUN_CENTR.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    BUTUN_SHADOW = Frame(BUTUN_CONTUR, bg="#58585A")
    BUTUN_SHADOW.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.2)

    BUTUN_O = Label(
        BLESF,
        text="o",
        font=("Minecraft Rus", 20),
        bg=BLESF["bg"],
        fg="white" if switch_state[0] else "black"
    )
    BUTUN_O.place(relx=0.65, rely=0.01, relwidth=0.3, relheight=0.9)

    BUTUN_I = Label(
        BLESF,
        text="|",
        font=("Minecraft Rus", 13),
        bg=BLESF["bg"],
        fg="white" if not switch_state[0] else "gray"
    )
    BUTUN_I.place(relx=0.1, rely=0.07, relwidth=0.3, relheight=0.9)

    Label(
        tk,
        text=text,
        bg="#1e1e1e",
        fg="White",
        font=("Minecraft Rus", 20)
    ).place(relx=x + 0.07, rely=y + 0.015)

    def toggle_switch(event=None):
        switch_state[0] = not switch_state[0]
        variable.set(switch_state[0])

        command = command_true if switch_state[0] else command_false
        send_server_command(command)

        print(f"[INFO] Переключатель '{text}': {'Включен' if switch_state[0] else 'Выключен'}")


        def animate_lever_ease_in_out(start, end, duration=100):
            steps = 10
            for i in range(steps + 1):
                t = i / steps
                ease = t * t * (3 - 2 * t)
                value = start + (end - start) * ease
                tk.after(i * (duration // steps), lambda v=value: BUTUN_CONTUR.place_configure(relx=v))

        current_relx = float(BUTUN_CONTUR.place_info()["relx"])
        target_relx = 0.5 if switch_state[0] else 0
        animate_lever_ease_in_out(current_relx, target_relx)
        BLESF.config(bg="#3C8527" if switch_state[0] else "#8C8D90")
        BUTUN_O.config(bg=BLESF["bg"], fg="white" if switch_state[0] else "black")
        BUTUN_I.config(bg=BLESF["bg"], fg="white" if not switch_state[0] else "gray")

    for widget in (BLESF, BUTUN_O, BUTUN_I, BUTUN_CONTUR, BUTUN_CENTR, BUTUN_SHADOW, BUTUN_BLESK, BLESk):
        widget.bind("<ButtonRelease-1>", toggle_switch)

create_checkbox(var_inventory, 0.65, 0.4, "KeepInventory", "gamerule keepInventory true", "gamerule keepInventory false")
create_checkbox(var_autosave, 0.65, 0.5, "AutoSave", "gamerule doDaylightCycle true", "gamerule doDaylightCycle false")
create_checkbox(var_commandblocks, 0.65, 0.6, "CommandBlocks", "gamerule commandBlockOutput true", "gamerule commandBlockOutput false")


def auto_update_players():
    if server_process and server_process.poll() is None:
        try:
            server_process.stdin.write("list\n")
            server_process.stdin.flush()
        except Exception as e:
            log_output(f"Ошибка обновления списка игроков: {e}\n", "error")
    tk.after(5000, auto_update_players)

def send_server_command(cmd):
    if server_process and server_process.poll() is None:
        try:
            server_process.stdin.write(cmd + "\n")
            server_process.stdin.flush()
            log_output(f"> {cmd}\n", "usercmd")
        except Exception as e:
            log_output(f"Ошибка отправки команды: {e}\n", "error")

def set_day():
    send_server_command("time set day")

def set_night():
    send_server_command("time set night")

def kill_all():
    send_server_command("kill @e[type=!player]")

def choose_difficulty():
    send_server_command("difficulty peaceful")

def BUTTON_CREATE(x, y, color_bg, color_fg, color_blesk, color_shadows, color_pressed_bg, title, command):
    button_id = str(uuid.uuid4())
    def on_press_start(event):
        globals()[f"Frame_c_{button_id}"].place(relx=x, rely=y + 0.01, relwidth=0.3, relheight=0.09)
        globals()[f"Frame_bl_{button_id}"].config(bg=color_blesk)
        globals()[f"Frame_bl_{button_id}"].place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.89)
        globals()[f"Frame_otxt_{button_id}"].config(bg=color_pressed_bg)
        globals()[f"Frame_otxt_{button_id}"].place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.8)
        globals()[f"Frame_sh_{button_id}"].place(relx=0.02, rely=0.8, relwidth=0.96, relheight=0.15)
        globals()[f"Text_{button_id}"].config(text=title, bg=color_pressed_bg)

    def on_release_start(event):
        globals()[f"Frame_c_{button_id}"].place(relx=x, rely=y, relwidth=0.3, relheight=0.1)
        globals()[f"Frame_bl_{button_id}"].config(bg=color_blesk)
        globals()[f"Frame_bl_{button_id}"].place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.9)
        globals()[f"Frame_otxt_{button_id}"].config(bg=color_pressed_bg)
        globals()[f"Frame_otxt_{button_id}"].place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.65)
        globals()[f"Frame_sh_{button_id}"].place(relx=0.01, rely=0.8, relwidth=0.98, relheight=0.15)
        globals()[f"Text_{button_id}"].config(text=title, bg=color_bg, fg=color_fg)
        if command:
            command()

    globals()[f"Frame_c_{button_id}"] = Frame(tk, bg="#000000")
    globals()[f"Frame_c_{button_id}"].place(relx=x, rely=y, relwidth=0.3, relheight=0.1)
    globals()[f"Frame_bl_{button_id}"] = Frame(globals()[f"Frame_c_{button_id}"], bg=color_blesk)
    globals()[f"Frame_bl_{button_id}"].place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.9)
    globals()[f"Frame_sh_{button_id}"] = Frame(globals()[f"Frame_c_{button_id}"], bg=color_shadows)
    globals()[f"Frame_sh_{button_id}"].place(relx=0.01, rely=0.8, relwidth=0.98, relheight=0.15)
    globals()[f"Frame_otxt_{button_id}"] = Frame(globals()[f"Frame_c_{button_id}"], bg=color_pressed_bg)
    globals()[f"Frame_otxt_{button_id}"].place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.65)
    globals()[f"Text_{button_id}"] = Label(
        globals()[f"Frame_otxt_{button_id}"],
        text=title,
        bg=color_bg,
        fg=color_fg,
        font=("Minecraft Rus", 20)
    )
    globals()[f"Text_{button_id}"].place(relx=0, rely=0, relwidth=1.0, relheight=1)

    globals()[f"Frame_bl_{button_id}"].bind("<ButtonPress-1>", on_press_start)
    globals()[f"Frame_bl_{button_id}"].bind("<ButtonRelease-1>", on_release_start)
    globals()[f"Frame_c_{button_id}"].bind("<ButtonPress-1>", on_press_start)
    globals()[f"Frame_c_{button_id}"].bind("<ButtonRelease-1>", on_release_start)
    globals()[f"Frame_otxt_{button_id}"].bind("<ButtonPress-1>", on_press_start)
    globals()[f"Frame_otxt_{button_id}"].bind("<ButtonRelease-1>", on_release_start)
    globals()[f"Text_{button_id}"].bind("<ButtonPress-1>", on_press_start)
    globals()[f"Text_{button_id}"].bind("<ButtonRelease-1>", on_release_start)
    globals()[f"Frame_sh_{button_id}"].bind("<ButtonPress-1>", on_press_start)
    globals()[f"Frame_sh_{button_id}"].bind("<ButtonRelease-1>", on_release_start)

BUTTON_CREATE(0.65, 0.0, "#D0D1D4", "#1E1E1F", "#ECEDEE", "#58585A", "#58585A", "Установить день", set_day)
BUTTON_CREATE(0.65, 0.1, "#D0D1D4", "#1E1E1F", "#ECEDEE", "#58585A", "#58585A", "Установить ночь", set_night)
BUTTON_CREATE(0.65, 0.2, "#D0D1D4", "#1E1E1F", "#ECEDEE", "#58585A", "#58585A", "Убить всех", kill_all)
BUTTON_CREATE(0.65, 0.3, "#D0D1D4", "#1E1E1F", "#ECEDEE", "#58585A", "#58585A", "N\A", choose_difficulty)

auto_update_players()

tk.mainloop()
