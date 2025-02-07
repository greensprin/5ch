# Youtube 5chまとめ動画作成

## 情報収集

- 5ch
    - [現行スレッド](https://itest.5ch.net/topics/news)
        - ニュースのランキングから人気の話題を確認
    - [過去スレ](https://kakolog.jp/)
        - キーワードで検索する
    - まとめサイト
- X
    - トレンドやインフルエンサーのポストから
- ニュースサイト
    - [yahooニュース](https://news.yahoo.co.jp/)
    - [yahooコメントランキング](https://news.yahoo.co.jp/ranking/comment)
        - コメント多い話題が2chやXでも話題になっていないか (yahooコメントは引用不可のため)
    - その他ニュースサイト、アプリなんでもOK
- [Googleトレンド](https://trends.google.co.jp/trends/)
    - 急上昇から話題を探す
- Youtube
    - 似たチャンネルがどのようなネタを扱っているかを参考にする

## webツール

- [まとめくす](https://2mtmex.com/editor)
    - 2chスレをまとめるために使う
- [Twitter動画保存](https://twidropper.com/)
    - Xの話題を扱う際、ポストの画像を引用するときに使う
- [背景切り取り](https://www.bannerkoubou.com/photoeditor/transparent/)
    - フリーの画像などの背景を切り取りたい場合に使う
- [人物背景切り抜き](https://clipping-ac.com/)
    - 人物の背景を切り抜きたい場合に使う

## 必要ツール

- python
- git
- sourcetree
- YMM4

## 初期設定

- YMM4
    - 設定をコピーする
- python
    1. 仮想環境を作成する
        ``` shell
        python -m venv --upgrade-deps .env
        ```
    1. 仮想環境に入る
        ```shell
        # windows
        .env\Scripts\activate
        # mac
        .env/bin/activate
        ```
    1. 仮想環境にライブラリをインストールする
        ```shell
        pip install -r doc/requirements.txt
        ```

## 動画作成手順

1. 情報収集先で話題を探す
1. 情報をまとめる
    - 5chスレの場合は、まとめくすを使う
    - Xの場合手動でポストをコピーして、input/daihon.txtにペーストする
    - どちらの場合もコメントは11個取得する
1. daihon.csvを作成する
    - 仮想環境に入る ※すでに入っている場合は不要
        ```shell
        # windows
        .env\Scripts\activate
        # mac
        .env/bin/activate
        ```
    - まとめくすの場合は、「タグ発行」→「本文+続きをコピー」をクリックし以下のコマンド実行
        ```shell
        python matomex_to_daihon.py
        ```
    - Xの場合は、以下のコマンドを実行
        ```shell
        python assign_character.py
        ```
1. 出力されたdaihon.csvの整理を行う
    - ニュース部分の台本を整理する
    - 順番を入れ替える
    - 5個の塊を2個作成する
        - 各塊の3番目と4番目に強いコメント持ってくる
    - 最後の言葉を考える
1. YMM4を起動する
1. daihon.csvを読み込ませる
1. コメントの位置を調整する
1. 最後のコメントを調整
    - 基本変更不要だが、文章短くて文字が小さければ少し大きくする
1. 画像を追加する
1. ニュース, コメントの表示時に効果音をつける
1. サムネを作成する
    - 画像を挿入する
    - サムネの文字を考える
    - サムネのコメントを考える
    - 装飾をつけるかを考える
    - サムネの文字で書いたものを読み上げさせる
    - 読み上げの長さに他のオブジェクトを合わせる
    - 読み上げの字幕を非表示にする
1. 全体を通して動画をチェックする