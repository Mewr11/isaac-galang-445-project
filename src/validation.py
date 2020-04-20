
import re

def phoneNumber(pn):
    if(re.search("(\\d.*){10}", pn) is not None):
        return True
    else:
        return False

def date(d): # Only supported date format is dd-MMM-yyyy
    if(re.search("\\d{2}-\\D{3}-\\d{4}", d) is not None):
        return True
    else:
        return False

def name(n): # Don't support numeric characters in names
    if(re.search("\\d", n) is not None):
        return False
    else:
        return True

