from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    orders = db.get_all_orders()
    warning = request.args.get('warning')
    return render_template('form.html', orders=orders, warning=warning)

def product():
    # 查詢產品名稱或價格
    if request.method == 'GET':
        category = request.args.get("category")
        product_name = request.args.get("product")
        if category:
            names = db.get_product_names_by_category(category)
            return jsonify({"product": names}), 200
        if product_name:
            price = db.get_product_price(product_name)
            return jsonify({"price": price}), 200
        return jsonify({"error": "Missing category or product parameter"}), 400
    
    # 新增訂單
    elif request.method == 'POST':
        data = request.get_json()
        order_data = {
            "product_date":    data.get("date"),
            "customer_name":   data.get("customer_name"),
            "product_name":    data.get("product"),
            "product_amount":  data.get("amount"),
            "product_total":   data.get("total"),
            "product_status":  data.get("status"),
            "product_note":    data.get("note")

        }
        # Add the order to the database
        db.add_order(order_data)

        return redirect(url_for('index', warning="Order added successfully"))
    # 刪除訂單
    elif request.method == 'DELETE':
        order_id = request.args.get('order_id')

        if not order_id:
            return jsonify({"error": "Missing order_id parameter"}), 400

        db.delete_order(order_id)

        return jsonify({"message": "Order deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
