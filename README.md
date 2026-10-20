# OpsTrack API

API em **Flask** para acompanhamento de chamados (tickets) de TI. Nesta etapa foram adicionados **testes automatizados com pytest**, **medição de cobertura de código** e o fluxo de trabalho com **Git** (branch própria, Pull Request e main protegida).

Este README documenta o que foi feito e como reproduzir cada passo.

---

## Resumo do que foi feito

**Testes unitários**
- Clonagem do repositório e criação da branch `feature/testes`
- Ambiente virtual (`venv`) e instalação das dependências
- Ajuste do `app.py`: rotas organizadas e corrigidas
- Suíte de testes em `tests/` e `pytest.ini`
- Dois testes incompletos (`COMPLETE AQUI`) completados com o padrão Arrange / Act / Assert
- Erro proposital em uma rota para comprovar que o teste detecta falhas

**Cobertura de código**
- Relatório de cobertura (90%) e identificação das linhas não cobertas

**Git**
- `.gitignore` preenchido
- Nome do arquivo de dependências padronizado para `requirements.txt`
- Commit no padrão Conventional Commits, Pull Request e regra de proteção da `main`

---

## Estrutura do projeto

```
opstrack-api/
├── app.py            # API Flask (rotas)
├── requirements.txt  # dependências da aplicação
├── pytest.ini        # configuração do pytest
├── .gitignore        # arquivos ignorados pelo Git
└── tests/
    ├── conftest.py   # fixture do client de teste
    └── test_api.py   # testes da API
```

---

## Rodando os testes

Passo a passo para quem está entrando agora no projeto:

```powershell
git clone https://github.com/riquelme23456/opstrack-api.git
cd opstrack-api
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pytest pytest-cov
pytest
```

Resultado esperado: todos os testes com `passed` e nenhum `failed`. Para ver quais linhas do `app.py` não foram executadas:

```powershell
pytest --cov=app --cov-report=term-missing
```

Como ler a saída:

- `.` é um teste que passou e `F` é um teste que falhou, na ordem do arquivo
- Em caso de falha, a linha que começa com `E` mostra o valor esperado e o obtido; leia ela primeiro
- Na tabela de cobertura, `Miss` é a quantidade de linhas não executadas e `Missing` mostra quais são

O ambiente virtual precisa ser criado **antes** de ser ativado, e o terminal mostra `(venv)` quando ele está ativo. Em Linux/macOS, ative com `source venv/bin/activate`. O `pytest` e o `pytest-cov` não fazem parte do `requirements.txt`, por isso são instalados à parte.

---

## Como foi feito (passo a passo)

### 1. Clonar e criar a branch

```powershell
git clone https://github.com/riquelme23456/opstrack-api.git
cd opstrack-api
git checkout -b feature/testes
```

### 2. Rotas da API

O `app.py` foi reorganizado e tinha problemas de indentação (decoradores `@app.route` dentro de funções). Rotas atuais:

| Método | Rota        | Resposta                                          |
| ------ | ----------- | ------------------------------------------------- |
| GET    | `/`         | `{"servico": "OpsTrack API", "status": "online"}` |
| GET    | `/status`   | `{"status": "ok"}`                                |
| GET    | `/version`  | `{"version": "1.2"}`                              |
| GET    | `/tickets`  | Lista com 2 tickets de exemplo                    |
| GET    | `/usuarios` | Lista com 2 usuários de exemplo                   |

As rotas antigas `/health` e `/sobre` foram removidas. Qualquer rota inexistente retorna **404**.

### 3. Configuração do pytest (`pytest.ini`)

```ini
[pytest]
pythonpath = .
testpaths = tests
```

Sem o `pythonpath = .`, o pytest não encontra o `app.py` e acusa `ModuleNotFoundError: No module named 'app'`.

### 4. Testes

Os testes ficam em `tests/test_api.py` e seguem o padrão **AAA**:

1. **Arrange**: preparar o cenário (o `client` vem da fixture em `conftest.py`)
2. **Act**: executar a ação (por exemplo, `client.get('/status')`)
3. **Assert**: verificar status code e conteúdo

Os dois testes incompletos foram completados:

- `test_usuarios_retorna_dois_usuarios`: `GET` em `/usuarios`, status `200` e exatamente 2 usuários
- `test_rota_inexistente_retorna_404`: `GET` em `/nao-existe`, status `404`

### 5. Evolução das execuções

| Execução | Resultado | Motivo |
| -------- | --------- | ------ |
| 1ª | 3 passed, 2 failed | Os testes de `/usuarios` e de rota inexistente ainda estavam incompletos |
| 2ª | 5 passed | Testes completados |
| 3ª | 1 failed, 4 passed | Erro proposital (`'oks'` no lugar de `'ok'`) para comprovar que o teste de `/status` detecta falhas |
| 4ª | 5 passed | Alteração desfeita |

Na 3ª execução, o pytest mostrou o teste que falhou, o valor esperado (`'ok'`), o obtido (`'oks'`) e o caractere a mais. Um linter como o flake8 diria `0` para o mesmo código, porque o erro é de comportamento e não de estilo.

---

## Cobertura de código

Cobertura = linhas executadas ÷ linhas executáveis × 100.

```powershell
pytest --cov=app --cov-report=term-missing
```

```
Name     Stmts   Miss  Cover   Missing
app.py      21      2    90%   18, 40
```

Como se lê: `Stmts` são as linhas executáveis (21), `Miss` são as não executadas (2), e `Cover` é (21 - 2) ÷ 21 ≈ 90%. `Missing` mostra quais são.

Linhas não cobertas:

| Linha | Código | O que é |
| ----- | ------ | ------- |
| 18 | `return {'version': '1.2'}` | Retorno da rota `/version`, que nenhum teste chama |
| 40 | `app.run(debug=True)` | Início do servidor, executado só com `python app.py` |

---

## Git e regras do repositório

### Fluxo de trabalho

```
Branch  →  Commit  →  Push  →  Pull Request  →  Merge e pull
```

```powershell
git add app.py tests/ pytest.ini .gitignore requirements.txt
git commit -m "test: adiciona testes automatizados para API"
git push -u origin feature/testes
```

Depois do `push`, o Pull Request é aberto no GitHub e, depois do merge, a `main` local é atualizada com `git checkout main` e `git pull`. A conferência dos arquivos é feita com `git ls-files`.

### Regra de proteção da `main`

A `main` é protegida: ninguém altera ela por push direto, e toda mudança entra por branch, Pull Request e merge. A regra foi criada em **Settings > Rules > Rulesets** (novo ruleset de branch), com alvo na branch padrão (`main`), enforcement **Active** e estas opções:

| Opção | Estado | Para que serve |
| ----- | ------ | -------------- |
| Require a pull request before merging | Ativada, com **0** aprovações | Toda mudança entra por Pull Request. Sem exigir aprovação, quem trabalha sozinho consegue dar o merge |
| Restrict deletions | Ativada | Impede que a `main` seja apagada |
| Block force pushes | Ativada | Impede reescrever o histórico da `main` |

As demais opções ficaram desativadas. A exigência de status checks, por exemplo, só faz sentido quando houver uma pipeline de CI.

Com a regra ativa, um `git push origin main` é recusado, e isso é o esperado.

---

### Commits (Conventional Commits)

Padrão `tipo: descrição curta`:

| Tipo    | Uso                                  |
| ------- | ------------------------------------ |
| `feat`  | nova funcionalidade                  |
| `fix`   | correção de bug                      |
| `test`  | criação ou ajuste de testes          |
| `docs`  | documentação                         |
| `chore` | configuração e manutenção            |

Commit desta etapa: `5977265 test: adiciona testes automatizados para API` (6 arquivos alterados, 92 inserções, 33 remoções).

### `.gitignore`

```
venv/
__pycache__/
.pytest_cache/
.coverage
htmlcov/
*.py[cod]
```

Evita versionar o ambiente virtual, caches e arquivos de cobertura.

---

## Problemas encontrados e soluções

| Problema | Solução |
| -------- | ------- |
| `pytest` não reconhecido | Ativar o `venv` e instalar o pytest dentro dele |
| `ModuleNotFoundError: No module named 'app'` | Criar o `pytest.ini` com `pythonpath = .` |
| `Could not open requirements file: 'requirement.txt'` | O nome correto é `requirements.txt` (com **s**) |
| Erro ao ativar o `venv` | Criar com `python -m venv venv` e ativar com `.\venv\Scripts\Activate.ps1` |
| `git diff` abre tela que não fecha | Apertar `q`, ou usar `git --no-pager diff` |
| `a branch named 'feature/testes' already exists` | Usar `git checkout feature/testes` (sem `-b`) |
| Aviso de identidade do Git no commit | `git config --global user.name "Seu Nome"` e `git config --global user.email "seu@email.com"` |
