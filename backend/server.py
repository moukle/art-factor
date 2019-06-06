from flask import render_template
from flask_cors import CORS
import connexion
import settings

app = connexion.App(__name__, specification_dir="./")
CORS(app.app)
app.add_api("swagger.yml")

@app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=False)