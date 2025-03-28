from flask_restful import Resource
from flask import request
from transits import find_transits, get_daily_transit_report, find_upcoming_transits

class TransitTodayResource(Resource):
    def get(self):
        natal = request.args.get("natal")
        date = request.args.get("date")
        lat = request.args.get("lat", "0.0")
        lng = request.args.get("lng", "0.0")
        orb = float(request.args.get("orb", 2.0))

        if not natal or not date:
            return {"error": "Missing required parameters: 'natal' and 'date'"}, 400

        transits = find_transits(natal, date, lat, lng, orb)
        return {"transits": transits}


class TransitReportResource(Resource):
    def get(self):
        natal = request.args.get("natal")
        date = request.args.get("date")
        lat = request.args.get("lat", "0.0")
        lng = request.args.get("lng", "0.0")
        orb = float(request.args.get("orb", 2.0))

        if not natal or not date:
            return {"error": "Missing required parameters: 'natal' and 'date'"}, 400

        report = get_daily_transit_report(natal, date, lat, lng, orb)
        return {"report": report}


class TransitUpcomingResource(Resource):
    def get(self):
        natal = request.args.get("natal")
        start = request.args.get("start")
        lat = request.args.get("lat", "0.0")
        lng = request.args.get("lng", "0.0")
        orb = float(request.args.get("orb", 2.0))
        days = int(request.args.get("days", 30))

        if not natal or not start:
            return {"error": "Missing required parameters: 'natal' and 'start'"}, 400

        transits = find_upcoming_transits(natal, datetime.fromisoformat(start), lat, lng, days, orb)
        return {"upcoming_transits": transits}
