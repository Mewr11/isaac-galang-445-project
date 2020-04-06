'''
Unit tests for account.py
'''

import unittest
import account

class AccountTest(unittest.TestCase):
    def setUp(self):
        self.a = account.Account(firstName="John", lastName="Smith",
                                 phone="312-456-7890",
                                 picture="https://example.com/images/john-smith.jpeg")
    
    # Ensure accounts can be created
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
        self.a.update(firstName="Jane")
        self.assertEqual(self.a.firstName, "Jane")
        self.assertEqual(self.a.lastName, "Smith")
        self.a.update(picture="localhost:5000/pics/example.jpg")
        self.assertEqual(self.a.picture, "localhost:5000/pics/example.jpg")
        self.a.update(lastName="Garcia")
        self.assertEqual(self.a.lastName, "Garcia")
        self.a.update(phone="555-555-1234")
        self.assertEqual(self.a.phone, "555-555-1234")
        # Teardown to ensure teset order doesn't matter
        self.a.update(firstName="John", lastName="Smith",
                      phone="312-456-7890",
                      picture="https://example.com/images/john-smith.jpeg")
        # Also one more test 'cause why not
        self.assertEqual(self.a.firstName, "John")

if __name__ == '__main__':
    unittest.main()
