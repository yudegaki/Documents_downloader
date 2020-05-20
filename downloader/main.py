'''
Documents Downloader

Copyright (c) 2020 yudegaki

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
'''

# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import time,os,urllib.parse,glob,shutil,sys,json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

S = {}

def load_config():
    global S
    path = './secure_login.json'
    try:
        with open(path,mode = 'r') as f:
            S = json.load(f)
    except FileNotFoundError:
        print("E: ./secure_login.json not found.")
        sys.exit(1)

def chrome_init():
    driver_path = S['chromedriver_dir_path']
    options = Options()
    #複数ダウンロードを許可
    prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=driver_path,chrome_options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    url = 'https://google.com/accounts?hl=ja-JP'
    driver.get(url)

    download_path = S['dl_dir_path']
    #仮の空ファイルを作成
    with open(download_path + 'new_tmp.txt','w') as f:
        f.write('')

    return driver

def chrome_login(driver):
    #学籍番号
    student_id = S['student_id']
    #パスワード
    login_passwd = S['g_login_passwd']
    login_id = student_id + '@g.kogakuin.jp'

    ### IDを入力
    login_id_xpath = '//*[@id="identifierNext"]'
    # xpathの要素が見つかるまで待機
    wait_time = 15
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, login_id_xpath)))
    driver.find_element_by_name("identifier").send_keys(login_id)
    driver.find_element_by_xpath(login_id_xpath).click()
    ### パスワードを入力
    login_passwd_xpath = '//*[@id="passwordNext"]'
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, login_passwd_xpath)))
    driver.find_element_by_name("password").send_keys(login_passwd)
    driver.find_element_by_xpath(login_passwd_xpath).click()
    return

def login_CoursePower(driver):
    student_id = S['student_id']
    login_passwd = S['c_login_passwd']

    url = 'https://study.ns.kogakuin.ac.jp/'
    driver.get(url)

    driver.find_element_by_name("userId").send_keys(student_id)
    driver.find_element_by_name("password").send_keys(login_passwd)
    driver.find_element_by_name("loginButton").click()
    return

def make_dir(dir_name):
    path = S['target_dir_path'] + dir_name
    os.makedirs(path,exist_ok = True)
    return path

def get_latest_filename(dir_name):
    target_dir = dir_name + '/*'
    files_list = glob.glob(target_dir)
    latest_file = max(files_list,key = os.path.getctime)
    return latest_file

def is_complete(dir_name,cnt):
    #最新ファイル名が'new_tmp.txt'or'*.crdownload'の場合ダウンロードが完了していない!!
    s = get_latest_filename(dir_name)
    print('latest file is ' + s)
    if s == dir_name + 'new_tmp.txt':
        if cnt < 100:
            return True
        else:
            #何かしらの異常が起こってるのでerror
            print('Error: ダウンロードエラーが発生しています.通信環境をチェックするかダウンロード先のフォルダ名が正しいものか確認してください.',file=sys.stderr)
            sys.exit(1)
            #一応書いておく
            return False
    elif len(s) >= 4 and s[-4:] == '.tmp':
        return True
    elif len(s) >= 11 and s[-11:] == '.crdownload':
        return True
    else:
        return False

def wait_download(dir_name,driver):
    download_path = S['dl_dir_path']
    cnt = 0
    while is_complete(download_path,cnt):
        cnt += 1
        time.sleep(0.5)
    move_target = get_latest_filename(download_path)
    #フォルダを移動
    find_pos = move_target.rfind('/') + 1
    #Windowsの場合/でファイル名を取得できないため,場合分けする
    if find_pos == 0:
        find_pos = move_target.rfind('\\') + 1
    if os.path.exists(dir_name + move_target[find_pos:]):
        os.remove(download_path + move_target[find_pos:])
        print("This file already exists")
    else :
        shutil.move(move_target,dir_name)
        print("Moved to " + dir_name + move_target[find_pos:] + " !!")
    return

def mark_as_referenced(is_visit,driver):
    #参照済みにする
    is_visit_xpath = '//a[contains(@onclick,"' + is_visit + '")]'
    is_visit_elem = driver.find_element_by_xpath(is_visit_xpath)
    is_visit_elem.click()
    handle_arr = driver.window_handles

    driver.switch_to.window(handle_arr[1])
    driver.close()
    driver.switch_to.window(handle_arr[0])
    return

def download_lecture_document(lecture_name,link,driver):
    driver.execute_script(link)
    title_list = driver.find_elements_by_class_name('courseFolderName')
    document_list = driver.find_elements_by_class_name('kyozaiHidden')

    for i in range(len(document_list)):
        title_list = driver.find_elements_by_class_name('courseFolderName')
        document_list = driver.find_elements_by_class_name('kyozaiHidden')

        save_dir = make_dir(lecture_name + '/' + title_list[i].text + '/')

        link_list = document_list[i].find_elements_by_tag_name('a')
        img_list = document_list[i].find_elements_by_tag_name('img')
        dl_links = []
        img_lists = []

        for l in link_list:
            if l.get_attribute('onclick')[0] == 'k':
                dl_links.append('javascript:' + l.get_attribute('onclick'))
        for l in img_list:
            img_lists.append(l.get_attribute('alt'))
        
        for j in range(min(len(img_lists),len(dl_links))):
            if img_lists[j] != '資料':
                continue            
            driver.execute_script(dl_links[j])
            
            save_link = driver.find_element_by_class_name('courseTable3').find_elements_by_tag_name('a')
            save_links = []
            for sl in save_link:
                if sl.get_attribute('href') == 'javascript:void(0);':
                    save_links.append(sl.get_attribute('onclick'))
            for rop in range(len(save_links)):  
                #Google Driveからのダウンロードかそうでないかで処理を分ける
                if save_links[rop][0] == 'd':
                    driver.execute_script(save_links[rop])
                    wait_download(save_dir,driver)
                elif save_links[rop][0] == 'o':
                    is_visit = save_links[rop]
                    slice_st = save_links[rop].find('http')
                    slice_ed = save_links[rop].find("'",slice_st)
                    save_links[rop] = save_links[rop][slice_st:slice_ed]
                    #urlデコード
                    save_links[rop] = urllib.parse.unquote(save_links[rop])
                    
                    if save_links[rop][:30] == 'https://drive.google.com/file/'or save_links[rop][:30] == 'https://drive.google.com/open?':
                        #参照済みにする
                        mark_as_referenced(is_visit,driver)
                        #ダウンロード
                        driver.get(save_links[rop])
                        elem_xpath = "//div[contains(@aria-label,'ダウンロード')]"
                        target_elem = driver.find_element_by_xpath(elem_xpath)
                        time.sleep(1)
                        target_elem.click()
                        wait_download(save_dir,driver)
                        driver.back()
                    elif save_links[rop][:25] == 'https://drive.google.com/':

                        is_visit_xpath = '//a[contains(@onclick,"' + is_visit + '")]'
                        is_visit_elem = driver.find_element_by_xpath(is_visit_xpath)
                        is_visit_elem.click()
                        handle_arr = driver.window_handles

                        driver.switch_to.window(handle_arr[1])
                        #google driveのダウンロードリストを取得
                        target_elem = driver.find_elements_by_class_name("WYuW0e")
                        time.sleep(1)
                        # Perform double-click action on the element
                        webdriver.ActionChains(driver).double_click(target_elem[0]).perform()
                                            
                        for k in range(len(target_elem)):

                            elem_xpath = "//div[contains(@aria-label,'ダウンロード')]"
                            tg_elem = driver.find_element_by_xpath(elem_xpath)
                            time.sleep(1)
                            tg_elem.click()
                            wait_download(save_dir,driver)
                            if k != len(target_elem)-1:
                                exit_xpath = "//div[contains(@aria-label,'次へ')]"
                                exit_elem = driver.find_element_by_xpath(exit_xpath)
                                exit_elem.click()
                            
                        #画面を閉じ,元のタブにハンドルを戻す
                        driver.close()
                        driver.switch_to.window(handle_arr[0]) 
                    else:
                        #参照済みにする
                        mark_as_referenced(is_visit,driver)


            driver.back()
    
def get_lectures(driver):
    elem = driver.find_elements_by_class_name('courseCard')
    lectures = []
    lecture_links = []
    for i in range(len(elem)):
        s = elem[i].text.splitlines()
        #○限と表記のある要素のみ取得
        if s[0][0].isdigit():
            is_avaiable = elem[i].find_element_by_tag_name('choose').text
            #バグの元凶 絶対にゆるさん
            if is_avaiable == '利用不可':
                continue
            val = elem[i].find_element_by_tag_name('a').get_attribute('onclick')
            lectures.append(s[2])
            lecture_links.append(val)
    #途中でエラーが発生した場合このrangeを変更してダウンロードを省略してみてください
    for i in range(len(lectures)):
        link = 'javascript:' +  lecture_links[i]
        download_lecture_document(lectures[i],link,driver)
        driver.back()   
    
    #作成した仮ファイルを削除
    download_path = S['dl_dir_path']
    os.remove(download_path + 'new_tmp.txt')

    #ログアウト処理
    logout_target = driver.find_element_by_class_name('logoutButtonFrame')
    logout_target.click()
    Alert(driver).accept()
    driver.close()
    
    print('Downloads completed')

if __name__ == '__main__':
    load_config()
    driver = chrome_init()
    chrome_login(driver)
    login_CoursePower(driver)
    get_lectures(driver)