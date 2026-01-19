# Drawing With Your Hands

Aplicación de visión por computadora desarrollada en Python que permite dibujar en un lienzo digital mediante el seguimiento de gestos de la mano en tiempo real. Utiliza **MediaPipe** para la detección de puntos de referencia (landmarks) de la mano y **OpenCV** para el procesamiento de imágenes.

## Descripción Técnica

El sistema captura la entrada de video de la cámara web y procesa cada fotograma para detectar la mano del usuario. A través de la lógica de posicionamiento de los dedos (específicamente el índice, pulgar y meñique), el algoritmo determina el estado del sistema (dibujar, borrar, seleccionar color o ajustar tamaño) y renderiza los trazos correspondientes en una interfaz gráfica basada en OpenCV y Tkinter.

### Características Principales
* **Detección de manos en tiempo real:** Uso de `mediapipe.solutions.hands`.
* **Dibujo "en el aire":** Mapeo de coordenadas de la punta del dedo índice a la pantalla.
* **Interfaz Interactiva:** Selección de colores y herramientas mediante gestos espaciales.
* **Ajuste dinámico:** Modificación del grosor del pincel basado en la distancia euclidiana entre dedos.

## Tecnologías Utilizadas

* **Python 3.x**
* **OpenCV:** Procesamiento de imágenes y dibujo de primitivas.
* **MediaPipe:** Framework para la detección y seguimiento multimodal de la mano.
* **NumPy:** Operaciones matemáticas para cálculo de coordenadas.
* **Tkinter:** Gestión de ventanas e interfaz de usuario auxiliar.
