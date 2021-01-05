import pandas as pd
import numpy as np
from math import floor
import random
import json


def getTypeList() -> list:
    """タイプのリストを返す

    Returns:
        list -- タイプのリスト
    """

    tList = ["ノーマル", "ほのお", "みず", "でんき", "くさ", "こおり", "かくとう", "どく", "じめん",
             "ひこう", "エスパー", "むし", "いわ", "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー"]

    return tList


def convertType(typeName: str) -> int:
    """タイプ名を数値に変換する

    Arguments:
        type {str} -- タイプ名

    Returns:
        int -- 変更後のタイプ
    """

    li = getTypeList()

    return li.index(typeName)


def getCompatibility(attack: int, defence: int) -> float:
    """タイプ相性表からタイプ相性を求める

    Arguments:
        attack {int}: 攻撃する側のタイプ(0~17)
        defence {int}: 攻撃を受ける側のタイプ(0~17)

    Returns:
        int: [効果抜群: 2.0, 効果普通: 1.0, 効果今ひとつ: 0.5, 効果なし: 0.0]
    """

    # タイプ相性表
    TypeCompatibility = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0, 1, 1, 0.5, 1],
        [1, 0.5, 0.5, 1, 2, 2, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 1, 2, 1],
        [1, 2, 0.5, 1, 0.5, 1, 1, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 1, 1],
        [1, 1, 2, 0.5, 0.5, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0.5, 1, 1, 1],
        [1, 0.5, 2, 1, 0.5, 1, 1, 0.5, 2, 0.5, 1, 0.5, 2, 1, 0.5, 1, 0.5, 1],
        [1, 0.5, 0.5, 1, 2, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 0.5, 1],
        [2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 2, 0.5],
        [1, 1, 1, 1, 2, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 0, 2],
        [1, 2, 1, 2, 0.5, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 1, 2, 1],
        [1, 1, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 0.5, 1],
        [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0, 0.5, 1],
        [1, 0.5, 1, 1, 2, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 2, 0.5, 0.5],
        [1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 0.5, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0.5, 0],
        [1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 0.5],
        [1, 0.5, 0.5, 0.5, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0.5, 2],
        [1, 0.5, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 2, 2, 0.5, 1]
    ]

    TypeCompatibility = pd.DataFrame(TypeCompatibility,
                                     index=getTypeList(),
                                     columns=getTypeList())

    return float(TypeCompatibility.iloc[attack, defence])


def damage(power: int, skill: str, attack: int, defence: int, rate: float = 1.0) -> int:
    """ダメージ計算

    Arguments:
        power {int}: 技の威力
        skill {str}: 攻撃(a) or 特攻(c)
        attack {int}: 攻撃(a) or 特攻(c)の実数値
        defence {int}: 防御(b) or 特防(d)の実数値

    Keyword Arguments:
        rate {float}: 倍率 (default: {1.0})

    Returns:
        int: ダメージ量
    """

    # 相性を無視した技の威力(レベル50想定)
    # ダメージ = ((攻撃側のレベル × 2 ÷ 5 ＋ 2) × 技の威力 × 攻撃側の実数値 ÷ 防御側の実数値) ÷ 50 ＋ 2
    level = 50
    damage = floor(floor(floor(level * 2 / 5 + 2) *
                         power * attack / defence) / 50 + 2)

    # 乱数補正
    damage = floor(damage * random.uniform(0.85, 1.00))

    # 倍率補正
    damage = floor(rate * damage)

    return damage


class Elepoke():
    def __init__(self, datas=pd.read_csv("./data/pokemon.csv", index_col=0)):
        self.datas = datas
        self.pokemon = [[], []]
        self.result = [[], []]

    def append(self, name: list = [[], []], reset: bool = False):
        """ポケモンをモデルにセットする

        Keyword Arguments:
            name {list} -- [[自分のポケモン], [相手のポケモン]] (default: {[[], []]})
            reset {bool} -- モデルのリセット (default: {False})
        """

        # セットされたポケモンを削除
        if reset:
            self.pokemon[0] = []
            self.pokemon[1] = []

        # ポケモンをセット
        self.pokemon[0].extend(name[0])
        self.pokemon[1].extend(name[1])

        # ポケモンが6匹を超えたら、古いポケモンを削除
        len0 = len(self.pokemon[0]) - 6
        if len0 < 0:
            len0 = 0
        len1 = len(self.pokemon[1]) - 6
        if len1 < 0:
            len1 = 0
        self.pokemon[0] = self.pokemon[0][len0:]
        self.pokemon[1] = self.pokemon[1][len1:]

        return

    def _raceVal(self, name: str) -> dict:
        """ポケモン名から種族値データ等を取得する

        Arguments:
            name {str} -- ポケモン名

        Returns:
            dict -- ポケモンのスペック {name, h, a, b, c, d, s, sum, type1, type2, type1_int, type2_int}
        """

        pdRow = self.datas.loc[self.datas["name"] == name]
        ob = pdRow.iloc[0, 0:]
        dictData = json.loads(ob.to_json())

        return dictData

    def _spec(self, name: str, level: int = 50, h: int = 252, a: int = 252, b: int = 252, c: int = 252, d: int = 252, s: int = 252) -> dict:
        """ポケモン名から能力値データ等を取得する

        Arguments:
            name {str} -- ポケモン名

        Keyword Arguments:
            level {int} -- レベル (default: 50)
            h {int} -- HPの努力値(0~252) (default: 252)
            a {int} -- 攻撃の努力値(0~252) (default: 252)
            b {int} -- 防御の努力値(0~252) (default: 252)
            c {int} -- 特攻の努力値(0~252) (default: 252)
            d {int} -- 特防の努力値(0~252) (default: 252)
            s {int} -- 素早さの努力値(0~252) (default: 252)

        Returns:
            dict -- ポケモンのスペック {name, h, a, b, c, d, s, sum, type1, type2, type1_int, type2_int}
        """

        # ポケモン名から種族値データを取得
        poke = self._raceVal(name)

        # 能力値算出(個体値V想定、性格補正無視)
        # 能力値(HP) = (種族値×2＋個体値＋努力値÷4)×レベル÷100＋レベル＋10
        # 能力値(HP以外) = {(種族値×2＋個体値＋努力値÷4)×レベル÷100＋5}×性格補正
        poke["h"] = floor(floor(poke["h"] * 2 + 31 + h / 4)
                          * level / 100) + level + 10
        poke["a"] = floor((poke["a"] * 2 + 31 + floor(a / 4))
                          * level / 100) + 5
        poke["b"] = floor((poke["b"] * 2 + 31 + floor(b / 4))
                          * level / 100) + 5
        poke["c"] = floor((poke["c"] * 2 + 31 + floor(c / 4))
                          * level / 100) + 5
        poke["d"] = floor((poke["d"] * 2 + 31 + floor(d / 4))
                          * level / 100) + 5
        poke["s"] = floor((poke["s"] * 2 + 31 + floor(s / 4))
                          * level / 100) + 5

        return poke

    def _maxDamage(self, attacker: str, defender: str, power: int = 100) -> int:
        """タイプ一致技のなかで最大打点を算出

        Arguments:
            attacker {str} -- 攻撃するポケモンの名前
            defender {str} -- 防御するポケモンの名前

        Keyword Arguments:
            power {int} -- 技の威力 (default: {100})

        Returns:
            int -- 最大ダメージ量
        """

        # ポケモンの情報を取得
        attacker = self._spec(attacker)
        defender = self._spec(defender)

        # ポケモンの名前からタイプを取得
        attackType1 = attacker["type1_int"]
        attackType2 = attacker["type2_int"]
        defenceType1 = defender["type1_int"]
        defenceType2 = defender["type2_int"]

        # 攻撃と特攻の種族値を比較し、攻撃技or特攻技を決定
        if attacker["a"] >= attacker["c"]:
            skill = "a"
            attack = attacker["a"]
            defence = defender["b"]
        else:
            skill = "c"
            attack = attacker["c"]
            defence = defender["d"]

        # 倍率を算出(攻撃側の一つ目のタイプ)
        rate1 = 1.5
        rate1 *= getCompatibility(attackType1, defenceType1)
        if defenceType2 != -1:
            rate1 *= getCompatibility(attackType1, defenceType2)

        # 倍率を算出(攻撃側の二つ目のタイプ)
        if attackType2 != -1:
            rate2 = 1.5
            rate2 *= getCompatibility(attackType2, defenceType1)
            if defenceType2 != -1:
                rate2 *= getCompatibility(attackType2, defenceType2)
        else:
            rate2 = 0.0

        # ダメージを算出
        dm1 = damage(power=power, skill=skill, attack=attack,
                     defence=defence, rate=rate1)
        dm2 = damage(power=power, skill=skill, attack=attack,
                     defence=defence, rate=rate2)

        # タイプ一致技のダメージを格納
        dmList = [dm1, dm2]

        return max(dmList)

    def _calc(self) -> list:
        """相手のポケモンに対するダメージ量の期待値

        Returns:
            list -- 計算結果
        """
        # 初期化
        self.result = [[], []]

        # 結果格納用の配列
        myPokeList = []
        opPokeList = []

        # 自分のポケモンが相手のポケモンに与えるダメージ
        for index, attacker in enumerate(self.pokemon[0]):
            dmList = []
            if attacker:
                for defender in self.pokemon[1]:
                    if defender:
                        dm = self._maxDamage(attacker, defender)
                        dmList.append(dm)
                average = floor(np.average(dmList))
            else:
                average = 0.0
            poke = {"index": index, "name": attacker, "Evaluation": average}
            myPokeList.append(poke)

        # 順位の設定
        myPokeList.sort(key=lambda x: x['Evaluation'], reverse=True)
        for index, mypoke in enumerate(myPokeList):
            if mypoke["name"]:
                mypoke['rank'] = index + 1
            else:
                mypoke['rank'] = 0
        myPokeList.sort(key=lambda x: x['index'])

        # 相手のポケモンが自分のポケモンに与えるダメージ
        for index, attacker in enumerate(self.pokemon[1]):
            dmList = []
            if attacker:
                for defender in self.pokemon[0]:
                    if defender:
                        dm = self._maxDamage(attacker, defender)
                        dmList.append(dm)
                average = floor(np.average(dmList))
            else:
                average = 0.0
            poke = {"index": index, "name": attacker, "Evaluation": average}
            opPokeList.append(poke)

        # 順位の設定
        opPokeList.sort(key=lambda x: x['Evaluation'], reverse=True)
        for index, oppoke in enumerate(opPokeList):
            if oppoke["name"]:
                oppoke['rank'] = index + 1
            else:
                oppoke['rank'] = 0
        opPokeList.sort(key=lambda x: x['index'])

        # 結果をセット
        self.result = [myPokeList, opPokeList]

        return self.result

    def fit(self, calc: int = 0):
        """学習

        Keyword Arguments:
            calc {int} -- 使用するアルゴリズム (default: {0})
        """
        if (calc == 0):
            self._calc()
