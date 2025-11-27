from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # 假資料（前端測試用）
    orders = [
        {"id": 1, "product": "T-Shirt", "qty": 2, "subtotal": 50},
        {"id": 2, "product": "Shoes", "qty": 1, "subtotal": 90},
    ]
    return render_template('form.html', orders=orders)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
