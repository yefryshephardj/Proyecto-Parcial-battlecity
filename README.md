# 🎮 BATTLE CITTY 🎮

```ascii


## 📑 Tabla de Contenidos

- [Introducción](#-introducción)
- [Características](#-características)
- [Instalación](#-instalación)
- [Jugabilidad](#-jugabilidad)
- [Controles](#-controles)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Implementación de IA](#-implementación-de-ia)
- [Diseño de Audio](#-diseño-de-audio)
- [Diseño Visual](#-diseño-visual)
- [Aspectos Técnicos Destacados](#-aspectos-técnicos-destacados)
- [Créditos](#-créditos)

## 🚀 Introducción

 battle city, donde los jugadores controlan un tanque y navegan por un mapa basado en cuadrículas, destruyendo tanques enemigos mientras evitan ser destruidos. El juego fue desarrollado usando Python y Pygame, con características avanzadas como IA enemiga usando árboles de comportamiento y búsqueda de caminos.

## ✨ Características

- **Jugabilidad Interactiva**: Controla tu tanque para navegar por el campo de batalla
- **Enemigos con IA**: Tanques enemigos con comportamiento inteligente usando árboles de comportamiento y búsqueda de caminos A\*
- **Entorno Destructible**: Destruye paredes de ladrillo con tus misiles
- **Múltiples Estados de Juego**: Sistema de menús, gameplay, pausa, pantallas de game over y victoria
- **Retroalimentación de Audio**: Efectos de sonido y música para varios eventos del juego
- **Soporte para Controladores**: Juega con teclado o gamepad/joystick
- **Soporte de Pantalla Completa**: Alterna entre modo ventana y pantalla completa con F11

## 🔧 Instalación

### Requisitos Previos

- Python 3.7+
- Pygame
- Pygame-menu

### Configuración

1. Clona el repositorio o descarga el código fuente
2. Instala las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

3. Asegúrate de que todos los recursos estén en las ubicaciones correctas
4. Ejecuta el juego:

   ```bash
   python Battle_City.py
   ```

## 🎯 Jugabilidad

### Objetivo

Destruye todos los tanques enemigos mientras proteges tu tanque. El juego se gana cuando todos los tanques enemigos son destruidos, y se pierde si tu tanque es destruido (la salud llega a 0).

### Elementos del Juego

- **Tanque del Jugador**: Tanque verde controlado por el jugador
- **Tanques Enemigos**: Tanques rojos que persiguen y atacan al jugador
- **Misiles**: Proyectiles disparados por tanques que pueden destruir ladrillos y dañar tanques
- **Paredes de Ladrillo**: Obstáculos destructibles
- **Paredes de Acero**: Obstáculos indestructibles

### Sistema de Puntuación

- Destruir un tanque enemigo: 100 puntos
- Destruir un ladrillo: 10 puntos

## 🎮 Controles

### Teclado

- **Teclas de Flecha**: Mueve tu tanque arriba, abajo, izquierda, derecha
- **Espacio**: Dispara misil
- **ESC**: Pausa el juego
- **F11**: Alterna pantalla completa

### Gamepad/Joystick

- **D-pad o Stick Analógico Izquierdo**: Mueve tu tanque
- **Botón A/X**: Dispara misil
- **Botón Start**: Pausa el juego
- **Botones Back + Start**: Alterna pantalla completa

<a id="arquitectura"></a>

## 🏗️ Arquitectura

### Componentes Principales

1. **Motor de Juego**: Gestiona el bucle del juego, eventos, renderizado y estado del juego
2. **Sistema de Entidades**: Clases para jugador, enemigos, misiles
3. **Sistema de IA**: Árboles de comportamiento y búsqueda de caminos A\* para la IA enemiga
4. **Sistema de Menús**: Menús interactivos usando pygame-menu
5. **Sistemas de Utilidad**: Gestión de recursos, constantes, manejo de temas

### Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal
- **Pygame**: Biblioteca de desarrollo de juegos
- **Pygame-menu**: Biblioteca de creación de menús
- **Búsqueda de Caminos A\***: Para navegación enemiga
- **Árboles de Comportamiento**: Para toma de decisiones de IA enemiga

## 📁 Estructura del Proyecto

```plaintext
BattleCity/
├── Algoritmos/             # Algoritmos de IA
│   ├── A_Star.py           # Búsqueda de caminos A*
│   ├── Nodo.py             # Implementación del árbol de comportamiento
├── Entidades/              # Entidades del juego
│   ├── Jugador.py          # Tanque del jugador
│   ├── Enemigo.py          # Tanque enemigo
│   ├── Misil.py            # Misiles/proyectiles
├── Juego/                  # Componentes del juego
│   ├── Juego.py            # Clase principal del juego
│   ├── Mapa.py             # Mapa/nivel del juego
├── Utilidades/             # Módulos de utilidad
│   ├── Assets.py           # Rutas de recursos
│   ├── Constantes.py       # Constantes del juego
│   ├── Setup.py            # Inicialización del juego
│   ├── Strings.py          # Cadenas de texto
│   ├── Theme.py            # Tema de UI
├── assets/                 # Recursos del juego
│   ├── image/              # Sprites e imágenes
│   ├── sounds/             # Efectos de sonido y música
├── Battle_City.py          # Punto de entrada principal
├── README.md               # Esta documentación
```

## 🧠 Implementación de IA

### Árbol de Comportamiento Enemigo

Los tanques enemigos utilizan una arquitectura de árbol de comportamiento para tomar decisiones:

1. **Selector Raíz**: Selector principal de comportamiento
2. **Secuencia de Movimiento**: Controla el comportamiento de movimiento
   - **Selector de Comportamiento**: Elige entre persecución o patrulla
     - **Secuencia de Persecución**: Comprueba si el jugador es visible, luego persigue
     - **Acción de Patrulla**: Comportamiento de patrulla predeterminado cuando el jugador no es visible
   - **Actualizar Posición**: Actualiza la posición del tanque después de la selección de comportamiento
3. **Secuencia de Disparo**: Maneja decisiones de disparo
   - **Comprobar Visibilidad del Jugador**: Verifica si el jugador está en línea de visión
   - **Intentar Disparar**: Intenta disparar al jugador
4. **Actualización de Animación**: Actualiza la representación visual del tanque

### Búsqueda de Caminos

El juego utiliza el algoritmo A\* para la navegación enemiga:

- Encuentra la ruta óptima del enemigo al jugador
- Tiene en cuenta obstáculos (paredes) y otros tanques
- Se actualiza dinámicamente cuando la ruta está bloqueada

## 🎵 Diseño de Audio

- **Música de Fondo**: Suena durante la navegación por menús
- **Inicio de Juego**: Sonido especial al iniciar un nivel
- **Sonido de Disparo**: Al disparar misiles
- **Selección de Menú**: Al navegar por menús
- **Música de Victoria**: Suena al completar un nivel
- **Música de Game Over**: Suena cuando el jugador pierde

## 🎨 Diseño Visual

- **Tema de Menú**: Texto de estilo digital con resaltados verdes
- **Interfaz de Juego**: Barra de estado superior con información del juego
- **Animación de Tanques**: Sprites direccionales para tanques
- **Explosiones**: Retroalimentación visual para destrucción
- **Barras de Salud**: Indicador visual de la salud del tanque

## 🔍 Aspectos Técnicos Destacados

### Modo Pantalla Completa

Implementa escalado adaptativo con preservación de relación de aspecto usando:

- **Letterboxing/Pillarboxing**: Agrega barras negras para mantener la relación de aspecto
- **Escalado de Superficie**: Escala suavemente la superficie del juego

### Manejo de Entrada

Sistema de entrada unificado que soporta:

- **Controles de Teclado**: Usando mapeo de teclas dedicado
- **Joystick/Gamepad**: Con manejo de zona muerta y mapeo de botones
- **Debouncing de Entrada**: Previene la repetición rápida de entrada

### Gestión de Estado de Juego

Clara separación de:

- **Estado de Menú**: Menú principal, menú de pausa, etc.
- **Estado de Gameplay**: Gameplay activo
- **Estados de Victoria/Derrota**: Estados de fin de juego con transiciones

## 📝 Créditos

- **Desarrollo**: Yefry Shephard J 22-SISN-2-020
- **Materia**: Inteligencia Artificial
- **Recursos**: Varias fuentes incluidas en la carpeta de assets
- **Bibliotecas**: Pygame y Pygame-menu

---

<div align="center">

## 🎮 ¡Juega y diviértete! 🎮

</div>

