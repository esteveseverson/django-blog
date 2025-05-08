# 📚 Documentação do Projeto Django Blog

## 💡 Visão Geral
Projeto de estudo, fazendo um blog em Django. O projeto conta com leitura de blog sem autenticar, ou fazer o login para criar uma nova sala de conversa. Conta com busca por tópicos e mensagens mais recentes.

## 🗃️ Modelos (base/models.py)

`Topic`
- Campos:
  - name: CharField com máximo de 200 caracteres
- Retorno (__str__): nome do tópico

`Room`
- Campos:
  - host: chave estrangeira para User
  - topic: chave estrangeira para Topic
  - name: nome da sala
  - description: descrição opcional
  - participants: muitos para muitos com User
  - created_at, updated_at: timestamps automáticos
- Meta:
  - ordenação decrescente por updated_at e created_at
- Retorno (__str__): nome da sala

`Message`
- Campos:
  - user: autor da mensagem
  - room: sala relacionada
  - body: conteúdo da mensagem
  - created_at, updated_at: timestamps
- Retorno (__str__): primeiros 50 caracteres da mensagem

## 🔧 Views (base/views.py)
### Autenticação:
- login_page, logout_user, register_user

### Funcionalidades do Usuário:
- user_profile(pk): perfil do usuário com seus quartos e mensagens
- update_profile: atualiza username e email

### Home e Navegação:
- home: lista de salas e mensagens, com busca por tópico/nome
- topics_page: filtra tópicos por nome
- activity_page: últimas mensagens (3)

### Gerenciamento de Salas:
- room(pk): visualização de uma sala e envio de mensagens
- create_room, update_room, delete_room: CRUD de salas

### Gerenciamento de Mensagens:
- delete_message: exclusão se usuário for dono

## 📝 Formulários (base/forms.py)
`RoomForm`
- Baseado no modelo Room
- Campos excluídos: host, participants

`UserForm`
- Baseado no modelo User
- Campos incluídos: username, email

## ⚙️ Configurações Principais (django_blog/settings.py)
Apps instalados:
- Padrão Django + base, rest_framework, corsheaders

Middlewares relevantes:
- CorsMiddleware ativado
- Proteção CSRF, sessões, etc.

Banco de dados:
- SQLite (db.sqlite3)

Arquivos estáticos:
- static/ como diretório padrão

Internacionalização:
- Idioma: en-us
- Fuso horário: UTC

CORS:
- Todas as origens permitidas: CORS_ALLOW_ALL_ORIGINS = True

## Execução do projeto
O gerenciador de ambiente utilizado foi o UV, então utilizando o `uv run` ele já baixa todas as dependecias do projeto.
```
Após clonar o projeto, entre na pasta

uv run manage.py runserver
```
