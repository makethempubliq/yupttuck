from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/get_data', methods=('GET', 'POST'))
def get_data():
    data_for_gangnam = {
        'images': ['동대문엽기떡볶이 강남점 긍정부정.jpg', '동대문엽기떡볶이 강남점 워드클라우드.jpg'],
        'descriptions': ['강남점 이미지 1에 대한 설명', '강남점 이미지 2에 대한 설명']
    }
    print('겟데이타아아아ㅏ')
    return jsonify(data_for_gangnam)

if __name__ == '__main__':
    app.run(debug=True)