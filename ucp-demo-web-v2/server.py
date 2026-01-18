"""
UCP + AP2 Shopping Agent - Web Server
A Flask-based backend for the shopping agent demo
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import urllib.request
import json
import hashlib
import datetime
import random
import string
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# ============================================
# CONFIGURATION
# ============================================
API_KEY = os.environ.get('GEMINI_API_KEY', 'Use your API Key')

# ============================================
# USER PROFILE (Simulated)
# ============================================
user_profile = {
    "user_id": "user_12345",
    "name": "Ayush",
    "email": "ayush@example.com",
    "payment_methods": [
        {
            "id": "pm_1",
            "type": "credit_card",
            "brand": "Visa",
            "last_four": "4242",
            "is_default": True
        },
        {
            "id": "pm_2",
            "type": "paypal",
            "email": "ayush@paypal.com",
            "is_default": False
        }
    ],
    "shipping_address": {
        "street": "123 Main Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "zip": "400001",
        "country": "India"
    }
}

# ============================================
# STATE
# ============================================
cart = []
intent_mandates = []
order_history = []
conversation_history = []
last_mentioned_product = None

# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_mandate_id():
    return "mandate_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

def generate_order_id():
    return "order_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_signature(data):
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode()).hexdigest()[:16]

def get_timestamp():
    return datetime.datetime.now().isoformat()

def load_products():
    with open("products.json", "r") as file:
        data = json.load(file)
    return data["products"]

def find_product_by_id(products, product_id):
    for product in products:
        if product["id"] == str(product_id):
            return product
    return None

def get_cart_total(products):
    total = 0
    for product_id in cart:
        product = find_product_by_id(products, product_id)
        if product:
            total += product["price"]
    return total

def get_cart_items(products):
    items = []
    for product_id in cart:
        product = find_product_by_id(products, product_id)
        if product:
            items.append(product)
    return items

# ============================================
# AP2 FUNCTIONS
# ============================================

def create_cart_mandate(products):
    cart_items = []
    for product_id in cart:
        product = find_product_by_id(products, product_id)
        if product:
            cart_items.append({
                "product_id": product["id"],
                "name": product["name"],
                "price": product["price"]
            })
    
    total = get_cart_total(products)
    
    mandate = {
        "mandate_id": generate_mandate_id(),
        "mandate_type": "CART_MANDATE",
        "status": "PENDING_APPROVAL",
        "created_at": get_timestamp(),
        "user_id": user_profile["user_id"],
        "cart_items": cart_items,
        "total_amount": total,
        "currency": "USD",
        "payment_method": next(pm for pm in user_profile["payment_methods"] if pm["is_default"]),
        "shipping_address": user_profile["shipping_address"],
        "signature": None
    }
    
    return mandate

def sign_mandate(mandate):
    mandate['status'] = "APPROVED"
    mandate['approved_at'] = get_timestamp()
    mandate['signature'] = generate_signature(mandate)
    mandate['user_signature'] = f"sig_{user_profile['user_id']}_{generate_signature({'user': user_profile['user_id'], 'time': get_timestamp()})}"
    return mandate

def process_payment(mandate):
    payment_mandate = {
        "payment_mandate_id": generate_mandate_id(),
        "cart_mandate_id": mandate['mandate_id'],
        "amount": mandate['total_amount'],
        "currency": mandate['currency'],
        "payment_method_token": f"tok_{generate_signature(mandate['payment_method'])}",
        "merchant_id": "merchant_ucp_demo",
        "processed_at": get_timestamp(),
        "status": "COMPLETED",
        "authorization_code": ''.join(random.choices(string.digits, k=6))
    }
    return payment_mandate

def create_order(cart_mandate, payment_mandate):
    order = {
        "order_id": generate_order_id(),
        "status": "CONFIRMED",
        "created_at": get_timestamp(),
        "customer": {
            "user_id": user_profile["user_id"],
            "name": user_profile["name"],
            "email": user_profile["email"]
        },
        "items": cart_mandate['cart_items'],
        "total": cart_mandate['total_amount'],
        "currency": cart_mandate['currency'],
        "shipping_address": cart_mandate['shipping_address'],
        "payment": {
            "method": cart_mandate['payment_method']['type'],
            "authorization_code": payment_mandate['authorization_code'],
            "payment_mandate_id": payment_mandate['payment_mandate_id']
        },
        "ap2_verification": {
            "cart_mandate_id": cart_mandate['mandate_id'],
            "cart_mandate_signature": cart_mandate['signature'],
            "user_signature": cart_mandate.get('user_signature'),
            "payment_mandate_id": payment_mandate['payment_mandate_id']
        },
        "estimated_delivery": (datetime.datetime.now() + datetime.timedelta(days=4)).strftime("%B %d, %Y")
    }
    
    order_history.append(order)
    return order

def create_intent_mandate(conditions):
    mandate = {
        "mandate_id": generate_mandate_id(),
        "mandate_type": "INTENT_MANDATE",
        "status": "ACTIVE",
        "created_at": get_timestamp(),
        "user_id": user_profile["user_id"],
        "conditions": conditions,
        "max_amount": conditions.get("max_price", 100),
        "currency": "USD",
        "valid_until": (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat(),
        "signature": generate_signature(conditions)
    }
    
    intent_mandates.append(mandate)
    return mandate

def check_intent_mandates(product):
    for mandate in intent_mandates:
        if mandate['status'] != 'ACTIVE':
            continue
        
        conditions = mandate['conditions']
        
        if 'category' in conditions:
            if conditions['category'].lower() != product['category'].lower():
                continue
        
        if 'max_price' in conditions:
            if product['price'] > conditions['max_price']:
                continue
        
        return mandate
    
    return None

# ============================================
# AI FUNCTIONS
# ============================================

def ask_gemini(user_message, products):
    global last_mentioned_product
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    products_list = ""
    for p in products:
        products_list += f"ID:{p['id']} - {p['name']} ({p['brand']}) - ${p['price']} - {p['category']}\n"
    
    last_product_info = "None"
    if last_mentioned_product:
        last_product_info = f"ID:{last_mentioned_product['id']} - {last_mentioned_product['name']}"
    
    history = "\n".join(conversation_history[-6:]) if conversation_history else "None"
    
    prompt = f"""You are a shopping assistant.

AVAILABLE PRODUCTS:
{products_list}

LAST DISCUSSED PRODUCT: {last_product_info}

CONVERSATION:
{history}

USER: {user_message}

Determine intent and respond in this EXACT format:

INTENT: [BROWSE/ADD_TO_CART/VIEW_CART/CHECKOUT/CHAT]
PRODUCT_ID: [number or NONE]
RESPONSE: [Your helpful message]

Important: If user wants to add a product, identify the correct PRODUCT_ID from the list above."""

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"INTENT: CHAT\nPRODUCT_ID: NONE\nRESPONSE: Sorry, I encountered an error: {e}"

def parse_gemini_response(response):
    lines = response.strip().split('\n')
    
    intent = "CHAT"
    product_id = None
    message_lines = []
    in_response = False
    
    for line in lines:
        line_stripped = line.strip()
        
        if line_stripped.upper().startswith("INTENT:"):
            intent = line_stripped.split(":", 1)[1].strip().upper()
        elif line_stripped.upper().startswith("PRODUCT_ID:"):
            pid = line_stripped.split(":", 1)[1].strip()
            if pid.upper() != "NONE" and pid != "":
                pid_clean = ''.join(filter(str.isdigit, pid))
                if pid_clean:
                    product_id = pid_clean
        elif line_stripped.upper().startswith("RESPONSE:"):
            in_response = True
            rest = line_stripped.split(":", 1)[1].strip() if ":" in line_stripped else ""
            if rest:
                message_lines.append(rest)
        elif in_response:
            message_lines.append(line_stripped)
    
    message = " ".join(message_lines) if message_lines else response
    return intent, product_id, message

# ============================================
# API ROUTES
# ============================================

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/user', methods=['GET'])
def get_user():
    return jsonify(user_profile)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = load_products()
    return jsonify(products)

@app.route('/api/cart', methods=['GET'])
def get_cart():
    products = load_products()
    items = get_cart_items(products)
    total = get_cart_total(products)
    return jsonify({
        "items": items,
        "total": total,
        "count": len(cart)
    })

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    global last_mentioned_product
    
    data = request.json
    product_id = str(data.get('product_id'))
    
    products = load_products()
    product = find_product_by_id(products, product_id)
    
    if product:
        cart.append(product_id)
        last_mentioned_product = product
        
        # Check for intent mandate
        matching_mandate = check_intent_mandates(product)
        
        return jsonify({
            "success": True,
            "product": product,
            "cart_count": len(cart),
            "auto_buy_triggered": matching_mandate is not None,
            "mandate": matching_mandate
        })
    
    return jsonify({"success": False, "error": "Product not found"})

@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    cart.clear()
    return jsonify({"success": True})

@app.route('/api/checkout/mandate', methods=['POST'])
def create_checkout_mandate():
    products = load_products()
    
    if not cart:
        return jsonify({"success": False, "error": "Cart is empty"})
    
    mandate = create_cart_mandate(products)
    return jsonify({
        "success": True,
        "mandate": mandate,
        "user": user_profile
    })

@app.route('/api/checkout/approve', methods=['POST'])
def approve_checkout():
    data = request.json
    mandate = data.get('mandate')
    
    if not mandate:
        return jsonify({"success": False, "error": "No mandate provided"})
    
    # Sign mandate
    signed_mandate = sign_mandate(mandate)
    
    # Process payment
    payment_mandate = process_payment(signed_mandate)
    
    # Create order
    order = create_order(signed_mandate, payment_mandate)
    
    # Clear cart
    cart.clear()
    
    return jsonify({
        "success": True,
        "signed_mandate": signed_mandate,
        "payment_mandate": payment_mandate,
        "order": order
    })

@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify(order_history)

@app.route('/api/intent-mandate', methods=['POST'])
def create_intent_mandate_route():
    data = request.json
    conditions = data.get('conditions', {})
    
    mandate = create_intent_mandate(conditions)
    return jsonify({
        "success": True,
        "mandate": mandate
    })

@app.route('/api/intent-mandates', methods=['GET'])
def get_intent_mandates():
    return jsonify(intent_mandates)

@app.route('/api/chat', methods=['POST'])
def chat():
    global last_mentioned_product
    
    data = request.json
    user_message = data.get('message', '')
    
    products = load_products()
    
    # Get AI response
    response = ask_gemini(user_message, products)
    intent, product_id, message = parse_gemini_response(response)
    
    # Update conversation history
    conversation_history.append(f"User: {user_message}")
    conversation_history.append(f"Agent: {message[:100]}")
    
    # Build response
    result = {
        "intent": intent,
        "message": message,
        "product_id": product_id
    }
    
    # Handle different intents
    if intent == "ADD_TO_CART" and product_id:
        product = find_product_by_id(products, product_id)
        if product:
            cart.append(product_id)
            last_mentioned_product = product
            result["added_product"] = product
            result["cart_count"] = len(cart)
            
            # Check for intent mandate
            matching_mandate = check_intent_mandates(product)
            if matching_mandate:
                result["auto_buy_triggered"] = True
                result["mandate"] = matching_mandate
    
    elif intent == "VIEW_CART":
        result["cart"] = {
            "items": get_cart_items(products),
            "total": get_cart_total(products)
        }
    
    elif intent == "BROWSE":
        # Update last mentioned product from response
        for product in products:
            if product["name"].lower() in message.lower():
                last_mentioned_product = product
                break
    
    return jsonify(result)

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🛒 UCP + AP2 Shopping Agent - Web Server")
    print("=" * 50)
    print("\nStarting server at http://localhost:5000")
    print("Open this URL in your browser to use the demo.\n")
    
    app.run(debug=True, port=5000)
