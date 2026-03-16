class User:
    
    def __init__(self, name, email, password, role):

        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.credibility_score = 0

    def to_dict(self):

        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "credibility_score": self.credibility_score
        }