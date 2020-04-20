
import unittest
import api
import simpledataholder

class APITest(unittest.TestCase):
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
    

if __name__ == "__main__":
    unittest.main()
