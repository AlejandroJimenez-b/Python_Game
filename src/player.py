from weapon import Weapon


class Player:

    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.weapon = None
        self.dodge_available = True

    # Getters

    def can_dodge(self):
        return self.dodge_available

    def get_name(self):
        return self.name

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health

    def get_weapon(self):
        return self.weapon

    def set_weapon(self, weapon):
        self.weapon = weapon

    # Métodos

    def use_dodge(self):

        if not self.dodge_available:
            return False

        self.dodge_available = False
        return True

    def reset_dodge(self):
        self.dodge_available = True