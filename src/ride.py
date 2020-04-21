

class Ride:
    def __init__(self, fromCity, fromZip, toCity, toZip,
                 date, time,
                 make, model, color, lpState, lpNumber,
                 passengers, fare,
                 conditions, driver, datePosted):
        self.fromCity = fromCity
        self.fromZip = fromZip
        self.toCity = toCity
        self.toZip = toZip
        self.date = date
        self.time = time
        self.make = make
        self.model = model
        self.color = color
        self.lpState = lpState
        self.lpNumber = lpNumber
        self.passengers = passengers
        self.fare = fare
        self.conditions = conditions
        self.driver = driver
        self.datePosted = datePosted
        self.messages = []
        self.joinRequests = []
        self.riders = []

    def update(self, fromCity, fromZip, toCity, toZip,
               date, time,
               make, model, color, lpState, lpNumber,
               passengers, fare,
               conditions):
        self.fromCity = fromCity
        self.fromZip = fromZip
        self.toCity = toCity
        self.toZip = toZip
        self.date = date
        self.time = time
        self.make = make
        self.model = model
        self.color = color
        self.lpState = lpState
        self.lpNumber = lpNumber
        self.passengers = passengers
        self.fare = fare
        self.conditions = conditions

    '''
    Returns (fromCity, fromZip, toCity, toZip)
    '''
    def getLocationInfo(self):
        return (self.fromCity, self.fromZip, self.toCity, self.toZip)

    '''
    Returns (date, time)
    '''
    def getTimeInfo(self):
        return (self.date, self.time)

    def getCarInfo(self):
        return (self.make, self.model, self.color, self.lpState, self.lpNumber)

    def addMessage(self, sender, msg, date):
        mid = len(self.messages)
        self.messages.append(self.Message(self, sender, msg, date))
        return mid

    class Message:
        def __init__(self, ride, poster, message, date):
            self.ride = ride
            self.poster = poster
            self.message = message
            self.date = date

    def addJoinRequest(self, requester, passengers):
        jrid = len(self.joinRequests)
        self.joinRequests.append(self.JoinRequest(self, requester, passengers))
        return jrid

    def confirmJoinRequest(self, jri):
        self.joinRequests[jri].confirmed = True

    def denyJoinRequest(self, jri):
        self.joinRequests[jri].confirmed = False

    def confirmPickup(self, jri):
        if(self.joinRequests[jri].confirmed):
            self.joinRequests[jri].pickup = True
            self.driver.drives += 1
            self.joinRequests[jri].rider.rides += 1
            self.riders.append(self.joinRequests[jri].rider)
            return None
        else:
            return "Cannot pick up unconfirmed passenger"
    
    
    class JoinRequest:
        def __init__(self, ride, rider, passengers):
            self.ride = ride
            self.rider = rider
            self.passengers = passengers
            self.confirmed = None
            self.pickup = None
