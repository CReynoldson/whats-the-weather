from app import app 
environment = app.config.get("ENVIRONMENT")

@app.route("/")
def the_root():
    return "I am Root"

if __name__ == "__main__":
    if environment == "development":
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0")
