

class Account:
    def __init__(self, firstName, lastName, phone, picture):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.picture = picture
        self.isActive = False

    def activate(self):
        self.isActive = True

    def update(self, firstName=None, lastName=None, phone=None, picture=None):
        if firstName:
            self.firstName = firstName
        if lastName:
            self.lastName = lastName
        if phone:
            self.phone = phone
        if picture:
            self.picture = picture

