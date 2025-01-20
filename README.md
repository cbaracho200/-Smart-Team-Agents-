# Smart Team Agents 🤖🤝

Um framework Python para criar e gerenciar times de agentes inteligentes que trabalham colaborativamente, com suporte a análise de documentos e memória compartilhada.

## 🌟 Características

- 🤖 Criação simplificada de agentes especializados
- 🤝 Colaboração inteligente entre agentes
- 📚 Análise integrada de documentos (PDF, TXT, etc.)
- 🧠 Memória compartilhada entre agentes
- 📋 Sistema de logging detalhado
- 🎯 Fácil de usar - apenas 3-4 linhas de código

## 📦 Instalação

```bash
pip install smart-team-agents
```

## 🚀 Uso Rápido

```python
from smart_team_agents import TeamFramework, KnowledgeBaseChatManager
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. Setup
llm = OpenAI(model="gpt-4", temperature=0.3)
framework = TeamFramework(
    memory_manager=KnowledgeBaseChatManager(
        collection_name="my_team",
        embedding_function=OpenAIEmbedding()
    ),
    llm=llm
)

# 2. Criar time e adicionar agentes
team = framework.create_team(
    team_name="Time de Análise",
    objective="Análise multidisciplinar"
)

team.add_leader(
    framework.create_agent(
        name="Coordenador",
        expertise=["Metodologia Científica"],
        personality="Analítico"
    )
)

# 3. Obter resposta
response = team.collaborate("Sua pergunta aqui")
```

## 📚 Documentação Detalhada

### Estrutura de Diretórios

```
smart_team_agents/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── agent.py
│   ├── memory.py
│   └── team.py
├── utils/
│   ├── __init__.py
│   ├── logging.py
│   └── document_processor.py
└── examples/
    ├── simple_team.py
    └── document_analysis.py
```

### 1. Configuração Inicial

Para começar, você precisa de uma chave API do OpenAI:

```python
import os
os.environ["OPENAI_API_KEY"] = "sua-chave-api"
```

### 2. Criar um Time

```python
# Criar time
team = framework.create_team(
    team_name="Time de Análise",
    objective="Fornecer análises aprofundadas",
    collaboration_style="Colaborativo e construtivo"
)
```

### 3. Adicionar Agentes

```python
# Adicionar líder
team.add_leader(
    framework.create_agent(
        name="Coordenador",
        expertise=["Metodologia Científica", "Gestão do Conhecimento"],
        personality="Analítico e integrador"
    )
)

# Adicionar especialistas
team.add_agent(
    framework.create_agent(
        name="Especialista em IA",
        expertise=["Machine Learning", "Neural Networks"],
        personality="Técnico e inovador"
    )
)
```

### 4. Adicionar Documentos

```python
# Adicionar documentos para análise
knowledge_manager.add_document(
    "documento.pdf",
    metadata={"tipo": "artigo", "área": "IA"}
)
```

### 5. Colaborar

```python
# Obter resposta colaborativa
response = team.collaborate(
    "Como a IA está impactando a indústria?"
)
```

## 🎯 Exemplos

### Exemplo 1: Time Simples

```python
from smart_team_agents import TeamFramework, KnowledgeBaseChatManager

# Setup
framework = TeamFramework(...)

# Criar time
team = framework.create_team("Time Básico", "Análise geral")
team.add_leader(framework.create_agent(...))
team.add_agent(framework.create_agent(...))

# Usar
response = team.collaborate("Sua pergunta")
```

### Exemplo 2: Análise de Documentos

```python
# Setup com documentos
knowledge_manager = KnowledgeBaseChatManager(...)
knowledge_manager.add_document("relatório.pdf")
knowledge_manager.add_document("dados.csv")

# Criar time
framework = TeamFramework(memory_manager=knowledge_manager, ...)
team = framework.create_team("Time de Análise", "Análise de documentos")

# Adicionar especialistas
team.add_leader(...)
team.add_agent(...)

# Analisar documentos
response = team.collaborate("Analise os relatórios e forneça insights")
```

## 📋 Requisitos

- Python 3.8+
- llama-index
- openai
- langchain
- pydantic

## 🛠️ Desenvolvimento

Para contribuir com o projeto:

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/smart-team-agents.git
```

2. Instale em modo de desenvolvimento
```bash
pip install -e .
```

3. Execute os testes
```bash
pytest tests/
```

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ⚙️ Configuração Avançada

### Configuração de Memória

```python
knowledge_manager = KnowledgeBaseChatManager(
    collection_name="my_team",
    embedding_function=OpenAIEmbedding(),
    persist_directory="./knowledge_base",
    chunk_size=1000,
    chunk_overlap=20
)
```

### Configuração de Agentes

```python
agent = framework.create_agent(
    name="Especialista",
    expertise=["Área 1", "Área 2"],
    personality="Descritivo",
    temperature=0.3,
    max_tokens=2000
)
```

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de API Key**
```python
os.environ["OPENAI_API_KEY"] = "sua-chave"
```

2. **Erro de Memória**
```python
# Limpar memória
knowledge_manager.clear_chat()
```

3. **Documentos não encontrados**
```python
# Verificar documentos carregados
docs = knowledge_manager.list_documents()
print(docs)
```

## 📊 Performance

- Tempo médio de resposta: 2-5 segundos
- Uso de memória: ~500MB
- Suporte a múltiplos documentos simultâneos

## 🔄 Updates

v1.0.0 (2024-01-18)
- Lançamento inicial
- Suporte básico a times
- Integração com documentos

v1.1.0 (2024-01-25)
- Melhorias na memória compartilhada
- Novo sistema de logging
- Suporte a mais formatos de documento
