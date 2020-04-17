

class Account:
    def __init__(self, firstName, lastName, phone, picture):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.picture = picture
        self.isActive = False
        self.driverRatings = []

    def activate(self):
        self.isActive = True

    def update(self, firstName, lastName, phone, picture):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.picture = picture

    def addDriverRating(self, rater, ride, rating, comment):
        self.driverRatings.append(self.Rating(self, rater, ride, rating,
                                              comment))
        return len(self.driverRatings) - 1

    def addRiderRating(self, rater, ride, rating, comment):
        self.riderRatings.append(self.Rating(self, rater, ride, rating,
                                             comment))
        return len(self.riderRatings) - 1


    class Rating:
        def __init__(self, rated, rater, ride, rating, comment):
            self.rated = rated
            self.rater = rater
            self.ride = ride
            self.rating = rating
            self.comment = comment
    

