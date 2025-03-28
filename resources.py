from flask_restful import Resource, reqparse
from flask import request
from transits import get_transits_today, get_transit_report, get_upcoming_transits
import logging

logger = logging.getLogger(__name__)

# =========================
# TRANSITS: Today
# =========================
class TransitTodayResource(Resource):
    def get(self):
        try:
            natal = request.args.get('natal')
            date = request.args.get('date')
            lat = request.args.get('lat', '0.0')
            lng = request.args.get('lng', '0.0')
            orb = float(request.args.get('orb', 1.0))

            if not natal or not date:
                return {"error": "Missing 'natal' or 'date' parameter"}, 400

            transits = get_transits_today(natal, date, lat, lng, orb)
            return {"transits": transits}

        except Exception as e:
            logger.error(f"TransitTodayResource Error: {str(e)}")
            return {"error": str(e)}, 500

# =========================
# TRANSITS: Report
# =========================
class TransitReportResource(Resource):
    def get(self):
        try:
            natal = request.args.get('natal')
            date = request.args.get('date')
            lat = request.args.get('lat', '0.0')
            lng = request.args.get('lng', '0.0')
            orb = float(request.args.get('orb', 1.0))

            if not natal or not date:
                return {"error": "Missing 'natal' or 'date' parameter"}, 400

            report = get_transit_report(natal, date, lat, lng, orb)
            return {"report": report}

        except Exception as e:
            logger.error(f"TransitReportResource Error: {str(e)}")
            return {"error": str(e)}, 500

# =========================
# TRANSITS: Upcoming
# =========================
class TransitUpcomingResource(Resource):
    def get(self):
        try:
            natal = request.args.get('natal')
            start = request.args.get('start')
            days = int(request.args.get('days', 30))
            lat = request.args.get('lat', '0.0')
            lng = request.args.get('lng', '0.0')
            orb = float(request.args.get('orb', 1.0))

            if not natal or not start:
                return {"error": "Missing 'natal' or 'start' parameter"}, 400

            upcoming = get_upcoming_transits(natal, start, lat, lng, orb, days)
            return {"upcoming": upcoming}

        except Exception as e:
            logger.error(f"TransitUpcomingResource Error: {str(e)}")
            return {"error": str(e)}, 500
