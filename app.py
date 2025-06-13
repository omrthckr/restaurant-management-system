from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# In-memory storage (in production, use a database)
menu_items = {
    "appetizers": [
        {"id": 1, "name": "Buffalo Wings", "price": 12.99, "description": "Crispy wings with spicy buffalo sauce", "available": True, "prep_time": 15},
        {"id": 2, "name": "Mozzarella Sticks", "price": 8.99, "description": "Golden fried mozzarella with marinara sauce", "available": True, "prep_time": 10},
        {"id": 3, "name": "Loaded Nachos", "price": 10.99, "description": "Tortilla chips with cheese, jalapeños, and sour cream", "available": True, "prep_time": 12}
    ],
    "mains": [
        {"id": 4, "name": "Grilled Salmon", "price": 24.99, "description": "Fresh Atlantic salmon with lemon butter sauce", "available": True, "prep_time": 25},
        {"id": 5, "name": "Ribeye Steak", "price": 32.99, "description": "12oz prime ribeye cooked to perfection", "available": True, "prep_time": 30},
        {"id": 6, "name": "Chicken Parmesan", "price": 18.99, "description": "Breaded chicken breast with marinara and mozzarella", "available": True, "prep_time": 20},
        {"id": 7, "name": "Vegetarian Pasta", "price": 16.99, "description": "Penne pasta with seasonal vegetables and herb sauce", "available": True, "prep_time": 18}
    ],
    "desserts": [
        {"id": 8, "name": "Chocolate Cake", "price": 7.99, "description": "Rich chocolate layer cake with ganache", "available": True, "prep_time": 5},
        {"id": 9, "name": "Cheesecake", "price": 6.99, "description": "New York style cheesecake with berry compote", "available": True, "prep_time": 5},
        {"id": 10, "name": "Ice Cream Sundae", "price": 5.99, "description": "Vanilla ice cream with your choice of toppings", "available": True, "prep_time": 5}
    ],
    "beverages": [
        {"id": 11, "name": "Craft Beer", "price": 5.99, "description": "Local IPA on tap", "available": True, "prep_time": 2},
        {"id": 12, "name": "House Wine", "price": 8.99, "description": "Red or white wine by the glass", "available": True, "prep_time": 2},
        {"id": 13, "name": "Fresh Juice", "price": 3.99, "description": "Orange, apple, or cranberry juice", "available": True, "prep_time": 3},
        {"id": 14, "name": "Soft Drinks", "price": 2.99, "description": "Coke, Pepsi, Sprite, or water", "available": True, "prep_time": 1}
    ]
}

# Tables management
tables = {}
for i in range(1, 21):  # 20 tables
    tables[i] = {
        "id": i,
        "capacity": 4 if i <= 15 else 6,  # Tables 1-15 seat 4, 16-20 seat 6
        "status": "available",  # available, occupied, reserved, cleaning
        "current_order": None,
        "waiter": None,
        "reservation_time": None,
        "customer_name": None
    }

# Storage
orders = []
kitchen_orders = []
inventory = {
    1: {"id": 1, "name": "Chicken Breast", "current_stock": 50, "min_stock": 10, "unit": "lbs", "cost_per_unit": 5.99},
    2: {"id": 2, "name": "Buffalo Sauce", "current_stock": 5, "min_stock": 3, "unit": "bottles", "cost_per_unit": 3.99},
    3: {"id": 3, "name": "Mozzarella Cheese", "current_stock": 15, "min_stock": 5, "unit": "lbs", "cost_per_unit": 4.99},
    4: {"id": 4, "name": "Salmon Fillet", "current_stock": 25, "min_stock": 5, "unit": "lbs", "cost_per_unit": 12.99},
}
staff = {
    1: {"id": 1, "name": "John Manager", "role": "manager", "email": "john@restaurant.com", "phone": "555-0101", "hourly_rate": 25.00, "status": "active"},
    2: {"id": 2, "name": "Sarah Chef", "role": "chef", "email": "sarah@restaurant.com", "phone": "555-0102", "hourly_rate": 22.00, "status": "active"},
}
schedules = []
payments = []
order_counter = 1
payment_counter = 1

def read_html_file(filename):
    """Safely read HTML files with multiple encoding attempts"""
    try:
        if os.path.exists(filename):
            # Try multiple encodings in order of preference
            encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings_to_try:
                try:
                    with open(filename, 'r', encoding=encoding) as f:
                        content = f.read()
                        print(f"✅ Successfully read {filename} with {encoding} encoding")
                        return content
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"❌ Error with {encoding} encoding for {filename}: {str(e)}")
                    continue
            
            # If all encodings fail, try reading as binary and decode with error handling
            try:
                with open(filename, 'rb') as f:
                    content = f.read()
                    # Try to decode with utf-8 and replace problematic characters
                    decoded_content = content.decode('utf-8', errors='replace')
                    print(f"⚠️ Read {filename} with error replacement")
                    return decoded_content
            except Exception as e:
                return f"<h1>Error reading file: {filename}</h1><p>All encoding attempts failed. Error: {str(e)}</p>"
        else:
            return f"<h1>File not found: {filename}</h1><p>Make sure all HTML files are in the same directory as app.py</p>"
    except Exception as e:
        return f"<h1>Unexpected error reading file: {filename}</h1><p>Error: {str(e)}</p>"

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Restaurant Management System</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                padding: 40px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                margin: 0;
                color: white;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            h1 { 
                text-align: center; 
                font-size: 3rem; 
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            .subtitle {
                text-align: center;
                font-size: 1.2rem;
                margin-bottom: 40px;
                opacity: 0.9;
            }
            .system-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 25px;
                margin-top: 30px;
            }
            .system-card {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            .system-card:hover {
                transform: translateY(-5px);
                border-color: rgba(255, 255, 255, 0.5);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            }
            .system-icon {
                font-size: 3rem;
                margin-bottom: 20px;
            }
            .system-title {
                font-size: 1.4rem;
                font-weight: bold;
                margin-bottom: 15px;
            }
            .system-link {
                display: inline-block;
                padding: 12px 24px;
                background: rgba(255, 255, 255, 0.2);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            .system-link:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍽️ Restaurant Management System</h1>
            <p class="subtitle">Complete solution for restaurant operations</p>
            
            <div class="system-grid">
                <div class="system-card">
                    <div class="system-icon">🍕</div>
                    <div class="system-title">Customer Menu</div>
                    <p>Online ordering system for customers</p>
                    <a href="/menu" class="system-link">View Menu</a>
                </div>
                
                <div class="system-card">
                    <div class="system-icon">👨‍💼</div>
                    <div class="system-title">Admin Dashboard</div>
                    <p>Manage orders, tables, and restaurant operations</p>
                    <a href="/admin" class="system-link">Admin Panel</a>
                </div>
                
                <div class="system-card">
                    <div class="system-icon">👨‍🍳</div>
                    <div class="system-title">Kitchen System</div>
                    <p>Track and manage kitchen orders</p>
                    <a href="/kitchen" class="system-link">Kitchen View</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# ============= MENU ROUTES =============
@app.route('/menu')
def customer_menu():
    return read_html_file('restaurant_menu_html.html')

@app.route('/admin')
def admin_dashboard():
    return read_html_file('admin_dashboard.html')

@app.route('/kitchen')
def kitchen_system():
    return read_html_file('kitchen_system.html')

# ============= API ROUTES =============
@app.route('/api/menu')
def get_menu():
    return jsonify(menu_items)

@app.route('/api/menu', methods=['POST'])
def add_menu_item():
    data = request.json
    category = data.get('category')
    if category not in menu_items:
        return jsonify({'success': False, 'message': 'Invalid category'}), 400
    
    new_id = max([item['id'] for cat in menu_items.values() for item in cat]) + 1
    new_item = {
        'id': new_id,
        'name': data['name'],
        'price': float(data['price']),
        'description': data['description'],
        'available': data.get('available', True),
        'prep_time': int(data.get('prep_time', 15))
    }
    
    menu_items[category].append(new_item)
    return jsonify({'success': True, 'item': new_item})

@app.route('/api/tables')
def get_tables():
    return jsonify(list(tables.values()))

@app.route('/api/tables/available')
def get_available_tables():
    available = [table for table in tables.values() if table['status'] == 'available']
    return jsonify(available)

@app.route('/api/tables/<int:table_id>', methods=['PUT'])
def update_table(table_id):
    if table_id not in tables:
        return jsonify({'success': False, 'message': 'Table not found'}), 404
    
    data = request.json
    tables[table_id].update(data)
    return jsonify({'success': True, 'table': tables[table_id]})

@app.route('/api/order', methods=['POST'])
def place_order():
    global order_counter
    try:
        data = request.json
        
        # Calculate total and estimated time
        total = 0
        estimated_time = 0
        order_items = []
        
        for item in data['items']:
            # Find menu item details
            menu_item = None
            for category in menu_items.values():
                for m_item in category:
                    if m_item['id'] == item['id']:
                        menu_item = m_item
                        break
                if menu_item:
                    break
            
            if menu_item:
                item_total = menu_item['price'] * item['quantity']
                total += item_total
                estimated_time = max(estimated_time, menu_item['prep_time'])
                
                order_items.append({
                    'id': item['id'],
                    'name': menu_item['name'],
                    'price': menu_item['price'],
                    'quantity': item['quantity']
                })
        
        # Create order
        order = {
            'id': order_counter,
            'order_type': data.get('order_type', 'pickup'),
            'customer_name': data.get('customer_name', 'Anonymous'),
            'customer_phone': data.get('customer_phone', ''),
            'customer_address': data.get('customer_address', ''),
            'table_number': data.get('table_number'),
            'items': order_items,
            'total': round(total, 2),
            'status': 'pending',
            'timestamp': datetime.now().isoformat(),
            'estimated_time': estimated_time
        }
        
        orders.append(order)
        
        # Add to kitchen queue
        kitchen_order = {
            'id': order_counter,
            'table_number': data.get('table_number'),
            'order_type': data.get('order_type', 'pickup'),
            'items': order_items,
            'status': 'pending',
            'timestamp': datetime.now().isoformat(),
            'estimated_time': estimated_time
        }
        kitchen_orders.append(kitchen_order)
        
        # Update table status if dine-in
        if data.get('table_number') and data.get('order_type') == 'dine-in':
            table_id = int(data['table_number'])
            if table_id in tables:
                tables[table_id].update({
                    'status': 'occupied',
                    'current_order': order_counter,
                    'customer_name': data.get('customer_name')
                })
        
        order_counter += 1
        
        return jsonify({
            'success': True,
            'order_id': order['id'],
            'total': order['total'],
            'estimated_time': estimated_time,
            'message': 'Order placed successfully!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error placing order: {str(e)}'}), 400

@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    new_status = data.get('status')
    
    # Update main order
    for order in orders:
        if order['id'] == order_id:
            order['status'] = new_status
            break
    
    # Update kitchen order
    for kitchen_order in kitchen_orders:
        if kitchen_order['id'] == order_id:
            kitchen_order['status'] = new_status
            break
    
    return jsonify({'success': True, 'status': new_status})

@app.route('/api/kitchen/orders')
def get_kitchen_orders():
    return jsonify(kitchen_orders)

@app.route('/api/kitchen/orders/<int:order_id>/complete', methods=['POST'])
def complete_kitchen_order(order_id):
    for kitchen_order in kitchen_orders:
        if kitchen_order['id'] == order_id:
            kitchen_order['status'] = 'completed'
            kitchen_order['completed_time'] = datetime.now().isoformat()
            break
    
    # Also update main order
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'ready'
            break
    
    return jsonify({'success': True})

@app.route('/api/inventory')
def get_inventory():
    return jsonify(list(inventory.values()))

@app.route('/api/inventory/low-stock')
def get_low_stock():
    low_stock = [item for item in inventory.values() if item['current_stock'] <= item['min_stock']]
    return jsonify(low_stock)

@app.route('/api/staff')
def get_staff():
    return jsonify(list(staff.values()))

@app.route('/api/schedules')
def get_schedules():
    return jsonify(schedules)

@app.route('/api/payments')
def get_payments():
    return jsonify(payments)

@app.route('/api/reports/sales')
def sales_report():
    # Calculate total sales
    total_sales = sum(order['total'] for order in orders if order['status'] == 'paid')
    
    # Popular items
    item_sales = defaultdict(lambda: {'quantity': 0, 'revenue': 0, 'name': ''})
    
    for order in orders:
        if order['status'] == 'paid':
            for item in order['items']:
                item_sales[item['id']]['name'] = item['name']
                item_sales[item['id']]['quantity'] += item['quantity']
                item_sales[item['id']]['revenue'] += item['price'] * item['quantity']
    
    # Convert to list and sort by quantity
    popular_items = sorted(
        [{'id': k, **v} for k, v in item_sales.items()],
        key=lambda x: x['quantity'],
        reverse=True
    )
    
    paid_orders = [o for o in orders if o['status'] == 'paid']
    report = {
        'total_orders': len(paid_orders),
        'total_sales': round(total_sales, 2),
        'average_order_value': round(total_sales / max(len(paid_orders), 1), 2),
        'popular_items': popular_items[:10],
        'total_customers': len(set(order.get('customer_name', 'Anonymous') for order in orders)),
        'generated_at': datetime.now().isoformat()
    }
    
    return jsonify(report)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    print("🍽️ Restaurant Management System Starting...")
    print("📍 Available at: http://localhost:5000")
    print("🍕 Customer Menu: http://localhost:5000/menu")
    print("👨‍💼 Admin Dashboard: http://localhost:5000/admin")
    print("👨‍🍳 Kitchen System: http://localhost:5000/kitchen")
    app.run(debug=True, host='0.0.0.0', port=5000)