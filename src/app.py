from flask import Flask, jsonify, request, send_from_directory
from game import Game
import os

app = Flask(__name__)
game = Game()

# =========================
# ARMAS DEL JUEGO
# =========================

game.add_weapon("hacha", 15)
game.add_weapon("martillo", 10)
game.add_weapon("mazo", 20)
game.add_weapon("espada", 15)


BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/game", methods=["POST"])
def start_game():

    global game

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No se han recibido datos."
        }), 400

    player_one = data.get("player_one")
    player_two = data.get("player_two")

    if not player_one or not player_two:
        return jsonify({
            "error": "Se necesitan los datos de ambos jugadores."
        }), 400

    name_one = player_one.get("name")
    weapon_one = player_one.get("weapon")

    name_two = player_two.get("name")
    weapon_two = player_two.get("weapon")

    if not name_one or not weapon_one:
        return jsonify({
            "error": "El jugador 1 necesita nombre y arma."
        }), 400

    if not name_two or not weapon_two:
        return jsonify({
            "error": "El jugador 2 necesita nombre y arma."
        }), 400


    # Crear jugadores
    result_one = game.add_player(
        name_one,
        100,
        weapon_one
    )

    result_two = game.add_player(
        name_two,
        100,
        weapon_two
    )

    if not result_one or not result_two:

        return jsonify({
            "error": "No se han podido crear los jugadores."
        }), 400

    player_one_obj = game.get_player_by_name(name_one)
    player_two_obj = game.get_player_by_name(name_two)

    return jsonify({

        "player_one": {
            "name": player_one_obj.get_name(),
            "health": player_one_obj.get_health(),
            "weapon": player_one_obj.get_weapon().get_name_weapon(),
            "weapon_damage": player_one_obj.get_weapon().get_damage(),
            "can_dodge": player_one_obj.can_dodge()
        },

        "player_two": {
            "name": player_two_obj.get_name(),
            "health": player_two_obj.get_health(),
            "weapon": player_two_obj.get_weapon().get_name_weapon(),
            "weapon_damage": player_two_obj.get_weapon().get_damage(),
            "can_dodge": player_two_obj.can_dodge()
        }

    }), 201

@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@app.route("/api")
def home():
    return "Turn Based Game"


# Armas
@app.route("/weapons", methods=["GET"])
def get_weapons():

    weapons = []

    for weapon in game.list_weapons:
        weapons.append({
            "name": weapon.get_name_weapon(),
            "damage": weapon.get_damage()
        })

    return jsonify(weapons)

# Estado de la partida
@app.route("/game", methods=["GET"])
def get_game_state():

    player_one = game.list_players[0]
    player_two = game.list_players[1]

    weapon_one = player_one.get_weapon()
    weapon_two = player_two.get_weapon()

    return jsonify({
        "player_one": {
            "name": player_one.get_name(),
            "health": player_one.get_health(),
            "weapon": weapon_one.get_name_weapon(),
            "weapon_damage": weapon_one.get_damage(),
            "can_dodge": player_one.can_dodge()
        },
        "player_two": {
            "name": player_two.get_name(),
            "health": player_two.get_health(),
            "weapon": weapon_two.get_name_weapon(),
            "weapon_damage": weapon_two.get_damage(),
            "can_dodge": player_two.can_dodge()
        }
    })

# Resolver turnos
@app.route("/turn", methods=["POST"])
def resolve_turn():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No se han recibido datos."
        }), 400

    player_one = data.get("player_one_action")
    player_two = data.get("player_two_action")

    if not player_one or not player_two:
        return jsonify({
            "error": "Se necesitan las acciones de ambos jugadores."
        }), 400

    name_one = player_one.get("name")
    action_one = player_one.get("action")

    name_two = player_two.get("name")
    action_two = player_two.get("action")

    valid_actions = {
        "attack",
        "defend",
        "dodge"
    }

    if action_one not in valid_actions:
        return jsonify({
            "error": "Acción no válida para el jugador 1."
        }), 400

    if action_two not in valid_actions:
        return jsonify({
            "error": "Acción no válida para el jugador 2."
        }), 400

    result = game.resolve_turn(
        name_one,
        action_one,
        name_two,
        action_two
    )

    if not result:
        return jsonify({
        "error": "No se ha podido resolver el turno.",
        "player_one": {
            "name": name_one,
            "action": action_one
        },
        "player_two": {
            "name": name_two,
            "action": action_two
        }
    }), 400

    player_one_obj = game.get_player_by_name(name_one)
    player_two_obj = game.get_player_by_name(name_two)

    # comprobar ganador
    winner = None

    if not game.is_alive(name_one):
        winner = name_two

    elif not game.is_alive(name_two):
        winner = name_one

    return jsonify({
        "success": True,

        "player_one": {
            "name": player_one_obj.get_name(),
            "health": player_one_obj.get_health(),
            "weapon": player_one_obj.get_weapon().get_name_weapon(),
            "can_dodge": player_one_obj.can_dodge()
        },

        "player_two": {
            "name": player_two_obj.get_name(),
            "health": player_two_obj.get_health(),
            "weapon": player_two_obj.get_weapon().get_name_weapon(),
            "can_dodge": player_two_obj.can_dodge()
        },

        "winner": winner
    })

# Reiniciar partida
@app.route("/game/reset", methods=["POST"])
def reset_game():

    global game

    game = Game()

    game.add_weapon("hacha", 15)
    game.add_weapon("martillo", 10)
    game.add_weapon("mazo", 20)
    game.add_weapon("espada", 15)

    return jsonify({
        "message": "Partida reiniciada correctamente."
    })
# print(os.getcwd())
# print(os.path.exists("frontend/index.html"))
if __name__ == "__main__":
    app.run(debug=True)