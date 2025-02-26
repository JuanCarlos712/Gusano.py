import os
import sys
import curses
import time

# Verificar que el script se está ejecutando en GitHub Actions
if os.getenv("GITHUB_ACTIONS") != "true":
    print("Este script solo se ejecuta en GitHub Actions.")
    sys.exit(1)

# Configuración de la cuadrícula
GRID_ROWS = 7   # Simulando 7 días (filas)
GRID_COLS = 20  # Número de columnas (por ejemplo, semanas o cuadritos en la animación)

# Símbolos para la animación
GREEN_SQUARE = "■"  # Cuadrito "verde"
EMPTY_SQUARE = " "  # Cuadrito "comido"
WORM_CHAR = "@"     # Representación del gusano

# Tiempo de espera entre movimientos (segundos)
DELAY = 0.1

def draw_grid(stdscr, grid, worm_pos=None):
    stdscr.clear()
    for i, row in enumerate(grid):
        line = ""
        for j, cell in enumerate(row):
            # Si la posición coincide con la del gusano, dibuja el gusano
            if worm_pos and worm_pos == (i, j):
                line += WORM_CHAR
            else:
                line += cell
        stdscr.addstr(i, 0, line)
    stdscr.refresh()

def create_grid():
    """Crea una cuadrícula inicial llena de 'cuadritos verdes'."""
    return [[GREEN_SQUARE for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

def main(stdscr):
    # Configuración de curses
    curses.curs_set(0)  # Ocultar el cursor
    stdscr.nodelay(0)   # Modo bloqueante

    # Crea la cuadrícula inicial
    grid = create_grid()

    # Define un camino para el gusano (lista de (fila, columna))
    worm_path = []
    # Ejemplo: recorre la cuadrícula en forma serpentina
    for i in range(GRID_ROWS):
        if i % 2 == 0:
            for j in range(GRID_COLS):
                worm_path.append((i, j))
        else:
            for j in range(GRID_COLS - 1, -1, -1):
                worm_path.append((i, j))

    # Bucle infinito de animación
    while True:
        # Reinicia la cuadrícula al inicio del ciclo
        grid = create_grid()

        # Dibuja la cuadrícula inicial
        draw_grid(stdscr, grid)
        time.sleep(0.5)

        # Recorre el camino del gusano
        for pos in worm_path:
            i, j = pos
            # Muestra al gusano en la posición actual
            draw_grid(stdscr, grid, worm_pos=pos)
            time.sleep(DELAY)

            # El gusano "come" el cuadrito (si está verde)
            if grid[i][j] == GREEN_SQUARE:
                grid[i][j] = EMPTY_SQUARE

            # Redibuja la cuadrícula sin el cuadrito (ya comido)
            draw_grid(stdscr, grid)
            time.sleep(DELAY)

        # Al finalizar el recorrido, espera un momento y reinicia la animación
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)
