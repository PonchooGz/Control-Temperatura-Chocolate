import machine
import time
import onewire
import ds18x20

# --- 1. Configuración de Hardware ---
pin_datos = machine.Pin(4) 
sensor_ds = ds18x20.DS18X20(onewire.OneWire(pin_datos))
roms = sensor_ds.scan()

# PWM por hardware a 1 Hz para el Relevador de Estado Sólido
ssr_pwm = machine.PWM(machine.Pin(2), freq=1)
ssr_pwm.duty(0)

def leer_temperatura():
    if roms:
        sensor_ds.convert_temp()
        time.sleep_ms(750) 
        return sensor_ds.read_temp(roms[0])
    return None

# --- 2. Parámetros del Controlador PI ---
Kp = 6.0     
Ki = 0.02
setpoint = 50.0 

print("Iniciando Controlador PI y guardando datos en 'datos_pi.csv'...")

# --- Inicialización del Archivo CSV ---
# Abrimos el archivo en modo escritura ('w') para limpiar datos anteriores
try:
    with open('datos_pi.csv', 'w') as archivo:
        archivo.write("Tiempo(s),Temperatura(C)\n")
except Exception as e:
    print("Error al crear el archivo:", e)

integral = 0.0
tiempo_inicio = time.ticks_ms()
tiempo_previo = tiempo_inicio

# --- 3. Lazo de Control Cerrado ---
while True:
    try:
        temp_actual = leer_temperatura()
        tiempo_actual = time.ticks_ms()
        
        if temp_actual is None:
            print("Error crítico de sensor. Apagando el sistema.")
            ssr_pwm.duty(0)
            break
            
        # Calcular el tiempo transcurrido en segundos para el PID (dt)
        dt = time.ticks_diff(tiempo_actual, tiempo_previo) / 1000.0
        if dt <= 0: dt = 0.01 
            
        # Calcular el tiempo total transcurrido desde el inicio para el CSV
        tiempo_total_segundos = time.ticks_diff(tiempo_actual, tiempo_inicio) / 1000.0
            
        error = setpoint - temp_actual
        
        # Acción Proporcional
        P = Kp * error
        
        # Acción Integral (Cálculo temporal)
        integral_temporal = integral + (error * dt)
        I = Ki * integral_temporal
        
        # Salida Provisional
        salida_pi = P + I
        
        # --- 4. ANTI-WINDUP INDUSTRIAL (Back-Calculation) ---
        if salida_pi > 100.0:
            salida_pi = 100.0
            integral = (100.0 - P) / Ki  
        elif salida_pi < 0.0:
            salida_pi = 0.0
            integral = (0.0 - P) / Ki    
        else:
            integral = integral_temporal 
            
        # --- 5. Ejecución del PWM ---
        duty_cycle = int((salida_pi / 100.0) * 1023)
        ssr_pwm.duty(duty_cycle)
        
        # Imprimir en consola
        print(f"T: {tiempo_total_segundos:.1f}s | Temp: {temp_actual:.2f}C | Err: {error:.2f} | P: {P:.1f}% | I: {I:.1f}% | PWM: {salida_pi:.1f}%")
        
        # --- 6. Guardar en el archivo CSV ---
        # Abrimos en modo 'a' (append) para añadir líneas sin borrar lo anterior
        with open('datos_pi.csv', 'a') as archivo:
            # Escribimos el tiempo total y la temperatura separados por coma
            archivo.write(f"{tiempo_total_segundos:.2f},{temp_actual:.2f}\n")
        
        tiempo_previo = tiempo_actual
        
    except KeyboardInterrupt:
        # Esto permite detener el programa limpiamente con STOP en Thonny
        print("\nPrueba detenida por el usuario. Apagando SSR.")
        ssr_pwm.duty(0)
        break
    except Exception as e:
        print("\nError inesperado:", e)
        ssr_pwm.duty(0)
        break