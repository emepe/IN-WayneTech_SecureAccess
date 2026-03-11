# IN-WAYNETECH SecureAccess

Sistema web full stack desenvolvido para o projeto final da Infinity School com o objetivo de gerenciar segurança, controle de acesso e recursos internos das Indústrias Wayne. A aplicação foi criada para permitir autenticação de usuários, controle por níveis de permissão, administração de recursos e visualização de informações relevantes em um dashboard. 

## Sobre o projeto

Este projeto foi desenvolvido com base na proposta de criar um **Sistema de Gerenciamento de Segurança** para as Indústrias Wayne. O sistema busca atender às necessidades de controle de acesso às áreas restritas, gestão de recursos internos e visualização de dados importantes relacionados à segurança e às atividades da empresa. 

A proposta do projeto exige uma aplicação web full stack que demonstre integração entre frontend, backend e banco de dados, além de apresentar um protótipo funcional acompanhado de documentação. 

## Objetivos

- Permitir o acesso apenas a usuários autorizados.
- Implementar autenticação e autorização com diferentes tipos de usuário.
- Gerenciar recursos internos, como equipamentos, veículos e dispositivos de segurança.
- Exibir um dashboard com informações relevantes sobre segurança, recursos e atividades.
- Demonstrar a integração entre interface, regras de negócio e banco de dados. [file:2]

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

O sistema foi pensado para trabalhar com diferentes níveis de permissão, conforme solicitado no enunciado do projeto. Entre os perfis previstos estão funcionários, gerentes e administradores de segurança, cada um com responsabilidades e acessos específicos dentro da plataforma. [file:2]

Exemplo de organização de permissões:
- **Funcionário:** acesso a informações básicas do sistema.
- **Gerente:** acesso à visualização e gerenciamento de determinados recursos.
- **Administrador de segurança:** controle total sobre usuários, recursos e informações de segurança.

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

Contém os arquivos relacionados ao banco de dados da aplicação.

- `schema.sql`: responsável pela criação da estrutura do banco de dados.
- `seed.sql`: responsável pela inserção de dados iniciais para testes ou uso do sistema.

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

## Tecnologias utilizadas

As tecnologias exatas podem variar de acordo com a implementação final, mas este projeto se caracteriza como uma aplicação web full stack com integração entre interface, backend e banco de dados, conforme exigido pelo enunciado.

Tecnologias presentes na estrutura do projeto:

- HTML
- CSS
- SQL
- Templates HTML para renderização das páginas
- Banco de dados relacional

> Se desejar, você pode complementar esta seção com o backend que usou, por exemplo: Flask, Node.js, PHP ou outro.

## Requisitos do projeto atendidos

Com base no enunciado, o sistema foi desenvolvido para atender aos seguintes requisitos: 

- Sistema de controle de acesso para usuários autorizados.
- Autenticação e autorização para diferentes tipos de usuários.
- Gestão de recursos internos.
- Interface administrativa para adicionar, remover e atualizar recursos.
- Dashboard com visualização de dados relevantes.
- Protótipo funcional com integração entre frontend e backend.
- Entrega com código-fonte e documentação detalhada.

## Como executar o projeto

> **Importante:** ajuste esta seção de acordo com a tecnologia backend que você utilizou.

Passos gerais para execução:

1. Clone este repositório.
2. Acesse a pasta do projeto.
3. Configure o banco de dados utilizando os scripts `schema.sql` e `seed.sql`.
4. Instale as dependências do backend, caso existam.
5. Inicie o servidor da aplicação.
6. Acesse o sistema no navegador pelo endereço configurado localmente.

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

## Documentação

Este projeto faz parte da entrega do projeto final e deve ser acompanhado de documentação detalhada, conforme solicitado no enunciado.

A documentação pode incluir:

- objetivo do sistema;
- requisitos funcionais e não funcionais;
- descrição da arquitetura;
- modelagem do banco de dados;
- explicação das telas;
- fluxo de autenticação;
- regras de permissão;
- melhorias futuras.

## Considerações finais

Este sistema foi desenvolvido como projeto final com foco em demonstrar conhecimentos de desenvolvimento full stack por meio da construção de uma aplicação web funcional. A solução proposta atende ao cenário das Indústrias Wayne, integrando controle de acesso, gestão de recursos e visualização de informações de segurança em uma única plataforma. 
