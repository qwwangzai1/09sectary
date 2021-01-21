import re
import requests
import json
import os
from threading import Thread
from pojo import Player, Game

game_type_code = 1

def req_content(url):
    response = requests.get(url)
    return response.content.decode('utf-8')


def is_name(n):
    pat = '^[0-9A-F]{8}'
    return re.match(pat, n) and n.find('|r') != -1


def get_players():
    acc = {}
    with open('names.dat', 'rb') as s:
        bs = s.read(8000)
        content = bs.decode('utf-8', 'ignore')
        names = content.split('|c')
        for name in names:
            if is_name(name):
                index = name[0:8]
                final = name[8:name.find('|r')]
                if final.find('%') == -1:
                    p = Player(final)
                    acc[index] = p

    return classify(acc)


def diff(s1, s2):
    acc = []
    for e in s1:
        if e not in s2:
            acc.append(e)
    return acc


order = ['FF0042FF', 'FF1CE6B9', 'FF540081', 'FFFFFC01', 'FFFE8A0E',  # 近卫
         'FFE55BB0', 'FF959697', 'FF7EBFF1', 'FF106246', 'FF4E2A04']  # 天灾


def classify(ps):
    def addon(start, end):
        acc = []
        for i in order[start:end]:
            if i in ps.keys():
                acc.append(ps[i])
        return acc

    return Game(addon(0, 5), addon(5, 10))


def get_id(name):
    content = req_content("http://users.09game.com/home/GetUserPub?user_name=%27" + name + "%27")
    dic = json.loads(content)
    return dic['temp'][0]['user_id']


def get_history(user_id):
    json_str = req_content("http://score.09game.com/Ordinary/SeasonSummary?GameTypeID="+str(game_type_code)+"&UserID=" + str(user_id))
    dic = json.loads(json_str)
    total = dic['data']['total'][0]
    return total['total_win'], total['total_times']


def web_data(player):
    try:
        user_id = get_id(player.name)
        score = get_history(user_id)
        player.score = score
    except:
        pass


def run_thread(players):
    threadpool = []
    for p in players:
        t = Thread(target=web_data,  args=[p])
        threadpool.append(t)

    for t in threadpool:
        t.start()

    for t in threadpool:
        t.join()


def is_valid(ps):
    return '天灾军团' in ps.values()


def show_grade(ps):
    names = []
    names.extend(ps.sen)
    names.extend(ps.sco)
    run_thread(names)

    return ps


def call_exe(parm=''):
    return os.system("print.exe " + parm)


def results(game_type):
    now = player_names()

    global game_type_code
    game_type_code = {'DOTA': 1, # dota
                      'OMG': 21, # omg
                      'IM': 2}[game_type]  # im

    if now:
        res = show_grade(now)
        return res
    else:
        return None

def player_names():
    call_exe()
    return get_players()


def update_heros(game):
    with open('names.dat', 'rb') as s:
        bs = s.read(8000)
        content = bs.decode('utf-8', 'ignore')
        # print(content)
        for p in game.toarr():
            p.set_hero(content)
        return game






