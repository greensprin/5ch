import re
from collections import defaultdict
import random
import spacy

# 0: 1レス目のIDに対して必ずずんだもんを設定, 1: ランダムでキャラクター設定
RANDOM_CHARACTER_MODE = 1

# 自動で台本を生成する (0: 生成しない, 1: 生成する(レスポンスがある人気のスレだけを残す))
AUTO_DAIHON_EN    = 1
SELECT_ANCHER_NUM = 0 # いくつレスポンスがついているものを残すか？

SEPARATE_SENTENCE_EN = 0

PRE_CHARACTER_ID = -1

def randint_nodup(start, end, pre_val):
    while(True):
        val = random.randint(start, end)
        if (val != pre_val):
            break

    return val

def init_dict(thread_dict, key):
    thread_dict[key] = {
        "id"         : "",
        "comment"    : "",
        "response"   : [],
        "ancher_flag": 0,
    }

    return thread_dict

def write_comment(f, thread_dict, key, thread_main_id):
    global PRE_CHARACTER_ID

    response_num = len(thread_dict[key]["response"])

    if (AUTO_DAIHON_EN == 0 or response_num >= SELECT_ANCHER_NUM or thread_dict[key]["ancher_flag"] == 1):
        for i in range(response_num + 1):
            if (i == 0):
                id      = thread_dict[key]["id"] 
                comment = thread_dict[key]["comment"]

                if (RANDOM_CHARACTER_MODE == 0):
                    character_id = randint_nodup(1, len(character_list) - 1, PRE_CHARACTER_ID)
                    character = "ずんだもん" if (thread_main_id == id) else character_list[character_id]
                else:
                    character_id = randint_nodup(0, len(character_list) - 1, PRE_CHARACTER_ID)
                    character = character_list[character_id]

                # １つ前がどのキャラだったかを覚えておく
                PRE_CHARACTER_ID = character_id

                # f.write(f'{character},{comment}\n')

                if (SEPARATE_SENTENCE_EN == 1):
                    doc = nlp(comment)
                    for sent in doc.sents:
                        f.write(f'{character},{sent.text}\n')
                else:
                    f.write(f'{character},{comment}\n')
            else:
                res_num = thread_dict[key]["response"][i-1]
                write_comment(f, thread_dict, res_num, thread_main_id)

        return 1
    else:
        return 0

if __name__ == "__main__":
    # ID, コメント取得
    thread_dict = {}
    with open("input/matomex.html", "r", encoding="utf-8", errors="ignore") as f:
        comment_cnt = 0
        for i, line in enumerate(f.readlines()):
            i = i - comment_cnt
            commentout_check = re.search("\<!--.*--\>", line)
            if (commentout_check != None):
                comment_cnt += 1
                continue

            if (i % 2 == 0):
                # === レス番号取得 ==
                res_num = re.search("(?<=\>)[0-9]+(?=\:)", line).group()

                # === ID取得 ===
                id = re.search("ID.*?(?=\<)", line)

                if ((res_num in thread_dict) == False):
                    init_dict(thread_dict, res_num)

                if (id == None):
                    continue
                
                thread_dict[res_num]["id"] = id.group()
            else:
                # === コメント取得 ===
                # アンカ先取得
                ancher = re.search("(?<=\&gt\;\&gt\;)[0-9]+", line)

                # アンカー対策
                # line = re.sub("\&gt\;", "<", line) # アンカーを残す
                line = re.sub("\&gt\;\&gt\;([0-9]*)?", ">>", line) # アンカーを消す

                # 空白など削除
                line = re.sub("\s", "", line)

                # HTMLタグ削除
                comment = re.sub("\<.*?\>", "", line)

                thread_dict[res_num]["comment"] = comment

                if (ancher != None and AUTO_DAIHON_EN != 0):
                    ancher = ancher.group()

                    if ((ancher in thread_dict) == False):
                        init_dict(thread_dict, ancher)

                    thread_dict[ancher]["response"].append(res_num)

                    thread_dict[res_num]["ancher_flag"] = 1

    # 文章区切り
    nlp = spacy.load("ja_ginza_electra")

    # 台本作成
    character_list = [
        # "ずんだもん",
        "四国めたん",
        "春日部つむぎ",
        # "青山龍星",
        "もち子さん",
    ]
    with open("output/daihon.csv", "w", encoding="cp932", errors="ignore") as f:
        for i, key in enumerate(thread_dict):
            if (i == 0):
                thread_main_id = thread_dict[key]["id"]

            if (thread_dict[key]["ancher_flag"] == 1):
                # アンカーのコメントは別で読みだされるのでここでは処理しない
                continue

            res = write_comment(f, thread_dict, key, thread_main_id)

            if (res == 1):
                f.write("\n")