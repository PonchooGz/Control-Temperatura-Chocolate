# Sistema de Control Térmico para Atemperado de Chocolate 🍫

Este repositorio contiene los códigos fuente en MicroPython y los scripts de análisis en MATLAB desarrollados para el proyecto de Control Avanzado (Semestre 2026A - UAEMex). El objetivo del sistema es gobernar la inercia térmica de un baño maría para mantener el chocolate de cobertura dentro de un rango seguro (48°C - 50°C), evitando la ebullición del agua.

**Integrantes del Equipo:**
* Alfonso Ramírez González
* Javier Gonzalez Estrada
* Rafael Arriaga Valencia

---

## 📁 Estructura del Repositorio

El proyecto se divide en dos fases de desarrollo correspondientes a las entregas de la asignatura:

### 1. Primer Avance: Control Clásico ON/OFF (PrimerParcial)
Contiene la implementación inicial del sistema térmico.
* **Hardware:** ESP32, Relevador de Estado Sólido (SSR) y termopar con módulo MAX6675.
* **Lógica:** Controlador tipo ON/OFF con histéresis programada.
* **Archivo principal:** `MedicionTemperaturaONOFF.py`

### 2. Control PI y Lógica Difusa (SegundoParcial)
Contiene la evolución del sistema utilizando controladores continuos y un sensor digital para mayor precisión y mitigación de ruido.
* **Hardware:** ESP32, Relevador de Estado Sólido (SSR) y sensor sumergible DS18B20 (OneWire).
* **Controlador 1:** PI con sintonización por curva de reacción y mecanismo Anti-Windup tipo *Back-Calculation* (`ControlPI.py`).
* **Controlador 2:** Inteligencia Artificial basada en Lógica Difusa tipo Sugeno (`ControladorLogicaDifusa.py`).
* **Análisis de Datos:** Ambos códigos en MicroPython incluyen un Datalogger interno que exporta la respuesta del sistema a archivos CSV. Se incluye el script `RespuestaPI_Difusa.m` para renderizar las curvas de comportamiento en MATLAB.

---

## ⚙️ Reproducibilidad y Ejecución

Para reproducir los controladores:
1. Conectar el sensor DS18B20 al pin GPIO 4 (con resistencia pull-up de 4.7kΩ) y el SSR al pin GPIO 2 del ESP32.
2. Cargar el script deseado (`ControlPI.py` o `ControladorLogicaDifusa.py`) utilizando el entorno Thonny.
3. El sistema comenzará a modular el PWM a 1 Hz y registrará automáticamente los datos en la memoria flash interna del ESP32.
4. Al detener la ejecución, descargar el archivo `.csv` generado y ejecutar `RespuestaPI_Difusa.m` en MATLAB asegurándose de que ambos archivos estén en el mismo directorio.
