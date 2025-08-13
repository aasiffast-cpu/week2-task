from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-to-a-random-secret"

@app.route("/")
def home():
   
    return redirect(url_for("contact"))

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
      
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

      
        errors = []
        if not username:
            errors.append("Name is required.")
        if not email:
            errors.append("Email is required.")
        if not message:
            errors.append("Message is required.")

        if errors:
      
            for e in errors:
                flash(e, "danger")
            return redirect(url_for("contact"))

       
        msgs = session.get("messages", [])
        msgs.append({"username": username, "email": email, "message": message})
        session["messages"] = msgs

       
        flash("Your message was received. Thank you!", "success")
        return redirect(url_for("messages"))


    return render_template("contact.html")

@app.route("/messages", methods=["GET"])
def messages():
    msgs = session.get("messages", [])
    return render_template("messages.html", messages=msgs)

@app.route("/clear", methods=["POST"])
def clear():
  
    session.pop("messages", None)
    flash("All messages cleared.", "info")
    return redirect(url_for("messages"))

if __name__ == "__main__":
    app.run(debug=True)
