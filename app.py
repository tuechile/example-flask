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
        personal_websites = ["afvs", "essays", "fysemr", "illustration", "portal", "street", "superface"] 
        collab_websites = ["highlander", "recit", "olympics", "gifafvs"]
        flat = ["about", "client", "collab", "personal"]
        # Add valid template names
        if finder.lower() in flat:
            return render_template(f"{finder}.html")
        elif finder.lower() in personal_websites:
            return render_template(f"personal websites/{finder}.html")
        elif finder.lower() in collab_websites:
            return render_template(f"collab websites/{finder}.html")
        
        elif finder.lower() in ["chi", "pirenily", "me", "chi le", "emily", "iron pig", "chi bell", "myself", "i", "artist"]:
            return render_template("about.html")
        elif finder.lower() in ["commission", "client work", "commissioned work", "commissions", "client"]:
            return render_template("client.html")
        elif finder.lower() in ["collaborative work", "collaborations", "collaboration", "member", "film", "direction", "director", "collab"]:
            return render_template("collab.html")
        elif finder.lower() in ["personal work", "self", "person", "mine", "free", "journey"]:
            return render_template("personal.html")
        
        else:
            finder = random.choice(personal_websites + collab_websites + flat)
            # Abort with a 404 error if the template is not allowed
            if finder in personal_websites:
                return render_template(f"personal websites/{finder}.html")
            elif finder in collab_websites:
                return render_template(f"collab websites/{finder}.html")
            else:
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
    return render_template("personal websites/illustration.html")


@app.route("/portal")
def portal():
    return render_template("personal websites/portal.html")

@app.route("/street")
def street():
    return render_template("personal websites/street.html")

@app.route("/superface")
def superface():
    return render_template("personal websites/superface.html")

@app.route("/afvs")
def afvs():
    return render_template("personal websites/afvs.html")

@app.route("/gifafvs")
def gifafvs():
    return render_template("personal websites/gifafvs.html")

@app.route("/fysemr")
def fysemr():
    return render_template("personal websites/fysemr.html")

@app.route("/essays")
def essays():
    return render_template("personal websites/essays.html")

@app.route("/highlander")
def highlander():
    return render_template("collab websites/highlander.html")

@app.route("/recit")
def recit():
    return render_template("collab websites/recit.html")

@app.route("/olympics")
def olympics():
    return render_template("collab websites/olympics.html")

if __name__ == "__main__":
    app.run(debug=True)
