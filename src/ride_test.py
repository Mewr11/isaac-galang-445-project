'''
Unit tests for ride.py
'''

import unittest
import ride
import account

class RideTest(unittest.TestCase):
    def setUp(self):
        self.a = account.Account("Bruce", "Banner", "123-456-7890", "Hulk")
        self.r = ride.Ride("Barrington", "60010", "Milwaukee", "53202",
                           "14-Apr-2020", "09:00",
                           "Audi", "A4", "Gray", "IL", "COVID19",
                           2, 15.00,
                           "Some conditions may apply", self.a)
    
    def testNewRideCorrectlyInitialized(self):
        self.assertEqual(self.r.fromCity, "Barrington")
        self.assertEqual(self.r.fromZip, "60010")
        self.assertEqual(self.r.toCity, "Milwaukee")
        self.assertEqual(self.r.toZip, "53202")
        self.assertEqual(self.r.date, "14-Apr-2020")
        self.assertEqual(self.r.time, "09:00")
        self.assertEqual(self.r.make, "Audi")
        self.assertEqual(self.r.model, "A4")
        self.assertEqual(self.r.color, "Gray")
        self.assertEqual(self.r.lpState, "IL")
        self.assertEqual(self.r.lpNumber, "COVID19")
        self.assertEqual(self.r.passengers, 2)
        self.assertEqual(self.r.fare, 15.00)
        self.assertEqual(self.r.conditions, "Some conditions may apply")

    def testRideUpdate(self):
        self.r.update("Madison", "53704", "Middleton", "53562",
                      "15-Jun-2020", "23:59",
                      "Toyota", "Prius", "Navy", "WI", "123-ABC",
                      3, 10.00,
                      "No Pets")
        self.assertEqual(self.r.fromCity, "Madison")
        self.assertEqual(self.r.fromZip, "53704")
        self.assertEqual(self.r.toCity, "Middleton")
        self.assertEqual(self.r.toZip, "53562")
        self.assertEqual(self.r.date, "15-Jun-2020")
        self.assertEqual(self.r.time, "23:59")
        self.assertEqual(self.r.make, "Toyota")
        self.assertEqual(self.r.model, "Prius")
        self.assertEqual(self.r.color, "Navy")
        self.assertEqual(self.r.lpState, "WI")
        self.assertEqual(self.r.lpNumber, "123-ABC")
        self.assertEqual(self.r.passengers, 3)
        self.assertEqual(self.r.fare, 10.00)
        self.assertEqual(self.r.conditions, "No Pets")
        # Teardown to ensure test run order doesn't matter
        self.r.update("Barrington", "60010", "Milwaukee", "53202",
                      "14-Apr-2020", "09:00",
                      "Audi", "A4", "Gray", "IL", "COVID19",
                      2, 15.00,
                      "Some conditions may apply")

    def testRideLocationInfo(self):
        li = self.r.getLocationInfo()
        self.assertEqual(li[0], "Barrington")
        self.assertEqual(li[1], "60010")
        self.assertEqual(li[2], "Milwaukee")
        self.assertEqual(li[3], "53202")

    def testRideTimeInfo(self):
        ti = self.r.getTimeInfo()
        self.assertEqual(ti[0], "14-Apr-2020")
        self.assertEqual(ti[1], "09:00")

    def testRideCarInfo(self):
        ci = self.r.getCarInfo()
        self.assertEqual(ci[0], "Audi")
        self.assertEqual(ci[1], "A4")
        self.assertEqual(ci[2], "Gray")
        self.assertEqual(ci[3], "IL")
        self.assertEqual(ci[4], "COVID19")

    def testAddJoinRequest(self):
        jri = self.r.addJoinRequest("Requester", 2)
        jr = self.r.joinRequests[jri]
        self.assertEqual(jr.ride, self.r)
        self.assertEqual(jr.rider, "Requester")
        self.assertEqual(jr.passengers, 2)

    def testConfirmJoinRequest(self):
        jri = self.r.addJoinRequest("Request", 2)
        jr = self.r.joinRequests[jri]
        self.assertEqual(jr.confirmed, False)
        self.r.confirmJoinRequest(jri)
        self.assertEqual(jr.confirmed, True)

    def testConfirmPickup(self):
        requester = account.Account("Tony", "Stark", "987-654-3210", "Iron")
        jri = self.r.addJoinRequest(requester, 2)
        jr = self.r.joinRequests[jri]
        self.assertEqual(self.r.confirmPickup(jri),
                         "Cannot pick up unconfirmed passenger")
        self.assertEqual(jr.pickup, False)
        self.r.confirmJoinRequest(jri)
        self.r.confirmPickup(jri)
        self.assertEqual(jr.pickup, True)
        self.assertEqual(requester.rides, 1)
        self.assertEqual(self.a.drives, 1)

    def testAddMessage(self):
        mid = self.r.addMessage("Sender", "Message", "12-Apr-2020, 17:23:15")
        message = self.r.messages[mid]
        self.assertEqual(message.ride, self.r)
        self.assertEqual(message.poster, "Sender")
        self.assertEqual(message.message, "Message")
        self.assertEqual(message.date, "12-Apr-2020, 17:23:15")

if __name__ == '__main__':
    unittest.main()
