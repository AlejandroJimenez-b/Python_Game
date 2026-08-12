const API_URL = "";

let playerOneAction = null;
let playerTwoAction = null;
let gameState = null;
let turnResolving = false;

// =====================================
// ELEMENTOS DEL DOM
// =====================================

const setupScreen =
    document.getElementById("setup-screen");

const combatScreen =
    document.getElementById("combat-screen");

const playerOneNameInput =
    document.getElementById("player-one-name");

const playerTwoNameInput =
    document.getElementById("player-two-name");

const playerOneWeapon =
    document.getElementById("player-one-weapon");

const playerTwoWeapon =
    document.getElementById("player-two-weapon");

const setupMessage =
    document.getElementById("setup-message");


// =====================================
// CARGAR ARMAS
// =====================================

async function loadWeapons() {

    try {

        const response = await fetch("/weapons");

        const weapons = await response.json();

        weapons.forEach(weapon => {

            const optionOne =
                document.createElement("option");

            optionOne.value = weapon.name;

            optionOne.textContent =
                `${weapon.name} - ${weapon.damage} daño`;

            playerOneWeapon.appendChild(optionOne);


            const optionTwo =
                document.createElement("option");

            optionTwo.value = weapon.name;

            optionTwo.textContent =
                `${weapon.name} - ${weapon.damage} daño`;

            playerTwoWeapon.appendChild(optionTwo);
        });

    } catch (error) {

        setupMessage.textContent =
            "No se ha podido conectar con el servidor.";
    }
}


// =====================================
// CREAR PARTIDA
// =====================================

document
    .getElementById("start-game")
    .addEventListener("click", async () => {

        const nameOne =
            playerOneNameInput.value.trim();

        const nameTwo =
            playerTwoNameInput.value.trim();

        const weaponOne =
            playerOneWeapon.value;

        const weaponTwo =
            playerTwoWeapon.value;


        if (
            !nameOne ||
            !nameTwo ||
            !weaponOne ||
            !weaponTwo
        ) {

            setupMessage.textContent =
                "Completa todos los campos.";

            return;
        }


        try {

            const response = await fetch(
                "/game",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        player_one: {
                            name: nameOne,
                            weapon: weaponOne
                        },

                        player_two: {
                            name: nameTwo,
                            weapon: weaponTwo
                        }
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                setupMessage.textContent =
                    data.error ||
                    "No se pudo crear la partida.";

                return;
            }


            showCombatScreen(data);

        } catch (error) {

            setupMessage.textContent =
                "Error conectando con el servidor.";
        }
    });


// =====================================
// MOSTRAR COMBATE
// =====================================

function showCombatScreen(data) {

    setupScreen.classList.add("hidden");

    combatScreen.classList.remove("hidden");

    updateGameState(data);
}


// =====================================
// ACTUALIZAR ESTADO
// =====================================

function updateGameState(data) {

    gameState = data;


    // =================================
    // INFORMACIÓN JUGADOR 1
    // =================================

    document.getElementById("name-one").textContent =
        data.player_one.name;

    document.getElementById("health-one").textContent =
        data.player_one.health;

    document.getElementById("weapon-one").textContent =
        data.player_one.weapon;


    // =================================
    // INFORMACIÓN JUGADOR 2
    // =================================

    document.getElementById("name-two").textContent =
        data.player_two.name;

    document.getElementById("health-two").textContent =
        data.player_two.health;

    document.getElementById("weapon-two").textContent =
        data.player_two.weapon;


    // =================================
    // ACTUALIZAR ESQUIVAS
    // =================================

    updateDodgeButtons();
}


// =====================================
// ACTUALIZAR BOTONES DE ESQUIVA
// =====================================

function updateDodgeButtons() {

    if (!gameState) {
        return;
    }


    const playerOneDodge =
        document.querySelector(
            '[data-player="one"][data-action="dodge"]'
        );

    const playerTwoDodge =
        document.querySelector(
            '[data-player="two"][data-action="dodge"]'
        );


    if (playerOneDodge) {

        playerOneDodge.disabled =
            !gameState.player_one.can_dodge;
    }


    if (playerTwoDodge) {

        playerTwoDodge.disabled =
            !gameState.player_two.can_dodge;
    }
}


// =====================================
// ACCIONES
// =====================================

document
    .querySelectorAll("[data-action]")
    .forEach(button => {

        button.addEventListener("click", () => {

            // No permitir acciones mientras
            // se está resolviendo el turno

            if (turnResolving) {
                return;
            }


            const player =
                button.dataset.player;

            const action =
                button.dataset.action;


            // =================================
            // JUGADOR 1
            // =================================

            if (player === "one") {

                if (playerOneAction !== null) {
                    return;
                }

                // Seguridad adicional:
                // no permitir esquiva si está en cooldown

                if (
                    action === "dodge" &&
                    !gameState.player_one.can_dodge
                ) {
                    return;
                }

                playerOneAction = action;
            }


            // =================================
            // JUGADOR 2
            // =================================

            else {

                if (playerTwoAction !== null) {
                    return;
                }

                // Seguridad adicional:
                // no permitir esquiva si está en cooldown

                if (
                    action === "dodge" &&
                    !gameState.player_two.can_dodge
                ) {
                    return;
                }

                playerTwoAction = action;
            }


            button.classList.add("selected");


            checkActions();
        });
    });


// =====================================
// COMPROBAR SI AMBOS HAN ELEGIDO
// =====================================

function checkActions() {

    if (!playerOneAction || !playerTwoAction) {
        return;
    }


    turnResolving = true;


    fetch("/turn", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            player_one_action: {

                name: gameState.player_one.name,

                action: playerOneAction
            },

            player_two_action: {

                name: gameState.player_two.name,

                action: playerTwoAction
            }
        })
    })


    .then(response => response.json())


    .then(data => {

        if (data.error) {

            document
                .getElementById("result-message")
                .textContent = data.error;

            resetActions();

            turnResolving = false;

            return;
        }


        // Actualizar todo el estado del juego
        // incluyendo can_dodge

        updateGameState(data);


        // Preparar siguiente turno

        resetActions();


        // Comprobar ganador

        if (data.winner) {

            showWinner(data.winner);

            turnResolving = false;

            return;
        }


        document
            .getElementById("result-message")
            .textContent =
            "Turno resuelto. Elige las acciones del siguiente turno.";


        turnResolving = false;
    })


    .catch(error => {

        console.error(error);

        document
            .getElementById("result-message")
            .textContent =
            "Error conectando con el servidor.";

        resetActions();

        turnResolving = false;
    });
}


// =====================================
// REINICIAR ACCIONES
// =====================================

function resetActions() {

    playerOneAction = null;

    playerTwoAction = null;


    document
        .querySelectorAll("[data-action]")
        .forEach(button => {

            button.classList.remove("selected");
        });


    // Volvemos a aplicar el estado de las esquivas

    updateDodgeButtons();
}


// =====================================
// GANADOR
// =====================================

function showWinner(winner) {

    const winnerScreen =
        document.getElementById("winner-screen");

    const winnerMessage =
        document.getElementById("winner-message");


    winnerMessage.textContent =
        `¡${winner} ha ganado la partida!`;


    winnerScreen.classList.remove("hidden");


    document
        .querySelectorAll("[data-action]")
        .forEach(button => {

            button.disabled = true;
        });
}


// =====================================
// REINICIAR PARTIDA
// =====================================

document
    .getElementById("restart-game")
    .addEventListener("click", () => {

        location.reload();
    });


// =====================================
// INICIO
// =====================================

loadWeapons();