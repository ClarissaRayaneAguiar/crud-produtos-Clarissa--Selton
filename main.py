from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/produtos", response_model=list[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()


@app.get("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@app.post("/produtos", status_code=status.HTTP_201_CREATED, response_model=schemas.ProdutoResponse)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = models.Produto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@app.put("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_total(produto_id: int, produto_atualizado: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    produto_db = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    for key, value in produto_atualizado.dict().items():
        setattr(produto_db, key, value)
    
    db.commit()
    return produto_db


@app.patch("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_parcial(produto_id: int, produto_data: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    produto_db = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    dados_atualizar = produto_data.dict(exclude_unset=True) # Pega apenas o que foi enviado
    for key, value in dados_atualizar.items():
        setattr(produto_db, key, value)
    
    db.commit()
    return produto_db


@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto_db = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto_db)
    db.commit()
    return None