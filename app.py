from flask import Flask, jsonify, render_template, request
import firebase_admin
from firebase_admin import credentials, db, firestore
from flask_mail import Mail, Message
import os

# 🔥 FLASK + FIREBASE SETUP
# ─────────────────────────────────────────────
app = Flask(__name__)

# Load Firebase private key


# --- FIREBASE SETUP USING ENV VARIABLE ---
FIREBASE_KEY_PATH = "/app/firebase_key.json"  # Railway will store this
REALTIME_DB_URL = os.environ.get("REALTIME_DB_URL")

cred = credentials.Certificate(FIREBASE_KEY_PATH)

firebase_admin.initialize_app(cred, {
    "databaseURL": REALTIME_DB_URL
})

firestore_db = firestore.client()

# --- GMAIL SETTINGS FROM ENV VARIABLES ---
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

mail = Mail(app)


# ─────────────────────────────────────────────
# 🍗 KARNATAKA FRIED CHICKEN - MENU DATA
# ─────────────────────────────────────────────
menu_data = {
    "Chicken Burgers": [
        {"name": "Chicken Zinger Burger", "desc": "Classic fried chicken burger with lettuce and mayo.", "price": 100, "img": "chicken_zinger.jpg"},
        {"name": "Spicy Zinger Burger", "desc": "Zesty and fiery spicy zinger burger.", "price": 100, "img": "spicy_zinger.jpg"},
        {"name": "Classic Zinger Burger", "desc": "Signature crunchy zinger burger.", "price": 100, "img": "classic_zinger.jpg"},
        {"name": "Tandoori Zinger Burger", "desc": "Grilled tandoori spiced chicken burger.", "price": 100, "img": "tandoori_zinger.jpg"},
    ],

    "Crispy Chicken Rolls": [
        {"name": "Chicken Roll", "desc": "Crispy chicken roll with veggies and sauce.", "price": 100, "img": "chicken_roll.jpg"},
        {"name": "Chicken Roll With Cheese", "desc": "Cheesy chicken roll loaded with flavor.", "price": 140, "img": "cheese_roll.jpg"},
    ],

    "Double Chicken Burgers": [
        {"name": "Chicken Zinger Burger", "desc": "Double the chicken, double the crunch.", "price": 190, "img": "double_zinger.jpg"},
        {"name": "Spicy Zinger Burger", "desc": "Extra spicy double-layer burger.", "price": 210, "img": "double_spicy.jpg"},
        {"name": "Classic Zinger Burger", "desc": "Double crispy chicken fillets with lettuce.", "price": 210, "img": "double_classic.jpg"},
        {"name": "Tandoori Zinger Burger", "desc": "Double tandoori zinger chicken burger.", "price": 210, "img": "double_tandoori.jpg"},
    ],

    "Chicken Boneless Strips": [
        {"name": "4 Piece Strips", "desc": "Crispy chicken boneless strips (4 pcs).", "price": 150, "img": "boneless_4.jpg"},
        {"name": "6 Piece Strips", "desc": "Crispy chicken boneless strips (6 pcs).", "price": 210, "img": "boneless_4.jpg"},
        {"name": "8 Piece Strips", "desc": "Crispy chicken boneless strips (8 pcs).", "price": 280, "img": "boneless_4.jpg"},
        {"name": "10 Piece Strips", "desc": "Crispy chicken boneless strips (10 pcs).", "price": 330, "img": "boneless_4.jpg"},
        {"name": "12 Piece Strips", "desc": "Crispy chicken boneless strips (12 pcs).", "price": 380, "img": "boneless_4.jpg"},
    ],

    "Hot & Crispy Chicken": [
        {"name": "1 Pc Hot & Crispy", "desc": "Single piece golden fried chicken.", "price": 110, "img": "hot1.jpg"},
        {"name": "2 Pc Hot & Crispy", "desc": "Two spicy crispy fried chicken pieces.", "price": 190, "img": "hot1.jpg"},
        {"name": "4 Pc Hot & Crispy", "desc": "Four-piece hot and crispy combo.", "price": 399, "img": "hot1.jpg"},
        {"name": "6 Pc Hot & Crispy", "desc": "Six-piece family fried chicken pack.", "price": 549, "img": "hot1.jpg"},
        {"name": "8 Pc Hot & Crispy", "desc": "Eight pieces of crunchy fried chicken.", "price": 749, "img": "hot1.jpg"},
        {"name": "10 Pc Hot & Crispy", "desc": "Ten pieces of ultimate crispy chicken.", "price": 849, "img": "hot1.jpg"},
    ],

    "Smoky Chicken": [
        {"name": "1 Pc Smoky Leg", "desc": "Grilled smoky chicken leg piece.", "price": 110, "img": "smoky1.jpg"},
        {"name": "2 Pc Smoky Leg", "desc": "Two pieces smoky chicken leg.", "price": 190, "img": "smoky1.jpg"},
        {"name": "4 Pc Smoky Leg", "desc": "Four grilled smoky chicken legs.", "price": 399, "img": "smoky1.jpg"},
        {"name": "8 Pc Smoky Leg", "desc": "Eight pieces smoky chicken legs combo.", "price": 749, "img": "smoky1.jpg"},
        {"name": "10 Pc Smoky Leg", "desc": "Ten smoky chicken legs feast.", "price": 849, "img": "smoky1.jpg"},
        {"name": "6 Pc Smoky Wings", "desc": "Six smoky chicken wings.", "price": 170, "img": "smoky2.jpg"},
        {"name": "6 Pc Smoky Boneless", "desc": "Six smoky boneless chicken bites.", "price": 210, "img": "smoky_boneless.jpg"},
    ],

    "Chicken Snacks & Fries": [
        {"name": "6 Pc Hot Wings", "desc": "Crispy hot chicken wings.", "price": 170, "img": "hot_wings6.jpg"},
        {"name": "12 Pc Hot Wings", "desc": "Dozen spicy chicken wings.", "price": 320, "img": "hot_wings6.jpg"},
        {"name": "Chicken Popcorn (M)", "desc": "Medium crispy chicken popcorn.", "price": 130, "img": "popcorn_m.jpg"},
        {"name": "Chicken Popcorn (L)", "desc": "Large bucket of chicken popcorn.", "price": 150, "img": "popcorn_l.jpg"},
        {"name": "Peri-Peri Fries (M)", "desc": "Spicy peri-peri fries (medium).", "price": 100, "img": "peri_m.jpg"},
        {"name": "Peri-Peri Fries (L)", "desc": "Spicy peri-peri fries (large).", "price": 120, "img": "peri_l.jpg"},
        {"name": "Loaded Fries", "desc": "Cheesy loaded fries with toppings.", "price": 200, "img": "loaded_fries.jpg"},
        {"name": "Loaded Chicken Popcorn", "desc": "Loaded popcorn with mayo and cheese.", "price": 250, "img": "loaded_popcorn.jpg"},
    ],
}

# ─────────────────────────────────────────────
# 🏠 HOME PAGE
# ─────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html', active_page='home')

# ─────────────────────────────────────────────
# 🍗 MENU PAGE
# ─────────────────────────────────────────────
@app.route('/menu')
def menu():
    ref = db.reference('comments')
    all_comments = ref.get() or {}
    avg_ratings = {}

    for item, comments in all_comments.items():
        ratings = [c['rating'] for c in comments.values() if 'rating' in c]
        avg_ratings[item] = round(sum(ratings) / len(ratings), 1) if ratings else 0

    return render_template('menu.html', menu_data=menu_data, avg_ratings=avg_ratings, active_page='menu')


# ─────────────────────────────────────────────
# 📞 CONTACT PAGE
# ─────────────────────────────────────────────
@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')

# ✔ STORE CONTACT FORM → FIRESTORE ONLY
# ✔ SEND EMAILS TO USER + OWNER
@app.route('/submit_event', methods=['POST'])
def submit_event():
    data = request.get_json()

    # Store in Firestore (not in realtime)
    firestore_db.collection("contact_form").add(data)
    print("📨 Contact Form Saved:", data)

    # Send emails
    try:
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        event_name = data.get("eventName")
        guests = data.get("guests")

        # Owner email
        msg_owner = Message(
            subject=f"📩 New Booking: {name}",
            recipients=["galennavernaveen@gmail.com"],
            body=f"New booking:\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nEvent: {event_name}\nGuests: {guests}"
        )
        mail.send(msg_owner)

        # User confirmation
        msg_user = Message(
            subject="🎉 Karnataka F.C - Booking Received",
            recipients=[email],
            body=f"Hi {name},\n\nWe received your booking for '{event_name}'. We will contact you soon!"
        )
        mail.send(msg_user)

    except Exception as e:
        print("⚠ Email Error:", e)

    return jsonify(success=True)


# ─────────────────────────────────────────────
# ⭐ COMMENT PAGE (Stored in REALTIME DB ONLY)
# ─────────────────────────────────────────────
@app.route('/comment')
def comment_page():
    item = request.args.get("item", "Unknown Item")
    ref = db.reference(f"comments/{item}")
    comments = ref.get() or {}
    comments_list = list(comments.values())

    avg_rating = 0
    if comments_list:
        avg_rating = round(sum(c['rating'] for c in comments_list) / len(comments_list), 1)

    return render_template("comment.html", item=item, comments=comments_list, avg_rating=avg_rating)


@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    data = request.get_json()
    item = data.get("item")
    name = data.get("name")
    comment = data.get("comment")
    rating = int(data.get("rating", 0))

    # Store in **Realtime Database only**
    ref = db.reference(f"comments/{item}")
    ref.push({
        "name": name,
        "comment": comment,
        "rating": rating
    })

    return jsonify(success=True)


# ─────────────────────────────────────────────
# 🚀 RUN APP
# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
