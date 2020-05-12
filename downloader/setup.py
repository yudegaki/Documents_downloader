import os,shutil,sys

path = './secure_login.py'

def make_setup():
    print('学籍番号を入力してください ex)j012345 >')
    s = input()
    s = "student_id = '" + s + "'\n"
    with open(path,mode = 'w') as f:
        f.write(s)
    print('G Suiteアカウントのパスワードを入力してください >')
    s = input()
    s = "g_login_passwd = '" + s + "'\n"
    with open(path,mode = 'a') as f:
        f.write(s)
    print('Course Powerアカウントのパスワードを入力してください >')
    s = input()
    s = "c_login_passwd = '" + s + "'\n"
    with open(path,mode = 'a') as f:
        f.write(s)
    print('デフォルトのダウンロードディレクトリの絶対パスを入力してください ex)/home/tmp/Downloads/>')
    s = input()
    s = "dl_dir_pass = '" + s + "'\n"
    with open(path,mode = 'a') as f:
        f.write(s)
    print('ダウンロードした教材を保存したいディレクトリの絶対パスを入力してください ex)/home/tmp/escape/>')
    s = input()
    s = "target_dir_pass = '" + s + "'\n"
    with open(path,mode = 'a') as f:
        f.write(s)
    print('chrome driverを置いたディレクトリのパスを入力してください ex)./chromedriver >\n注)Windowsを使っている方は拡張子.exeを付けてください. chromedriverはmain.pyと同じフォルダに配置してください')
    s = input()
    s = "chromedriver_dir_pass = '" + s + "'\n"
    with open(path,mode = 'a') as f:
        f.write(s)
    print('先程入力した内容はsecure_login.pyに保存されています.内容を変更したい場合はもう一度setup.pyを実行するか,secure.pyを編集してください.')

def setup_init():
    if os.path.exists(path):
        print('設定ファイルは既に存在します.新たな設定ファイルを作成しますか? y:n >')
        s = input()
        while not (s == 'y' or s == 'n'):
            print('Please input only y or n >')
            s = input()
        if s == 'y':
            os.remove(path)
            return True
        else:
            return False
    else:
        return True

if __name__ == '__main__':
    if setup_init():
        make_setup()
