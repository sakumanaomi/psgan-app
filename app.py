import os
# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory

from gnrtimg import gnrtimg

# 画像のアップロード先のディレクトリ

UPLOAD_FOLDER = './templates/images'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__, static_folder='./templates/images')
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ファイルを受け取る方法の指定
@app.route('/', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'img1' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        img1 = request.files['img1']
        img2 = request.files['img2']
        # ファイル名がなかった時の処理
        if img1.filename == '':
            flash('img1ファイルがありません')
            return redirect(request.url)
        if img2.filename == '':
            flash('img2ファイルがありません')
            return redirect(request.url)
        
        filename1 = secure_filename(img1.filename)
        filename2 = secure_filename(img2.filename)
        
        img1_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        img2_path = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        
        img1.save(img1_path)
        img2.save(img2_path)
        
        generated_img_name = 'makeup.png'
        save_path=os.path.join(app.config['UPLOAD_FOLDER'], generated_img_name)
        
        gnrtimg(img1_path, img2_path, save_path)
        
#         return redirect(url_for('uploaded_file', filename=generated_img_name))
        
        return redirect(url_for('show_result', res=generated_img_name))
        
    return render_template('index.html')

@app.route('/<res>')
# 結果を表示する
def show_result(res):
    image_path = f"images/{res}"
    return render_template('result.html', image_path=image_path)




if __name__ == "__main__":
    app.run()