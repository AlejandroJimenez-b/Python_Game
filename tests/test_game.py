# Tests

# Test para Player

from player import Player
from weapon import Weapon
from game import Game

# El player se crea con la salud correcta
def test_player_starts_with_correct_health():

    player = Player("Geralt", 100)

    assert player.get_health() == 100

# El player se crea con el nombre correcto
def test_player_has_correct_name():

    player = Player("Geralt", 100)

    assert player.get_name() == "Geralt"

# El player puede modificar su salud (por si es atacado)
def test_player_can_change_health():

    player = Player("Geralt", 100)

    player.set_health(75)

    assert player.get_health() == 75

# El player puede tener un arma asignada
def test_player_can_have_weapon():

    player = Player("Geralt", 100)
    weapon = Weapon("hacha", 15)

    player.set_weapon(weapon)

    assert player.get_weapon() == weapon

# Esquivas del player
# Tiene disponibles
def test_player_starts_with_dodge_available():

    player = Player("Geralt", 100)

    assert player.can_dodge() is True

# Utilizar las esquivas las consume
def test_use_dodge_consumes_dodge():

    player = Player("Geralt", 100)

    result = player.use_dodge()

    assert result is True
    assert player.can_dodge() is False

# No puede utilizarla dos veces
def test_player_cannot_use_dodge_twice():

    player = Player("Geralt", 100)

    player.use_dodge()

    result = player.use_dodge()

    assert result is False

# Se resetean las esquivas
def test_reset_dodge_makes_dodge_available():

    player = Player("Geralt", 100)

    player.use_dodge()
    player.reset_dodge()

    assert player.can_dodge() is True


# Tests para Weapon
# Comprobar el arma por su nombre
def test_weapon_has_correct_name():

    weapon = Weapon("Hacha", 15)

    assert weapon.get_name_weapon() == "Hacha"

# Comprobar el daño que infringe el arma
def test_weapon_has_correct_damage():

    weapon = Weapon("Hacha", 15)

    assert weapon.get_damage() == 15

# Comprobar que se puede modificar el daño del arma
def test_weapon_can_change_damage():

    weapon = Weapon("Hacha", 15)

    weapon.set_damage(20)

    assert weapon.get_damage() == 20

# Tests para Game (comportamiento del juego)

# Gestion de armas
# Añadir un arma
def test_game_can_add_weapon():

    game = Game()

    result = game.add_weapon("Hacha", 15)

    assert result is True

# Buscar un arma por su nombre
def test_game_can_find_added_weapon():

    game = Game()

    game.add_weapon("Hacha", 15)

    weapon = game.get_weapon_by_name("Hacha")

    assert weapon is not False

# Comprobar si el arma tiene el daño correcto
def test_game_finds_weapon_with_correct_damage():

    game = Game()

    game.add_weapon("Hacha", 15)

    weapon = game.get_weapon_by_name("Hacha")

    assert weapon.get_damage() == 15

# Comprobacion de duplicado de armas prohibido
def test_game_forbidden_duplicates_weapon():

    game = Game()

    permitted = game.add_weapon("Hacha", 15)
    forbidden = game.add_weapon("Hacha", 15)

    assert permitted is True
    assert forbidden is False

    assert len(game.list_weapons) == 1

# Gestion de Players
# Añadir un jugador
def test_game_can_add_player():

    game = Game()

    game.add_weapon("Hacha", 15)

    result = game.add_player("Geralt", 100, "Hacha")

    assert result is True

# Comprobacion de duplicado de armas prohibido
def test_game_forbidden_duplicate_player():

    game = Game()

    game.add_weapon("Hacha", 15)

    permitted = game.add_player(
        "Geralt",
        100,
        "Hacha"
    )

    forbidden = game.add_player(
        "Geralt",
        100,
        "Hacha"
    )

    assert permitted is True
    assert forbidden is False

# Buscar un jugador por su nombre
def test_game_can_find_added_player():

    game = Game()

    game.add_weapon("Hacha", 15)

    game.add_player("Geralt", 100, "Hacha")

    player = game.get_player_by_name("Geralt")

    assert player is not False

# Comprobar jugador se añade con su arma correcta
def test_player_is_created_with_weapon():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_player("Geralt", 100, "Hacha")

    player = game.get_player_by_name("Geralt")

    assert player.get_weapon().get_name_weapon() == "Hacha"

# Tests para mecanica y reglas del juego (metodo resolve_turn)

# Ataque vs ...
# Ataque contra Ataque (los dos jugadores pierden 15 de vida)
def test_resolve_turn_attack_vs_attack():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "attack",
        "Cirilla",
        "attack"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 85
    assert cirilla.get_health() == 85

# Ataque contra defensa (el jugador atacado pierde un 50% menos que si no se defiende)
def test_resolve_turn_attack_vs_defend():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "attack",
        "Cirilla",
        "defend"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 100
    assert cirilla.get_health() == 93

# Ataque contra esquiva(el jugador atacado pierde 0 de vida, pero consume la posibilidad de esquiva en ese mismo turno)
def test_resolve_turn_attack_vs_dodge():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "attack",
        "Cirilla",
        "dodge"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 100
    assert cirilla.get_health() == 100

    assert cirilla.can_dodge() is False

# Defensa vs ...
# Defensa vs Ataque
def test_resolve_turn_defend_vs_attack():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "defend",
        "Cirilla",
        "attack"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 93
    assert cirilla.get_health() == 100

# Defend vs Defend
def test_resolve_turn_defend_vs_defend():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "defend",
        "Cirilla",
        "defend"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 100
    assert cirilla.get_health() == 100


# Defend vs Dodge
def test_resolve_turn_defend_vs_dodge():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "defend",
        "Cirilla",
        "dodge"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 100
    assert cirilla.get_health() == 100

    assert cirilla.can_dodge() is False

# Dodge vs ...
# Dodge vs Attack
def test_resolve_turn_dodge_vs_attack():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "attack"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 100
    assert cirilla.get_health() == 100

    assert geralt.can_dodge() is False

# Dodge vs Defend
def test_resolve_turn_dodge_vs_defend():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "defend"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 100
    assert cirilla.get_health() == 100

    assert geralt.can_dodge() is False

# Dodge vs Dodge
def test_resolve_turn_dodge_vs_dodge():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "dodge"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 100
    assert cirilla.get_health() == 100

    assert geralt.can_dodge() is False
    assert cirilla.can_dodge() is False

# Tests Casos limite
# Player no puede tener vida < 0
def test_player_cannot_have_negative_health():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 20)

    game.add_player("Geralt", 10, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "attack",
        "Cirilla",
        "attack"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    assert geralt.get_health() == 0
    assert cirilla.get_health() == 85

# Player sin vida is False
def test_player_without_live():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 20)

    game.add_player("Geralt", 10, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "attack",
        "Cirilla",
        "attack"
    )

    geralt = game.get_player_by_name("Geralt")
    cirilla = game.get_player_by_name("Cirilla")

    player_no_life = game.is_alive(geralt.get_name())
    player_life = game.is_alive(cirilla.get_name())
    
    assert player_no_life is False
    assert player_life is True

# Player no existente is False
def test_game_no_detect_no_exist_player():

    game = Game()
    
    assert game.is_alive("Geralt") is False

# Player existente is True
def test_game_detects_alive_player():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_player("Geralt", 100, "Hacha")

    assert game.is_alive("Geralt") is True

# Test de esquiva en game (comprobar comportamiento correcto en la mecanica de juego)
# Puedo usar esquiva consumida en primer turno en el segundo turno? -> False
def test_resolve_turn_cannot_use_dodge_during_cooldown():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    # Primer turno: Geralt utiliza su esquiva
    first_turn = game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "attack"
    )

    # Segundo turno: intenta esquivar otra vez
    second_turn = game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "attack"
    )

    assert first_turn is True
    assert second_turn is False

# Test la esquiva vuelve a estar disponible en el tercer turno (si se ha consumido en el primero)
def test_resolve_turn_available_dodge_in_third_turn():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    # Primer turno: Geralt utiliza su esquiva
    first_turn = game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "attack"
    )

    # Segundo turno: Geralt ataca porque la esquiva no se puede utilizar en este turno
    second_turn = game.resolve_turn(
        "Geralt",
        "attack",
        "Cirilla",
        "attack"
    )

    assert game.dodge_cooldowns["Geralt"] == 0
    assert game.get_player_by_name("Geralt").can_dodge() is True

    # Tercer turno: intenta esquivar otra vez (debe ser True)
    third_turn = game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "attack"
    )

    assert first_turn is True
    assert second_turn is True
    assert third_turn is True

# Test de esquiva con desventaja por arma más fuerte
# Si el arma del jugador que esquiva hace más daño que la del rival,
# la esquiva debe restaurarse en el CUARTO turno (cooldown = 3), no en el tercero
def test_resolve_turn_dodge_cooldown_extended_with_stronger_weapon():

    game = Game()

    game.add_weapon("Hacha", 20)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    # Turno 1: Geralt esquiva con un arma más dañina que la de Cirilla
    first_turn = game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "attack"
    )

    # El cooldown se fija en 3 y se reduce a 2 tras el propio turno
    assert game.dodge_cooldowns["Geralt"] == 2
    assert game.get_player_by_name("Geralt").can_dodge() is False

    # Turno 2: en la mecánica normal ya estaría bloqueada, aquí también
    second_turn = game.resolve_turn(
        "Geralt",
        "attack",
        "Cirilla",
        "attack"
    )

    assert game.dodge_cooldowns["Geralt"] == 1
    assert game.get_player_by_name("Geralt").can_dodge() is False

    # Turno 3: en la mecánica normal ya se restauraría, pero aquí sigue bloqueada
    third_turn = game.resolve_turn(
        "Geralt",
        "attack",
        "Cirilla",
        "attack"
    )

    assert game.dodge_cooldowns["Geralt"] == 0
    assert game.get_player_by_name("Geralt").can_dodge() is True

    # Turno 4: ahora sí puede volver a esquivar
    fourth_turn = game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "attack"
    )

    assert first_turn is True
    assert second_turn is True
    assert third_turn is True
    assert fourth_turn is True

# Test de esquiva con armas de igual daño
# Si ambas armas causan el mismo daño, el cooldown debe ser el normal (2, no 3)
def test_resolve_turn_dodge_cooldown_normal_with_equal_weapons():

    game = Game()

    game.add_weapon("Hacha", 15)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "attack"
    )

    # Cooldown normal: se fija en 2 y se reduce a 1 tras el propio turno
    assert game.dodge_cooldowns["Geralt"] == 1


# Test de esquiva con arma más débil
# Si el arma del jugador que esquiva causa MENOS daño que la del rival,
# no hay penalización: el cooldown sigue siendo el normal (2)
def test_resolve_turn_dodge_cooldown_normal_with_weaker_weapon():

    game = Game()

    game.add_weapon("Hacha", 10)
    game.add_weapon("Espada", 15)

    game.add_player("Geralt", 100, "Hacha")
    game.add_player("Cirilla", 100, "Espada")

    game.resolve_turn(
        "Geralt",
        "dodge",
        "Cirilla",
        "attack"
    )

    assert game.dodge_cooldowns["Geralt"] == 1

# No se puede añadir un player con el mismo nombre
def test_cannot_add_player_with_same_name():

    game = Game()

    game.add_weapon("Hacha", 15)

    permited = game.add_player("Geralt", 100, "Hacha")
    forbidden = game.add_player("Geralt", 100, "Hacha")

    assert permited is True
    assert forbidden is False

    assert len(game.list_players) == 1

# No se puede añadir un player con un arma inexistente
def test_cannot_add_player_with_nonexistent_gun():

    game = Game()

    game.add_weapon("Hacha", 15)

    gun_non_existent = game.add_player("Geralt", 100, "Mazo")

    assert gun_non_existent is False
    assert len(game.list_players) == 0