# Projeto Final - Infinity School: WTSA WayneTech SecureAccess

Sistema web full stack desenvolvido para o projeto final da Infinity School com o objetivo de gerenciar segurança, controle de acesso e recursos internos das Indústrias Wayne. A aplicação foi criada para permitir autenticação de usuários, controle por níveis de permissão, administração de recursos e visualização de informações relevantes em um dashboard. 

## Sobre o projeto

Este repositório contém o protótipo completo da aplicação, incluindo:

- backend em **Python/Flask** (`app.py`);
- telas de login, registro e dashboard;
- estilos CSS aplicados individualmente a cada página;
- scripts SQL para criar/seedar a base de dados usada pelo protótipo.

O objetivo principal é demonstrar uma aplicação web full‑stack funcional, com o servidor Flask servindo os templates e processando formulários.

A proposta do projeto exige uma aplicação web full stack que demonstre integração entre interface, regras de negócio e banco de dados. Neste repositório só estão os componentes de frontend e os arquivos de banco; o código do servidor pode ser acrescentado separadamente (por exemplo em Flask ou Node.js). 

## Objetivos

- Permitir o acesso apenas a usuários autorizados.
- Implementar autenticação e autorização com diferentes tipos de usuário.
- Gerenciar recursos internos, como equipamentos, veículos e dispositivos de segurança.
- Exibir um dashboard com informações relevantes sobre segurança, recursos e atividades.
- Demonstrar a integração entre interface, regras de negócio e banco de dados.

## Funcionalidades

- Cadastro de usuários.
- Login de usuários.
- Controle de acesso por perfil.
- Dashboard administrativo.
- Cadastro de recursos internos.
- Edição de recursos cadastrados.
- Gerenciamento de usuários.
- Registro e acompanhamento de informações relacionadas à segurança.

## Perfis de acesso

A interface contempla telas destinadas a distintos níveis de permissão — funcionalmente:

- **Funcionário:** visualiza seus próprios dados e relatórios básicos.
- **Gerente:** além da visualização, pode cadastrar e editar recursos.
- **Administrador de segurança:** acesso completo, capaz de gerenciar usuários, recursos e incidentes.

O comportamento real destes perfis depende do código do backend que autentica e autoriza as requisições.

*(os perfis são ilustrativos; a lógica de permissão está aguardando implementação no servidor)*

## Estrutura do projeto

A estrutura de pastas está organizada para separar banco de dados, arquivos estáticos e templates da aplicação:

```bash
IN-WAYNETECH_SECUREACCESS/
├── app/
│   └── db/
│       ├── schema.sql
│       └── seed.sql
├── static/
│   ├── css/
│   │   ├── dashboard.css
│   │   ├── login.css
│   │   └── register.css
│   └── img/
│       ├── background-upscale...
│       ├── background.png
│       ├── background2.jpeg
│       ├── caution.png
│       ├── logo.png
│       ├── logo2.png
│       ├── logo3-icon.png
│       └── logo3.png
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── edit_resource.html
│   ├── edit_user.html
│   ├── login.html
│   ├── new_incident.html
│   ├── register.html
│   ├── resources.html
│   ├── security.html
│   └── users.html
└── README.md
```

## Descrição das pastas e arquivos

### `app/db/`

Scripts SQL do banco de dados usados no protótipo.

- `schema.sql` cria as tabelas de usuários, recursos, incidentes etc.
- `seed.sql` insere registros de exemplo para testes e demonstrações.

### `static/`

Armazena os arquivos estáticos utilizados na interface.

- `css/`: arquivos de estilização das páginas.
- `img/`: imagens usadas no sistema, como logos e planos de fundo.

### `templates/`

Contém as páginas HTML da aplicação.

- `base.html`: template base utilizado como estrutura principal.
- `login.html`: tela de login.
- `register.html`: tela de cadastro de usuários.
- `dashboard.html`: painel principal do sistema.
- `resources.html`: página de listagem e gerenciamento de recursos.
- `edit_resource.html`: edição de recursos cadastrados.
- `users.html`: listagem de usuários.
- `edit_user.html`: edição de usuários.
- `new_incident.html`: cadastro de novos incidentes.
- `security.html`: área relacionada à segurança do sistema.

## Tecnologias presentes

Os artefatos contidos aqui são responsáveis pela camada de apresentação e pelo banco de dados:

- HTML (templates das páginas)
- CSS (estilos em `static/css/`)
- SQL (scripts de `schema` e `seed`)
- Imagens e arquivos estáticos

O servidor web e a lógica de backend estão implementados no arquivo `app.py`, que usa Flask e PyMySQL para conectar‑se à base de dados. Basta instalar as dependências listadas na seção seguinte e executar `python app.py` para iniciar o protótipo.

## Requisitos do projeto atendidos

Com base no enunciado, o sistema foi desenvolvido para atender aos seguintes requisitos: 

- Sistema de controle de acesso para usuários autorizados.
- Autenticação e autorização para diferentes tipos de usuários.
- Gestão de recursos internos.
- Interface administrativa para adicionar, remover e atualizar recursos.
- Dashboard com visualização de dados relevantes.
- Protótipo funcional com integração entre frontend e backend.
- Entrega com código-fonte e documentação detalhada.

## Como executar o protótipo

1. Clone o repositório na sua máquina.
2. Instale Python 3.10+ e crie um ambiente virtual (opcional).
3. Instale as dependências:
   ```bash
   pip install flask pymysql
   ```
4. Crie o banco de dados e rode `app/db/schema.sql` e `app/db/seed.sql` (o `app.py`
   já está configurado para se conectar a `localhost`/`root` sem senha; ajuste
   conforme necessário).
5. Execute o servidor:
   ```bash
   python app.py
   ```
6. Abra `http://localhost:5000` no navegador e teste as telas de login, registro
   e dashboard.

> O backend Flask serve as rotas e os templates; não é necessário montar outro
servidor adicional.

## Fluxo básico de uso

1. O usuário acessa a tela de login.
2. O sistema valida as credenciais informadas.
3. Após autenticação, o usuário é direcionado ao dashboard.
4. De acordo com o perfil de acesso, ele pode visualizar, cadastrar, editar ou gerenciar recursos e usuários.
5. O sistema também permite registrar e acompanhar informações relacionadas à segurança.

## Interface do sistema

A interface foi organizada para facilitar a navegação entre as principais áreas da aplicação, como autenticação, dashboard, gerenciamento de usuários, recursos e incidentes. A presença de arquivos específicos para login, cadastro, dashboard, recursos, usuários e segurança mostra uma separação funcional clara entre os módulos da aplicação.

Além disso, a estrutura de arquivos CSS separados por páginas contribui para a organização visual e manutenção do projeto.

## Possíveis melhorias futuras

- Implementação de relatórios mais detalhados.
- Criação de gráficos no dashboard.
- Registro de logs de auditoria.
- Filtros avançados para recursos e usuários.
- Melhorias de responsividade para dispositivos móveis.
- Reforço das validações de segurança no backend.
- Recuperação de senha e gerenciamento de sessão mais robusto.

## Considerações finais

Este sistema foi desenvolvido como projeto final com foco em demonstrar conhecimentos de desenvolvimento full stack por meio da construção de uma aplicação web funcional. A solução proposta atende ao cenário das Indústrias Wayne, integrando controle de acesso, gestão de recursos e visualização de informações de segurança em uma única plataforma. 
