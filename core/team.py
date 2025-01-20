from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum
import json
from datetime import datetime
import time

class TeamRole(Enum):
    LEADER = "leader"
    SPECIALIST = "specialist"
    CRITIC = "critic"
    SYNTHESIZER = "synthesizer"

@dataclass
class ConversationLog:
    """Classe para registrar a conversa entre agentes"""
    timestamp: str
    agent: str
    role: str
    message: str
    message_type: str

@dataclass
class TeamConfig:
    team_name: str
    objective: str
    collaboration_style: str = "Collaborative and respectful"
    max_rounds: int = 3
    show_thoughts: bool = True

@dataclass
class SharedMemory:
    """Memória compartilhada entre os agentes"""
    current_discussion: List[Dict] = field(default_factory=list)
    context: Dict = field(default_factory=dict)
    
    def add_response(self, agent_name: str, expertise: List[str], content: str, 
                    response_type: str):
        self.current_discussion.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "expertise": expertise,
            "content": content,
            "type": response_type
        })
    
    def get_discussion_summary(self) -> str:
        return json.dumps(self.current_discussion, indent=2, ensure_ascii=False)
    
    def get_previous_responses(self, exclude_agent: str = None) -> List[Dict]:
        if exclude_agent:
            return [r for r in self.current_discussion if r["agent"] != exclude_agent]
        return self.current_discussion

@dataclass
class AgentTeam:
    config: TeamConfig
    memory_manager: 'KnowledgeBaseChatManager'
    llm: 'OpenAI'
    shared_memory: SharedMemory = field(default_factory=SharedMemory)
    leader: Optional['BaseAgent'] = None
    agents: List['BaseAgent'] = field(default_factory=list)
    conversation_history: List[ConversationLog] = field(default_factory=list)
    
    def _log_conversation(self, agent: str, role: str, message: str, message_type: str):
        """Registra e exibe uma entrada na conversa"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log = ConversationLog(
            timestamp=timestamp,
            agent=agent,
            role=role,
            message=message,
            message_type=message_type
        )
        self.conversation_history.append(log)
        
        # Formatação do display
        role_color = {
            'leader': '\033[95m',  # magenta
            'specialist': '\033[94m',  # blue
            'critic': '\033[91m',  # red
            'synthesizer': '\033[92m',  # green
            'system': '\033[93m'  # yellow
        }
        type_symbol = {
            'thought': '💭',
            'response': '💬',
            'critique': '🔍',
            'synthesis': '✨',
            'info': 'ℹ️'
        }
        
        color = role_color.get(role, '\033[0m')
        symbol = type_symbol.get(message_type, '•')
        
        print(f"\n{color}[{timestamp}] {symbol} {agent} ({role}):\033[0m")
        print(f"{message}\n")
        print("-" * 80)
        time.sleep(1)
    
    def add_leader(self, agent: 'BaseAgent') -> None:
        """Adiciona um agente líder ao time"""
        self.leader = agent
        self._log_conversation(
            agent=agent.config.name,
            role="leader",
            message=f"Entrei no time como líder. Minha expertise: {', '.join(agent.config.expertise)}",
            message_type="thought"
        )
    
    def add_agent(self, agent: 'BaseAgent') -> None:
        """Adiciona um agente especialista ao time"""
        self.agents.append(agent)
        self._log_conversation(
            agent=agent.config.name,
            role="specialist",
            message=f"Entrei no time como especialista. Minha expertise: {', '.join(agent.config.expertise)}",
            message_type="thought"
        )

    def _get_relevant_documents(self, query: str) -> List[Dict]:
        """Busca documentos relevantes para a query"""
        results = self.memory_manager.search_knowledge_base(
            query=query,
            k=3,
            include_sources=True
        )
        
        self._log_conversation(
            "Sistema", "system",
            f"Encontrados {len(results)} documentos relevantes",
            "info"
        )
        
        return results
    
    def _get_agent_contribution(self, agent: 'BaseAgent', query: str, 
                              previous_responses: List[Dict],
                              relevant_docs: List[Dict]) -> str:
        """Obtém contribuição do agente considerando documentos e contexto"""
        docs_context = ""
        for doc in relevant_docs:
            docs_context += f"\nDocumento: {doc.get('filename', 'Sem nome')}\nConteúdo: {doc.get('content', 'Sem conteúdo')}\n"
        
        prompt = f"""
        {agent._create_system_prompt()}
        
        PERGUNTA ORIGINAL:
        {query}
        
        DOCUMENTOS RELEVANTES:
        {docs_context}
        
        DISCUSSÃO ATUAL:
        {json.dumps(previous_responses, indent=2, ensure_ascii=False)}
        
        INSTRUÇÕES:
        Como especialista em {', '.join(agent.config.expertise)}, forneça uma contribuição 
        que integre os documentos e o contexto da discussão.
        """
        
        return agent._get_llm_response(prompt)
    
    def _leader_guide_discussion(self, query: str, relevant_docs: List[Dict]) -> str:
        """Líder guia a discussão considerando documentos"""
        docs_context = ""
        for doc in relevant_docs:
            docs_context += f"\nDocumento: {doc.get('filename', 'Sem nome')}\nConteúdo: {doc.get('content', 'Sem conteúdo')}\n"
        
        prompt = f"""
        {self.leader._create_system_prompt()}
        
        DOCUMENTOS DISPONÍVEIS:
        {docs_context}
        
        DISCUSSÃO ATUAL:
        {self.shared_memory.get_discussion_summary()}
        
        INSTRUÇÕES:
        Como líder, analise a discussão e os documentos para guiar a equipe.
        """
        
        guidance = self.leader._get_llm_response(prompt)
        self._log_conversation(
            self.leader.config.name, "leader", guidance, "guidance"
        )
        return guidance
    
    def collaborate(self, query: str) -> str:
        """Processo colaborativo com acesso a documentos"""
        if not self.leader or not self.agents:
            raise ValueError("Team needs at least one leader and one agent")
            
        self.shared_memory = SharedMemory()
        relevant_docs = self._get_relevant_documents(query)
        
        self._log_conversation(
            self.leader.config.name, "leader",
            f"Iniciando análise da pergunta: '{query}'", "thought"
        )
        
        # Fase 1: Contribuições iniciais
        for agent in self.agents:
            previous_responses = self.shared_memory.get_previous_responses(agent.config.name)
            contribution = self._get_agent_contribution(
                agent, query, previous_responses, relevant_docs
            )
            
            self.shared_memory.add_response(
                agent.config.name,
                agent.config.expertise,
                contribution,
                "initial"
            )
            
            self._log_conversation(
                agent.config.name, "specialist",
                contribution, "response"
            )
        
        # Fase 2: Síntese e revisão
        final_response = self._leader_guide_discussion(query, relevant_docs)
        
        # Salvar na memória
        self.memory_manager.add_message("user", query)
        self.memory_manager.add_message("assistant", final_response)
        
        return final_response

@dataclass
class TeamFramework:
    """Framework para criar e gerenciar times de agentes"""
    memory_manager: 'KnowledgeBaseChatManager'
    llm: 'OpenAI'
    
    def create_team(
        self,
        team_name: str,
        objective: str,
        collaboration_style: str = "Collaborative and respectful"
    ) -> AgentTeam:
        """Cria um novo time de agentes"""
        config = TeamConfig(
            team_name=team_name,
            objective=objective,
            collaboration_style=collaboration_style
        )
        
        team = AgentTeam(
            config=config,
            memory_manager=self.memory_manager,
            llm=self.llm
        )
        
        print(f"\n{'='*80}")
        print(f"🌟 Time '{team_name}' criado!")
        print(f"📋 Objetivo: {objective}")
        print(f"{'='*80}\n")
        
        return team


