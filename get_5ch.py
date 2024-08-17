import requests
import re
import argparse
from collections import defaultdict
import yaml
from yaml.representer import Representer

def set_argparse(parser):
    parser.add_argument("url", help="5chスレッドのURLを記入")
    parser.add_argument("--mode", "-m", default=0, type=int, help="0: 稼働中のスレッド, 1: DAT落ちしたスレッド")

def change_url_to_apiurl(url_org, mode=0):
    # URLを以下のように書き換える (API用のURL) 関数
    # url_org = "https://itest.5ch.net/asahi/test/read.cgi/newsplus/1723624289"
    # url     = "https://asahi.5ch.net/newsplus/dat/1723624289.dat"

    if (url_org.find("itest.5ch.net") != -1):
        server_name = re.search("(?<=5ch\.net\/).*?(?=\/)", url_org).group()
        thread_name = re.search("(?<=test\/read.cgi\/).*?(?=\/)", url_org).group()
        thread_id   = re.search(f"(?<=test\/read.cgi\/{thread_name}\/)[0-9]*", url_org).group()
    else:
        server_name = re.search("(?<=https:\/\/).*?(?=\.5ch\.net)", url_org).group()
        thread_name = re.search("(?<=test\/read.cgi\/).*?(?=\/)", url_org).group()
        thread_id   = re.search(f"(?<=test\/read.cgi\/{thread_name}\/)[0-9]*", url_org).group()

    if (mode == 0):
        url = f"https://{server_name}.5ch.net/{thread_name}/dat/{thread_id}.dat"
    elif (mode == 1):
        url = f"https://{server_name}.5ch.net/{thread_name}/oyster/{thread_id[0:4]}/{thread_id}.dat"
    else:
        print(f"mode = {mode} is not supported.")
        quit()

    return url

def thread_parser(text):
    # 1レス毎に分割する
    text_lines = text.split("\n")

    thread_dict = defaultdict(lambda: defaultdict(str))

    for i, line in enumerate(text_lines):
        # 最初のレスからタイトルを抽出する
        if (i == 0):
            thread_title = line.split("<>")[-1]
            thread_dict["title"] = thread_title

        # IDとレス内容を抽出する
        line_body = re.search("(?=ID).*(?=\<\>)", line)

        # 何も抽出できていなければ終了
        if (line_body == None):
            continue

        # 正規表現で抽出した内容を文字列に変換
        line_body= line_body.group()

        # IDとレス内容を分離
        res_id  = line_body.split("<>")[0]
        comment = line_body.split("<>")[1]

        # レス内容保存 (i+1としているのは、レス順番と関連付けるため)
        thread_dict[f"{i+1}"]["id"]      = res_id
        thread_dict[f"{i+1}"]["comment"] = comment

    return thread_dict

def toCP932(text):
    text = text.encode(response.encoding).decode("cp932", errors="ignore")
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="5chのURLを入力してスレッドの内容を取得するスクリプト")
    set_argparse(parser)
    args = parser.parse_args()

    print(f"url_org : {args.url}")
    print(f"mode    : {args.mode}")

    # URLをAPI用のURLに変換
    url = change_url_to_apiurl(args.url, args.mode)
    print(f"api_url : {url}")

    response = requests.get(url)

    response.encoding = response.apparent_encoding
    print(response.encoding)

    # APIから受け取ったthreadの内容をhtml形式でそのまま出力
    with open("output/output.html", "w", encoding=response.encoding, errors="ignore") as f:
        f.write(response.text)

    # threadの内容をparseして出力
    thread_dict = thread_parser(response.text)

    yaml.add_representer(defaultdict, Representer.represent_dict) # yaml を defaultdict に対応させる
    with open("output/output.yaml", "w", encoding=response.encoding, errors="ignore") as f:
        yaml.dump(thread_dict, f, default_flow_style=False, allow_unicode=True, sort_keys=False, indent=4)

    with open("output/daihon.csv", "w", encoding="cp932", errors="ignore") as f:
        for i, key in enumerate(thread_dict):
            if (i == 0):
                print(toCP932(thread_dict["title"]))
                continue

            if (i == 1):
                thread_main_id = thread_dict[key]["id"]

            comment = thread_dict[key]["comment"]
            comment = toCP932(comment)
            comment = re.sub("\<.*\>", "", comment)
            comment = re.sub("\s+", "", comment)

            character = "ずんだもん" if (thread_main_id == thread_dict[key]["id"]) else "四国めたん"
            f.write(f'{character}, {comment}\n')