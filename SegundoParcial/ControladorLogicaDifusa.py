import machine
import time
import onewire
import ds18x20

# --- 1. Configuración de Hardware ---
pin_datos = machine.Pin(4) 
sensor_ds = ds18x20.DS18X20(onewire.OneWire(pin_datos))
roms = sensor_ds.scan()

ssr_pwm = machine.PWM(machine.Pin(2), freq=1)
ssr_pwm.duty(0)

setpoint = 50.0 

def leer_temperatura():
    if roms:
        sensor_ds.convert_temp()
        time.sleep_ms(750) 
        return sensor_ds.read_temp(roms[0])
    return None

# --- 2. Funciones de Pertenencia (Fuzificación) ---
def grado_frio(error):
    if error >= 2.0: return 1.0
    elif 0.0 < error < 2.0: return error / 2.0
    else: return 0.0

def grado_ideal(error):
    if -1.0 <= error <= 1.0: return 1.0 - abs(error)
    else: return 0.0

def grado_caliente(error):
    if error <= -1.0: return 1.0
    elif -1.0 < error < 0.0: return abs(error)
    else: return 0.0

def grado_subiendo(delta_t):
    if delta_t >= 0.2: return 1.0
    elif 0.0 < delta_t < 0.2: return delta_t / 0.2
    else: return 0.0

print("Iniciando Controlador Difuso y guardando datos en 'datos_difuso.csv'...")

# --- Inicialización del Archivo CSV ---
try:
    with open('datos_difuso.csv', 'w') as archivo:
        archivo.write("Tiempo(s),Temperatura(C)\n")
except Exception as e:
    print("Error al crear el archivo:", e)

temp_previa = leer_temperatura()
if temp_previa is None: temp_previa = 20.0

tiempo_inicio = time.ticks_ms()
tiempo_previo = tiempo_inicio

# --- 3. Bucle Principal ---
while True:
    try:
        temp_actual = leer_temperatura()
        tiempo_actual = time.ticks_ms()
        
        if temp_actual is None:
            print("Error de sensor. Apagando.")
            ssr_pwm.duty(0)
            break
            
        dt = time.ticks_diff(tiempo_actual, tiempo_previo) / 1000.0
        if dt <= 0: dt = 0.01 
            
        tiempo_total_segundos = time.ticks_diff(tiempo_actual, tiempo_inicio) / 1000.0
            
        error = setpoint - temp_actual
        delta_t = (temp_actual - temp_previa) / dt  # Velocidad de cambio
        
        # Evaluar grados de pertenencia
        frio = grado_frio(error)
        ideal = grado_ideal(error)
        caliente = grado_caliente(error)
        subiendo = grado_subiendo(delta_t)
        
        # --- 4. Base de Reglas y Defuzificación (Sugeno) ---
        OUT_ALTA = 100.0
        OUT_MANTENIMIENTO = 15.0
        OUT_APAGADO = 0.0
        
        peso_total = 0.0
        salida_difusa = 0.0
        
        # Regla 1: SI está Frío, ENTONCES potencia Alta.
        peso1 = frio
        salida_difusa += peso1 * OUT_ALTA
        peso_total += peso1
        
        # Regla 2: SI está Ideal Y NO está Subiendo muy rápido, ENTONCES Mantenimiento.
        peso2 = min(ideal, 1.0 - subiendo)
        salida_difusa += peso2 * OUT_MANTENIMIENTO
        peso_total += peso2
        
        # Regla 3: SI está Caliente O (está Ideal Y Subiendo rápido), ENTONCES Apagado.
        peso3 = max(caliente, min(ideal, subiendo))
        salida_difusa += peso3 * OUT_APAGADO
        peso_total += peso3
        
        # Evitar división por cero
        if peso_total == 0:
            salida_final = 0.0
        else:
            salida_final = salida_difusa / peso_total
            
        # Saturación de seguridad
        if salida_final > 100: salida_final = 100
        if salida_final < 0: salida_final = 0
            
        # Enviar al hardware
        duty_cycle = int((salida_final / 100.0) * 1023)
        ssr_pwm.duty(duty_cycle)
        
        # Imprimir en consola
        print(f"T: {tiempo_total_segundos:.1f}s | Temp: {temp_actual:.2f}C | Err: {error:.2f} | Difuso: {salida_final:.1f}%")
        
        # --- 5. Guardar en el archivo CSV ---
        with open('datos_difuso.csv', 'a') as archivo:
            archivo.write(f"{tiempo_total_segundos:.2f},{temp_actual:.2f}\n")
        
        temp_previa = temp_actual
        tiempo_previo = tiempo_actual
        
    except KeyboardInterrupt:
        print("\nPrueba detenida por el usuario. Apagando SSR.")
        ssr_pwm.duty(0)
        break
    except Exception as e:
        print("\nError inesperado:", e)
        ssr_pwm.duty(0)
        break