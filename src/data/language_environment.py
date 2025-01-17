from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
import sys
import os
# sys.path.append("/u/buseskorkmaz/Bias-ILQL/")
from utils.cache import Cache


class Language_Observation(ABC):
    @abstractmethod
    def to_sequence(self) -> Tuple[List[str, Optional[float]], bool]:
        # returns a List of Tuples and a bool indicating terminal
        # each state Tuple should be: (str, None)
        # each action Tuple should be: (str, reward)
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def metadata(self) -> Optional[Dict[str, Any]]:
        return None


class Language_Environment(ABC):
    @abstractmethod
    def step(self, action: str) -> Tuple[Language_Observation, float, bool]:
        pass

    @abstractmethod
    def reset(self) -> Language_Observation:
        pass

    @abstractmethod
    def is_terminal(self) -> bool:
        pass

class Policy(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.cache = Cache()

    @abstractmethod
    def act(self, obs: Language_Observation) -> str:
        pass

    def train(self):
        pass

    def eval(self):
        pass

def interact_environment(env: Language_Environment, policy: Policy, obs: Optional[Language_Observation]=None):
    obs_sequence = []
    if obs is None:
        obs = env.reset()
    while not env.is_terminal():
        # print("INTERACTING")
        action = policy.act(obs)
        # if action != ' ' and action != '':
        # print("action:", action)
        new_obs, r, t = env.step(action)
        # print("New_obs", new_obs.__str__())
        # print("r", r, "t", t)
        obs_sequence.append((obs, action, r, t))
        obs = new_obs
    # obs_sequence.append((obs, None, 0, True))
    return obs, obs_sequence
