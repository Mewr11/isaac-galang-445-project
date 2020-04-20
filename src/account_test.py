'''
Unit tests for account.py
'''

import unittest
import account

class AccountTest(unittest.TestCase):
    def setUp(self):
        self.a = account.Account(firstName="John", lastName="Smith",
                                 phone="312-456-7890",
                                 picture="https://example.com/images/john-smith.jpeg",
                                 date="20-Apr-2020")
    
    # Ensure accounts are initialized correctly
    def testNewAccountCanBeCreated(self):
        self.assertEqual(self.a.firstName, "John")
        self.assertEqual(self.a.lastName, "Smith")
        self.assertEqual(self.a.phone, "312-456-7890")
        self.assertEqual(self.a.picture, "https://example.com/images/john-smith.jpeg")

    # Ensure new accounts are initially not active
    def testNewAccountNotActive(self):
        self.assertFalse(self.a.isActive)

    # Ensure activated accounts become active
    def testAccountValidation(self):
        self.a.activate()
        self.assertTrue(self.a.isActive)
        self.a.activate() # Ensure reduntant activations don't matter
        self.assertTrue(self.a.isActive)
        # Teardown to ensure test order doesn't matter
        self.a.isActive = False

    def testAccountUpdate(self):
        self.a.update("Jane", "Doe", "555-555-1234",
                      "https://example.com/images/jane-doe.png")
        self.assertEqual(self.a.firstName, "Jane")
        self.assertEqual(self.a.lastName, "Doe")
        self.assertEqual(self.a.phone, "555-555-1234")
        self.assertEqual(self.a.picture, "https://example.com/images/jane-doe.png")
        # Teardown to ensure test order doesn't matter
        self.a.update("John", "Smith", "312-456-7890",
                      "https://example.com/images/john-smith.jpeg")

    def testDriverRating(self):
        rid = self.a.addDriverRating("Judger", "Totes a ride", 1, "u suk",
                                     "20-Apr-2020")
        rating = self.a.driverRatings[rid]
        self.assertEqual(rating.rated, self.a)
        self.assertEqual(rating.rater, "Judger")
        self.assertEqual(self.a.getDriverRatingAverage(), 1.0)
        self.assertEqual(self.a.getDriverRatingDetail(rid),
                         (1, "u suk", "20-Apr-2020"))

    def testRiderRating(self):
        rid = self.a.addRiderRating("Nice Person", "Ride", 5, "Amazing!",
                                    "21-Apr-2020")
        self.assertEqual(self.a.getRiderRatingAverage(), 5.0)
        self.assertEqual(self.a.getRiderRatingDetail(rid),
                         (5, "Amazing!", "21-Apr-2020"))


if __name__ == '__main__':
    unittest.main()
