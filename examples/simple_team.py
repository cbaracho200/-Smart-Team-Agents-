from smart_team_agents import TeamFramework, KnowledgeBaseChatManager
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def main():
    # Setup
    llm = OpenAI(model="gpt-4", temperature=0.3)
    framework = TeamFramework(
        memory_manager=KnowledgeBaseChatManager(
            collection_name="example_team",
            embedding_function=OpenAIEmbedding()
        ),
        llm=llm
    )
    
    # Criar time
    team = framework.create_team(
        team_name="Time de Exemplo",
        objective="Demonstrar o funcionamento do framework"
    )
    
    # Adicionar agentes
    team.add_leader(
        framework.create_agent(
            name="Coordenador",
            expertise=["Gestão de Projetos"],
            personality="Organizado e metódico"
        )
    )
    
    team.add_agent(
        framework.create_agent(
            name="Especialista Técnico",
            expertise=["Python", "Machine Learning"],
            personality="Analítico e detalhista"
        )
    )
    
    # Colaborar
    response = team.collaborate(
        "Como podemos implementar um sistema de classificação de documentos?"
    )
    
    print("\nResposta Final:")
    print(response)

if __name__ == "__main__":
    main()
