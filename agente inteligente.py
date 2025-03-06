from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI  # Cambio de importación
from langchain.tools import Tool
import random
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "tu-clave-aqui")  
llm = ChatOpenAI(model_name="gpt-4", temperature=0.5, openai_api_key=OPENAI_API_KEY)


memory = ConversationBufferMemory(memory_key="history", return_messages=True)


def get_heart_rate():
    return random.randint(120, 190)  

def get_hydration_level():
    return random.uniform(0.3, 1.0)  


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


agent = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    tools=[heart_rate_tool, hydration_tool],
    llm=llm,
    verbose=True,
    memory=memory,
)


def monitor_atleta():
    hr = get_heart_rate()
    hydration = get_hydration_level()
    
    alertas = []
    
    if hr > 170:
        alertas.append("⚠️ Reduzca el ritmo, su frecuencia cardíaca es demasiado alta.")
    elif hr > 150:
        alertas.append("⚠️ Atención: su frecuencia cardíaca está elevada.")
    
    if hydration < 0.5:
        alertas.append("⚠️ Hidratación baja, beba agua en los próximos minutos.")
    
    return alertas if alertas else ["✅ Ritmo y estado óptimos."]


if __name__ == "__main__":
    print(" Monitoreo en tiempo real del atleta ")
    alertas = monitor_atleta()
    for alerta in alertas:
        print(alerta)
