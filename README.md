Caracterización del Sistema de Temperatura de Chocolate

Universidad Autónoma Del Estado De México - Facultad de Ingeniería - Ingeniería en Electrónica -  Control Avanzado (2026-A) 

Profesor: Dr. Javier Salas García

Autores: 

 Alfonso Ramírez González

Javier Gonzalez Estrada

Rafael Arriaga Valencia

Objetivo General

Evaluar la respuesta térmica de un sistema de calentamiento de chocolate mediante la aplicación de un controlador ON/OFF para poder obtener la temperatura ideal a la que el chocolate se funde correctamente para su posterior uso como recubrimiento en un bombón.

Descripción del Repositorio

Este repositorio contiene los códigos fuente utilizados para la implementación y caracterización del sistema de baño maría controlado por un ESP32. El sistema utiliza un termopar tipo K (MAX6675) y un Relevador de Estado Sólido (SSR EARU 40A) para modular una resistencia calefactora a 127VAC.

Archivos

MedicionTemperaturaONOFF.py: Script de la primera iteración del proyecto (Control ON/OFF) con ventana de histéresis (48°C - 50°C).

Reproducibilidad (Metodología)

Para replicar la extracción de datos:

Realizar las conexiones según el diagrama esquemático incluido en el reporte principal.

Cargar el script MedicionTemperaturaONOFF.py al microcontrolador ESP32 mediante la IDE de Thonny.

Asegurarse que el chocolate se derrita y alcance una viscosidad aceptable para su uso como recubrimiento de un bombón. 
