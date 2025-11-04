"""
    Yefry Shephard J
    22-SISN-2-020
"""

from pathlib import Path
from typing import List, Tuple
import os
import pygame
from Utilidades.Assets import ASSETS


class Setup:
    # Colores ANSI actualizados
    COLORS = {
        'GREEN': '\033[38;5;82m',    # Verde brillante
        'RED': '\033[38;5;196m',     # Rojo brillante
        'YELLOW': '\033[38;5;220m',  # Amarillo dorado
        'BLUE': '\033[38;5;39m',     # Azul cielo
        'MAGENTA': '\033[38;5;201m',  # Magenta brillante
        'CYAN': '\033[38;5;51m',     # Cyan brillante
        'RESET': '\033[0m'
    }

    # Variables para joystick
    joystick = None
    joystick_cooldown = 0
    joystick_cooldown_time = 10  # milisegundos entre pulsaciones

    # Variables para repetición de teclas en menú
    key_repeat_delay = 40  # Retraso inicial
    # Intervalo entre repeticiones
    key_repeat_interval = 20
    last_key_repeat_time = 0  # Último tiempo en que se repitió una tecla
    key_held_time = 0  # Tiempo que lleva presionada la tecla actual

    # Constantes para botones del joystick
    BUTTON_A = 0        # Disparo principal
    BUTTON_B = 1        # Cancelar/Atrás
    BUTTON_X = 2        # Disparo alternativo
    BUTTON_Y = 3
    BUTTON_LB = 4
    BUTTON_RB = 5
    BUTTON_BACK = 6     # Menú secundario
    BUTTON_START = 7    # Pausa

    # Constantes para teclas
    KEY_UP = pygame.K_UP
    KEY_DOWN = pygame.K_DOWN
    KEY_LEFT = pygame.K_LEFT
    KEY_RIGHT = pygame.K_RIGHT
    KEY_FIRE = pygame.K_SPACE
    KEY_PAUSE = pygame.K_ESCAPE
    KEY_ENTER = pygame.K_RETURN

    # Estado de teclas y botones para evitar repeticiones
    last_key_state: dict = {}

    @staticmethod
    def validate_assets() -> bool:
        """
        Valida todos los recursos requeridos del juego.

        Realiza una validación completa de los recursos del juego incluyendo:
        - Existencia del archivo
        - Permisos del archivo
        - Integridad básica del archivo

        Returns:
            bool: True si todos los recursos son válidos, False en caso contrario
        """
        missing_assets: List[Tuple[str, str, str]
                             ] = []  # (nombre, ruta, razón)
        total_assets = len(
            [asset for asset in ASSETS if asset.name != 'ASSETS_DIR'])
        validated = 0

        print(
            f"\n{Setup.COLORS['CYAN']}🔍 Iniciando verificación de recursos...{Setup.COLORS['RESET']}")

        for asset_enum in ASSETS:
            if asset_enum.name == 'ASSETS_DIR':
                continue

            asset_path = asset_enum.value
            validated += 1
            print(
                f"\r📊 Progreso: {Setup.COLORS['MAGENTA']}{validated}/{total_assets}{Setup.COLORS['RESET']} recursos analizados", end="")

            if not isinstance(asset_path, Path):
                missing_assets.append((
                    asset_enum.name,
                    str(asset_path),
                    "Tipo de ruta inválido"
                ))
                continue

            if not asset_path.exists():
                missing_assets.append((
                    asset_enum.name,
                    str(asset_path),
                    "Archivo no encontrado"
                ))
                continue

            if not os.access(asset_path, os.R_OK):
                missing_assets.append((
                    asset_enum.name,
                    str(asset_path),
                    "Archivo no legible"
                ))
                continue

            if asset_path.stat().st_size == 0:
                missing_assets.append((
                    asset_enum.name,
                    str(asset_path),
                    "Archivo está vacío"
                ))

        print()  # Nueva línea después del progreso

        if missing_assets:
            print(
                f"\n{Setup.COLORS['RED']}❌ ¡ALERTA! Validación de recursos fallida{Setup.COLORS['RESET']}")
            print(
                f"{Setup.COLORS['YELLOW']}⚠️  Se detectaron los siguientes problemas:{Setup.COLORS['RESET']}")
            for name, path, reason in missing_assets:
                print(f"\n📁 {name}:")
                print(f"  📍 Ruta: {path}")
                print(f"  ❗ Error: {reason}")
            print(
                f"\n{Setup.COLORS['YELLOW']}🔧 Por favor, soluciona estos problemas antes de continuar{Setup.COLORS['RESET']}")
            return False

        print(
            f"\n{Setup.COLORS['GREEN']}✨ ¡Validación completada con éxito!{Setup.COLORS['RESET']}")
        print(
            f"{Setup.COLORS['CYAN']}🎮 Iniciando Battle City...{Setup.COLORS['RESET']}")
        return True

    @staticmethod
    def init_joystick():
        """
        Inicializa y detecta joysticks conectados.
        Si no hay joystick, el juego funcionará normalmente con teclado.

        Returns:
            pygame.joystick.Joystick or None: Retorna el joystick detectado o None
        """
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        if (joystick_count > 0):
            Setup.joystick = pygame.joystick.Joystick(0)
            Setup.joystick.init()
            print(
                f"\n{Setup.COLORS['GREEN']}🎮 Joystick detectado: {Setup.joystick.get_name()}{Setup.COLORS['RESET']}")
            print(
                f"{Setup.COLORS['CYAN']}ℹ️  Se puede controlar el juego con joystick o teclado{Setup.COLORS['RESET']}")

            # Mostrar información del joystick
            buttons = Setup.joystick.get_numbuttons()
            axes = Setup.joystick.get_numaxes()
            hats = Setup.joystick.get_numhats()

            print(
                f"{Setup.COLORS['CYAN']}ℹ️  Información del joystick:{Setup.COLORS['RESET']}")
            print(f"  - Botones: {buttons}")
            print(f"  - Ejes: {axes}")
            print(f"  - D-pads: {hats}")

            return Setup.joystick
        else:
            print(
                f"\n{Setup.COLORS['YELLOW']}ℹ️  No se detectó joystick/gamepad. Usando controles de teclado.{Setup.COLORS['RESET']}")
            return None

    @staticmethod
    def is_joystick_connected():
        """
        Verifica si hay un joystick conectado y activo.

        Returns:
            bool: True si hay un joystick conectado, False en caso contrario
        """
        return Setup.joystick is not None

    @staticmethod
    def process_joystick_cooldown(current_time):
        """
        Gestiona el tiempo de espera entre pulsaciones de joystick.

        Args:
            current_time: El tiempo actual en milisegundos

        Returns:
            bool: True si el joystick está listo para ser usado, False si está en espera
        """
        if Setup.joystick_cooldown > 0 and current_time > Setup.joystick_cooldown:
            Setup.joystick_cooldown = 0
            return True

        return Setup.joystick_cooldown == 0

    @staticmethod
    def set_joystick_cooldown(current_time):
        """
        Establece el tiempo de espera para el joystick.

        Args:
            current_time: El tiempo actual en milisegundos
        """
        Setup.joystick_cooldown = current_time + Setup.joystick_cooldown_time

    @staticmethod
    def get_movement_input():
        """Obtiene la entrada de movimiento del joystick o teclado.

        Returns:
            tuple: (dx, dy) donde cada valor está en el rango [-1, 1]
        """
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        # Entrada de teclado
        if keys[Setup.KEY_LEFT]:
            dx = -1
        elif keys[Setup.KEY_RIGHT]:
            dx = 1

        if keys[Setup.KEY_UP]:
            dy = -1
        elif keys[Setup.KEY_DOWN]:
            dy = 1

        # Si hay joystick, verificar su entrada y dar prioridad si existe
        if Setup.joystick:
            # Obtener valores de los ejes
            axis_x = Setup.joystick.get_axis(0)
            axis_y = Setup.joystick.get_axis(1)

            # Aplicar zona muerta para evitar detección de movimiento con joystick en reposo
            if abs(axis_x) > 0.1:
                dx = axis_x
            if abs(axis_y) > 0.1:
                dy = axis_y

            # D-pad tiene prioridad sobre los ejes análogos
            if Setup.joystick.get_numhats() > 0:
                hat_x, hat_y = Setup.joystick.get_hat(0)
                if hat_x != 0:
                    dx = hat_x  # -1 (izquierda) o 1 (derecha)
                if hat_y != 0:
                    dy = -hat_y  # Invertido: -1 (abajo) o 1 (arriba)

        return (dx, dy)

    @staticmethod
    def is_fire_pressed():
        """Verifica si se presionó el botón/tecla de disparo.

        Returns:
            bool: True si se presionó el botón de disparo
        """
        # Verificar teclado
        keys = pygame.key.get_pressed()
        keyboard_fire = keys[Setup.KEY_FIRE]

        # Verificar joystick
        joystick_fire = False
        if Setup.joystick:
            joystick_fire = (Setup.joystick.get_button(Setup.BUTTON_A) or
                             Setup.joystick.get_button(Setup.BUTTON_X))

        return keyboard_fire or joystick_fire

    @staticmethod
    def is_pause_pressed():
        """Verifica si se presionó el botón/tecla de pausa.

        Returns:
            bool: True si se presionó pausa y es un nuevo evento
        """
        keys = pygame.key.get_pressed()
        key_pressed = keys[Setup.KEY_PAUSE]
        joystick_pressed = False
        if Setup.joystick:
            joystick_pressed = Setup.joystick.get_button(Setup.BUTTON_START)

        # Combinamos ambos y verificamos que sea un nuevo evento
        pressed = key_pressed or joystick_pressed

        # Usar último estado para detectar solo cuando cambia a presionado
        pause_key = "pause"
        is_new_press = pressed and not Setup.last_key_state.get(
            pause_key, False)
        Setup.last_key_state[pause_key] = pressed

        return is_new_press

    @staticmethod
    def is_confirm_pressed():
        """Verifica si se presionó el botón/tecla de confirmación.

        Returns:
            bool: True si se presionó confirmación y es un nuevo evento
        """
        # Verificar teclado
        keys = pygame.key.get_pressed()
        key_pressed = keys[Setup.KEY_ENTER] or keys[Setup.KEY_FIRE]

        # Verificar joystick
        joystick_pressed = False
        if Setup.joystick:
            joystick_pressed = Setup.joystick.get_button(Setup.BUTTON_A)

        # Combinamos ambos y verificamos que sea un nuevo evento
        pressed = key_pressed or joystick_pressed

        # Usar último estado para detectar solo cuando cambia a presionado
        confirm_key = "confirm"
        is_new_press = pressed and not Setup.last_key_state.get(
            confirm_key, False)
        Setup.last_key_state[confirm_key] = pressed

        return is_new_press

    @staticmethod
    def is_back_pressed():
        """Verifica si se presionó el botón/tecla de retroceso.

        Returns:
            bool: True si se presionó retroceso y es un nuevo evento
        """
        # Verificar teclado (por ahora también usamos ESC)
        keys = pygame.key.get_pressed()
        key_pressed = keys[Setup.KEY_PAUSE]

        # Verificar joystick
        joystick_pressed = False
        if Setup.joystick:
            joystick_pressed = (Setup.joystick.get_button(Setup.BUTTON_B) or
                                Setup.joystick.get_button(Setup.BUTTON_BACK))

        # Combinamos ambos y verificamos que sea un nuevo evento
        pressed = key_pressed or joystick_pressed

        # Usar último estado para detectar solo cuando cambia a presionado
        back_key = "back"
        is_new_press = pressed and not Setup.last_key_state.get(
            back_key, False)
        Setup.last_key_state[back_key] = pressed

        return is_new_press

    @staticmethod
    def get_menu_navigation():
        """Obtiene la dirección de navegación de menú.

        Returns:
            int: 1 (abajo), -1 (arriba), o 0 (sin movimiento)
        """
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # Detectar pulsación única, no continua
        up_key = "menu_up"
        down_key = "menu_down"

        up_pressed = keys[Setup.KEY_UP]
        down_pressed = keys[Setup.KEY_DOWN]

        # Verificar joystick
        if Setup.joystick:
            # Combinar con entrada de joystick
            axis_y = Setup.joystick.get_axis(1)
            if axis_y < -0.5:  # Hacia arriba
                up_pressed = True
            elif axis_y > 0.5:  # Hacia abajo
                down_pressed = True

            # D-pad
            if Setup.joystick.get_numhats() > 0:
                _, hat_y = Setup.joystick.get_hat(0)
                if (hat_y > 0):  # D-pad arriba
                    up_pressed = True
                elif (hat_y < 0):  # D-pad abajo
                    down_pressed = True

        # Verificar cambio de estado para detección inicial
        up_new = up_pressed and not Setup.last_key_state.get(up_key, False)
        down_new = down_pressed and not Setup.last_key_state.get(
            down_key, False)

        # Mantener un seguimiento del tiempo que las teclas han estado presionadas
        if up_pressed or down_pressed:
            # Si es una pulsación nueva, inicializar el tiempo
            if up_new or down_new:
                Setup.key_held_time = current_time
                Setup.last_key_repeat_time = current_time

            # Si se ha superado el tiempo de delay inicial y el intervalo de repetición
            elif current_time - Setup.key_held_time > Setup.key_repeat_delay and \
                    current_time - Setup.last_key_repeat_time > Setup.key_repeat_interval:
                # Actualizar el último tiempo de repetición
                Setup.last_key_repeat_time = current_time
                # Simular una pulsación nueva
                if up_pressed:
                    up_new = True
                elif down_pressed:
                    down_new = True
        else:
            # Resetear tiempos si no hay teclas presionadas
            Setup.key_held_time = 0
            Setup.last_key_repeat_time = 0

        # Actualizar estado
        Setup.last_key_state[up_key] = up_pressed
        Setup.last_key_state[down_key] = down_pressed

        # Determinar dirección (prioridad a arriba si ambos están presionados)
        if up_new:
            return -1
        elif down_new:
            return 1
        else:
            return 0

    @staticmethod
    def update_input_states():
        """Actualiza los estados de entrada para la próxima comparación.
        Debe llamarse al final de cada frame."""
        # Actualizar estados del teclado
        keys = pygame.key.get_pressed()

        # Actualizar estado de pausa
        pause_key = "pause"
        Setup.last_key_state[pause_key] = keys[Setup.KEY_PAUSE]
        if Setup.joystick:
            Setup.last_key_state[pause_key] |= Setup.joystick.get_button(
                Setup.BUTTON_START)

        # Actualizar estado de confirmación
        confirm_key = "confirm"
        Setup.last_key_state[confirm_key] = keys[Setup.KEY_ENTER] or keys[Setup.KEY_FIRE]
        if Setup.joystick:
            Setup.last_key_state[confirm_key] |= Setup.joystick.get_button(
                Setup.BUTTON_A)

        # Actualizar estado de retroceso
        back_key = "back"
        Setup.last_key_state[back_key] = keys[Setup.KEY_PAUSE]
        if Setup.joystick:
            Setup.last_key_state[back_key] |= (Setup.joystick.get_button(Setup.BUTTON_B) or
                                               Setup.joystick.get_button(Setup.BUTTON_BACK))

        # Actualizar estados de navegación del menú
        up_key = "menu_up"
        down_key = "menu_down"
        Setup.last_key_state[up_key] = keys[Setup.KEY_UP]
        Setup.last_key_state[down_key] = keys[Setup.KEY_DOWN]

        if Setup.joystick:
            # Actualizar con ejes del joystick
            axis_y = Setup.joystick.get_axis(1)
            if axis_y < -0.5:  # Hacia arriba
                Setup.last_key_state[up_key] = True
            elif axis_y > 0.5:  # Hacia abajo
                Setup.last_key_state[down_key] = True

            # Actualizar con D-pad
            if Setup.joystick.get_numhats() > 0:
                _, hat_y = Setup.joystick.get_hat(0)
                if hat_y > 0:  # D-pad arriba
                    Setup.last_key_state[up_key] = True
                elif hat_y < 0:  # D-pad abajo
                    Setup.last_key_state[down_key] = True
