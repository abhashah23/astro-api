from flask import Flask
from flask_restful import Api
from resources import TransitTodayResource, TransitReportResource, TransitUpcomingResource

app = Flask(__name__)
api = Api(app)

# Health check
@app.route("/")
def home():
    return "Astrology API is live!"

# API endpoints
api.add_resource(TransitTodayResource, "/transits")
api.add_resource(TransitReportResource, "/transits/report")
api.add_resource(TransitUpcomingResource, "/transits/upcoming")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
