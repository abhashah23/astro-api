from flask import Flask
from flask_restful import Api
from resources import (
    TransitTodayResource,
    TransitReportResource,
    TransitUpcomingResource,
    NatalChartResource
)

app = Flask(__name__)
api = Api(app)

# Health check
@app.route("/")
def home():
    return "Astrology API is live!"

# Register API endpoints
api.add_resource(TransitTodayResource, "/transits")
api.add_resource(TransitReportResource, "/transits/report")
api.add_resource(TransitUpcomingResource, "/transits/upcoming")
api.add_resource(NatalChartResource, "/natal/chart")

# Run server
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
