# Battle Game

Minijuego de batalla por turnos en consola, hecho en Python como proyecto de aprendizaje (mi primer software de videojuego). Dos jugadores eligen arma y se enfrentan turno a turno hasta que uno se queda sin vida.

## Características

- Sistema de turnos con 3 acciones: atacar, defender, esquivar.
- Sistema de armas con distinto daño por arma.
- Mecánica de cooldown de esquiva, con penalización adicional para quien elige el arma más dañina (evita que exista una "opción dominante" sin ningún trade-off).
- Cobertura de tests con `pytest` sobre las 3 clases principales.

## Estructura del proyecto
python_game/
```
├── docs
    ├── requirements.md
    ├── usecases.md
    └── design.md
    
├── frontend
    ├── index.html
    ├── styles.css
    ├── script.js
    
├── src
    ├── player.py # Clase Player
    ├── weapon.py # Clase Weapon
    ├── game.py # Clase Game (reglas y mecánica principal)
    
├── tests
    ├── test_game.py # Tests con pytest

```
## Requisitos

- Python 3.x
- pytest (solo para ejecutar los tests)

## Instalación

```bash
pip install pytest
```

## Cómo correr los tests

```bash
pytest
```

## Documentación

- [`design.md`](./design.md): reglas del juego y arquitectura del código.
- [`usecases.md`](./usecases.md): casos de uso de cada método público de `Game`.
- [`requirements.md`](./requirements.md): requisitos funcionales y no funcionales del proyecto.

## Estado del proyecto

Proyecto retomado tras un intento anterior sin terminar. Actualmente completo en cuanto a mecánica básica (ataque, defensa, esquiva con cooldown y penalización por arma fuerte) y con tests unitarios cubriendo `Player`, `Weapon` y `Game`.
