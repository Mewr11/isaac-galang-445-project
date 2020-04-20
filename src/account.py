

class Account:
    def __init__(self, firstName, lastName, phone, picture, date):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.picture = picture
        self.dateCreated = date
        self.isActive = False
        self.driverRatings = []
        self.riderRatings = []
        self.drives = 0
        self.rides = 0

    def activate(self):
        self.isActive = True

    def update(self, firstName, lastName, phone, picture):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.picture = picture

    def addDriverRating(self, rater, ride, rating, comment, date):
        ratingIndex = len(self.driverRatings)
        self.driverRatings.append(self.Rating(self, rater, ride, rating,
                                              comment, date))
        return ratingIndex

    def addRiderRating(self, rater, ride, rating, comment, date):
        ratingIndex = len(self.riderRatings)
        self.riderRatings.append(self.Rating(self, rater, ride, rating,
                                             comment, date))
        return ratingIndex

    def getRiderRatingAverage(self):
        return sum([r.rating
                    for r in self.riderRatings]) / len(self.riderRatings)

    def getDriverRatingAverage(self):
        return sum([r.rating
                    for r in self.driverRatings]) / len(self.driverRatings)

    def getRiderRatingDetail(self, index):
        rating = self.riderRatings[index]
        return (rating.rating, rating.comment, rating.date)

    def getDriverRatingDetail(self, index):
        rating = self.driverRatings[index]
        return (rating.rating, rating.comment, rating.date)


    class Rating:
        def __init__(self, rated, rater, ride, rating, comment, date):
            self.rated = rated
            self.rater = rater
            self.ride = ride
            self.rating = rating
            self.comment = comment
            self.date = date
    

