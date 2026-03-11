# Sample Flask Auth

Este projeto é uma API de autenticação e gerenciamento de usuários feita com Flask, Flask-Login, SQLAlchemy e MySQL.

## Funcionalidades
- Cadastro de usuários com senha criptografada (bcrypt)
- Login e logout
- Atualização de senha
- Exclusão de usuários (restrições de permissão)
- Proteção de rotas com autenticação

## Requisitos
- Python 3.13+
- MySQL
- Flask
- Flask-Login
- SQLAlchemy
- bcrypt
- pymysql

## Instalação
1. Clone o repositório:
	 ```bash
	 git clone <url-do-repo>
	 ```
2. Crie e ative um ambiente virtual:
	 ```bash
	 python -m venv .venv
	 .venv\Scripts\activate
	 ```
3. Instale as dependências:
	 ```bash
	 pip install -r requirements.txt
	 ```
4. Configure o banco de dados MySQL conforme a string de conexão em `app.py`.

## Uso
- Para rodar o projeto:
	```bash
	python app.py
	```
- As rotas principais são:
	- `POST /user` — Cria usuário
	- `POST /login` — Login
	- `GET /logout` — Logout
	- `PUT /user/<id>` — Atualiza senha
	- `DELETE /user/<id>` — Deleta usuário

## Segurança
- As senhas são criptografadas com bcrypt e não podem ser recuperadas.
- Apenas administradores podem deletar outros usuários.
- Usuários comuns só podem alterar a própria senha.

## Docker
- Exemplo de uso com MySQL via Docker:
	```yaml
	version: '3'
	services:
		db:
			image: mysql:latest
			environment:
				MYSQL_ROOT_PASSWORD: admin123
				MYSQL_DATABASE: flask-crud
			ports:
				- "3306:3306"
			volumes:
				- mysql-data:/var/lib/mysql
	volumes:
		mysql-data:
	```

## Licença
MIT
# sample_flask_auth

Repositório criado para armazenar o código da API de autenticação com banco de dados. 