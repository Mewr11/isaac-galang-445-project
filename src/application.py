
from flask import Flask, request
from flask_restful import Resource, Api
import api
from simpledataholder import SimpleDataHolder

app = Flask(__name__)
api_server = Api(app)
ds = SimpleDataHolder()

class Accounts(Resource):
    def post(self):
        return api.createAccount(ds, request.get_json())

    def get(self):
        key = request.args.get("key", "")
        if(key == ""):
            return api.getAllAccounts(ds)
        else:
            return api.searchAccounts(ds, key)

class AccountStatus(Resource):
    def put(self, aid):
        return api.activateAccount(ds, request.get_json(), aid)

class AccountAID(Resource):
    def put(self, aid):
        return api.updateAccount(ds, request.get_json(), aid)

    def delete(self, aid):
        return api.deleteAccount(ds, aid)

    def get(self, aid):
        return api.getAccountDetail(ds, aid)

class Ratings(Resource):
    def post(self, aid):
        return api.rate(ds, request.get_json(), aid)

class DriverRatings(Resource):
    def get(self, aid):
        return api.viewDriverRatings(ds, aid)

class RiderRatings(Resource):
    def get(self, aid):
        return api.viewRiderRatings(ds, aid)

class Rides(Resource):
    def post(self):
        return api.createRide(ds, request.get_json())

    def get(self):
        fromKey = request.args.get("fromKey", "")
        toKey = request.args.get("toKey", "")
        date = request.args.get("departure_date", "")
        if(fromKey == "" and toKey == "" and date == ""):
            return api.viewAllRides(ds)
        else:
            return api.searchRides(ds, fromKey, toKey, date)

class RideRID(Resource):
    def put(self, rid):
        return api.updateRide(ds, request.get_json(), rid)

    def delete(self, rid):
        return api.deleteRide(ds, rid)

    def get(self, rid):
        return api.viewRideDetail(ds, rid)

class JoinRequests(Resource):
    def post(self, rid):
        return api.createJoinRequest(ds, request.get_json(), rid)

class JoinRequestJID(Resource):
    def patch(self, rid, jid):
        keys = list(request.get_json().keys())
        if("ride_confirmed" in keys):
            return api.confirmJoinRequest(ds, request.get_json(), rid, jid)
        elif("pickup_confirmed" in keys):
            return api.confirmPickup(ds, request.get_json(), rid, jid)

class Messages(Resource):
    def post(self, rid):
        return api.addMessage(ds, request.get_json(), rid)

    def get(self, rid):
        return api.viewAllRideMessages(ds, rid)

class Reports(Resource):
    def get(self):
        return api.viewAllReports()

class ReportPID(Resource):
    def get(self, pid):
        return api.getReport(ds, pid)

api_server.add_resource(Accounts,
                        "/sar/accounts")
api_server.add_resource(AccountAID,
                        "/sar/accounts/<int:aid>")
api_server.add_resource(DriverRatings,
                        "/sar/accounts/<int:aid>/driver")
api_server.add_resource(Ratings,
                        "/sar/accounts/<int:aid>/ratings")
api_server.add_resource(RiderRatings,
                        "/sar/accounts/<int:aid>/rider")
api_server.add_resource(AccountStatus,
                        "/sar/accounts/<int:aid>/status")
api_server.add_resource(Reports,
                        "/sar/reports")
api_server.add_resource(ReportPID,
                        "/sar/reports/<int:pid>")
api_server.add_resource(Rides,
                        "/sar/rides")
api_server.add_resource(RideRID,
                        "/sar/rides/<int:rid>")
api_server.add_resource(JoinRequests,
                        "/sar/rides/<int:rid>/join_requests")
api_server.add_resource(JoinRequestJID,
                        "/sar/rides/<int:rid>/join_requests/<int:jid>")
api_server.add_resource(Messages,
                        "/sar/rides/<int:rid>/messages")

if __name__ == '__main__':
    app.run(port=8080)
