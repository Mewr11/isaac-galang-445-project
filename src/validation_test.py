
import unittest
import validation

class ValidationTest(unittest.TestCase):

    def testPhoneNumberValidation(self):
        self.assertEqual(validation.phoneNumber("312-456-7890"), True)
        self.assertEqual(validation.phoneNumber("312-456-789O"), False)

    def testDateValidation(self):
        self.assertEqual(validation.date("20-Apr-2020"), True)
        self.assertEqual(validation.date("04-20-2020"), False)

    def testNameValidation(self):
        self.assertEqual(validation.name("Prince"), True)
        self.assertEqual(validation.name("Pr1nce"), False)

    def testZipValidation(self):
        self.assertEqual(validation.zip("53562"), True)
        self.assertEqual(validation.zip("yolos"), False)

    def testTimeValidation(self):
        self.assertEqual(validation.time("11:11"), True)
        self.assertEqual(validation.time("7:11"), False)

    def testStateValidation(self):
        self.assertEqual(validation.state("FL"), True)
        self.assertEqual(validation.state("Florida"), False)

if __name__ == "__main__":
    unittest.main()
