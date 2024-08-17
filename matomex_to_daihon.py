import re
from collections import defaultdict
import random

if __name__ == "__main__":
    # ID, コメント取得
    thread_dict = defaultdict(lambda: defaultdict(str))
    with open("input/matomex.html", "r", encoding="utf-8", errors="ignore") as f:
        comment_cnt = 0
        for i, line in enumerate(f.readlines()):
            i = i - comment_cnt
            commentout_check = re.search("\<!--.*--\>", line)
            if (commentout_check != None):
                comment_cnt += 1
                continue

            if (i % 2 == 0):
                # === ID取得 ===
                id = re.search("ID.*?(?=\<)", line).group()
                thread_dict[f"{i//2}"]["id"] = id
            else:
                # === コメント取得 ===
                # アンカー対策
                # line = re.sub("\&gt\;", "<", line) # アンカーを残す
                line = re.sub("\&gt\;([0-9]*)?", "", line) # アンカーを消す

                # 空白など削除
                line = re.sub("\s", "", line)

                # HTMLタグ削除
                comment = re.sub("\<.*?\>", "", line)

                thread_dict[f"{i//2}"]["comment"] = comment

    # 台本作成
    character_list = [
        "四国めたん",
        "春日部つむぎ",
    ]
    with open("output/daihon.csv", "w", encoding="cp932", errors="ignore") as f:
        for i, key in enumerate(thread_dict):
            if (i == 0):
                thread_main_id = thread_dict[key]["id"]

            comment = thread_dict[key]["comment"]

            random_select = random.randint(0, 1)
            character = "ずんだもん" if (thread_main_id == thread_dict[key]["id"]) else character_list[random_select]
            f.write(f'{character}, {comment}\n')