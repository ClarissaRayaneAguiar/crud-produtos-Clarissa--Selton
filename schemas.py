from pydantic import BaseModel
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    categoria: str
    quantidade: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel): 
    nome: Optional[str] = None
    preco: Optional[float] = None
    categoria: Optional[str] = None
    quantidade: Optional[int] = None

class ProdutoResponse(ProdutoBase):
    id: int
    class Config:
        from_attributes = True