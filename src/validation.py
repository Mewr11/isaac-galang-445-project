
import re

def phoneNumber(pn):
    if(re.search("(\\d.*){10}", pn) is not None):
        return True
    else:
        return False

def date(d): # Only supported date format is dd-MMM-yyyy
    if(re.search("^\\d{2}-\\D{3}-\\d{4}$", d) is not None):
        return True
    else:
        return False

def name(n): # Don't support numeric characters in names
    if(re.search("\\d", n) is not None):
        return False
    else:
        return True

def zip(z):
    if(re.search("^\\d{5}$", z) is not None or z == ""):
        return True
    else:
        return False

def time(t):
    if(re.search("^\\d{2}:\\d{2}$", t) is not None):
        return True
    else:
        return False

def state(s):
    if(re.search("^\\D{2}$", s) is not None):
        return True
    else:
        return False


