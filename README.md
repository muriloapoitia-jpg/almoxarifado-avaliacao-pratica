# Sistema de Controle de Almoxarifado

Sistema informatizado utilizado pela empresa para o controle de insumos do almoxarifado
(materiais de limpeza). Esta é a versão atualmente em produção.

## Tecnologias

- Python 3
- FastAPI
- SQLAlchemy
- MySQL

## Como executar

**1. Criar e ativar o ambiente virtual**

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**3. Criar o banco de dados**

Abra o MySQL Workbench e execute o arquivo `database/script.sql` por completo.
Ele cria o banco `almoxarifado`, as tabelas e a carga inicial de dados.

**4. Conferir os dados de conexão**

A string de conexão está no início do arquivo `main.py`.
Ajuste usuário e senha conforme o MySQL da sua máquina.

**5. Subir o servidor**

```bash
uvicorn main:app --reload
```

O sistema ficará disponível em `http://localhost:8000`.
A documentação automática fica em `http://localhost:8000/docs`.

## Funcionalidades disponíveis hoje

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/produtos` | Lista os produtos cadastrados |
| GET | `/produtos/{id}` | Consulta um produto pelo id |
| POST | `/produtos` | Cadastra um novo produto |
| PUT | `/produtos/{id}` | Atualiza um produto |
| DELETE | `/produtos/{id}` | Exclui um produto |
| GET | `/movimentacoes` | Lista as movimentações registradas |
| POST | `/movimentacoes/entrada` | Registra entrada e soma no saldo do produto |
| POST | `/movimentacoes/saida` | Registra saída e subtrai do saldo do produto |

## Exemplos de requisição

**Cadastrar produto** — `POST /produtos`

```json
{
  "nome": "Sabao em Po 1kg",
  "unidade_medida": "CAIXA",
  "quantidade_estoque": 20,
  "valor_unitario": 16.40,
  "limite_minimo": 10,
  "limite_maximo": 100
}
```

**Registrar entrada** — `POST /movimentacoes/entrada`

```json
{
  "produto_id": 1,
  "quantidade": 10
}
```

**Registrar saída** — `POST /movimentacoes/saida`

```json
{
  "produto_id": 1,
  "quantidade": 5
}
```

## Estrutura das tabelas

**produtos**

| Coluna | Tipo |
|--------|------|
| id | INT AUTO_INCREMENT PK |
| nome | VARCHAR(100) |
| unidade_medida | VARCHAR(20) |
| quantidade_estoque | INT |
| valor_unitario | DECIMAL(10,2) |
| limite_minimo | INT |
| limite_maximo | INT |
| criado_em | DATETIME |

**movimentacoes**

| Coluna | Tipo |
|--------|------|
| id | INT AUTO_INCREMENT PK |
| produto_id | INT FK → produtos.id |
| tipo | ENUM('ENTRADA','SAIDA') |
| quantidade | INT |
| data_movimentacao | DATETIME |
