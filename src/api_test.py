
import unittest
import api
import simpledataholder

class APIAccountTest(unittest.TestCase):
    def setUp(self):
        self.ds = simpledataholder.SimpleDataHolder()
        self.createAccountResponse = api.createAccount(self.ds, {
            "first_name": "John",
            "last_name": "Smith",
            "phone": "312-456-7890",
            "picture": "http://example.com/images/john-smith.jpeg",
            "is_active": False
            })

    def testCreateAccount(self):
        self.assertEqual(self.createAccountResponse[0], {
            "aid": 0
            })

    def testAccountCreationError(self):
        errResponse = api.createAccount(self.ds, {
            "first_name": "John",
            "last_name": "Smith",
            "phone": "312-456-789O",
            "picture": "http://example.com/images/john-smith.jpeg",
            "is_active": False
            })
        self.assertEqual(errResponse[0], {
            "type": "http://cs.iit.edu/~virgil/cs445/project/api/problems/data-validation",
            "title": "Your request data didn't pass validation",
            "detail": "Invalid phone number",
            "status": 400,
            "instance": "/accounts"
            })

    def testAccountActivate(self):
        response = api.activateAccount(self.ds, {
            "first_name": "John",
            "last_name": "Smith",
            "phone": "312-456-7890",
            "picture": "http://example.com/images/john-smith.jpeg",
            "is_active": True
            }, 0)
        self.assertEqual(response[0], {})

    def testAccountActivateError(self):
        response = api.activateAccount(self.ds, {
            "first_name": "John",
            "last_name": "Smith",
            "phone": "312-456-7890",
            "picture": "http://example.com/images/john-smith.jpeg",
            "is_active": False
            }, 0)
        self.assertEqual(response[0], {
            "type": "http://cs.iit.edu/~virgil/cs445/project/api/problems/data-validation",
            "title": "Your request data didn't pass validation",
            "detail": "Invalid value for is_active",
            "status": 400,
            "instance": "/accounts/0/status"
            })

    def testAccountUpdate(self):
        response = api.updateAccount(self.ds, {
            "first_name": "John",
            "last_name": "Smith",
            "phone": "312-456-7809",
            "picture": "http://example.com/images/john-smith.jpeg",
            "is_active": False
            }, 0)
        self.assertEqual(response[0], {})

    def testAccountUpdateError(self):
        response = api.updateAccount(self.ds, {
            "first_name": "John",
            "last_name": "12345",
            "phone": "312-456-789O",
            "picture": "http://example.com/images/john-smith.jpeg",
            "is_active": False
            }, 0)
        self.assertEqual(response[0], {
            "type": "http://cs.iit.edu/~virgil/cs445/project/api/problems/data-validation",
            "title": "Your request data didn't pass validation",
            "detail": "The last name appears to be invalid.",
            "status": 400,
            "instance": "/accounts/0"
            })

    def testDeleteAccount(self):
        response = api.createAccount(self.ds, {
            "first_name": "Jane",
            "last_name": "Foster",
            "phone": "312-867-5319",
            "picture": "TaikaSelfie.png",
            "is_active": False
            })
        aid = response[0]["aid"]
        delResponse = api.deleteAccount(self.ds, aid)
        self.assertEqual(delResponse[1], 204)
        activateResponse = api.activateAccount(self.ds, {
            "first_name": "Jane",
            "last_name": "Foster",
            "phone": "312-867-5319",
            "picture": "TaikaSelfie.png",
            "is_active": True
            }, aid)
        self.assertEqual(activateResponse[1], 404)

    def testGetAllAccounts(self):
        response = api.getAllAccounts(self.ds)
        self.assertEqual(len(response[0]), 1)

    def testAccountDetail(self):
        response = api.getAccountDetail(self.ds, 0)
        self.assertEqual(response[1], 501)

    def testAccountSearch(self):
        response = api.searchAccounts(self.ds, "")
        self.assertEqual(len(response[0]), 1)
        response2 = api.searchAccounts(self.ds, "Johnson")
        self.assertEqual(len(response2[0]), 0)

class APIRideTest(unittest.TestCase):
    def setUp(self):
        self.ds = simpledataholder.SimpleDataHolder()
        api.createAccount(self.ds, { # aid 0
            "first_name": "Weiss",
            "last_name": "Schnee",
            "phone": "555-666-7788",
            "picture": "RWBY_selfie.png",
            "is_active": False
            })
        api.activateAccount(self.ds, {
            "first_name": "Weiss",
            "last_name": "Schnee",
            "phone": "555-666-7788",
            "picture": "RWBY_selfie.png",
            "is_active": True
            }, 0)
        api.createAccount(self.ds, { # aid 1
            "first_name": "Padme",
            "last_name": "Amidala",
            "phone": "314-159-2653",
            "picture": "vader.tiff",
            "is_active": False
            })
        api.activateAccount(self.ds, {
            "first_name": "Padme",
            "last_name": "Amidala",
            "phone": "314-159-2653",
            "picture": "vader.tiff",
            "is_active": True
            }, 1)
        api.createRide(self.ds, {
            "aid": 0,
            "location_info": {
      		"from_city": "Barrington",
      		"from_zip": "60010",
      		"to_city": "Milwaukee",
      		"to_zip": "53202"
            },
            "date_time": {
      		"date": "14-Apr-2020",
      		"time": "09:00"
            },
            "car_info": {
      		"make": "Audi",
      		"model": "A4",
      		"color": "Gray",
      		"plate_state": "IL",
      		"plate_serial": "COVID19"
            },
            "max_passengers": 2,
            "amount_per_passenger": 15.00,
            "conditions": "No more than one carry on per passenger. No pets."
            })

    def testCanUpdateRide(self):
        response = api.updateRide(self.ds, {
            "aid": 0,
            "location_info": {
      		"from_city": "Barrington",
      		"from_zip": "60010",
      		"to_city": "Milwaukee",
      		"to_zip": "53202"
            },
            "date_time": {
      		"date": "14-Apr-2020",
      		"time": "09:30"
            },
            "car_info": {
      		"make": "Audi",
      		"model": "A4",
      		"color": "Gray",
      		"plate_state": "IL",
      		"plate_serial": "COVID19"
            },
            "max_passengers": 2,
            "amount_per_passenger": 15.00,
            "conditions": "No more than one carry on per passenger. No pets."
            }, 0)
        self.assertEqual(response[0], {})

    def testUpdateRideError(self):
        response = api.updateRide(self.ds, {
            "aid": 1,
            "location_info": {
      		"from_city": "Barrington",
      		"from_zip": "60010",
      		"to_city": "Milwaukee",
      		"to_zip": "53202"
            },
            "date_time": {
      		"date": "14-Apr-2020",
      		"time": "09:30"
            },
            "car_info": {
      		"make": "Audi",
      		"model": "A4",
      		"color": "Gray",
      		"plate_state": "IL",
      		"plate_serial": "COVID19"
            },
            "max_passengers": 2,
            "amount_per_passenger": 15.00,
            "conditions": "No more than one carry on per passenger. No pets."
            }, 0)
        self.assertEqual(response[0], {
            "type": "http://cs.iit.edu/~virgil/cs445/project/api/problems/data-validation",
            "title": "Your request data didn't pass validation",
            "detail": "Only the creator of the ride may change it",
            "status": 400,
            "instance": "/rides/0"
            })

    def testDeleteRide(self):
        createResponse = api.createRide(self.ds, {
            "aid": 0,
            "location_info": {
      		"from_city": "Barrington",
      		"from_zip": "60010",
      		"to_city": "Milwaukee",
      		"to_zip": "53202"
            },
            "date_time": {
      		"date": "14-Apr-2020",
      		"time": "09:00"
            },
            "car_info": {
      		"make": "Audi",
      		"model": "A4",
      		"color": "Gray",
      		"plate_state": "IL",
      		"plate_serial": "COVID19"
            },
            "max_passengers": 2,
            "amount_per_passenger": 15.00,
            "conditions": "No more than one carry on per passenger. No pets."
            })
        delResponse = api.deleteRide(self.ds, createResponse[0]["rid"])
        self.assertEqual(delResponse[0], {})

    def testViewAllRides(self):
        response = api.viewAllRides(self.ds)
        self.assertEqual(len(response[0]), 1)

    def testSearchRides(self):
        response = api.searchRides(self.ds, "", "", "")
        self.assertEqual(len(response[0]), 1)
        response2 = api.searchRides(self.ds, "", "", "01-Jan-1970")
        self.assertEqual(len(response2[0]), 0)

    def testJoinRequests(self):
        joinResponse = api.createJoinRequest(self.ds, {
            "aid": 1,
            "passengers": 2,
            "ride_confirmed": None,
            "pickup_confirmed": None
            }, 0)
        self.assertEqual(joinResponse[0], {"jid": 0})
        confirmResponse = api.confirmJoinRequest(self.ds, {
            "aid": 0,
            "ride_confirmed": True
            }, 0, 0)
        self.assertEqual(confirmResponse[0], {})
        pickupResponse = api.confirmPickup(self.ds, {
            "aid": 1,
            "pickup_confirmed": True
            }, 0, 1)
        self.assertEqual(pickupResponse[0], {})

    def testMessages(self):
        msgResponse = api.addMessage(self.ds, {
            "aid": 1,
            "msg": "Tech Yeah!"
            }, 0)
        self.assertEqual(msgResponse[0], {"mid": 0})
        response = api.viewAllRideMessages(self.ds, 0)
        self.assertEqual(len(response[0]), 1)
        self.assertEqual(response[0][0]["sent_by_aid"], 1)

class APIRatingTest(unittest.TestCase):
    def setUp(self):
        self.ds = simpledataholder.SimpleDataHolder()
        api.createAccount(self.ds, { # aid 0
            "first_name": "Weiss",
            "last_name": "Schnee",
            "phone": "555-666-7788",
            "picture": "RWBY_selfie.png",
            "is_active": False
            })
        api.activateAccount(self.ds, {
            "first_name": "Weiss",
            "last_name": "Schnee",
            "phone": "555-666-7788",
            "picture": "RWBY_selfie.png",
            "is_active": True
            }, 0)
        api.createAccount(self.ds, { # aid 1
            "first_name": "Padme",
            "last_name": "Amidala",
            "phone": "314-159-2653",
            "picture": "vader.tiff",
            "is_active": False
            })
        api.activateAccount(self.ds, {
            "first_name": "Padme",
            "last_name": "Amidala",
            "phone": "314-159-2653",
            "picture": "vader.tiff",
            "is_active": True
            }, 1)
        api.createRide(self.ds, {
            "aid": 0,
            "location_info": {
      		"from_city": "Barrington",
      		"from_zip": "60010",
      		"to_city": "Milwaukee",
      		"to_zip": "53202"
            },
            "date_time": {
      		"date": "14-Apr-2020",
      		"time": "09:00"
            },
            "car_info": {
      		"make": "Audi",
      		"model": "A4",
      		"color": "Gray",
      		"plate_state": "IL",
      		"plate_serial": "COVID19"
            },
            "max_passengers": 2,
            "amount_per_passenger": 15.00,
            "conditions": "No more than one carry on per passenger. No pets."
            })
        api.createJoinRequest(self.ds, {
            "aid": 1,
            "passengers": 2,
            "ride_confirmed": None,
            "pickup_confirmed": None
            }, 0)
        api.confirmJoinRequest(self.ds, {
            "aid": 0,
            "ride_confirmed": True
            }, 0, 0)
        api.confirmPickup(self.ds, {
            "aid": 1,
            "pickup_confirmed": True
            }, 0, 0)

    def testRatings(self):
        driverRatingResponse = api.rate(self.ds, {
            "rid": 0,
            "sent_by_id": 1,
            "rating": 5,
            "comment": "Excellent"
            }, 0)
        self.assertEqual(driverRatingResponse[0], {"sid": 0})
        self.assertEqual(driverRatingResponse[2],
                         {"Location": "/accounts/0/ratings/0"})
        riderRatingResponse = api.rate(self.ds, {
            "rid": 0,
            "sent_by_id": 0,
            "rating": 5,
            "comment": "She slept the whole way"
            }, 1)
        driverRatings = api.viewDriverRatings(self.ds, 0)
        self.assertEqual(len(driverRatings[0]["detail"]), 1)
        riderRatings = api.viewRiderRatings(self.ds, 0)
        self.assertEqual(len(riderRatings[0]["detail"]), 0)
        rideDetail = api.viewRideDetail(self.ds, 0)
        self.assertEqual(rideDetail[0]["average_rating"], 5)

    def testSearch(self):
        response = api.search(self.ds, "", "20-Apr-2020", "20-May-2020")
        self.assertEqual(response[1], 501)
        

if __name__ == "__main__":
    unittest.main()
