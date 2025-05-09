# GitHub - Guia Básico 💡

### O que é Git?

O Git é um software de controle de versão distribuído. O controle de versão é uma maneira de salvar alterações ao longo do tempo sem sobrescrever versões anteriores. Ser distribuído significa que cada desenvolvedor que trabalha com um repositório Git tem uma cópia de todo o repositório – cada commit, cada branch, cada arquivo.

### Primeiros Passos com Git

* Instalação do Git: https://git-scm.com/downloads/win
* Configuração do Git:

        git config --global user.name "nome"
        git config --global user.email "seu@email.com"

* Clonar repositório:

        git clone url-do-repositorio

### Fluxo de Trabalho

#### 📂 Criação de Branches

* Siga a convenção abaixo ao criar uma branch:

  | Tipo       | Prefixo          |Exemplo                           |
  |------------|------------------|----------------------------------|
  | Feature    | `feature/`       | `feature/login-social`           |
  | Bugfix     | `bugfix/`        | `bugfix/corrigir-login`          |
  | Hotfix     | `hotfix/`        | `hotfix/erro-produção`           |
  | Release    | `release/x.y.z`  | `release/1.2.0`                  |
  | Refactor   | `refactor/`      | `refactor/melhorar-servico-api`  |
  | Docs       | `docs/`          | `docs/atualizar-readme`          |

* Exemplo de criação:

        git checkout main
        git pull origin main
        git checkout -b feature/nome-da-sua-feature

#### ✉️ Commits

Usamos a convenção *Conventional Commits* para padronizar mensagens de commit.

* Tipos comuns:

  - `feat:` nova funcionalidade

  - `fix:` correção de bug

  - `docs:` mudanças em documentação

  - `style:` ajustes de formatação (sem código)

  - `refactor:` refatoração de código (sem nova funcionalidade)

  - `test:` adição/modificação de testes

  - `chore:` manutenção geral (build, dependências etc.)


* Exemplo de criação:

        git commit -m "feat: adicionar autenticação com Google"

* Git Pull: Atualiza seu branch de trabalho local atual com todos os novos commits do branch remoto correspondente no GitHub.

        git pull 

* Git Push: Envia todos os commits do branch local para o remoto.

        git push

#### 📌 Merges

O comando *merge* fará a junção das alterações feitas à base de código em uma branch separada à sua branch atual como um novo commit.

* Exemplo de criação:

        git checkout main
        git pull origin main
        git merge feature/nome-feature

#### 🚀 Pull Requests

* Suba sua branch para o repositório remoto:

        git push origin nome-da-branch

* Crie um Pull Request (PR) no GitHub para main ou dev.

    - O PR deve:

      -Ter título e descrição claros

      -Ser revisado por pelo menos 1 pessoa

      -Passar nos checks automáticos (se configurados)