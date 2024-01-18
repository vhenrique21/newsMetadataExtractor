import json

from flask import Flask, Response, request

from execute import Execute

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/extract", methods=["POST"])
def extract_with_template():
    body = request.get_json()

    url = str(body.get("url"))
    template: str | None = (
        json.dumps(body.get("template")) if body.get("template") else None
    )

    output = Execute().run(url, template)

    print(body)
    return Response(json.dumps(output), mimetype="application/json"), 200


@app.route("/extract", methods=["GET"])
def extract():
    url = str(request.args.get("url"))
    output = Execute().run(url, None)
    return Response(json.dumps(output), mimetype="application/json"), 200
