% =========================================================================
% Gráfica de Respuesta en Lazo Cerrado (Controlador PI / Difuso)
% Proyecto de Control Avanzado
% =========================================================================
clear; clc; close all;

%% 1. Importar los datos del Datalogger
% Asegúrate de que el nombre del archivo coincida con el que descargaste
datos = readmatrix('datos_pi.csv', 'NumHeaderLines', 1);
t = datos(:, 1);
temp = datos(:, 2);

%% 2. Crear la figura profesional
fig = figure('Name', 'Respuesta en Lazo Cerrado', 'Color', 'w');

% Graficar la temperatura real del agua (Línea gruesa y azul)
plot(t, temp, 'Color', [0 0.4470 0.7410], 'LineWidth', 2.5); 
hold on;

% Graficar la línea de la meta / Setpoint
setpoint = 50.0;
yline(setpoint, '--', 'Setpoint (50 °C)', 'LabelHorizontalAlignment', 'left', ...
    'FontSize', 11, 'LineWidth', 2, 'Color', [0.8500 0.3250 0.0980]);

%% 3. Formato para el Reporte
title('Respuesta del Controlador en Lazo Cerrado', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('Tiempo (segundos)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Temperatura (°C)', 'FontSize', 12, 'FontWeight', 'bold');

% Ajuste de cuadrícula y ejes
set(gca, 'FontSize', 11);
grid on;

% Leyenda explicativa
legend('Temperatura del Baño María', 'Referencia', 'Location', 'southeast', 'FontSize', 11);

%% 4. Exportar imagen
exportgraphics(fig, 'Grafica_Lazo_Cerrado.png', 'Resolution', 300);
disp('¡Listo! Gráfica generada y guardada como Grafica_Lazo_Cerrado.png en tu carpeta.');