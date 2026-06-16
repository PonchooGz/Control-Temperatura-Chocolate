import machine
import time

# --- Configuración de Pines ---
# Pines del MAX6675 (Protocolo SPI manual / Bit-banging)
sck = machine.Pin(18, machine.Pin.OUT)
cs = machine.Pin(5, machine.Pin.OUT)
so = machine.Pin(19, machine.Pin.IN)

# Pin del Relevador de Estado Sólido (SSR)
ssr = machine.Pin(2, machine.Pin.OUT)

# Aseguramos que el relevador inicie apagado por seguridad
ssr.value(0) 

# --- Función para leer el MAX6675 ---
def leer_temperatura():
    """
    Lee los datos del MAX6675.
    Devuelve la temperatura en grados Celsius o 'None' si está desconectado.
    """
    cs.value(0)  # Seleccionamos el sensor para iniciar la comunicación
    time.sleep_us(10)
    
    data = 0
    # Leemos 16 bits del sensor
    for i in range(16):
        sck.value(1)
        time.sleep_us(1)
        data = (data << 1) | so.value() # Guardamos el bit leído
        sck.value(0)
        time.sleep_us(1)
    
    cs.value(1)  # Deseleccionamos el sensor

    # El bit 2 (contando desde 0 a la derecha) indica si el termopar está abierto/desconectado
    if data & 0x04:
        return None  # Retorna None indicando error crítico
    
    # Eliminamos los 3 bits de configuración/estado y calculamos la temperatura
    data >>= 3
    return data * 0.25 # Cada unidad equivale a 0.25 grados Celsius

# --- Bucle Principal de Control ---
print("Iniciando sistema de control de temperatura de la cafetera...")
print("Rango objetivo: 48°C a 50°C")

while True:
    temperatura = leer_temperatura()
    
    # 1. Validación de seguridad (¿Está conectado el termopar?)
    if temperatura is None:
        print("¡ALERTA! Termopar desconectado. Apagando resistencia por seguridad.")
        ssr.value(0) # Apagado forzoso
        
    else:
        # 2. Control con Histéresis
        print(f"Temperatura actual: {temperatura}°C", end=" -> ")
        
        if temperatura <= 48.0:
            ssr.value(1)  # Enciende la resistencia
            print("Estado: Calentando (SSR ON)")
            
        elif temperatura >= 50.0:
            ssr.value(0)  # Apaga la resistencia
            print("Estado: En reposo (SSR OFF)")
            
        else:
            # Si está entre 48 y 50, mantenemos el estado actual del relevador
            if ssr.value() == 1:
                print("Estado: Calentando para llegar a 50°C (SSR ON)")
            else:
                print("Estado: Enfriando hacia 48°C (SSR OFF)")
                
    # Esperamos 2 segundos antes de la siguiente lectura para no saturar el sensor
    time.sleep(2)
