
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
        self.ratings = []

    def addAccount(self, acc):
        aid = len(self.accounts)
        self.accounts.append(acc)
        return aid

    def getAccount(self, aid):
        return self.accounts[aid]

    def getAllAccounts(self):
        return [(i, self.accounts[i])
                for i in range(len(self.accounts))
                if self.accounts[i] is not None]

    def deleteAccount(self, aid):
        self.accounts[aid] = None

    def searchAccount(self, keyword):
        regex = ".*" + keyword.lower() + ".*"
        def searchKeyword(acc):
            foundInPhone = re.search(regex, acc.phone.lower()) is not None
            foundInFName = re.search(regex, acc.firstName.lower()) is not None
            foundInLName = re.search(regex, acc.lastName.lower()) is not None
            return foundInPhone or foundInFName or foundInLName
        return [(i, self.accounts[i])
                for i in range(len(self.accounts))
                if (self.accounts[i] is not None)
                and searchKeyword(self.accounts[i])]

    def addRide(self, ride):
        rid = len(self.rides)
        self.rides.append(ride)
        return rid

    def getRide(self, rid):
        return self.rides[rid]

    def getAllRides(self):
        return [(i, self.rides[i]) for i in range(len(self.rides))
                if self.rides[i] is not None]

    def deleteRide(self, rid):
        self.rides[rid] = None

    def searchRide(self, fromKey, toKey, date):
        fRegex = ".*" + fromKey.lower() + ".*"
        tRegex = ".*" + toKey.lower() + ".*"
        def searchKeyword(ride):
            fromMatch = re.search(fRegex, ride.fromCity.lower()) is not None
            toMatch = re.search(tRegex, ride.toCity.lower()) is not None
            dateMatch = ((ride.date == date) or date == "")
            return fromMatch and toMatch and dateMatch
        return [(i, self.rides[i])
                for i in range(len(self.rides))
                if (self.rides[i] is not None) and searchKeyword(self.rides[i])]

    def addMessage(self, rid, aid, message, date):
        mid = len(self.messages)
        sender = self.accounts[aid]
        mindex = self.rides[rid].addMessage(sender, message, date)
        self.messages.append((rid, mindex, aid))
        return mid

    def getMessages(self, rid):
        return [(i, self.messages[i][2], self.messages[i][1])
         for i in range(len(self.messages))
         if self.messages[i][0] == rid]

    def addJoinRequest(self, rid, sender, passengers):
        jrid = len(self.joinRequests)
        jrindex = self.rides[rid].addJoinRequest(sender, passengers)
        self.joinRequests.append((rid, jrindex))
        return jrid

    def getJoinRequest(self, jid):
        (rid, index) = self.joinRequests[jid]
        return (self.rides[rid], index)

    def addDriverRating(self, aid, raterID, rid, rating, comment, date):
        ratingID = len(self.ratings)
        driver = self.accounts[aid]
        rater = self.accounts[raterID]
        ride = self.rides[rid]
        ratingIndex = driver.addDriverRating(rater, ride, rating, comment, date)
        self.ratings.append((aid, raterID, rid, ratingIndex, "driver"))
        return ratingID

    def addRiderRating(self, aid, raterID, rid, rating, comment, date):
        ratingID = len(self.ratings)
        rider = self.accounts[aid]
        rater = self.accounts[raterID]
        ride = self.rides[rid]
        ratingIndex = rider.addRiderRating(rater, ride, rating, comment, date)
        self.ratings.append((aid, raterID, rid, ratingIndex, "rider"))
        return ratingID

    def getDriverRatings(self, aid):
        return [r for r in self.ratings
                if r[-1] == "driver" and r[0] == aid]

    def getRiderRatings(self, aid):
        return [r for r in self.ratings
                if r[-1] == "rider" and r[0] == aid]
