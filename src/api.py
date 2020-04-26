
import time
import validation
import account
import ride
import math

def dataValidationError(detail, instance):
    return {
        "type": "http://cs.iit.edu/~virgil/cs445/project/api/problems/data-validation",
        "title": "Your request data didn't pass validation",
        "detail": detail,
        "status": 400,
        "instance": instance
        }, 400

def createAccount(ds, form):
    if(form is None):
        return dataValidationError("No Data",
                                   "/accounts")
    firstName = form.get("first_name")
    lastName = form.get("last_name")
    phone = form.get("phone")
    picture = form.get("picture")
    isActive = form.get("is_active")
    if(firstName is None or lastName is None or phone is None or
       picture is None):
        return dataValidationError("Missing data",
                                   "/accounts")
    if(not validation.name(firstName)):
        return dataValidationError("The first name appears to be invalid.",
                                   "/accounts")
    if(not validation.name(lastName)):
        return dataValidationError("The last name appears to be invalid.",
                                   "/accounts")
    if(not validation.phoneNumber(phone)):
        return dataValidationError("Invalid phone number",
                                   "/accounts")
    if(isActive):
        return dataValidationError("Invalid value for is_active",
                                   "/accounts")
    date = time.strftime("%d-%b-%Y", time.gmtime())
    a = account.Account(firstName, lastName, phone, picture, date)
    aid = ds.addAccount(a)
    return ({"aid": aid}, 201, {"Location": "/accounts/%d" % aid})

def activateAccount(ds, form, aid):
    a = ds.getAccount(aid)
    if(a is None):
        return {}, 404
    if(form is None):
        return dataValidationError("No Data",
                                   "/accounts/%d/status" % aid)
    firstName = form.get("first_name")
    lastName = form.get("last_name")
    phone = form.get("phone")
    picture = form.get("picture")
    isActive = form.get("is_active")
    if(firstName is None or lastName is None or phone is None or
       picture is None or isActive is None):
        return dataValidationError("Missing data",
                                   "/accounts/%d/status" % aid)
    if(firstName != a.firstName):
        return dataValidationError("The first name appears to be invalid.",
                                   "/accounts/%d/status" % aid)
    if(lastName != a.lastName):
        return dataValidationError("The last name appears to be invalid.",
                                   "/accounts/%d/status" % aid)
    if(phone != a.phone):
        return dataValidationError("Invalid phone number",
                                   "/accounts/%d/status" % aid)
    if(picture != a.picture):
        return dataValidationError("Invalid picture",
                                   "/accounts/%d/status" % aid)
    if(not isActive):
        return dataValidationError("Invalid value for is_active",
                                   "/accounts/%d/status" % aid)
    a.activate()
    return {}, 204

def updateAccount(ds, form, aid):
    a = ds.getAccount(aid)
    if(a is None):
        return {}, 404
    if(form is None):
        return dataValidationError("No Data",
                                   "/accounts/%d" % aid)
    firstName = form.get("first_name")
    lastName = form.get("last_name")
    phone = form.get("phone")
    picture = form.get("picture")
    isActive = form.get("is_active")
    if(firstName is None or lastName is None or phone is None or
       picture is None or isActive is None):
        return dataValidationError("Missing data",
                                   "/accounts/%d" % aid)
    if(not validation.name(firstName)):
        return dataValidationError("The first name appears to be invalid.",
                                   "/accounts/%d" % aid)
    if(not validation.name(lastName)):
        return dataValidationError("The last name appears to be invalid.",
                                   "/accounts/%d" % aid)
    if(not validation.phoneNumber(phone)):
        return dataValidationError("Invalid phone number",
                                   "/accounts/%d" % aid)
    if(isActive):
        return dataValidationError("Invalid value for is_active",
                                   "/accounts/%d" % aid)
    a.update(firstName, lastName, phone, picture)
    return {}, 204

def deleteAccount(ds, aid):
    if(ds.getAccount(aid) is None):
        return {}, 404
    ds.deleteAccount(aid)
    return {}, 204

def getAllAccounts(ds):
    return [{
        "aid": a[0],
        "name": a[1].firstName + " " + a[1].lastName,
        "date_created": a[1].dateCreated,
        "is_active": a[1].isActive
        }
            for a in ds.getAllAccounts()], 200

def getAccountDetail(ds, aid):
    return {}, 501

def searchAccounts(ds, key):
    return [{
        "aid": a[0],
        "name": a[1].firstName + " " + a[1].lastName,
        "date_created": a[1].dateCreated,
        "is_active": a[1].isActive
        }
            for a in ds.searchAccounts(key)], 200

def createRide(ds, form):
    if(form is None):
        return dataValidationError("No Data",
                                   "/rides")
    aid = form.get("aid", None)
    locationInfo = form.get("location_info", None)
    dateTime = form.get("date_time", None)
    carInfo = form.get("car_info", None)
    passengers = form.get("max_passengers", None)
    fare = form.get("amount_per_passenger", None)
    conditions = form.get("conditions", None)
    
    if(aid is None or locationInfo is None or dateTime is None or
       carInfo is None or passengers is None or fare is None or
       conditions is None):
        return dataValidationError("Missing data",
                                   "/rides")
    
    fromCity = locationInfo.get("from_city")
    fromZip = locationInfo.get("from_zip", "")
    toCity = locationInfo.get("to_city")
    toZip = locationInfo.get("to_zip", "")
    departureDate = dateTime.get("date")
    departureTime = dateTime.get("time")
    make = carInfo.get("make")
    model = carInfo.get("model")
    color = carInfo.get("color")
    plateState = carInfo.get("plate_state")
    plateNumber = carInfo.get("plate_serial")
    
    if(fromCity is None or toCity is None or departureDate is None or
       time is None or make is None or model is None or plateState is None
       or plateNumber is None or color is None):
        return dataValidationError("Missing data",
                                    "/rides")

    if(not validation.zip(fromZip) or
       not validation.zip(toZip)):
        return dataValidationError("Invalid zip code",
                                   "/rides")
    if(not validation.state(plateState)):
        return dataValidationError("Invalid state code",
                                   "/rides")
    if(not validation.date(departureDate)):
        return dataValidationError("Invalid date",
                                   "/rides")
    if(not validation.time(departureTime)):
        return dataValidationError("Invalid time",
                                   "/rides")
    
    date = time.strftime("%d-%b-%Y", time.gmtime())
    driver = ds.getAccount(aid)

    if(driver is None):
        return dataValidationError("Invalid aid",
                                   "/rides")
    if(not driver.isActive):
        return dataValidationError("This account (%d) is not active, may not create a ride." % form["aid"],
                                   "/rides")
    
    r = ride.Ride(fromCity, fromZip, toCity, toZip,
                  departureDate, departureTime,
                  make, model, color, plateState, plateNumber,
                  passengers, fare, conditions,
                  driver, date)

    rid = ds.addRide(r)
    
    return ({"rid": rid}, 201, {"Location": "/rides/%d" % rid})

def updateRide(ds, form, rid):
    if(form is None):
        return dataValidationError("No Data",
                                   "/rides/%d" % rid)
    
    aid = form.get("aid", None)
    locationInfo = form.get("location_info", None)
    dateTime = form.get("date_time", None)
    carInfo = form.get("car_info", None)
    passengers = form.get("max_passengers", None)
    fare = form.get("amount_per_passenger", None)
    conditions = form.get("conditions", None)
    
    if(aid is None or locationInfo is None or dateTime is None or
       carInfo is None or passengers is None or fare is None or
       conditions is None):
        return dataValidationError("Missing data",
                                   "/rides")
    
    fromCity = locationInfo.get("from_city")
    fromZip = locationInfo.get("from_zip", "")
    toCity = locationInfo.get("to_city")
    toZip = locationInfo.get("to_zip", "")
    departureDate = dateTime.get("date")
    departureTime = dateTime.get("time")
    make = carInfo.get("make")
    model = carInfo.get("model")
    color = carInfo.get("color")
    plateState = carInfo.get("plate_state")
    plateNumber = carInfo.get("plate_serial")
    
    if(fromCity is None or toCity is None or departureDate is None or
       time is None or make is None or model is None or plateState is None
       or plateNumber is None or color is None):
        return dataValidationError("Missing data",
                                    "/rides")

    if(not validation.zip(fromZip) or not validation.zip(toZip)):
        return dataValidationError("Invalid zip code",
                                   "/rides/%d" % rid)
    if(not validation.state(plateState)):
        return dataValidationError("Invalid state code",
                                   "/rides/%d" % rid)
    if(not validation.date(departureDate)):
        return dataValidationError("Invalid date",
                                   "/rides/%d" % rid)
    if(not validation.time(departureTime)):
        return dataValidationError("Invalid time",
                                   "/rides/%d" % rid)
    r = ds.getRide(rid)

    if(r is None):
        return {}, 404
    
    driver = r.driver
    updater = ds.getAccount(aid)

    if(driver != updater):
        return dataValidationError("Only the creator of the ride may change it",
                                   "/rides/%d" % rid)

    r.update(fromCity, fromZip, toCity, toZip,
             departureDate, departureTime,
             make, model, color, plateState, plateNumber,
             passengers, fare, conditions)
    return {}, 204

def deleteRide(ds, rid):
    if(ds.getRide(rid) is None):
        return {}, 404
    ds.deleteRide(rid)
    return {}, 204

def viewAllRides(ds):
    return [{
        "rid": r[0],
        "location_info": {
            "from_city": r[1].fromCity,
            "from_zip": r[1].fromZip,
            "to_city": r[1].toCity,
            "to_zip": r[1].toZip
            },
        "date_time": {
            "date": r[1].date,
            "time": r[1].time
            }
        }for r in ds.getAllRides()], 200

def searchRides(ds, fromKey, toKey, date):
    return [{
        "rid": r[0],
        "location_info": {
            "from_city": r[1].fromCity,
            "from_zip": r[1].fromZip,
            "to_city": r[1].toCity,
            "to_zip": r[1].toZip
            },
        "date_time": {
            "date": r[1].date,
            "time": r[1].time
            }
        }for r in ds.searchRide(fromKey, toKey, date)], 200

def createJoinRequest(ds, form, rid):
    r = ds.getRide(rid)
    if(r is None):
        return {}, 404
    if(form is None):
        return dataValidationError("No Data",
                                   "/rides/%d/join_requests" % rid)
    aid = form.get("aid")
    passengers = form.get("passengers")
    rideConfirmed = form.get("ride_confirmed")
    pickupConfirmed = form.get("pickup_confirmed")
    
    if(aid is None or passengers is None):
        return dataValidationError("Missing data",
                                   "/rides/%d/join_requests" % rid)
    if(rideConfirmed is not None):
        return dataValidationError("Invalid value for ride_confirmed",
                                   "/rides/%d/join_requests" % rid)
    if(pickupConfirmed is not None):
        return dataValidationError("Invalid value for pickup_confirmed",
                                   "/rides/%d/join_requests" % rid)
    a = ds.getAccount(aid)
    if(a is None):
        return dataValidationError("Invalid aid",
                                   "/rides/%d/join_requests" % rid)
    if(not a.isActive):
        return dataValidationError("This account (%d) is not active, may not create a join ride request." % form["aid"],
                                   "/rides/%d/join_requests" % rid)
    jid = ds.addJoinRequest(rid, a, passengers)
    return ({"jid": jid}, 201,
            {"Location": "/rides/%d/join_requests/%d" % (rid, jid)})

def confirmJoinRequest(ds, form, rid, jid):
    if(form is None):
        return dataValidationError("No Data",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    r = ds.getRide(rid)
    if(r is None):
        return {}, 404
    j = ds.getJoinRequest(jid)
    if(j is None):
        return {}, 404
    aid = form.get("aid")
    rideConfirmed = form.get("ride_confirmed")
    if(aid is None or rideConfirmed is None):
        return dataValidationError("Missing Data",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(rideConfirmed not in [True, False]):
        return dataValidationError("Invalid value for ride_confirmed",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    a = ds.getAccount(aid)
    if(a != r.driver):
        return dataValidationError("This account (%d) didn't create the ride (%d)" % (form["aid"], rid),
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(j[0] != r):
        return dataValidationError("Invalid jid",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(rideConfirmed):
        r.confirmJoinRequest(j[1])
    else:
        r.denyJoinRequest(j[1])
    return {}, 200

def confirmPickup(ds, form, rid, jid):
    r = ds.getRide(rid)
    if(r is None):
        return {}, 404
    j = ds.getJoinRequest(jid)
    if(j is None):
        return {}, 404
    if(form is None):
        return dataValidationError("No Data",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    aid = form.get("aid")
    pickupConfirmed = form.get("pickup_confirmed")
    if(aid is None or pickupConfirmed is None):
        return dataValidationError("Missing Data",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(pickupConfirmed != True):
        return dataValidationError("Invalid value for pickup_confirmed",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(j[0] != r):
        return dataValidationError("Invalid jid",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    a = ds.getAccount(aid)
    if(a != r.joinRequests[j[1]].rider):
        return dataValidationError("This account (%d) has not requested to join this ride (%d)" % (form["aid"], rid),
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(not r.joinRequests[j[1]].confirmed):
        return dataValidationError("This join request has not been accepted",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    r.confirmPickup(j[1])
    return {}, 200

def addMessage(ds, form, rid):
    r = ds.getRide(rid)
    if(r is None):
        return {}, 404
    if(form is None):
        return dataValidationError("No Data",
                                   "/rides/%d/messages" % rid)
    aid = form.get("aid")
    msg = form.get("msg")
    if(aid is None or msg is None):
        return dataValidationError("Missing data",
                                   "/rides/%d/messages" % rid)
    a = ds.getAccount(aid)
    if(a is None):
        return dataValidationError("Invalid aid",
                                   "/rides/%d/messages" % rid)
    if(not a.isActive):
        return dataValidationError("Account is not active",
                                   "/rides/%d/messages" % rid)
    date = time.strftime("%d-%b-%Y", time.gmtime())
    mid = ds.addMessage(rid, aid, msg, date)
    return ({"mid": mid}, 201,
            {"Location": "/rides/%d/messages/%d" % (rid, mid)})

def viewAllRideMessages(ds, rid):
    r = ds.getRide(rid)
    if(r is None):
        return {}, 404
    msgs = ds.getMessages(rid)
    return [{
        "mid": m[0],
        "sent_by_aid": m[1],
        "date": r.messages[m[2]].date,
        "body": r.messages[m[2]].message
        }
            for m in msgs], 200

def rate(ds, form, aid):
    a = ds.getAccount(aid)
    if(a is None):
        return {}, 404
    if(form is None):
        return dataValidationError("No Data",
                                   "/accounts/%d/ratings" % aid)
    rid = form.get("rid")
    senderID = form.get("sent_by_id")
    rating = form.get("rating")
    comment = form.get("comment")
    if(rid is None or senderID is None or rating is None or comment is None):
        return dataValidationError("Missing data",
                                   "/accounts/%d/ratings" % aid)
    r = ds.getRide(rid)
    if(r is None):
        return dataValidationError("Invalid rid",
                                   "/accounts/%d/ratings" % aid)
    if(rating < 1 or rating > 5):
        return dataValidationError("Invalid rating",
                                   "/accounts/%d/ratings" % aid)
    s = ds.getAccount(senderID)
    if(s is None):
        return dataValidationError("Invalid sent_by_id",
                                   "/accounts/%d/ratings" % aid)
    date = time.strftime("%d-%b-%Y", time.gmtime())
    if(a == r.driver and s in r.riders):
        sid = ds.addDriverRating(aid, senderID, rid, rating, comment, date)
    elif(a in r.riders and s == r.driver):
        sid = ds.addRiderRating(aid, senderID, rid, rating, comment, date)
    else:
        return dataValidationError("This account (%d) didn't create this ride (%d) nor was it a passenger" % (form["sent_by_id"], form["rid"]),
                                   "/accounts/%d/ratings" % aid)
    return ({"sid": sid}, 201,
            {"Location": "/accounts/%d/ratings/%d" % (aid, sid)})

def viewDriverRatings(ds, aid):
    a = ds.getAccount(aid)
    if(a is None):
        return {}, 404
    details = [{
        "rid": r[2],
        "sent_by_id": r[1],
        "first_name": ds.getAccount(r[1]).firstName,
        "date": a.getDriverRatingDetail(r[3])[2],
        "rating": a.getDriverRatingDetail(r[3])[0],
        "comment": a.getDriverRatingDetail(r[3])[1]
        }
               for r in ds.getDriverRatings(aid)]
    return {
        "aid": aid,
        "first_name": a.firstName,
        "rides": a.drives,
        "ratings": len(a.driverRatings),
        "average_rating": a.getDriverRatingAverage(),
        "detail": details
        }, 200

def viewRiderRatings(ds, aid):
    a = ds.getAccount(aid)
    if(a is None):
        return {}, 404
    details = [{
        "rid": r[2],
        "sent_by_id": r[1],
        "first_name": ds.getAccount(r[1]).firstName,
        "date": a.getRiderRatingDetail(r[3])[2],
        "rating": a.getRiderRatingDetail(r[3])[0],
        "comment": a.getRiderRatingDetail(r[3])[1]
        }
               for r in ds.getRiderRatings(aid)]
    return {
        "aid": aid,
        "first_name": a.firstName,
        "rides": a.rides,
        "ratings": len(a.riderRatings),
        "average_rating": a.getRiderRatingAverage(),
        "detail": details
        }, 200

def viewRideDetail(ds, rid):
    r = ds.getRide(rid)
    if(r is None):
        return {}, 404
    for acc in ds.getAllAccounts():
        if(acc[1] == r.driver):
            aid = acc[0]
            break
    comments = [{
        "rid": rating[2],
        "date": r.driver.getDriverRatingDetail(rating[3])[2],
        "rating": r.driver.getDriverRatingDetail(rating[3])[0],
        "comment": r.driver.getDriverRatingDetail(rating[3])[1]
        }
                for rating in ds.getDriverRatings(aid)]
    return {
        "rid": rid,
        "location_info": {
            "from_city": r.fromCity,
            "from_zip": r.fromZip,
            "to_city": r.toCity,
            "to_zip": r.toZip
            },
        "date_time": {
            "date": r.date,
            "time": r.time,
            },
        "car_info": {
            "make": r.make,
            "model": r.model,
            "color": r.color,
            "plate_state": r.lpState,
            "plate_serial": r.lpNumber
            },
        "max_passengers": r.passengers,
        "amount_per_passenger": r.fare,
        "conditions": r.conditions,
        "driver": r.driver.firstName,
        "driver_picture": r.driver.picture,
        "rides": r.driver.drives,
        "ratings": len(r.driver.driverRatings),
        "average_rating": r.driver.getDriverRatingAverage(),
        "comments_about_driver": comments
        }, 200

def search(ds, key, start, end):
    return {}, 501

def viewAllReports():
    return ([{
        "pid": 0,
        "name": "Rides posted between two dates"
        },
             {
                 "pid": 1,
                 "name": "Rides taken between two dates"
                 }], 200)

def getReport(ds, pid, startDate, endDate):
    if(startDate == ""):
        startTime = 0
    else:
        startTime = time.mktime(time.strptime(startDate, "%d-%b-%Y"))
    if(endDate == ""):
        endTime = math.inf
    else:
        endTime = time.mktime(time.strptime(endDate, "%d-%b-%Y"))
    if(pid == 0):
        def isInRange(ride):
            date = time.mktime(time.strptime(ride.datePosted, "%d-%b-%Y"))
            return (startTime <= date and endTime >= date)
        name = "Rides posted between two dates"
    elif(pid == 1):
        def isInRange(ride):
            date = time.mktime(time.strptime(ride.date, "%d-%b-%Y"))
            return (startTime <= date and endTime >= date)
        name = "Rides taken between two dates"
    else:
            return dataValidationError("Invalid pid",
                                       "/reports/%d" % pid)
    report = []
    rides = 0
    for (_, ride) in ds.getAllRides():
        if(isInRange(ride)):
            rides += 1
            fromZip = ride.fromZip
            toZip = ride.toZip
            found = False
            for detail in report:
                if(detail["from_zip"] == fromZip and detail["to_zip"] == toZip):
                    detail["count"] += 1
                    found = True
            if(not found):
                report.append({
                    "from_zip": fromZip,
                    "to_zip": toZip,
                    "count": 1
                    })
        
    return {
        "pid": pid,
        "name": name,
        "start_date": startDate,
        "end_date": endDate,
        "rides": rides,
        "detail": report
        }, 200
