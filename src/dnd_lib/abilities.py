from dataclasses import dataclass
import random
import typing as t

from pydantic import BaseModel, Field

from .dices import D20


_T_ABILITY = t.TypeVar('_T_ABILITY', bound='Ability')


class Ability(BaseModel):    
    type: str = Field(..., allow_mutation=False)
    score: int = Field(min=1, default_factory=D20)
    
    class Config:
        validate_assignment = True
    
    @property
    def modifier(self) -> int:
        return (self.score - 10) // 2


@dataclass
class AbilitySet(t.Collection[_T_ABILITY]):
    _abilities: dict[str, _T_ABILITY]
    
    def __init__(self, **kwargs: _T_ABILITY | str):
        if len(kwargs) == 0:
            raise ValueError("No abbilities given. Required at least one.")
        
        self._abilities = {}
        ability_names = []        
        for ability_key, ability in kwargs.items():
            if isinstance(ability, str):
                ability = _T_ABILITY.randomize(ability)
            elif not isinstance(ability, Ability):
                raise TypeError(f"One of given abilities has improper type: {ability.__class__}")
            
            if ability.type in ability_names:
                raise ValueError(f"Two abilities with the same name appeared in arguments: {ability.type}")
            
            ability_names.append(ability.type)
            self._abilities.update({ability_key: ability})
            
    def __contains__(self, __x: object) -> bool:
        return self._abilities.__contains__(__x)
    
    def __iter__(self) -> t.Iterator[_T_ABILITY]:
        return self._abilities.values().__iter__()
    
    def __len__(self) -> int:
        return self._abilities.__len__()
    
    def __getitem__(self, key: str) -> _T_ABILITY:
        return self._abilities.get(key)
    
    def get_by_type(self, type_: str) -> _T_ABILITY:
        for ability in self:
            if ability.type == type_:
                return ability
        raise ValueError(f"Ability of given type not found: {type_}")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._abilities})"
