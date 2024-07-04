import json

from flask import Flask, request

from production_plan_calculator.services import production_service

app = Flask(__name__)


@app.route("/productionplan", methods=["POST"])
def production_plan():
    try:
        payload = json.loads(request.data)
        code = 200
        response = production_service.get_production_plan(payload)
    except Exception as exc:
        code = 400
        response = {"success": False, "message": str(exc)}

    return json.dumps(response), code
