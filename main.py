# ============================================================
# SISTEMA DE CONTROLE DE ALMOXARIFADO
# Versao atual em producao
# ============================================================

from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    create_engine,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker

# ------------------------------------------------------------
# CONEXAO COM O BANCO
# ------------------------------------------------------------

engine = create_engine(
    "mysql+pymysql://root:root@localhost:3306/almoxarifado",
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# ------------------------------------------------------------
# MODELOS
# ------------------------------------------------------------

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    unidade_medida = Column(String(20), nullable=False)
    quantidade_estoque = Column(Integer, nullable=False, default=0)
    valor_unitario = Column(Numeric(10, 2), nullable=False)
    limite_minimo = Column(Integer, nullable=False, default=0)
    limite_maximo = Column(Integer, nullable=False, default=100)
    criado_em = Column(DateTime, nullable=False, default=datetime.now)


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo = Column(Enum("ENTRADA", "SAIDA"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_movimentacao = Column(DateTime, nullable=False, default=datetime.now)


# ------------------------------------------------------------
# SCHEMAS
# ------------------------------------------------------------

class ProdutoEntrada(BaseModel):
    nome: str
    unidade_medida: str
    quantidade_estoque: int
    valor_unitario: float
    limite_minimo: int
    limite_maximo: int


class ProdutoAtualizacao(BaseModel):
    nome: str
    unidade_medida: str
    valor_unitario: float


class MovimentacaoEntrada(BaseModel):
    produto_id: int
    quantidade: int


# ------------------------------------------------------------
# APLICACAO
# ------------------------------------------------------------

app = FastAPI(title="Sistema de Almoxarifado")


# ------------------------------------------------------------
# PRODUTOS
# ------------------------------------------------------------

@app.get("/produtos")
def listar_produtos():
    sessao = SessionLocal()
    try:
        produtos = sessao.query(Produto).all()
        return produtos
    finally:
        sessao.close()


@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: str):
    sessao = SessionLocal()
    try:
        comando = text("SELECT * FROM produtos WHERE id = " + produto_id)
        resultado = sessao.execute(comando).mappings().all()
        return resultado
    finally:
        sessao.close()


@app.post("/produtos", status_code=201)
def cadastrar_produto(dados: ProdutoEntrada):
    sessao = SessionLocal()
    try:
        produto = Produto(
            nome=dados.nome,
            unidade_medida=dados.unidade_medida,
            quantidade_estoque=dados.quantidade_estoque,
            valor_unitario=dados.valor_unitario,
            limite_minimo=dados.limite_minimo,
            limite_maximo=dados.limite_maximo,
        )
        sessao.add(produto)
        sessao.commit()
        sessao.refresh(produto)
        return {"id": produto.id, "nome": produto.nome}
    except Exception as erro:
        sessao.rollback()
        print(erro)
        raise HTTPException(status_code=500, detail="erro ao cadastrar produto")
    finally:
        sessao.close()


@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, dados: ProdutoAtualizacao):
    sessao = SessionLocal()
    try:
        produto = sessao.query(Produto).filter(Produto.id == produto_id).first()
        produto.nome = dados.nome
        produto.unidade_medida = dados.unidade_medida
        produto.valor_unitario = dados.valor_unitario
        sessao.commit()
        return {"mensagem": "produto atualizado"}
    except Exception as erro:
        sessao.rollback()
        print(erro)
        raise HTTPException(status_code=500, detail="erro ao atualizar produto")
    finally:
        sessao.close()


@app.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int):
    sessao = SessionLocal()
    try:
        produto = sessao.query(Produto).filter(Produto.id == produto_id).first()
        sessao.delete(produto)
        sessao.commit()
        return {"mensagem": "produto excluido"}
    except Exception as erro:
        sessao.rollback()
        print(erro)
        raise HTTPException(status_code=500, detail="erro ao excluir produto")
    finally:
        sessao.close()


# ------------------------------------------------------------
# MOVIMENTACOES
# ------------------------------------------------------------

@app.get("/movimentacoes")
def listar_movimentacoes():
    sessao = SessionLocal()
    try:
        comando = text(
            "SELECT m.id, p.nome, m.tipo, m.quantidade, m.data_movimentacao "
            "FROM movimentacoes m "
            "INNER JOIN produtos p ON p.id = m.produto_id"
        )
        return sessao.execute(comando).mappings().all()
    finally:
        sessao.close()


# Registra a entrada de itens e soma no saldo do produto
@app.post("/movimentacoes/entrada", status_code=201)
def registrar_entrada(dados: MovimentacaoEntrada):
    sessao = SessionLocal()
    try:
        movimentacao = Movimentacao(
            produto_id=dados.produto_id,
            tipo="ENTRADA",
            quantidade=dados.quantidade,
        )
        sessao.add(movimentacao)

        produto = sessao.query(Produto).filter(Produto.id == dados.produto_id).first()
        produto.quantidade_estoque = produto.quantidade_estoque + dados.quantidade

        sessao.commit()
        return {"mensagem": "entrada registrada"}
    except Exception as erro:
        sessao.rollback()
        print(erro)
        raise HTTPException(status_code=500, detail="erro ao registrar entrada")
    finally:
        sessao.close()


# Registra a saida de itens e subtrai do saldo do produto
@app.post("/movimentacoes/saida", status_code=201)
def registrar_saida(dados: MovimentacaoEntrada):
    sessao = SessionLocal()
    try:
        movimentacao = Movimentacao(
            produto_id=dados.produto_id,
            tipo="SAIDA",
            quantidade=dados.quantidade,
        )
        sessao.add(movimentacao)

        produto = sessao.query(Produto).filter(Produto.id == dados.produto_id).first()
        produto.quantidade_estoque = produto.quantidade_estoque - dados.quantidade

        sessao.commit()
        return {"mensagem": "saida registrada"}
    except Exception as erro:
        sessao.rollback()
        print(erro)
        raise HTTPException(status_code=500, detail="erro ao registrar saida")
    finally:
        sessao.close()
