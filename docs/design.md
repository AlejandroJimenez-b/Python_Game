# Battle Game

## Descripción de juego

- El juego consistirá en una batalla básica por turnos alternados.
- Solo se permiten 2 jugadores.
- Mostrará unas opciones, las cuales el jugador es libre de elegir.
- Las opciones serán: elegir su nombre, su arma y las acciones de juego.

## Mecánica del juego

### 1 -> Imprimir por consola el nombre del juego.

### 2 -> Mostrar al jugador un menú con dos acciones:

- 1 Elegir armas:
    - Cada player tendrá que pulsar una tecla específica para elegir las armas disponibles en el juego.
    - Cada arma tiene un daño asignado y este es el daño que se le inflige a la vida del oponente.

- 2 Empezar el juego:
    - Una vez elegida el arma, el jugador deberá introducir su nombre y así comenzar el juego.

### 3 -> Funcionalidad del juego:

- El juego tendrá un sistema de turnos. En cada turno, al jugador se le dará a elegir entre 3 acciones:
    - **Atacar**: inflige a su oponente el mismo daño que causa su arma elegida.
    - **Defender**: se reduce al 50% el daño recibido del atacante.
    - **Esquivar**: los ataques no causan ningún daño.

- Sistema de esquiva (cooldown):
    - Tienes la oportunidad de elegir 1 esquiva por turno. Si la consumes, en el siguiente turno no la tendrás disponible (solo podrás atacar o defenderte), y se restaurará en el turno posterior a ese.
    - **Desventaja por arma fuerte**: si el arma elegida causa mayor daño que la del oponente, la esquiva tarda un turno extra en restaurarse (en vez de recuperarse al 3er turno, se recupera al 4º). Esto evita que elegir siempre el arma de más daño sea una decisión sin ningún coste.

- El proceso se repite hasta que uno de los jugadores pierda todos sus puntos de vida.

## Arquitectura del código

El proyecto sigue una separación simple en 3 clases, cada una con una única responsabilidad:

- **`Weapon`**: representa un arma. Atributos: `name_weapon`, `damage`. Expone getters (`get_name_weapon`, `get_damage`) y un setter (`set_damage`).

- **`Player`**: representa a un jugador. Atributos: `name`, `health`, `weapon`, `dodge_available`. Expone getters/setters de salud y arma, y la lógica propia de la esquiva individual (`use_dodge`, `reset_dodge`, `can_dodge`).

- **`Game`**: orquesta la partida. Mantiene las listas de jugadores y armas, y el diccionario `dodge_cooldowns` (control de turnos de bloqueo de esquiva por jugador). Contiene toda la lógica de reglas: registro de jugadores/armas, búsqueda por nombre, y la resolución de turnos (`resolve_turn`), que es el método central del juego.

La clase `Game` es la única que conoce las *reglas* (daño, cooldowns, condiciones de victoria); `Player` y `Weapon` son modelos de datos con comportamiento mínimo propio. Esto facilita testear cada pieza de forma aislada.