from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
from selenium.webdriver.support.ui import Select

from selenium.webdriver.chrome.options import Options #headlessモードの設定
options = Options()
options.add_argument("--headless")

elem_kamokus = ["理科教育通論","物理学通論","物理学実験基礎","化学通論","化学実験基礎","基礎生物学","生物学実験基礎","地学通論","地学実験基礎","美術科教育法総論","絵画基礎実習Ⅰ","絵画基礎実習Ⅱ","彫刻基礎実習Ⅰ","彫刻基礎実習Ⅱ","デザイン基礎演習","工芸概論","日本とアジアの美術（歴史と理論と鑑賞）","西洋美術（歴史と理論と鑑賞）"]
elem_name = []
elem_year = []
elem_tani = []
elem_day = []
elem_teacher1 = []
elem_teacher2 = []
elem_course = []
elem_cr_url = []
df = pd.DataFrame() #データフレームの新規作成

browser = webdriver.Chrome(options=options) #引数にoptions=optionsを入れるとheadlessモードになる
# sleep(3)

for i in elem_kamokus:
    browser.get("https://cu-syllabus-management.an.r.appspot.com/")
    
    elem_kamoku = browser.find_element(By.NAME, "KAIKO_KAMOKUWEBNM") #入力する場所の取得
    
    elem_kamoku.send_keys(i) #科目名の入力
    
    dropdown = browser.find_element(By.NAME, "SORT") #表示順の選択
    select = Select(dropdown)
    select.select_by_index(3)
    
    elem_kensaku = browser.find_element(By.CSS_SELECTOR, ".search_submit.btn_orange").click() #検索ボタンのクリック
    sleep(1)
    if len(browser.find_elements(By.CSS_SELECTOR, ".detail_submit.btn_yellow")) > 0:
        elem_syousai = browser.find_element(By.CSS_SELECTOR, ".detail_submit.btn_yellow").click() #詳細ボタンのクリック
        
        handle = browser.window_handles[-1] #一番右のタブに切り替え
        browser.switch_to.window(handle)
        sleep(1)
        elem_url = browser.current_url #urlの取得
        elem_title = browser.find_element(By.TAG_NAME, "h2") #科目名の取得
        elem_inf = browser.find_elements(By.TAG_NAME, "dd") #その他情報の取得
        elem_name.append(elem_title.text) #科目名の追加
        elem_year.append(elem_inf[1].text) #タームの追加
        elem_tani.append(elem_inf[2].text) #単位数の追加
        elem_day.append(elem_inf[4].text) #時間割の追加
        elem_teacher1.append(elem_inf[17].text)
        elem_teacher2.append(elem_inf[18].text)
        elem_course.append(elem_inf[14].text) #授業方法の追加
        elem_cr_url.append(elem_url) #urlの追加
    else:
        elem_name.append(i) #科目名の追加
        elem_year.append(" ") #タームの追加
        elem_tani.append(" ") #単位数の追加
        elem_day.append(" ") #時間割の追加
        elem_teacher1.append(" ")
        elem_teacher2.append(" ")
        elem_course.append(" ")
        elem_cr_url.append(" ")

browser.quit()

df["科目名"] = elem_name
df["年次：ターム"] = elem_year
df["時間割：教室"] = elem_day
df["単位数"] = elem_tani
df["教員名１"] = elem_teacher1
df["教員名２"] = elem_teacher2
df["授業方法"] = elem_course
df["url"] = elem_cr_url

df = df.replace("対面授業科目（メディア授業実施が半数以下） / On-site courses (Half or less classes of the course are delivered online)", "対面授業")
df = df.replace("メディア授業科目（全回メディア授業実施） / Online courses (Fully online)", "オンライン授業")
df = df.replace("メディア授業科目（メディア授業実施が半数を超える） / Online courses (More than half classes of the course are delivered online)", "オンライン授業")

i = 0
for elem_kamoku in elem_kamokus:
    df.iloc[i,2] = df.iloc[i,2].replace(" (Mon) ", " ")
    df.iloc[i,2] = df.iloc[i,2].replace(" (Tue) ", " ")
    df.iloc[i,2] = df.iloc[i,2].replace(" (Wed) ", " ")
    df.iloc[i,2] = df.iloc[i,2].replace(" (Thu) ", " ")
    df.iloc[i,2] = df.iloc[i,2].replace(" (Fri) ", " ")
    df.iloc[i,2] = df.iloc[i,2].replace("集中講義 (Intensive) ", " ")
    df.iloc[i,2] = df.iloc[i,2].replace(":", "/")
    i = i + 1

i = 0
for elem_kamoku in elem_kamokus:
    df.iloc[i,4] = df.iloc[i,4].replace("　", " ")
    df.iloc[i,4] = df.iloc[i,4].replace("　", " ")
    df.iloc[i,4] = df.iloc[i,4].replace("　", " ")
    df.iloc[i,4] = df.iloc[i,4].replace("　", " ")
    df.iloc[i,4] = df.iloc[i,4].replace("　", " ")
    df.iloc[i,4] = df.iloc[i,4].replace("　", " ")
    i = i + 1

i = 0
for elem_kamoku in elem_kamokus:
    df.iloc[i,5] = df.iloc[i,5].replace("　", " ")
    df.iloc[i,5] = df.iloc[i,5].replace("　", " ")
    df.iloc[i,5] = df.iloc[i,5].replace("　", " ")
    df.iloc[i,5] = df.iloc[i,5].replace("　", " ")
    df.iloc[i,5] = df.iloc[i,5].replace("　", " ")
    df.iloc[i,5] = df.iloc[i,5].replace("　", " ")
    i = i + 1


i = 0
for elem_kamoku in elem_kamokus:
    if df.iloc[i,1].endswith("/ １ターム") == True:
        df.iloc[i,1] = "１ターム"
        i = i + 1
    elif df.iloc[i,1].endswith("/ ２ターム") == True:
        df.iloc[i,1] = "２ターム"
        i = i + 1
    elif df.iloc[i,1].endswith("/ １－２ターム") == True:
        df.iloc[i,1] = "１－２ターム"
        i = i + 1
    elif df.iloc[i,1].endswith("/ ４ターム") == True:
        df.iloc[i,1] = "４ターム"
        i = i + 1
    elif df.iloc[i,1].endswith("/ ５ターム") == True:
        df.iloc[i,1] = "５ターム"
        i = i + 1
    elif df.iloc[i,1].endswith("/ ４－５ターム") == True:
        df.iloc[i,1] = "４－５ターム"
        i = i + 1
    elif df.iloc[i,1].endswith("/ 前期集中") == True:
        df.iloc[i,1] = "前期集中"
        i = i + 1
    elif df.iloc[i,1].endswith("/ 後期集中") == True:
        df.iloc[i,1] = "後期集中"
        i = i + 1
    elif df.iloc[i,1].endswith("/ 集中") == True:
        df.iloc[i,1] = "集中"
        i = i + 1
    else:
        i = i + 1

i = 0
for elem_kamoku in elem_kamokus:
    if df.iloc[i,0].startswith(elem_kamoku + " ") == True:
        df.iloc[i,0] = elem_kamoku
        i = i + 1
    elif df.iloc[i,0].endswith(elem_kamoku) == True:
        df.iloc[i,0] = elem_kamoku
        i = i + 1
    else:
        df.iloc[i,0] = "※※※" + elem_kamoku
        i = i + 1



df.to_csv("シラバス（第二免許）.csv", encoding="cp932", index=False)