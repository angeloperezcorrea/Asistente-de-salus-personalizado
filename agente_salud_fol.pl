% Definir hechos sobre el estado del atleta
atleta(juan).
atleta(maria).

% Datos sobre la salud del atleta (frecuencia cardíaca, hidratación, fatiga)
frecuencia_cardiaca_alta(juan).
hidratacion_baja(juan).
fatiga_alta(juan).

frecuencia_cardiaca_normal(maria).
hidratacion_optima(maria).
fatiga_baja(maria).

% Reglas para generar alertas
alerta(Atleta, 'Reducir ritmo y beber agua') :-
    frecuencia_cardiaca_alta(Atleta),
    hidratacion_baja(Atleta).

alerta(Atleta, 'Descansar inmediatamente') :-
    frecuencia_cardiaca_alta(Atleta),
    fatiga_alta(Atleta).

alerta(Atleta, 'Estado óptimo, continuar entrenamiento') :-
    frecuencia_cardiaca_normal(Atleta),
    hidratacion_optima(Atleta),
    fatiga_baja(Atleta).

% Consultas para verificar el estado del atleta
tomar_decision(Atleta, Recomendacion) :-
    alerta(Atleta, Recomendacion).
