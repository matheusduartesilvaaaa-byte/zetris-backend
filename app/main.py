from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import auth, customers, products, sales

app = FastAPI(
    title="Zetris API",
    description="Backend para o sistema de gestão Zetris",
    version="1.0.0"
)

# Configuração do CORS para permitir que o Frontend se conecte à API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua pelo link do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o banco de dados (cria as tabelas se não existirem)
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {
        "message": "Zetris API está online!",
        "docs": "/docs"
    }

# Inclui as rotas do sistema
app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(sales.router)
