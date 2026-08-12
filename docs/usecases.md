## Casos de uso — Battle Game

### show_weapons
- El juego debe mostrar por consola todas las armas disponibles, con su nombre y su daño, numeradas para facilitar la selección.

### get_player_by_name
- El juego debe permitir localizar a un jugador ya registrado a partir de su nombre.

### get_weapon_by_name
- El juego debe permitir localizar un arma ya registrada a partir de su nombre.

### add_weapon
- El juego debe permitir registrar una nueva arma (nombre + daño). No se permiten armas duplicadas por nombre.

### add_player
- El juego debe permitir registrar un nuevo jugador (nombre, vida, arma elegida). El arma debe existir previamente. No se permiten jugadores duplicados por nombre.

### can_dodge
- El juego debe poder consultar si un jugador tiene la esquiva disponible en el turno actual.

### resolve_turn
- El juego debe resolver un turno completo dadas las acciones de ambos jugadores (`attack`, `defend`, `dodge`):
- Calcula el daño según la combinación de acciones.
- Aplica el daño a la vida de cada jugador (sin permitir vida negativa).
- Gestiona el cooldown de esquiva de cada jugador, incluyendo la penalización extra cuando el arma causa más daño que la del rival.
- Muestra por consola el resultado del turno.

### is_alive
- El juego debe permitir comprobar si un jugador concreto sigue con vida (salud > 0).