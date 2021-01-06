import elepoke

mypokeList = ["ヒートロトム", "アイアント", "ローブシン", "ゴリランダー", "バイウールー", "トゲキッス"]
oppokeList = ["タチフサグマ", "ワタシラガ", "ウォッシュロトム", "アイアント", "ドリュウズ", "リザードン"]

if __name__ == "__main__":
    # Elepokeモデルを初期化
    el = elepoke.Elepoke()

    # セット
    el.append(name=[mypokeList, oppokeList], reset=True)

    # 計算
    el.fit()

    # 結果
    print(el.result)
