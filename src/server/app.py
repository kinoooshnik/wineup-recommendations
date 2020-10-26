from flask import Flask, request, Response, json, jsonify
app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/recommendations', methods=['GET'])
def recommendations_api():
    if request.args:
        if request.args.get("user_id").isnumeric():
            user_id = request.args.get("user_id")
            print("user_id =", user_id)
            example = {"wine_id": "1, 2, 3"}
            return Response(json.dumps(example), status=200, mimetype='application/json')
        else:
            return Response(status=400)
    return 'Recommendations Page'


@app.route('/rating', methods=['GET', 'PUT'])
def rating_api():
    if request.args:
        user_id = request.args.get("user_id")
        # if no user found return 401 error code
        wine_id = request.args.get("wine_id")
        # if no wine found return 402 error code
        rating = request.args.get("rating")
        variants = request.args.get("variants")
        if user_id and wine_id and rating and variants:
            example = {"user_id": user_id,
                       "wine_id": wine_id,
                       "rating": rating,
                       "variants": variants}
            return Response(json.dumps(example), status=200, mimetype='application/json')
        else:
            return Response(status=400)
    return 'Rating Page'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
