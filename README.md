# FileChecker
ファイルの変更(削除や作成、編集等)を監視するGUIアプリケーション

Windows10のみでしか動作確認してません

# 使い方
## Pythonを使う
watchdogとpystrayとPillowをインストールしてください

```bash
$ pip install watchdog pystray Pillow
```

あとはFileChecker.pyを実行するだけです
```bash
$ python3 FileChecker.py
```

## Python環境がない人
このリポジトリをgit cloneするかzipファイルをダウンロードするとFileChecker.exeが付いてくるのでそれをダブルクリック等で実行してください(ただし起動は激遅)
