from openai import OpenAI
import streamlit as st
import re
import time  # Importamos time para pausar entre caracteres

msg = []
base = ("Alex es un asistente financiero inteligente diseñado para ayudar a los usuarios a gestionar sus finanzas personales de manera eficiente. "
        "Mediante algoritmos avanzados de aprendizaje automático, Alex analiza ingresos, gastos y hábitos de consumo para ofrecer recomendaciones personalizadas "
        "y mejorar la toma de decisiones financieras.")

client = OpenAI(api_key="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")

st.title("Alex")

if "msg" not in st.session_state:
    st.session_state["msg"] = [{
        "role": "assistant",
        "content": "¡Hola! 👋 Soy Alex, tu asistente financiero personal. Estoy aquí para ayudarte a gestionar tu dinero de manera inteligente, "
                   "optimizar tus gastos y alcanzar tus metas financieras. 💰📊 Dime, ¿en qué puedo ayudarte hoy? 🚀"
    }]

# Función para mostrar mensaje con efecto de máquina de escribir
def mostrar_mensaje_progresivo(mensaje, rol, velocidad=0.02):
    placeholder = st.chat_message(rol).empty()
    texto = ""
    for char in mensaje:
        texto += char
        placeholder.markdown(texto)
        time.sleep(velocidad)

# Función para detectar LaTeX (opcional si usas markdown directamente en todo)
def mostrar_mensaje(mensaje, rol):
    if re.search(r"\$\$.*?\$\$|\$(.*?)\$", mensaje, re.DOTALL):
        st.chat_message(rol).markdown(mensaje, unsafe_allow_html=True)
    else:
        st.chat_message(rol).write(mensaje)

# Mostrar historial de mensajes anteriores
for msg in st.session_state["msg"]:
    mostrar_mensaje(msg["content"], msg["role"])

# Entrada del usuario
if userInput := st.chat_input():
    st.session_state["msg"].append({"role": "user", "content": userInput})
    st.chat_message("user").write(userInput)

    responder = client.responses.create(
        model="gpt-4o-mini",
        store=True,
        instructions=base,
        input=st.session_state["msg"],
        max_output_tokens=1000,
    )

    respuesta = responder.output_text
    st.session_state["msg"].append({"role": "assistant", "content": respuesta})
    
    # Mostrar con efecto de escritura
    mostrar_mensaje_progresivo(respuesta, "assistant")