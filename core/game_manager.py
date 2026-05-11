
from core.base import GameObject

class GameManager(GameObject):
    
    #The 'Referee'. This keeps track of scores and rules.
    
    def __init__(self, math_engine):
        super().__init__("Referee")
        # This is Class Interaction: we use the math engine here
        self.math_engine = math_engine 
        
        self.targets = []      # Where the 5 differences are
        self.found_list = []   # What we already found
        self.mistakes = 0
        self.max_mistakes = 3

    def load_game_data(self, coordinates):
         #Resets everything when we load a new picture 
        self.targets = coordinates
        self.found_list = []
        self.mistakes = 0

    def validate_click(self, x, y):
        #This checks if the click hit any of our 5 targets 
        for target in self.targets:
            target_x, target_y = target
            
            # We ask the math_engine to check the distance (Interaction)
            if self.math_engine.is_hit(x, y, target_x, target_y):
                # Make sure they don't click the same spot twice
                if target not in self.found_list:
                    self.found_list.append(target)
                    return "HIT", target
                return "ALREADY_FOUND", None
        
        # If we didn't hit anything in the loop, it's a mistake
        self.mistakes += 1
        return "MISS", None