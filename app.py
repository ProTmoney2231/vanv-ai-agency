import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY","super-secret-key")
AGENCY_NAME = os.getenv("AGENCY_NAME","Vanv AI Agency")
BOOK_DEMO_URL = os.getenv("BOOK_DEMO_URL","")
OWNER_EMAIL = os.getenv("OWNER_EMAIL","you@example.com")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY","")
STRIPE_MONTHLY_URL = os.getenv("STRIPE_MONTHLY_URL","")
STRIPE_HYBRID_URL  = os.getenv("STRIPE_HYBRID_URL","")
def send_lead(name,email,phone,company,message):
    if not SENDGRID_API_KEY: return False,"SendGrid key missing"
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        body=f"New Lead\\nName:{name}\\nEmail:{email}\\nPhone:{phone}\\nCompany:{company}\\n\\n{message}"
        m=Mail(from_email=("leads@vanvaiagency.com","Website Lead"),to_emails=[OWNER_EMAIL],subject="[Vanv AI] New Lead",plain_text_content=body)
        SendGridAPIClient(SENDGRID_API_KEY).send(m); return True,"ok"
    except Exception as e: return False,str(e)
@app.route("/")
def home(): return render_template("index.html",
    AGENCY_NAME=AGENCY_NAME,BOOK_DEMO_URL=BOOK_DEMO_URL,
    STRIPE_MONTHLY_URL=STRIPE_MONTHLY_URL,STRIPE_HYBRID_URL=STRIPE_HYBRID_URL)
@app.route("/lead",methods=["POST"])
def lead():
    f=request.form; ok,info=send_lead(f.get("name",""),f.get("email",""),f.get("phone",""),f.get("company",""),f.get("message",""))
    flash("Thanks! We received your info." if ok else f"Lead send failed: {info}","success" if ok else "error")
    return redirect(url_for("home")+"#lead")
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT",5000)),debug=True)

# ------------------------
# Privacy & Terms routes
# ------------------------
from flask import render_template

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")
