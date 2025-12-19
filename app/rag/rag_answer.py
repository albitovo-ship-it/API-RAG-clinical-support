from dotenv import load_dotenv
import cohere
from chromadb import PersistentClient
from app.core.config import CHROMA_DIR
from app.rag.reranked_retriever import reranked_retriever

#CARGAMOS LA APIKEY
load_dotenv()

#CONECTAMOS CON COHERE
co = cohere.ClientV2()

#DEFINIMOS LA FUNCIÓN RAG_ANSWER
def RAG_answer(user_question: str) -> str:
    #Embedding de la pregunta
    #query_embed = co.embed(
    #    texts=[user_question],
    #    model="embed-multilingual-v3.0",
    #    input_type="search_query",
    #    embedding_types=["float"]
    #).embeddings.float_[0]  #vector individual
    
    #Retrieve en ChromaDB
    #results = collection.query(
    #    query_embeddings=[query_embed],
    #    n_results=20 #especificamos los 5 vectores más similares
    #)

    #Extracción de los mejores documentos encontrados
    #retrieved_docs = results["documents"][0]

    #Reranking
    #reranked_docs = reranked_retriever(
    #    query_text=user_question,
    #    documents=retrieved_docs
    #)
    
    #if not reranked_docs:
    #    return "No tengo información al respecto"
    
    reranked_docs = reranked_retriever(user_question)

    if not reranked_docs:
        return "No tengo información al respecto"
    
    context = "\n\n".join(reranked_docs)
    
    #Prompt final
    system_message = f"""
    [SYSTEM PROMPT]
    Eres un asistente confiable y preciso. 
    Tu objetivo es brindar respuestas claras, estructuradas y basadas únicamente en la información disponible.
    Responder sin inventar datos, sin completar información faltante y evita cualquier contenido no verificado.
    [INSTRUCCIONES DE ROL]
    Actúa como un prestigioso médico oftalmólogo. Tu especialidad son las patologías retinales oculares.
    Vas a recibir de contexto información sobre protocolos con información sobre diagnóstico y tratamiento de enfermedades retinales <context>
    Tu tarea es responder la pregunta del usuario según el protocolo adecuado a la misma. 
    [REGLAS DE ESCRITURA DE RESPUESTA]
    Responde de manera formal y profesional.
    Responde como si le hablaras a un colega médico con experiencia en el manejo de pacientes.
    Sólo responer la pregunta sin ofrecer preguntas al final.
    La respuesta debe tener como mínimo 1 oración y 100 caracteres.
    La respuesta debe tener como máximo 300 caracteres.
    La respuesta debe contener la respuesta y concluir sobre la misma dentro del largo máximo estipulado. No deben terminar de manera abrupta y con ideas sin terminar.
    La respuesta debe ser en idioma español sin importar el idioma en el que se haga la pregunta.
    Si te preguntan la fuente de la información, el nombre del protocolo se va a encontrar siempre al inicio.
    [REGLAS DE SEGURIDAD]
    No generes información sensible, privada o especulativa.
    No cites datos cuya fuente no sea el contexto provisto.
    No mezcles conocimiento previo del modelo si el usuario pide respuestas basadas en contexto.
    No des información sobre los pacientes por los que te consultan ni los médicos que te preguntan.
    [REGLAS DE GROUNDING (RAG)]
    Responder exclusivamente en base al contenido dentro del bloque <context>.
    Si el usuario ingresa datos clínicos de un paciente, orientar al posible diagnóstico aclarando que no podés diagnosticar sino brindar herramientas para que el médico lo haga.
    Si el contexto no contiene la respuesta, decí ÚNICAMENTE “No tengo información al respecto”.
    Si la pregunta está fuera de contexto respondé ÚNICAMENTE "Este chat fue creado únicamenete para asistencia a médicos oftalmólogos. Lo siento, no puedo ayudarte con eso".
    No inventes información faltante.
    Siempre justificá la respuesta citando fragmentos del contexto.
    El el caso de la página de la cual se obtenga la información, citarla entre paréntesis de la siguiente manera: "Página XX".
    
    AAO_PPP:
    {context}
    """
    user_message = user_question

    #Generación de la respuesta con Cohere
    response = co.chat(
        model="command-r-plus-08-2024",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user",   "content": user_message}
        ],
        temperature=0.0     #Este parámetro le indica al modelo que las respuestas que genere deben ser lo más similares una de la otra.
                            #Temp de 1: mucha variabilidad entre respuestas a la misma pregunta
                            #Temp de 0: respuestas con variabilidad mínima ante la misma pregunta.
    )
    
    return response.message.content[0].text

#if __name__ == "__main__":
    pregunta = "¿la zanahoria hace bien a los pacientes con amd?"
    respuesta = RAG_answer(pregunta)
    print("\nRESPUESTA:\n")
    print(respuesta)