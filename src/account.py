

class Account:
    def __init__(self, firstName, lastName, phone, picture):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.picture = picture
        self.isActive = False

    def activate(self):
        self.isActive = True

    def update(self, firstName, lastName, phone, picture):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.picture = picture

