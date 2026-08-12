# Requisitos — Battle Game

## Requisitos funcionales

- El sistema debe permitir registrar armas con un nombre y un valor de daño.
- El sistema debe impedir registrar dos armas con el mismo nombre.
- El sistema debe permitir registrar jugadores con nombre, vida inicial y un arma ya existente.
- El sistema debe impedir registrar dos jugadores con el mismo nombre.
- El sistema debe impedir registrar un jugador con un arma inexistente.
- El sistema debe permitir consultar jugadores y armas por nombre.
- El sistema debe resolver un turno de combate a partir de las acciones elegidas por ambos jugadores (`attack`, `defend`, `dodge`).
- El daño de un ataque debe reducirse al 50% si el oponente se defiende, y a 0 si el oponente esquiva.
- La vida de un jugador nunca debe bajar de 0.
- Un jugador solo puede esquivar si tiene la esquiva disponible (`can_dodge`); si la usa, queda bloqueada 2 turnos (o 3 si su arma causa más daño que la del rival), tras los cuales se restaura automáticamente.
- El sistema debe permitir comprobar si un jugador sigue vivo (`is_alive`).

## Requisitos no funcionales

- El código debe seguir el principio de responsabilidad única: cada clase (`Player`, `Weapon`, `Game`) gestiona únicamente su propio dominio.
- La lógica de negocio debe estar cubierta por tests unitarios (`pytest`), siguiendo el patrón Arrange-Act-Assert.
- El proyecto no depende de librerías externas más allá de `pytest` para testing.
- La interacción con el usuario se realiza por consola (sin interfaz gráfica).

## Fuera de alcance (por ahora)

- Más de 2 jugadores simultáneos.
- Persistencia de partidas (guardado/carga).
- Interfaz gráfica o web.