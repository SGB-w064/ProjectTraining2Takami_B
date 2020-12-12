"""

流れメモ

ゲームの設定を指定させる(今回の場合は表示桁数、表示間隔、表示問題数)
↓
ゲーム枠取得
↓
桁数変更
↓
表示間隔変更
↓
表示問題数変更
↓
開始をクリック
↓
指定範囲内の数字を読み込み→文字列から桁数分スライスを使って切り取った上でint型に変えて加算していく
↓
加算した数値を答えに入力
↓
判定をクリックする
"""

import sys
import platform
import time
import webbrowser
import pyautogui
from mss import mss
import numpy as np
import cv2
import pytesseract

# ゲーム画面を取得する関数
def getGameWindow():
	try:
		global x_point, y_point, width, height
		if os_name == "Windows":
			x_point, y_point, width, height = pyautogui.locateOnScreen("game_win.png")
		else:
			x_point, y_point, width, height = pyautogui.locateOnScreen("game_mac.png")
			x_point /= 2
			y_point /= 2
	except:
		print("ゲーム画面が存在しないか、画面サイズが異なります")
		input("ゲーム画面が見える状態にしてEnterを入力")
		return getGameWindow()

# 桁数を指定する関数
def getDigits():
	input_num = input("1~5の桁数を入力: ")
	try:
		input_num = int(input_num)
	except:
		print("1~5を入力してください")
		return getDigits()
	if input_num in digitsList:
		return input_num
	else:
		print("1~5を入力してください")
		return getDigits()

# 表示間隔を指定する関数
def getInterval():
	input_num = input("{0}のうちから表示間隔を入力: ".format(intervalList))
	try:
		input_num = float(input_num)
	except:
		print("表示された数値の中から選んでください")
		return getInterval()
	if input_num in intervalList:
		return input_num
	else:
		print("表示された数値の中から選んでください")
		return getInterval()

# 表示回数を指定する関数
def getCount():
	input_num = input("{0}のうちから問題表示回数を入力: ".format(countList))
	try:
		input_num = int(input_num)
	except:
		print("表示された数値の中から選んでください")
		return getCount()
	if input_num in countList:
		return input_num
	else:
		print("表示された数値の中から選んでください")
		return getCount()

"""
----------ここから開始----------
"""

# OS名を取得
os_name = platform.system()

# 設定のプルダウンで設定できる数値をリストにして宣言
digitsList = [1, 2, 3, 4, 5]
intervalList = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
countList = [5, 10, 20, 30, 50, 100]

# ゲーム設定を取得
print("https://tomari.org/main/java/flash_anzan.html のフラッシュ暗算を自動で行います")
questionDigits = getDigits()
questionInterval = getInterval()
questionCount = getCount()

# ゲームサイトを開く
webbrowser.open_new("https://tomari.org/main/java/flash_anzan.html")
time.sleep(5)
# ウィンドウの最大化
if os_name == "Windows":
	pyautogui.hotkey("win", "up")
else:
	pyautogui.hotkey("command","ctrl", "f")
time.sleep(3)

# ゲーム画面取得
x_point, y_point, width, height = [0, 0, 0, 0]
getGameWindow()

print(x_point, y_point, width, height)

# ゲーム画面のメニュー座標を設定、OSによって画面比率が違うため分岐
if os_name == "Windows":
	leftMenu_x_point = 60					# メニューの左側のクリックするx座標
	rightMenu_x_point = 225					# メニューの右側のクリックするx座標
	digitsSettingPullDown_y_point = 25		# 桁数を指定するプルダウンのy座標
	intervalSettingPullDown_y_point = 65	# 表示間隔を指定するプルダウンのy座標
	countSettingPullDown_y_point = 100		# 表示回数を指定するプルダウンのy座標
	startButton_y_point = 135				# 開始ボタンのy座標
	showNumberRegion_left_point = 22		# 数字表示場所の左上のx座標
	showNumberRegion_top_point = 242		# 数字表示場所の左上のy座標
	showNumberRegion_width = 240			# 数字表示場所の横幅
	showNumberRegion_height = 110			# 数字表示場所の縦幅
	answerField_y_point = 220				# 回答入力フィールドのy座標
	checkAnswerButton_y_point = 210			# 判定ボタンのy座標
	#lagTime = 0							# PCの起動時間によって起こりうると思われる処理時間
else:
	#Macは座標が解像度/2のためすべて / 2する
	leftMenu_x_point = 200 / 2
	rightMenu_x_point = 470 / 2
	digitsSettingPullDown_y_point = 60 / 2
	intervalSettingPullDown_y_point = 135 / 2
	countSettingPullDown_y_point = 210 / 2
	startButton_y_point = 280 / 2
	showNumberRegion_left_point = 66 / 2
	showNumberRegion_top_point = 492 / 2
	showNumberRegion_width = 475 / 2
	showNumberRegion_height = 220 / 2
	answerField_y_point = 440 / 2
	checkAnswerButton_y_point = 410 / 2
	#lagTime = 0

# ゲーム設定を適用
# 桁数設定
pyautogui.leftClick(x_point + rightMenu_x_point, y_point + digitsSettingPullDown_y_point)
for _ in digitsList:
	pyautogui.press("up")
for _ in range(digitsList.index(questionDigits)):
	pyautogui.press("down")
pyautogui.press("Enter")

time.sleep(1)

# 表示間隔設定
pyautogui.leftClick(x_point + rightMenu_x_point, y_point + intervalSettingPullDown_y_point)
for _ in intervalList:
	pyautogui.press("up")
for _ in range(intervalList.index(questionInterval)):
	pyautogui.press("down")
pyautogui.press("Enter")

time.sleep(1)

# 問題数設定
pyautogui.leftClick(x_point + rightMenu_x_point, y_point + countSettingPullDown_y_point)
for _ in countList:
	pyautogui.press("up")
for _ in range(countList.index(questionCount)):
	pyautogui.press("down")
pyautogui.press("Enter")

time.sleep(1)

# 開始ボタンを押す
pyautogui.leftClick(x_point + leftMenu_x_point, y_point + startButton_y_point)
# 開始前待機
time.sleep(1)

# 取得した数字を格納するリストの宣言
#numbers = []

# 前回取得した数字を格納する変数の宣言
temp_num = -1
# 加算した回数を格納する変数の宣言
sum_count = 0

# 加算していく変数の宣言
sum = 0
#sum_lagTime = 0

# 回数指定ループは処理時間を求めなければいけないためやめる
'''
for i in range(questionCount + 1):
	# 開始時間取得
	nowTime = time.time()
	# mssを使った指定範囲のスクリーンショットを取得
	numImg = mss().grab({"left" : x_point + showNumberRegion_left_point, "top" : y_point + showNumberRegion_top_point, "width" : showNumberRegion_width, "height" : showNumberRegion_height})
	# 取得したスクリーンショットをnumpy配列にする(つまりスクリーンショットを数値化)
	numImg = np.array(numImg)
	#cv2.imwrite("numImg{0}.png".format(i + 1), numImg) # 確認用
	# 画像からテキストを読み込む
	# --psm 8は画像を１ブロックの単語として認識する-c tessedit_char_whitelistは読み込める文字を指定する
	text = pytesseract.image_to_string(numImg, config="--psm 8 -c tessedit_char_whitelist=0123456789")
	#numbers.append(text)
	# テキストから桁数分上をスライスして切り取り、int型に変換
	text = int(text[:questionDigits])
	print(text)
	# 加算していく
	sum += text
	# 指定した間隔時間から処理に掛かった時間を引いてその分待つ。また毎回の処理の誤差分を引く
	time.sleep(questionInterval - (time.time() - nowTime) - lagTime)
	print(time.time() - nowTime)
	sum_lagTime += time.time() - nowTime
	if((i + 1) % 10 == 0 and i != 0):
		print(f"{i + 1}回目時点での処理合計時間は{sum_lagTime}")
'''

# 普通にプレイする場合、同じ数字が2連続で出た場合判別がつきづらいため、起こり得ないと仮定した場合の処理方法。起こった場合は普通にエラる
while True:
	# 開始時間取得
	nowTime = time.time()
	# mssを使った指定範囲のスクリーンショットを取得
	numImg = mss().grab({"left" : x_point + showNumberRegion_left_point, "top" : y_point + showNumberRegion_top_point, "width" : showNumberRegion_width, "height" : showNumberRegion_height})
	# 取得したスクリーンショットをnumpy配列にする(つまりスクリーンショットを数値化)
	numImg = np.array(numImg)
	#cv2.imwrite("numImg{0}.png".format(i + 1), numImg) # 確認用
	# 画像からテキストを読み込んで桁数分上をスライスして切り取り、int型に変換
	# --psm 8は画像を１ブロックの単語として認識する-c tessedit_char_whitelistは読み込める文字を指定する
	text = int(pytesseract.image_to_string(numImg, config="--psm 8 -c tessedit_char_whitelist=0123456789")[:questionDigits])
	# 前回取得した数値と比較して、違った場合は数字一覧に加える
	if temp_num != text:
		sum += text
		temp_num = text
		sum_count += 1
		print(f"処理時間：{time.time() - nowTime}")
	# 加算回数が指定桁数+1個の時点でwhileループ脱出
	if questionCount + 1 == sum_count:
		break

# print(numbers)
# if len(numbers) != questionCount + 1:
	# print("読み込んだ数字の数が合わないため終了")
	# sys.exit()

# 数値を加算
#sum = sum(numbers)

# 加算した数値の表示
print(sum)

#print(sum_lagTime)

# 加算した数値をstringに変換
sum = str(sum)

# 待機時間(少なくとも表示時間分は待つ)
time.sleep(questionInterval + 1)

# ポップアップを閉じる操作
pyautogui.press("Escape")

# 待機時間
time.sleep(0.5)

# 答えを入力するフィールドをクリック
pyautogui.leftClick(x_point + leftMenu_x_point, y_point + answerField_y_point)
# 答えを入力する
pyautogui.typewrite(sum, interval = 1)
# 判定ボタンをクリックする
pyautogui.leftClick(x_point + rightMenu_x_point, y_point + checkAnswerButton_y_point)

# 待機時間および答えの確認時間
time.sleep(5)

# ポップアップを閉じる操作
pyautogui.press("Escape")

# 待機時間
time.sleep(0.5)

# 答えを入力するフィールドをクリック
pyautogui.leftClick(x_point + leftMenu_x_point, y_point + answerField_y_point)
# OSによってショートカットが違うため分岐
if os_name == "Windows":
	# WindowsならCtrl+Aで全選択
	pyautogui.hotkey("ctrl", "a")
else:
	# Linuxは考慮せずMacのみだとCommand+Aで全選択
	pyautogui.hotkey("command", "a")
# 選択した文字を削除
pyautogui.press("BackSpace")
# 終了のため何もないところをクリック
pyautogui.leftClick(x_point, y_point)
# フラッシュ暗算のページのタブを閉じる
if os_name == "Windows":
	pyautogui.hotkey("ctrl", "w")
else:
	pyautogui.hotkey("command", "w")

