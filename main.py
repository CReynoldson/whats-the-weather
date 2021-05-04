from flask import Flask 
from api.v1.routes import v1_api

app = Flask(__name__)
app.register_blueprint(v1_api)

@app.route("/")
def the_root():
    return "I am Root"


if __name__ == "__main__":
    app.run(debug=True)