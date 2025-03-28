from flask import Flask
from flask_restful import Api
from resources import TransitTodayResource, TransitUpcomingResource, TransitReportResource

app = Flask(__name__)
api = Api(app)

api.add_resource(TransitTodayResource, "/transits")
api.add_resource(TransitUpcomingResource, "/transits/upcoming")
api.add_resource(TransitReportResource, "/transits/report")

@app.route("/")
def home():
    return "Astrology API is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
