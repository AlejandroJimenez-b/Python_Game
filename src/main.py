from game import Game


def choose_action(game, player_name):

    while True:

        print(f"\n{player_name}, elige una acción:")
        print("1. Atacar")
        print("2. Defender")
        print("3. Esquivar")

        action = input("> ")

        if action == "1":

            return "attack"

        elif action == "2":

            return "defend"

        elif action == "3":

            if game.can_dodge(player_name):

                return "dodge"

            print(
                "No tienes la esquiva disponible este turno."
            )

        else:

            print("Acción no válida.")

def choose_weapon(game):

    game.show_weapons()

    while True:

        weapon_name = input(
            "Elige un arma por su nombre: "
        )

        if game.get_weapon_by_name(weapon_name):
            return weapon_name

        print("El arma seleccionada no existe.")

def main():

    game = Game()

    # =========================
    # ARMAS
    # =========================

    game.add_weapon("hacha", 15)
    game.add_weapon("martillo", 10)
    game.add_weapon("mazo", 20)
    game.add_weapon("espada", 15)

    # =========================
    # JUGADORES
    # =========================

    name_one = input(
        "Elige el nombre del jugador 1: "

    )

    gun_one = choose_weapon(game)


    name_two = input(
        "Elige el nombre del jugador 2: "
    )

    gun_two = choose_weapon(game)

    if name_one == "" or name_two == "":
        return

    game.add_player(
        name_one,
        100,
        gun_one
    )

    game.add_player(
        name_two,
        100,
        gun_two
    )

    # =========================
    # COMBATE
    # =========================

    while (
        game.is_alive(name_one)
        and game.is_alive(name_two)
    ):

        print("\n=============================")
        print("           NUEVO TURNO")
        print("=============================")

        player_one = game.get_player_by_name(name_one)
        player_two = game.get_player_by_name(name_two)

        print(
            f"\n{name_one}: "
            f"{player_one.get_health()} vida"
        )

        print(
            f"{name_two}: "
            f"{player_two.get_health()} vida"
        )

        # -------------------------
        # DECISIONES
        # -------------------------

        player_one_action = choose_action(
            game,
            name_one
        )

        player_two_action = choose_action(
            game,
            name_two
        )

        # -------------------------
        # RESOLVER TURNO
        # -------------------------

        game.resolve_turn(
            name_one,
            player_one_action,
            name_two,
            player_two_action
        )

    # =========================
    # GANADOR
    # =========================

    print("\n=============================")
    print("        FIN DEL COMBATE")
    print("=============================")

    if game.is_alive(name_one):

        print(
            f"\n¡Felicidades {name_one}! "
            f"Has ganado la partida."
        )

    else:

        print(
            f"\n¡Felicidades {name_two}! "
            f"Has ganado la partida."
        )


if __name__ == "__main__":
    main()