from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class AgentRole(Enum):
    LEADER = "leader"
    SPECIALIST = "specialist"

@dataclass
class AgentConfig:
    name: str
    expertise: List[str]
    personality: str
    temperature: float = 0.3
    max_tokens: int = 2000

@dataclass
class BaseAgent:
    config: AgentConfig
    llm: "OpenAI"
    
    def _create_system_prompt(self) -> str:
        return f"""Você é {self.config.name}, um especialista em {', '.join(self.config.expertise)}.
        Sua personalidade é {self.config.personality}.
        Responda sempre com base em sua expertise e mantenha sua personalidade consistente."""
    
    def _get_llm_response(self, prompt: str) -> str:
        response = self.llm.complete(prompt)
        return response.text
