
import datastorage
import re

'''
In a 'real' application, we would hook this up to a database of some sorts.
I'm just using a bunch of lists.
'''

class SimpleDataHolder(datastorage.DataStorageInterface):
    def __init__(self):
        self.accounts = []
        self.rides = []
        self.messages = []
        self.joinRequests = []

    def addAccount(self, acc):
        aid = len(self.accounts)
        self.accounts.append(acc)
        return aid

    def getAccount(self, aid):
        return self.accounts[aid]

    def getAllAccounts(self):
        return list(filter(lambda x: x[1] is not None,
                           [(i, self.accounts[i])
                            for i in range(len(self.accounts))]))

    def deleteAccount(self, aid):
        self.accounts[aid] = None

    def searchAccount(self, keyword):
        regex = ".*" + keyword.lower() + ".*"
        def searchKeyword(acc):
            foundInPhone = re.search(regex, acc.phone.lower()) is not None
            foundInFName = re.search(regex, acc.firstName.lower()) is not None
            foundInLName = re.search(regex, acc.lastName.lower()) is not None
            return foundInPhone or foundInFName or foundInLName
        return list(filter(lambda x: (x[1] is not None) and searchKeyword(x[1]),
                           [(i, self.accounts[i])
                            for i in range(len(self.accounts))]))

    def addRide(self, ride):
        rid = len(self.rides)
        self.rides.append(ride)
        return rid

    def getRide(self, rid):
        return self.rides[rid]

    def getAllRides(self):
        return [(i, self.rides[i]) for i in range(len(self.rides))]

    def searchRide(self, fromKey, toKey, date):
        fRegex = ".*" + fromKey.lower() + ".*"
        tRegex = ".*" + toKey.lower() + ".*"
        def searchKeyword(ride):
            fromMatch = re.search(fRegex, ride.fromCity.lower()) is not None
            toMatch = re.search(tRegex, ride.toCity.lower()) is not None
            dateMatch = ((ride.date == date) or date == "")
            return fromMatch and toMatch and dateMatch
        return list(filter(lambda x: searchKeyword(x[1]),
                           [(i, self.rides[i])
                            for i in range(len(self.rides))]))

    def addMessage(self, rid, sender, message, date):
        mid = len(self.messages)
        mindex = self.rides[rid].addMessage(sender, message, date)
        self.messages.append((rid, mindex))
        return mid



    def addJoinRequest(self, rid, sender, passengers):
        jrid = len(self.joinRequests)
        jrindex = self.rides[rid].addJoinRequest(sender, passengers)
        self.messages.append((rid, jrindex))
        return jrid
        


    
