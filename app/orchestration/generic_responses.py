
#DEFINIMOS ALGUNAS PREGUNTAS:RESPUESTAS GENÉRICAS
GENERIC_RESPONSES = {
    #SALUDOS
    ("hola", "buen dia", "hello", "hi"): 
        "Hola. Soy un asistente clínico oftalmólogo. ¿En qué puedo ayudarte?",

    #AGRADECIMIENTOS
    ("gracias", "muchas gracias", "thanks", "thank you!"): 
        "De nada. Si tenés otra consulta, estoy disponible para ayudarte.",

    #DESPEDIDAS
    ("chau", "adios", "nos vemos", "hasta luego", "see you", "bye"): 
        "Hasta luego. Recordá que la información brindada no reemplaza el criterio médico.",

    #AYUDA
    ("que podes hacer", "qué podés hacer", "ayuda", "what can you do"): 
        "Puedo responder preguntas clínicas sobre patologías retinales basadas en los protocolos y guías adoptadas por la institución."
}

def get_generic_response(question: str) -> str | None:
    """
    Devuelve una respuesta fija si la pregunta coincide con alguna regla.
    Si no hay coincidencia, devuelve None.
    """
    q = question.lower().strip()

    for keywords, response in GENERIC_RESPONSES.items():
        for kw in keywords:
            if kw in q:
                return response

    return None