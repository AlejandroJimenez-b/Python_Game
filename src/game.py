from player import Player
from weapon import Weapon


class Game:

    def __init__(self):
        self.list_players = []
        self.list_weapons = []
        self.pending_attack = None

        # 0 = disponible
        # 1 = bloqueada durante este turno
        # 2 = acaba de utilizarse
        self.dodge_cooldowns = {}

    def show_weapons(self):

        accountant = 0

        for gun in self.list_weapons:

            accountant += 1

            print(
                str(accountant) + ".-",
                gun.get_name_weapon(),
                "-",
                "damage",
                gun.get_damage()
            )

    def get_player_by_name(self, name):

        for player in self.list_players:

            if name == player.get_name():
                return player

        return False

    def get_weapon_by_name(self, name):

        for weapon in self.list_weapons:

            if name == weapon.get_name_weapon():
                return weapon

        return False

    def add_player(self, name, health, weapon_name):

        existing_user = self.get_player_by_name(name)
        weapon = self.get_weapon_by_name(weapon_name)

        if not existing_user:

            player = Player(name, health)

            if weapon:

                player.set_weapon(weapon)

                self.list_players.append(player)

                # La esquiva comienza disponible
                self.dodge_cooldowns[name] = 0

                return True

            return False

        return False

    def add_weapon(self, name, damage):

        weapon = self.get_weapon_by_name(name)

        if not weapon:

            weapon = Weapon(name, damage)

            self.list_weapons.append(weapon)

            return True

        return False

    def can_dodge(self, player_name):

        if player_name not in self.dodge_cooldowns:
            return False

        return self.dodge_cooldowns[player_name] == 0

    def resolve_turn(
        self,
        player_one_name,
        player_one_action,
        player_two_name,
        player_two_action
    ):

        player_one = self.get_player_by_name(player_one_name)
        player_two = self.get_player_by_name(player_two_name)

        if not player_one or not player_two:
            return False

        weapon_one = player_one.get_weapon()
        weapon_two = player_two.get_weapon()

        if not weapon_one or not weapon_two:
            return False

        # ==================================
        # COMPROBAR ESQUIVAS
        # ==================================

        if player_one_action == "dodge":

            if not self.can_dodge(player_one_name):
                return False

            player_one.use_dodge()

            # Si su arma causa más daño que la del rival,
            # la esquiva tarda un turno extra en restaurarse
            if weapon_one.get_damage() > weapon_two.get_damage():
                self.dodge_cooldowns[player_one_name] = 3
            else:
                self.dodge_cooldowns[player_one_name] = 2

        if player_two_action == "dodge":

            if not self.can_dodge(player_two_name):
                return False

            player_two.use_dodge()

            # Si su arma causa más daño que la del rival,
            # la esquiva tarda un turno extra en restaurarse
            if weapon_two.get_damage() > weapon_one.get_damage():
                self.dodge_cooldowns[player_two_name] = 3
            else:
                self.dodge_cooldowns[player_two_name] = 2

        # ==================================
        # CALCULAR DAÑO
        # ==================================

        damage_one = 0
        damage_two = 0

        # Jugador 1 ataca

        if player_one_action == "attack":

            if player_two_action == "attack":
                damage_two = weapon_one.get_damage()

            elif player_two_action == "defend":
                damage_two = weapon_one.get_damage() // 2

            elif player_two_action == "dodge":
                damage_two = 0

        # Jugador 2 ataca

        if player_two_action == "attack":

            if player_one_action == "attack":
                damage_one = weapon_two.get_damage()

            elif player_one_action == "defend":
                damage_one = weapon_two.get_damage() // 2

            elif player_one_action == "dodge":
                damage_one = 0

        # ==================================
        # APLICAR DAÑO
        # ==================================

        new_health_one = player_one.get_health() - damage_one
        player_one.set_health(new_health_one)

        new_health_two = player_two.get_health() - damage_two
        player_two.set_health(new_health_two)

        # Evitar vida negativa

        if player_one.get_health() < 0:
            player_one.set_health(0)

        if player_two.get_health() < 0:
            player_two.set_health(0)

        # ==================================
        # MOSTRAR RESULTADO
        # ==================================

        print("\n-----------------------------")
        print("RESULTADO DEL TURNO")
        print("-----------------------------")

        if player_one_action == "attack":

            print(
                f"{player_one.get_name()} ataca con "
                f"{weapon_one.get_name_weapon()}."
            )

        elif player_one_action == "defend":

            print(
                f"{player_one.get_name()} se defiende."
            )

        else:

            print(
                f"{player_one.get_name()} esquiva."
            )

        if player_two_action == "attack":

            print(
                f"{player_two.get_name()} ataca con "
                f"{weapon_two.get_name_weapon()}."
            )

        elif player_two_action == "defend":

            print(
                f"{player_two.get_name()} se defiende."
            )

        else:

            print(
                f"{player_two.get_name()} esquiva."
            )

        print()

        if damage_one > 0:

            print(
                f"{player_one.get_name()} recibe "
                f"{damage_one} de daño."
            )

        if damage_two > 0:

            print(
                f"{player_two.get_name()} recibe "
                f"{damage_two} de daño."
            )

        if damage_one == 0 and damage_two == 0:

            print("Nadie recibe daño.")

        print()

        print(
            f"{player_one.get_name()}: "
            f"{player_one.get_health()} vida"
        )

        print(
            f"{player_two.get_name()}: "
            f"{player_two.get_health()} vida"
        )

        # ==================================
        # REDUCIR COOLDOWN
        # ==================================

        if self.dodge_cooldowns[player_one_name] > 0:

            self.dodge_cooldowns[player_one_name] -= 1

        if self.dodge_cooldowns[player_two_name] > 0:

            self.dodge_cooldowns[player_two_name] -= 1

        # ==================================
        # RESTAURAR ESQUIVA
        # ==================================

        if self.dodge_cooldowns[player_one_name] == 0:

            player_one.reset_dodge()

        if self.dodge_cooldowns[player_two_name] == 0:

            player_two.reset_dodge()

        return True

    def is_alive(self, player_name):

        player = self.get_player_by_name(player_name)

        if not player:
            return False

        return player.get_health() > 0