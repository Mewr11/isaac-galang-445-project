
import unittest
import simpledataholder
import account
import ride

class SimpleDataHolderTest(unittest.TestCase):
    def setUp(self):
        self.sdh = simpledataholder.SimpleDataHolder()
        
        self.a1 = account.Account("John", "Doe", "555-555-1234", "pic")
        self.a2 = account.Account("Jane", "Foster", "312-456-7890", "ThorPic")
        self.did = self.sdh.addAccount(self.a1)
        self.aid = self.sdh.addAccount(self.a2)

        self.r = ride.Ride("Chicago", "60616", "Madison", "53704",
                           "30-Apr-2020", "13:00",
                           "Toyota", "Prius", "Silver", "WI", "123-ABC",
                           2, 15.00,
                           "None", self.a1)
        self.rid = self.sdh.addRide(self.r)

    def testCanRetrieveAccount(self):
        self.assertEqual(self.sdh.getAccount(self.aid), self.a2)

    def testGetAllAccounts(self):
        alist = self.sdh.getAllAccounts()
        self.assertEqual(alist[0][1], self.a1)
        self.assertEqual(alist[1][1], self.a2)

    def testCanDeleteAccount(self):
        delAid = self.sdh.addAccount("To Be Deleted")
        self.sdh.deleteAccount(delAid)
        self.assertIsNone(self.sdh.getAccount(delAid))

    def testCanSearchAccount(self):
        self.assertEqual(self.sdh.searchAccount("Jane")[0][1], self.a2)
        self.assertEqual(len(self.sdh.searchAccount("J")), 2)

    def testCanGetRide(self):
        self.assertEqual(self.sdh.getRide(self.rid), self.r)

    def testGetAllRides(self):
        self.assertEqual(len(self.sdh.getAllRides()), 1)
        self.assertEqual(self.sdh.getAllRides()[0][1], self.r)

    def testSearchRide(self):
        self.assertEqual(len(self.sdh.searchRide("Chicago", "", "")), 1)
        self.assertEqual(len(self.sdh.searchRide("", "", "12-Apr-2020")), 0)

    def testCanDeleteRide(self):
        delRid = self.sdh.addRide("Delete Me")
        self.sdh.deleteRide(delRid)
        self.assertIsNone(self.sdh.getRide(delRid))

    def testMessages(self):
        self.sdh.addMessage(self.rid, self.aid, "Hi!", "19-Apr-2020")
        self.sdh.addMessage(self.rid, self.aid, "Hi Again!",
                            "20-Apr-2020")
        msgs = self.sdh.getMessages(self.rid)
        self.assertEqual(len(msgs), 2)

    def testJoinRequests(self):
        jrid = self.sdh.addJoinRequest(self.rid, self.a2, 1)
        jrInfo = self.sdh.getJoinRequest(jrid)
        self.assertEqual(jrInfo[0], self.r)

    def testRatings(self):
        self.sdh.addDriverRating(self.did, self.aid, self.rid, 5, "Amazing",
                                 "21-Apr-2020")
        self.sdh.addRiderRating(self.aid, self.did, self.rid, 4, "Good",
                                "22-Apr-2020")
        dr = self.sdh.getDriverRatings(self.did)
        rr = self.sdh.getRiderRatings(self.aid)
        self.assertEqual(len(dr), 1)
        self.assertEqual(len(rr), 1)
        self.assertEqual(dr[0][0], self.did)
        self.assertEqual(dr[0][1], self.aid)
        self.assertEqual(dr[0][2], self.rid)
        self.assertEqual(rr[0][0], self.aid)
        self.assertEqual(rr[0][1], self.did)
        self.assertEqual(rr[0][2], self.rid)

if __name__ == "__main__":
    unittest.main()
