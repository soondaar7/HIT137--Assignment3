
import math
from core.base import GameObject

class CoordinateChecker(GameObject):

    #This handles the math logic. It 'inherits' from GameObject.
    
    def __init__(self, threshold=30):
        # This tells the parent class its name is MathEngine
        super().__init__("MathEngine") 
        # This is a private variable (Encapsulation) 
        # so other files can't mess with it
        self.__threshold = threshold    

    def get_status(self):
        # We are overriding the parent method here (Polymorphism)
        return f"MathEngine is ready. Radius is {self.__threshold}px"

    def is_hit(self, click_x, click_y, target_x, target_y):
        """ The math formula to see if we clicked close enough to the target """
        distance = math.sqrt((click_x - target_x)**2 + (click_y - target_y)**2)
        return distance <= self.__threshold