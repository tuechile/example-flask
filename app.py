from flask import Flask, render_template, request
import random

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        # Get the user input from the form
        finder = request.form.get("finder")

        # Validate the input against allowed templates (the exact names and similar names)
        allowed_templates = ["about", "client", "collab", "personal", "street", "olympics",
                             "highlander", "illustration", "recit", "superface"]  # Add valid template names
        if finder.lower() in allowed_templates:
            return render_template(f"{finder}.html")
        elif finder.lower() in ["chi", "pirenily", "me", "chi le", "emily", "iron pig", "chi bell", "myself", "i", "artist"]:
            return render_template("about.html")
        elif finder.lower() in ["commission", "client work", "commissioned work", "commissions", "client"]:
            return render_template("client.html")
        elif finder.lower() in ["collaborative work", "collaborations", "collaboration", "member", "film", "direction", "director"]:
            return render_template("collab.html")
        elif finder.lower() in ["personal work", "self", "person", "mine", "free", "journey"]:
            return render_template("personal.html")
        else:
            allowed_templates = ["about", "client", "collab", "personal",
                                 "illustration", "portal", "recit", "street"]  # Add valid template names
            finder = random.choice(allowed_templates)
            # Abort with a 404 error if the template is not allowed
            return render_template(f"{finder}.html")

# Generate template for each html page


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/client")
def client():
    return render_template("client.html")


@app.route("/personal")
def personal():
    return render_template("personal.html")


@app.route("/collab")
def collab():
    return render_template("collab.html")


@app.route("/illustration")
def illustration():
    return render_template("illustration.html")


@app.route("/portal")
def portal():
    return render_template("portal.html")


@app.route("/recit")
def recit():
    return render_template("recit.html")


@app.route("/street")
def street():
    return render_template("street.html")


@app.route("/highlander")
def highlander():
    return render_template("highlander.html")


@app.route("/superface")
def superface():
    return render_template("superface.html")


@app.route("/olympics")
def olympics():
    return render_template("olympics.html")


@app.route("/afvs")
def afvs():
    return render_template("afvs.html")

@app.route("/fysemr")
def fysemr():
    return render_template("fysemr.html")

@app.route("/essays")
def essays():
    return render_template("essays.html")


if __name__ == "__main__":
    app.run(debug=True)
