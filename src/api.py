
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
    return {"aid": aid}, 201

def activateAccount(ds, form, aid):
    if(aid < 0 or aid >= len(ds.accounts)):
        return {}, 404
    a = ds.getAccount(aid)
    if(a is None):
        return {}, 404
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
    if(aid < 0 or aid >= len(ds.accounts)):
        return {}, 404
    a = ds.getAccount(aid)
    if(a is None):
        return {}, 404
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
    if(aid < 0 or aid >= len(ds.accounts)):
        return {}, 404
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
