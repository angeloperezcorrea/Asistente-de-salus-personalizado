from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI  # Cambio de importación
from langchain.tools import Tool
import random
import os
import time
import sqlite3
from pyswip import Prolog

#  Configuración del modelo de lenguaje
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "tu-clave-aqui")  
llm = ChatOpenAI(model_name="gpt-4", temperature=0.5, openai_api_key=OPENAI_API_KEY)

#  Memoria para recordar datos del corredor
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

#  Configuración de la base de datos para almacenamiento histórico
conn = sqlite3.connect("athlete_data.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS athlete_monitoring (
                    timestamp TEXT,
                    heart_rate INTEGER,
                    hydration REAL,
                    fatigue REAL
                )''')
conn.commit()

#  Sensores simulados para monitorear salud del atleta
def get_heart_rate():
    return random.randint(120, 190)  # Simulación de ritmo cardíaco

def get_hydration_level():
    return random.uniform(0.3, 1.0)  # Simulación de nivel de hidratación (0 a 1)

def get_fatigue():
    return random.uniform(0, 1.0)  # Simulación de nivel de fatiga (0 a 1)

#  Definición de herramientas
heart_rate_tool = Tool(
    name="HeartRateSensor",
    func=get_heart_rate,
    description="Obtiene la frecuencia cardíaca del atleta en tiempo real."
)

hydration_tool = Tool(
    name="HydrationSensor",
    func=get_hydration_level,
    description="Obtiene el nivel de hidratación del atleta en tiempo real."
)

fatigue_tool = Tool(
    name="FatigueSensor",
    func=get_fatigue,
    description="Obtiene el nivel de fatiga del atleta en tiempo real."
)

#  Definir el agente con LangChain
agent = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    tools=[heart_rate_tool, hydration_tool, fatigue_tool],
    llm=llm,
    verbose=True,
    memory=memory,
)

#  Implementación del Algoritmo A*
def heuristic(heart_rate, hydration, fatigue):
    return (heart_rate - 140) + ((1.0 - hydration) * 100) + (fatigue * 100)

def monitor_atleta():
    hr = get_heart_rate()
    hydration = get_hydration_level()
    fatigue = get_fatigue()
    f_score = heuristic(hr, hydration, fatigue)
    
    alertas = []
    
    if f_score > 150:
        alertas.append("⚠️ Estado crítico, reduzca la velocidad y beba agua.")
    elif f_score > 100:
        alertas.append("⚠️ Atención: tome precauciones, su fatiga e hidratación están en niveles riesgosos.")
    elif hr > 170:
        alertas.append("⚠️ Reduzca el ritmo, su frecuencia cardíaca es demasiado alta.")
    elif hr > 150:
        alertas.append("⚠️ Atención: su frecuencia cardíaca está elevada.")
    
    if hydration < 0.5:
        alertas.append("⚠️ Hidratación baja, beba agua en los próximos minutos.")
    
    # Guardar datos en la base de datos
    cursor.execute("INSERT INTO athlete_monitoring (timestamp, heart_rate, hydration, fatigue) VALUES (datetime('now'), ?, ?, ?)", (hr, hydration, fatigue))
    conn.commit()
    
    return alertas if alertas else ["✅ Ritmo y estado óptimos."]

#  Monitoreo continuo en tiempo real
if __name__ == "__main__":
    print(" Monitoreo en tiempo real del atleta 🏃")
    while True:
        alertas = monitor_atleta()
        for alerta in alertas:
            print(alerta)
        time.sleep(10)  # Simula monitoreo en tiempo real cada 10 segundos