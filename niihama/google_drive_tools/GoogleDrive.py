# -*- coding: utf-8 -*-
import os
import shutil
import xarray as xr
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

drive = ''
save_dir_name = 'tmp' #ダウンロード先のフォルダ名

# Google Driveと接続
def init_drive():
    global drive
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

# ファイルをダウンロードしてxarrayのデータを返す。ダウンロードファイルは削除
def download_file(dir_name, file_name):
    global drive
    global save_dir_name

    save_dir = os.path.join(os.getcwd(), save_dir_name)

    # フォルダのidを取得
    query = "title = '{}'".format(dir_name)
    dirs = drive.ListFile({'q': query}).GetList()
    if len(dirs) > 2:
        raise Exception('同名ディレクトリが複数存在します')

    dir_id = dirs[0]['id']

    # ファイルを取得
    query = "title = '{0}' and '{1}' in parents".format(file_name, dir_id)
    files = drive.ListFile({'q': query}).GetList()
    if len(files) > 2:
        raise Exception('同名ファイルが複数存在します')

    file_id = files[0]['id']

    file = drive.CreateFile({'id': file_id})

    # ダウンロード先のフォルダを準備
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    # 同名のダウンロードファイルが存在していたらエラー
    if os.path.exists(os.path.join(save_dir, file['title'])):
        raise Exception('同名のファイルがダンロード済みです。delete_download_filesを実行してください')
    # ダウンロード
    file.GetContentFile(os.path.join(save_dir, file['title']))

    data_array = xr.open_dataarray(os.path.join(save_dir, file['title']))

    os.remove(os.path.join(save_dir, file['title']))

    return data_array


# ダウンロード先にしたファイルを全て削除する
def delete_download_files():
    global save_dir_name

    save_dir = os.path.join(os.getcwd(), save_dir_name)
    shutil.rmtree(save_dir)
