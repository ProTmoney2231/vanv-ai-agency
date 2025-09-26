import os
from flask import Flask, render_template

app = Flask(__name__)

OWNER_EMAIL = os.getenv("OWNER_EMAIL", "vanvaiagency@gmail.com")
MONTHLY_URL = os.getenv("STRIPE_MONTHLY_URL", "#")
HYBRID_URL  = os.getenv("STRIPE_HYBRID_URL",  "#")
BOOK_DEMO_URL = os.getenv("BOOK_DEMO_URL", "mailto:" + OWNER_EMAIL)

@app.route("/")
def index():
    return render_template("index.html",
        monthly_url=MONTHLY_URL, hybrid_url=HYBRID_URL, book_demo_url=BOOK_DEMO_URL)

@app.route("/pricing")
def pricing():
    return render_template("pricing.html",
        monthly_url=MONTHLY_URL, hybrid_url=HYBRID_URL)

@app.route("/privacy")
def privacy():
    return render_template("privacy.html", owner_email=OWNER_EMAIL)

@app.route("/terms")
def terms():
    return render_template("terms.html", owner_email=OWNER_EMAIL)

@app.route("/_healthz")
def healthz():
    return "ok", 200

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
