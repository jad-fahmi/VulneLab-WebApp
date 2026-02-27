from flask import Flask, request, render_template, Markup

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "")
    result = Markup(query) if query else None
    return render_template("search.html", query=query, result=result)

if __name__ == "__main__":
    app.run(port=5005, debug=True)