import ctypes
import sys
import tkinter as tk
from factor import results, player_names, get_players, update_heros
from system_hotkey import SystemHotkey
from key import key_press
import time

last = None

is_show = True
MAX_WIDTH = 230
MAX_HEIGHT = 300
SEN_COLOR = '#09F7F7'
SCO_COLOR = '#33FF00'

def gui_init():
    def get_score():
        global last
        new_game = player_names()

        if last:
            if new_game.not_empty():
                update_heros(last)
            else:
                last = None
        else:
            if new_game.not_empty():
                clear()
                g = results('DOTA')
                render_text(g)
                show()
                last = g
                window.after(1000*60*3, show_heros, g)
            else:
                pass

    def show_heros(g):
        def render():
            if g.enough_heros():
                render_img(g)
                show()

        key_press('f11')
        key_press('f11')
        window.after(4000, render)

    def raise_above():
        window.attributes("-topmost", True)

    def clear():
        for l in img_labels:
            l.configure(text='', image='')
        for l in text_labels:
            l.configure(text='', image='')

    def loop():
        get_score()
        window.after(3000, loop)

    def align_right(width, height):
        screen_width = window.winfo_screenwidth()
        size = '{}x{}+{}+{}'.format(width, height, screen_width-width, 0)
        window.geometry(size)
        window.update()

    def show():
        global is_show
        align_right(MAX_WIDTH, MAX_HEIGHT)
        raise_above()
        is_show = False

    def hide():
        global is_show
        align_right(0, 0)
        is_show = True

    def change_status(event):
        if is_show:
            show()
        else:
            hide()

    def init_heros():
        with open('dict.txt', 'r', encoding='utf-8') as f:
            table = list(map(lambda x: x[0:-1].split(' '), f.readlines()))

        dic = {'default': tk.PhotoImage(file='static\\placehold.png')}
        for names in table:
            file_name = names[0]
            game_name = names[-1]
            photo = tk.PhotoImage(file='static\\' + file_name + '.png')
            dic[game_name] = photo
            dic[file_name] = photo

        return dic

    def render_text(game):
        def render_sco():
            img_labels[6].configure(text='天灾', fg=SCO_COLOR)
            start = 7
            for i in range(0, len(game.sco)):
                text_labels[i + start].configure(text=str(game.sco[i]), fg=SCO_COLOR)

        def render_sen():
            img_labels[0].configure(text='近卫', fg=SEN_COLOR)
            start = 1
            for i in range(0, len(game.sen)):
                text_labels[i + start].configure(text=str(game.sen[i]), fg=SEN_COLOR)

        render_sen()
        render_sco()

    def render_img(game):
        def render_sen():
            start = 1
            for i in range(0, len(game.sen)):
                hero = game.sen[i].hero
                if hero:
                    img_labels[i + start].configure(image=HEROS[hero])
                else:
                    img_labels[i + start].configure(image=HEROS['default'])

        def render_sco():
            start = 7
            for i in range(0, len(game.sco)):
                hero = game.sco[i].hero
                if hero:
                    img_labels[i + start].configure(image=HEROS[hero])
                else:
                    img_labels[i + start].configure(image=HEROS['default'])

        render_sen()
        render_sco()


    window = tk.Tk()
    window.title('09小秘书')

    HEROS = init_heros()
    img_labels = []
    text_labels = []
    for i in range(12):
        img = tk.Label(window, bg='black')
        img.grid(row=i, column=0)
        img_labels.append(img)

        text = tk.Label(window, font=('Microsoft YaHei', 10), anchor=tk.W, bg='black')
        text.grid(row=i, column=1, sticky=tk.W)
        text_labels.append(text)

    hk = SystemHotkey()
    hk.register(['f3'], callback=change_status)

    window.config(bg='black')
    window.overrideredirect(True)
    window.bind('<Motion>', lambda e: hide())
    align_right(MAX_WIDTH, MAX_HEIGHT)
    window.after(3000, loop)
    window.mainloop()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if is_admin():
        gui_init()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 6)