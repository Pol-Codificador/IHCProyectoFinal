# Define el estado del juego activo
# Define el estado del juego activo
GAME_ACTIVE = None  # Valor inicial

# Función para obtener el valor de GAME_ACTIVE
def get_game_active():
    global GAME_ACTIVE
    return GAME_ACTIVE

# Función para actualizar el valor de GAME_ACTIVE
def set_game_active(value):
    global GAME_ACTIVE
    GAME_ACTIVE = value