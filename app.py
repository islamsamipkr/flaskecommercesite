from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

# ---------- Fake product data ----------
PRODUCTS = [
    {
        "id": 1,
        "name": "Inovo Hoodie",
        "category": "Clothing",
        "description": "Cozy unisex hoodie with minimal InovoCB logo.",
        "price": 49.99,
    },
    {
        "id": 2,
        "name": "Data Points T-Shirt",
        "category": "Clothing",
        "description": "Soft cotton tee for data lovers.",
        "price": 24.99,
    },
    {
        "id": 3,
        "name": "Inovo Mug",
        "category": "Accessories",
        "description": "Ceramic mug for your everyday coffee + code sessions.",
        "price": 14.50,
    },
    {
        "id": 4,
        "name": "Sticker Pack",
        "category": "Accessories",
        "description": "Set of vinyl stickers: robot, bear, data icons.",
        "price": 7.99,
    },
    {
        "id": 5,
        "name": "Laptop Sleeve 13\"",
        "category": "Gear",
        "description": "Padded sleeve with futuristic Inovo pattern.",
        "price": 32.00,
    },
    {
        "id": 6,
        "name": "Desk Mat",
        "category": "Gear",
        "description": "Extended mouse pad / desk mat with neon grid design.",
        "price": 29.99,
    },
]


def find_product(prod_id: int):
    for p in PRODUCTS:
        if p["id"] == prod_id:
            return p
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/products", methods=["GET"])
def get_products():
    """Return product catalog."""
    return jsonify(PRODUCTS)


@app.route("/api/checkout", methods=["POST"])
def checkout():
    """Fake checkout endpoint."""
    data = request.get_json(force=True) or {}

    customer = data.get("customer", {})
    items = data.get("items", [])

    name = (customer.get("name") or "").strip()
    email = (customer.get("email") or "").strip()
    address = (customer.get("address") or "").strip()

    if not name or not email or not address:
        return jsonify({"error": "Please provide name, email and address."}), 400

    if not items:
        return jsonify({"error": "Your cart is empty."}), 400

    detailed_items = []
    total = 0.0

    for item in items:
        prod_id = int(item.get("id"))
        qty = int(item.get("quantity", 0))
        if qty <= 0:
            continue

        product = find_product(prod_id)
        if not product:
            continue

        line_total = product["price"] * qty
        total += line_total
        detailed_items.append({
            "id": product["id"],
            "name": product["name"],
            "quantity": qty,
            "price": product["price"],
            "line_total": round(line_total, 2),
        })

    if not detailed_items:
        return jsonify({"error": "No valid items in cart."}), 400

    order_id = f"EC-{int(time.time())}"

    response = {
        "orderId": order_id,
        "customer": {
            "name": name,
            "email": email,
            "address": address,
        },
        "items": detailed_items,
        "total": round(total, 2),
        "message": "Order placed successfully (demo only, no real payment).",
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
