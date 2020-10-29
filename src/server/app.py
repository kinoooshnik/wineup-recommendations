from flask import Flask, request, Response, json, jsonify

app = Flask(__name__)


@app.route("/recommendations", methods=["GET"])
def recommendations_api():
    if request.args and request.args.get("user_id").isnumeric():
        user_id = request.args.get("user_id")
        example = {"wine_id": "[1, 2, 3]"}
        return Response(json.dumps(example), status=200, mimetype="application/json")
    return Response(status=400)


@app.route("/rating", methods=["PUT"])
def rating_api():
    if request.json:
        data = request.json
        if (
            "user_id" not in data
            or "wine_id" not in data
            or "rating" not in data
            or "variants" not in data
        ):
            return Response(status=400)
        return Response(
            json.dumps({"status": "ok"}), status=200, mimetype="application/json"
        )
    return Response(status=400)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
