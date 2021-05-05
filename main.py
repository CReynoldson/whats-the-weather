from app import app 

@app.route("/")
def the_root():
    return "I am Root"

if __name__ == "__main__":
    app.run(debug=True)