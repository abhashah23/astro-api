from flask_restful import Resource
from flask import request
from datetime import datetime
import logging

from transits import (
    get_daily_transit_report,
    find_upcoming_transits,
    get_natal_chart  # <-- Make sure this is in your transits.py
)

logger = logging.getLogger(__name__)

# =========================
# TRANSITS: Today
# =========================
class TransitTodayResource(Resource):
    def get(self):
        try:
            natal = request.args.get('natal')
            lat = request.args.get('lat', '0.0')
            lng = request.args.get('lng', '0.0')
            orb = float(request.args.get('orb', 2.0))

            if not natal:
                return {"error": "Missing 'natal' parameter"}, 400

            today = datetime.utcnow().isoformat()
            report = get_daily_transit_report(natal, today, lat, lng, orb)
            return {"date": today, "report": report}

        except Exception as e:
            logger.error(f"TransitTodayResource Error: {str(e)}")
            return {"error": str(e)}, 500

# =========================
# TRANSITS: Report (specific date)
# =========================
class TransitReportResource(Resource):
    def get(self):
        try:
            natal = request.args.get('natal')
            date = request.args.get('date')
            lat = request.args.get('lat', '0.0')
            lng = request.args.get('lng', '0.0')
            orb = float(request.args.get('orb', 2.0))

            if not natal or not date:
                return {"error": "Missing 'natal' or 'date' parameter"}, 400

            report = get_daily_transit_report(natal, date, lat, lng, orb)
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
            orb = float(request.args.get('orb', 2.0))

            if not natal or not start:
                return {"error": "Missing 'natal' or 'start' parameter"}, 400

            start_date = datetime.fromisoformat(start)
            upcoming = find_upcoming_transits(natal, start_date, lat, lng, days, orb)
            return {"start_date": start, "days": days, "transits": upcoming}

        except Exception as e:
            logger.error(f"TransitUpcomingResource Error: {str(e)}")
            return {"error": str(e)}, 500

# =========================
# NATAL CHART: Full chart with aspects and houses
# =========================
class NatalChartResource(Resource):
    def get(self):
        try:
            date = request.args.get("date")
            lat = request.args.get("lat")
            lng = request.args.get("lng")

            if not date or not lat or not lng:
                return {"error": "Missing 'date', 'lat', or 'lng' parameter"}, 400

            chart = get_natal_chart(date, lat, lng)
            return {"chart": chart}

        except Exception as e:
            logger.error(f"NatalChartResource Error: {str(e)}")
            return {"error": str(e)}, 500
