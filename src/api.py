
import time
import validation
import account
import ride

def dataValidationError(detail, instance):
    return {
        "type": "http://cs.iit.edu/~virgil/cs445/project/api/problems/data-validation",
        "title": "Your request data didn't pass validation",
        "detail": detail,
        "status": 400,
        "instance": instance
        }, 400

def createAccount(ds, form):
    keys = list(form.keys())
    if("first_name" not in keys or "last_name" not in keys or
       "phone" not in keys or "picture" not in keys or"is_active" not in keys):
        return dataValidationError("Missing data",
                                   "/accounts")
    if(not validation.name(form["first_name"])):
        return dataValidationError("The first name appears to be invalid.",
                                   "/accounts")
    if(not validation.name(form["last_name"])):
        return dataValidationError("The last name appears to be invalid.",
                                   "/accounts")
    if(not validation.phoneNumber(form["phone"])):
        return dataValidationError("Invalid phone number",
                                   "/accounts")
    if(form["is_active"]):
        return dataValidationError("Invalid value for is_active",
                                   "/accounts")
    date = time.strftime("%d-%b-%Y", time.gmtime())
    a = account.Account(form["first_name"], form["last_name"], form["phone"],
                        form["picture"], date)
    aid = ds.addAccount(a)
    return ({"aid": aid}, 201, {"Location": "/accounts/%d" % aid})

def activateAccount(ds, form, aid):
    if(aid < 0 or aid >= len(ds.accounts)):
        return {}, 404
    a = ds.getAccount(aid)
    if(a is None):
        return {}, 404
    keys = list(form.keys())
    if("first_name" not in keys or "last_name" not in keys or
       "phone" not in keys or "picture" not in keys or"is_active" not in keys):
        return dataValidationError("Missing data",
                                   "/accounts/%d/status" % aid)
    if(form["first_name"] != a.firstName):
        return dataValidationError("The first name appears to be invalid.",
                                   "/accounts/%d/status" % aid)
    if(form["last_name"] != a.lastName):
        return dataValidationError("The last name appears to be invalid.",
                                   "/accounts/%d/status" % aid)
    if(form["phone"] != a.phone):
        return dataValidationError("Invalid phone number",
                                   "/accounts/%d/status" % aid)
    if(form["picture"] != a.picture):
        return dataValidationError("Invalid picture",
                                   "/accounts/%d/status" % aid)
    if(not form["is_active"]):
        return dataValidationError("Invalid value for is_active",
                                   "/accounts/%d/status" % aid)
    a.activate()
    return {}, 204

def updateAccount(ds, form, aid):
    a = ds.getAccount(aid)
    if(a is None):
        return {}, 404
    keys = list(form.keys())
    if("first_name" not in keys or "last_name" not in keys or
       "phone" not in keys or "picture" not in keys or"is_active" not in keys):
        return dataValidationError("Missing data",
                                   "/accounts/%d" % aid)
    if(not validation.name(form["first_name"])):
        return dataValidationError("The first name appears to be invalid.",
                                   "/accounts/%d" % aid)
    if(not validation.name(form["last_name"])):
        return dataValidationError("The last name appears to be invalid.",
                                   "/accounts/%d" % aid)
    if(not validation.phoneNumber(form["phone"])):
        return dataValidationError("Invalid phone number",
                                   "/accounts/%d" % aid)
    if(form["is_active"]):
        return dataValidationError("Invalid value for is_active",
                                   "/accounts/%d" % aid)
    a.update(form["first_name"], form["last_name"], form["phone"],
             form["picture"])
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
    keys = list(form.keys())
    if("aid" not in keys or "location_info" not in keys or
       "date_time" not in keys or "car_info" not in keys or
       "max_passengers" not in keys or "amount_per_passenger" not in keys or
       "conditions" not in keys):
        return dataValidationError("Missing data",
                                   "/rides")
    
    locationKeys = list(form["location_info"].keys())
    dateKeys = list(form["date_time"].keys())
    carKeys = list(form["car_info"].keys())
    if("from_city" not in locationKeys or "to_city" not in locationKeys or
       "date" not in dateKeys or "time" not in dateKeys or "make" not in carKeys
       or "model" not in carKeys or "color" not in carKeys or
       "plate_state" not in carKeys or "plate_serial" not in carKeys):
        return dataValidationError("Missing data",
                                    "/rides")
    
    if("from_zip" not in locationKeys):
        form["location_info"]["from_zip"] = ""
    if("to_zip" not in locationKeys):
        form["location_info"]["to_zip"] = ""

    if(not validation.zip(form["location_info"]["from_zip"]) or
       not validation.zip(form["location_info"]["to_zip"])):
        return dataValidationError("Invalid zip code",
                                   "/rides")
    if(not validation.state(form["car_info"]["plate_state"])):
        return dataValidationError("Invalid state code",
                                   "/rides")
    if(not validation.date(form["date_time"]["date"])):
        return dataValidationError("Invalid date",
                                   "/rides")
    if(not validation.time(form["date_time"]["time"])):
        return dataValidationError("Invalid time",
                                   "/rides")
    
    date = time.strftime("%d-%b-%Y", time.gmtime())
    driver = ds.getAccount(form["aid"])

    if(driver is None):
        return dataValidationError("Invalid aid",
                                   "/rides")
    if(not driver.isActive):
        return dataValidationError("This account (%d) is not active, may not create a ride." % form["aid"],
                                   "/rides")
    
    r = ride.Ride(form["location_info"]["from_city"],
                  form["location_info"]["from_zip"],
                  form["location_info"]["to_city"],
                  form["location_info"]["to_zip"],
                  form["date_time"]["date"], form["date_time"]["time"],
                  form["car_info"]["make"], form["car_info"]["model"],
                  form["car_info"]["color"], form["car_info"]["plate_state"],
                  form["car_info"]["plate_serial"], form["max_passengers"],
                  form["amount_per_passenger"], form["conditions"],
                  driver, date)

    rid = ds.addRide(r)
    
    return ({"rid": rid}, 201, {"Location": "/rides/%d" % rid})

def updateRide(ds, form, rid):
    keys = list(form.keys())
    if("aid" not in keys or "location_info" not in keys or
       "date_time" not in keys or "car_info" not in keys or
       "max_passengers" not in keys or "amount_per_passenger" not in keys or
       "conditions" not in keys):
        return dataValidationError("Missing data",
                                   "/rides/%d" % rid)
    
    locationKeys = list(form["location_info"].keys())
    dateKeys = list(form["date_time"].keys())
    carKeys = list(form["car_info"].keys())
    if("from_city" not in locationKeys or "to_city" not in locationKeys or
       "date" not in dateKeys or "time" not in dateKeys or "make" not in carKeys
       or "model" not in carKeys or "color" not in carKeys or
       "plate_state" not in carKeys or "plate_serial" not in carKeys):
        return dataValidationError("Missing data",
                                    "/rides/%d" % rid)
    
    if("from_zip" not in locationKeys):
        form["location_info"]["from_zip"] = ""
    if("to_zip" not in locationKeys):
        form["location_info"]["to_zip"] = ""

    if(not validation.zip(form["location_info"]["from_zip"]) or
       not validation.zip(form["location_info"]["to_zip"])):
        return dataValidationError("Invalid zip code",
                                   "/rides/%d" % rid)
    if(not validation.state(form["car_info"]["plate_state"])):
        return dataValidationError("Invalid state code",
                                   "/rides/%d" % rid)
    if(not validation.date(form["date_time"]["date"])):
        return dataValidationError("Invalid date",
                                   "/rides/%d" % rid)
    if(not validation.time(form["date_time"]["time"])):
        return dataValidationError("Invalid time",
                                   "/rides/%d" % rid)
    r = ds.getRide(rid)

    if(r is None):
        return {}, 404
    
    driver = r.driver
    updater = ds.getAccount(form["aid"])

    if(driver != updater):
        return dataValidationError("Only the creator of the ride may change it",
                                   "/rides/%d" % rid)

    r.update(form["location_info"]["from_city"],
                form["location_info"]["from_zip"],
                form["location_info"]["to_city"],
                form["location_info"]["to_zip"],
                form["date_time"]["date"], form["date_time"]["time"],
                form["car_info"]["make"], form["car_info"]["model"],
                form["car_info"]["color"], form["car_info"]["plate_state"],
                form["car_info"]["plate_serial"], form["max_passengers"],
                form["amount_per_passenger"], form["conditions"])
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

def viewRideDetail(ds, rid):
    if(ds.getRide(rid) is None):
        return {}, 404
    return {}, 501

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
    keys = list(form.keys())
    if("aid" not in keys or "passengers" not in keys or
       "ride_confirmed" not in keys or "pickup_confirmed" not in keys):
        return dataValidationError("Missing data",
                                   "/rides/%d/join_requests" % rid)
    if(form["ride_confirmed"] is not None):
        return dataValidationError("Invalid value for ride_confirmed",
                                   "/rides/%d/join_requests" % rid)
    if(form["pickup_confirmed"] is not None):
        return dataValidationError("Invalid value for pickup_confirmed",
                                   "/rides/%d/join_requests" % rid)
    a = ds.getAccount(form["aid"])
    if(a is None):
        return dataValidationError("Invalid aid",
                                   "/rides/%d/join_requests" % rid)
    if(not a.isActive):
        return dataValidationError("This account(%d) is not active, may not create a join ride request." % form["aid"],
                                   "/rides/%d/join_requests" % rid)
    jid = ds.addJoinRequest(rid, a, form["passengers"])
    return ({"jid": jid}, 201,
            {"Location": "/rides/%d/join_requests/%d" % (rid, jid)})

def confirmJoinRequest(ds, form, rid, jid):
    r = ds.getRide(rid)
    if(r is None):
        return {}, 404
    j = ds.getJoinRequest(jid)
    if(j is None):
        return {}, 404
    keys = list(form.keys())
    if("aid" not in keys or "ride_confirmed" not in keys):
        return dataValidationError("Missing Data",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(form["ride_confirmed"] not in [True, False]):
        return dataValidationError("Invalid value for ride_confirmed",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    a = ds.getAccount(form["aid"])
    if(a != r.driver):
        return dataValidationError("This account (%d) didn't create the ride (%d)" % (form["aid"], rid),
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(j[0] != r):
        return dataValidationError("Invalid jid",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(form["ride_confirmed"]):
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
    keys = list(form.keys())
    if("aid" not in keys or "pickup_confirmed" not in keys):
        return dataValidationError("Missing Data",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(form["pickup_confirmed"] != True):
        return dataValidationError("Invalid value for pickup_confirmed",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    if(j[0] != r):
        return dataValidationError("Invalid jid",
                                   "/rides/%d/join_requests/%d" % (rid, jid))
    a = ds.getAccount(form["aid"])
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
    keys = list(form.keys())
    if("aid" not in keys or "msg" not in keys):
        return dataValidationError("Missing data",
                                   "/rides/%d/messages" % rid)
    a = ds.getAccount(form["aid"])
    if(a is None):
        return dataValidationError("Invalid aid",
                                   "/rides/%d/messages" % rid)
    if(not a.isActive):
        return dataValidationError("Account is not active",
                                   "/rides/%d/messages" % rid)
    date = time.strftime("%d-%b-%Y", time.gmtime())
    mid = ds.addMessage(rid, form["aid"], form["msg"], date)
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
