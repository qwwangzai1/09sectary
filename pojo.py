import re

HERO_NAMES = ['昆卡', '海军上将', '雷克萨', '兽王', '半人马酋长', '撼地神牛', '全能骑士', '熊猫酒仙', '斯文', '流浪剑客', '小小', '山岭巨人', '牛头人酋长', '鲁夫特伦', '树精卫士', '守护精灵', '精灵守卫', '炼金术士', '发条地精', '达维安爵士', '龙骑士', '哈斯卡', '神灵武士', '刚背兽', '凤凰', '巨牙海民', '军团指挥官', '地精撕裂者', '大地之灵', '斧王', '涅沙', '混沌骑士', '路西法', '末日使者', '奈克斯', '食尸鬼', '亚巴顿', '地狱领主', '狼人', '巴拉那', '暗夜魔王', '深渊领主', '胖子', '屠夫', '骷髅王', '斯拉达', '鱼人守卫', '不朽尸王', '潮汐猎人', '马格纳斯', '半人猛犸', '巴拉森', '裂魂人', '克里瑟历斯', '沙王', '玛吉纳', '敌法师', '矮人狙击手', '尤涅若', '主宰', '悉拉贝尔', '德鲁伊', '月之骑士', '变体精灵', '司里希丝', '娜迦海妖', '幻影长矛手', '月之女祭司', '力丸', '隐形刺客', '巨魔战将', '矮人直升机', '崔希丝', '黑暗游侠', '拉娜娅', '圣堂刺客', '熊战士', '复仇之魂', '刚铎', '赏金猎人', '灰烬之灵', '史德利古尔', '血魔', '克林克兹', '骷髅射手', '育母蜘蛛', '地穴刺客', '地穴编织者', '茉崔蒂', '幻影刺客', '奈文摩尔', '影魔', '恐怖利刃', '灵魂守卫', '幽鬼', '剧毒术士', '蝮蛇', '冥界亚龙', '地卜师', '剃刀', '闪电幽魂', '斯拉克', '鱼人夜行者', '虚空假面', '美杜莎', '蛇发女妖', '弧光守望者', '水晶室女', '魅惑魔女', '帕克', '仙女龙', '陈', '圣骑士', '伊扎洛', '光之守卫', '宙斯', '众神之王', '弗里奥', '先知', '诺崇', '沉默术士', '秀逗魔导士', '风暴之灵', '风行者', '萨尔', '干扰者', '食人魔法师', '地精工程师', '哥布林工程师', '杰奇洛', '双头龙', '地精修补匠', '罗斯塔', '暗影萨满', '卢比克', '大魔导师', '天怒法师', '神谕者', '阿特洛波斯', '祸乱之源', '黑暗贤者', '克萝贝露丝', '死亡先知', '莱恩', '恶魔巫师', '谜团', '巫妖', '死灵法师', '帕格纳', '遗忘法师', '黑曜毁灭者', '阿卡莎', '痛苦女王', '术士', '暗影恶魔', '蝙蝠骑士', '戴泽', '暗影牧师', '祈求者', '召唤师', '维萨吉', '死灵飞龙', '受折磨的灵魂', '巫医', '远古冰魄', '极寒幽魂', '寒冬飞龙']


class Player:
    def __init__(self, name, score=None, hero=None):
        self.name = name
        self.hero = hero
        self.score = score

    def __str__(self):
        return self.name + ' : ' + self.fmt_score()

    def fmt_score(self):
        if self.score:
            win, total = self.score
            rate = round(win/total, 2)
            return str(round(rate * 100, 1)) + '%' + '/' + str(total)
        else:
            return '-/-'

    def get_rate(self):
        print(self.score)
        if self.score:
            win, total = self.score
            return win/total
        else:
            return 0

    def set_hero(self, text):
        pat = self.name + r'\(.+?\)'
        for match in re.findall(pat, text):
            new_hero = match[match.index('(')+1: match.index(')')]
            print(self.name, '-', new_hero)
            if new_hero in HERO_NAMES:
                self.hero = new_hero
            else:
                pass


class Game:
    def __init__(self, sen, sco):
        self.sen = sen
        self.sco = sco

    def toarr(self):
        arr = []
        arr.extend(self.sen)
        arr.extend(self.sco)
        return arr

    def is_better(self, other):
        return len(self.toarr()) >= len(other.toarr())

    def not_empty(self):
        return self.sen or self.sco

    def enough_heros(self):
        count = 0
        for p in self.toarr():
            if p.hero:
                count = count + 1
        return count >= 6
