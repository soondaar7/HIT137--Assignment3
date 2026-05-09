import math

# ==========================================
# 1. BASE CLASS (Inheritance & Polymorphism)
# ==========================================
class GameObject:
    """ 
    Base class to demonstrate Inheritance. 
    Every game component is a 'GameObject'.
    """
    def __init__(self, name):
        self.name = name

    def get_status(self):
        """ This will be overridden (Polymorphism) """
        return f"Component: {self.name}"

# ==========================================
# 2. COORDINATE CHECKER (Encapsulation)
# ==========================================
class CoordinateChecker(GameObject):
    """ 
    Handles the math logic. Inherits from GameObject.
    """
    def __init__(self, threshold=30):
        super().__init__("MathEngine") # Constructor calling parent
        self.__threshold = threshold    # PRIVATE variable (Encapsulation)

    # Polymorphism: Overriding the parent's get_status method
    def get_status(self):
        return f"MathEngine active. Accuracy radius: {self.__threshold}px"

    def calculate_distance(self, x1, y1, x2, y2):
        """ The Euclidean distance math formula """
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def is_hit(self, click_x, click_y, target_x, target_y):
        """ Checks if the click is within the private threshold """
        distance = self.calculate_distance(click_x, click_y, target_x, target_y)
        return distance <= self.__threshold

# ==========================================
# 3. GAME MANAGER (Class Interaction)
# ==========================================
class GameManager(GameObject):
    """ 
    The 'Referee'. Manages the score and rules.
    """
    def __init__(self, math_engine):
        super().__init__("Referee")
        # CLASS INTERACTION: GameManager uses the CoordinateChecker object
        self.math_engine = math_engine 
        
        self.targets = []      # List of (x,y) from Student B
        self.found_list = []   # Differences already found
        self.mistakes = 0
        self.max_mistakes = 3

    def load_game_data(self, coordinates):
        """ Resets the state for a new image """
        self.targets = coordinates
        self.found_list = []
        self.mistakes = 0

    def validate_click(self, x, y):
        """
        The core game logic:
        1. Checks proximity using the math_engine.
        2. Prevents double-clicking the same difference.
        3. Tracks the 3-mistake rule.
        """
        for target in self.targets:
            target_x, target_y = target
            
            # Interaction: Asking the math_engine to check the hit
            if self.math_engine.is_hit(x, y, target_x, target_y):
                if target not in self.found_list:
                    self.found_list.append(target)
                    return "HIT", target
                return "ALREADY_FOUND", None
        
        # No hits found in the loop = Mistake
        self.mistakes += 1
        return "MISS", None