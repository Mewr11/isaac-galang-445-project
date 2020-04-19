
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
    def addMessage(self, rid, sender, message, date):
        pass
    def getMessage(self, mid):
        pass
    def addJoinRequest(self, rid, i):
        pass
    def getJoinRequest(self, jid):
        pass
    
