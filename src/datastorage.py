
'''
This is an interface. I wouldn't recommendinstantiating it, but this is python.
  I can't really stop you.
'''
class DataStorageInterface:
    def addAccount(self, account):
        pass
    def getAccount(self, aid):
        pass
    def getAllAccounts(self):
        '''
        Returns all active accounts as a list of (aid, account) tuples
        '''
        pass
    def deleteAccount(self, aid):
        pass
    def searchAccounts(self, keyword):
        '''
        Returns all active accounts containing keyword as a list of
          (aid, account) tuples
        '''
        pass
    def addRide(self, ride):
        pass
    def getRide(self, rid):
        pass
    def getAllRides(self):
        '''
        Returns all rides as a list of (rid, ride) tuples
        '''
        pass
    def searchRide(self, fromKey, toKey, date):
        '''
        Returns all rides matching the given to and from departing at date as
          a list of (rid, ride) tuples
        '''
        pass
    def addMessage(self, rid, aid, message, date):
        pass
    def getMessages(self, rid):
        '''
        Returns all messages for the given ride as (mid, aid, index) tuples.
          Since getMessages takes rid as a parameter, we don't return the
          ride object like we do with getJoinRequest.
        '''
        pass
    def addJoinRequest(self, rid, sender, passengers):
        pass
    def getJoinRequest(self, jid):
        '''
        Returns an ride and an index; the actual join request can be confirmed
          by calling confirmJoinRequest or confirmPickup with the given index
        '''
        pass
    def addDriverRating(self, aid, raterID, rid, rating, comment):
        pass
    def addRiderRating(self, aid, raterID, rid, rating, comment):
        pass
    def getDriverRatings(self, aid):
        pass
    def getRiderRatings(self, aid):
        pass
    
