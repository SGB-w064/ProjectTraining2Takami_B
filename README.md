# 2020年度プロジェクト実習2　高見班Bグループの成果

これは https://tomari.org/main/java/flash_anzan.html のフラッシュ暗算を自動化したものです。

## 動作条件
- Python3.8をインストールしている
- 必要モジュールや関連ソフトウェアをインストールしている
    - pipでインストール出来るもの
        - pyautogui, mss, numpy, opencv-python, pyocr, pytesseract
    - 外部でインストールするもの
        - Tesseract_OCR(32bit)
- Windowsの場合以下の環境変数PATHを通す
    - 変数名 : Path 値 : C:\Program Files\Tesseract-OCR
    - 変数名 : TESSDATA_PREFIX 値 : C:\Program Files\Tesseract-OCR\tessdata

## 動作確認を行った機種
- MacBook Pro
    - 13-inch, 2017, Thunderbolt 3ポートx 2
- Windows10 
    - 23.6インチ, 1920x1080, Intel Core i9 9900K, Memory 32GB
    - 24インチ, 1280x720, Intel Core i5 6500, Memory 8GB

## 実行方法
ダウンロードしたZipファイルを解凍し、.pyが存在する階層にてターミナルなどのCLIを使いMacの場合は "python3 1116FlashAnzan.py" を実行。Windowsの場合は "py 1116FlashAnzan.py" を実行。<br>
CLI上に表示される操作に従うことで処理に移る。

## 諸注意
Mac上では桁数5の指定は現状出来ません。対応予定は今の所ないです。
実行ファイルにして配布しようと思いましたが、動作が割と重かったのでやめました。精進します。
