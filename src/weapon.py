# clase Weapon

class Weapon:
    def __init__(self,name_weapon,damage):
        self.name_weapon = name_weapon
        self.damage = damage

    #getters
        
    def get_name_weapon(self):
        return self.name_weapon
    
    def get_damage(self):
        return self.damage
    
    #setters

    def set_damage(self,damage):
        self.damage = damage
