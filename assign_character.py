import random
import shutil
import yaml

def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config

def randint_nodup(start, end, pre_val):
    while(True):
        val = random.randint(start, end)
        if (val != pre_val):
            break

    return val

def main():
    # 設定読み込み
    config = load_yaml("settings\setting.yaml")

    character_list = [
        # "ずんだもん",
        "四国めたん",
        "春日部つむぎ",
        # "青山龍星",
        "もち子さん",
    ]

    with open("input/daihon.txt" , "r", encoding="utf-8", errors="ignore") as fr, \
         open("output/daihon.csv", "w", encoding="utf-8", errors="ignore") as fw:
        
        pre_character_id = -1
        for line in fr.readlines():
            character_id = randint_nodup(0, len(character_list) - 1, pre_character_id)
            fw.write(f"{character_list[character_id]},{line}")

            pre_character_id = character_id

    # 結果をコピー
    output_dir = config["out_dir"]
    shutil.copytree(f"{output_dir}/zz_template", f"{output_dir}/tmp")
    shutil.copy(f"output/daihon.csv", f"{output_dir}/tmp/daihon.csv")

if __name__ == "__main__":
    main()