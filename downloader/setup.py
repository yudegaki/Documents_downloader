import os,sys,json

path = './secure_login.json'

conf = {
    'student_id': '',
    'g_login_passwd': '',
    'c_login_passwd': '',
    'dl_dir_path': '',
    'target_dir_path': '',
    'chromedriver_dir_path': ''
}

def make_setup():
    print('学籍番号を入力してください ex)j012345 >')
    conf['student_id'] = input()

    print('G Suiteアカウントのパスワードを入力してください >')
    conf['g_login_passwd'] = input()

    print('Course Powerアカウントのパスワードを入力してください >')
    conf['c_login_passwd'] = input()

    print('デフォルトのダウンロードディレクトリの絶対パスを入力してください ex-linux-ver)/home/tmp/Downloads/ ex-windows-ver)C:\\\\Users\\\\hoge\\\\Downloads\\\\ >')
    conf['dl_dir_path'] = input()

    print('ダウンロードした教材を保存したいディレクトリの絶対パスを入力してください ex-linux-ver)/home/tmp/escape/ ex-windows-ver)C:\\\\Users\\\\hoge\\\\Documents\\\\escape\\\\ >')
    conf['target_dir_path'] = input()

    print('chrome driverを置いたディレクトリのパスを入力してください ex-linux-ver)./chromedriver ex-windows-ver).\\\\chromedriver.exe >\n注)chromedriverはmain.pyと同じフォルダに配置してください')
    conf['chromedriver_dir_path'] = input()

    with open(path,mode = 'w') as f:
        json.dump(conf,f,indent = 4)

    print('先程入力した内容はsecure_login.jsonに保存されています.内容を変更したい場合はもう一度setup.pyを実行するか,secure_login.jsonを編集してください.')

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
