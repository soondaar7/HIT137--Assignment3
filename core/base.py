

class GameObject:
    
    #This is the main 'parent' class. Everything in our game is a 'GameObject'.

    def __init__(self, name):
        self.name = name

    def get_status(self):
        # This will be changed by the other classes (Polymorphism)
        return f"Component: {self.name}"