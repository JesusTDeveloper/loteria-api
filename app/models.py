from pydantic import BaseModel
from typing import List, Optional

# Animalitos
class AnimalitoItem(BaseModel):
    time: str
    number: str
    animal: str
    image: Optional[str] = None  # <- imagen del animal

class AnimalitoBlock(BaseModel):
    lottery: str
    items: List[AnimalitoItem]

class AnimalitosResponse(BaseModel):
    date: str
    source: str
    count: int
    data: List[AnimalitoBlock]

# Loterías (triples, trío, terminales)
class TripleItem(BaseModel):
    time: str
    A: Optional[str] = None
    B: Optional[str] = None
    C: Optional[str] = None
    sign: Optional[str] = None
    value: Optional[str] = None  # solo en terminales

class TripleBlock(BaseModel):
    lottery: str
    image: Optional[str] = None   # <- imagen de la lotería (icono del header)
    items: List[TripleItem]

class LoteriasResponse(BaseModel):
    date: str
    source: str
    count: int
    data: List[TripleBlock]
