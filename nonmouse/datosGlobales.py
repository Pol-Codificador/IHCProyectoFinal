# Define el estado del juego activo //variables globales 
GAME_ACTIVE = None  # Valor inicial ningun juego por default

# Función para obtener el valor de GAME_ACTIVE Setters y Getters
def get_game_active():
    global GAME_ACTIVE
    return GAME_ACTIVE

# Función para actualizar el valor de GAME_ACTIVE
def set_game_active(value):
    global GAME_ACTIVE
    GAME_ACTIVE = value