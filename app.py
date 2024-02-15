# app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/grocery_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:onkar123@localhost/grocery_db'
db = SQLAlchemy(app)

# Define GroceryItem model
class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)

# API Endpoints
# Admin endpoints
@app.route('/api/admin/grocery-items', methods=['POST'])
def add_grocery_item():
    data = request.json
    new_item = GroceryItem(name=data['name'], price=data['price'], inventory=data['inventory'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Grocery item added successfully."}), 201

@app.route('/api/admin/grocery-items', methods=['GET'])
def view_grocery_items():
    items = GroceryItem.query.all()
    output = []
    for item in items:
        item_data = {'id': item.id, 'name': item.name, 'price': item.price, 'inventory': item.inventory}
        output.append(item_data)
    return jsonify({"grocery_items": output}), 200

@app.route('/api/admin/grocery-items/<int:item_id>', methods=['DELETE'])
def remove_grocery_item(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Grocery item removed successfully."}), 204

@app.route('/api/admin/grocery-items/<int:item_id>', methods=['PUT'])
def update_grocery_item(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    data = request.json
    item.name = data['name']
    item.price = data['price']
    item.inventory = data['inventory']
    db.session.commit()
    return jsonify({"message": "Grocery item updated successfully."}), 200

@app.route('/api/admin/grocery-items/<int:item_id>/inventory', methods=['PATCH'])
def manage_inventory(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    data = request.json
    item.inventory += data['change']
    db.session.commit()
    return jsonify({"message": "Inventory managed successfully."}), 200

# User endpoints
@app.route('/api/grocery-items', methods=['GET'])
def view_available_items():
    items = GroceryItem.query.filter(GroceryItem.inventory > 0).all()
    output = []
    for item in items:
        item_data = {'id': item.id, 'name': item.name, 'price': item.price}
        output.append(item_data)
    return jsonify({"available_items": output}), 200

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    # For simplicity, assuming the order format is a list of dictionaries with item_id and quantity
    # Implement actual order creation logic as per requirement
    order_details = []
    for order_item in data['items']:
        item = GroceryItem.query.get(order_item['item_id'])
        if item and item.inventory >= order_item['quantity']:
            order_details.append({'item_id': item.id, 'name': item.name, 'price': item.price, 'quantity': order_item['quantity']})
            item.inventory -= order_item['quantity']
    if order_details:
        # Implement order creation logic
        return jsonify({"order_details": order_details}), 201
    else:
        return jsonify({"message": "Unable to create order. Invalid items or insufficient inventory."}), 400

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

