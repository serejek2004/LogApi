from datetime import datetime
from flask import request, jsonify
from app.log.service import LogService
from app import app, db
from flask_jwt_extended import jwt_required

LogService = LogService(db)


@app.route('/logs', methods=['POST'])
@jwt_required()
def upload_log_file():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "File not provided"}), 400

    response, status_code = LogService.process_file(file)

    return jsonify(response), status_code


@app.route('/logs', methods=['GET'])
@jwt_required()
def get_all_logs():
    logs = LogService.get_all()
    return jsonify(logs), 200


def parse_datetime(date_str: str) -> datetime | None:
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None


@app.route('/logs/<string:start_datetime>/<string:end_datetime>')
@jwt_required()
def get_logs_by_time(start_datetime: str, end_datetime: str):
    start_date = parse_datetime(start_datetime)
    end_date = parse_datetime(end_datetime)

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DDTHH:MM:SS'"}), 400

    logs = LogService.get_logs_by_time(start_date, end_date)
    return jsonify(logs), 200


@app.route('/logs/<fragment>')
@jwt_required()
def get_logs_by_fragment(fragment: str):
    logs = LogService.get_logs_by_fragment(fragment)
    return jsonify(logs), 200


@app.route('/logs/<string:fragment>/<string:start_datetime>/<string:end_datetime>')
@jwt_required()
def get_logs_by_fragment_and_by_time(fragment: str, start_datetime: str, end_datetime: str):
    start_date = parse_datetime(start_datetime)
    end_date = parse_datetime(end_datetime)

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DDTHH:MM:SS'"}), 400

    logs = LogService.get_logs_by_fragment_and_by_time(fragment, start_date, end_date)

    return jsonify(logs), 200
