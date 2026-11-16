# Plano de Gerência de Configuração de Software (PGCS)

**Projeto:** ETL-Python  
**Repositório:** https://github.com/gabrieldsantana28/ETL-Python  
**Responsável:** Gabriel Santana (`gabrieldsantana28`)  
**Disciplina:** Gerenciamento, Configuração e Processos de Software  
**Versão do plano:** 1.0 — 16/11/2026  
**Situação:** Proposta para adoção; controles devem ser efetivamente configurados e evidenciados no GitHub.

## 1. Objetivo e escopo
Estabelecer procedimentos para identificar, versionar, revisar, aprovar e rastrear mudanças nos artefatos do projeto ETL-Python, que utiliza Python e Airflow. O plano abrange código-fonte, configurações não sigilosas, documentação, workflows e evidências. Não implica que o projeto tenha deploy de produção real.

## 2. Papéis e responsabilidades
| Papel | Responsabilidade |
|---|---|
| Responsável pelo projeto | Manter o plano, administrar o repositório, autorizar alterações e revisar a liberação em `production`. |
| Par revisor | Colaborador com acesso de escrita; revisar Pull Requests, testar e registrar aprovações. **Nome/usuário a preencher após aceite do convite.** |
| Autor da mudança | Criar branch, documentar alteração, validar e abrir Pull Request. |

## 3. Itens de configuração (IC)
| Identificador | Item | Localização / controle |
|---|---|---|
| IC-01 | Código da ETL | `etl_rnp/` e demais fontes existentes; Git |
| IC-02 | Plano GCS | `docs/PLANO_GCS.md`; Git e revisão por PR |
| IC-03 | Documentação operacional | `README.md`, `docs/`; Git |
| IC-04 | Automação de verificação e demonstração | `.github/workflows/`; Git |
| IC-05 | Regras de acesso, proteção e ambientes | Configurações do GitHub; capturas em `docs/evidencias/` |
| IC-06 | Dependências e parâmetros não sigilosos | Arquivos já existentes ou adicionados futuramente; Git |

Segredos, tokens, senhas, arquivos `.env` e dados pessoais não devem ser versionados. Arquivos existentes devem ser preservados.

## 4. Identificação, versões e baselines
- Branch `main`: referência estável, com alteração apenas por Pull Request aprovado.
- Branches `feature/<descricao>`, `fix/<descricao>` e `docs/<descricao>`: desenvolvimento isolado.
- Commits claros, por exemplo `docs: adiciona plano de GCS` e `fix: corrige tratamento de dados`.
- Versões aprovadas podem receber tags anotadas `vMAJOR.MINOR.PATCH` (por exemplo `v1.0.0`). Uma tag só é considerada baseline após revisão e aprovação; não criar tags retroativas para simular aprovação.
- A baseline identifica um estado reproduzível do repositório, seu commit e documentação correspondente.

## 5. Controle de mudanças
1. Registrar a necessidade em uma Issue ou descrição de Pull Request.
2. Criar branch a partir de `main` atualizada.
3. Implementar e validar a alteração; não incluir credenciais nem dados sensíveis.
4. Abrir Pull Request para `main`, descrevendo motivação, arquivos afetados, validação e riscos.
5. Solicitar revisão do par com acesso Write; corrigir apontamentos.
6. Integrar somente após aprovação e verificações exigidas pelas regras do repositório.
7. Registrar o PR e o commit resultante no histórico; criar tag de baseline quando aplicável.

## 6. Políticas de integridade e acesso
- Habilitar Ruleset ativo para `main`: `Require a pull request before merging`, pelo menos uma aprovação, bloqueio de force push e exclusão; sem bypass para o responsável.
- Comprovar o bloqueio com uma tentativa real e não destrutiva de push direto na `main`, preservando o terminal e a mensagem de recusa.
- Convidar um par revisor com permissão Write e registrar o aceite; nunca publicar dados pessoais desnecessários.
- Usar acesso mínimo necessário; revogar acesso quando não mais necessário.
- Revisar arquivos de configuração e documentação como qualquer outro IC.

## 7. Ambientes e liberação
- `staging`: ambiente lógico de validação/demonstração, sem execução da ETL real.
- `production`: ambiente lógico de aprovação/demonstração, sem execução da ETL real.
- Configurar `production` com `Required reviewers`: `gabrieldsantana28` e, quando disponível, impedir autoaprovação. O revisor deve ser diferente de quem inicia a liberação quando a prevenção de autoaprovação estiver habilitada.
- O workflow de demonstração aciona um job em `staging` e outro em `production`; o segundo fica sujeito às regras do ambiente configuradas no GitHub.
- Nenhum segredo ou infraestrutura real é acessado pelo workflow demonstrativo.

## 8. Auditoria, verificação e evidências
Verificar periodicamente: estrutura do repositório, presença do PGCS, histórico de PRs e aprovações, proteção de `main`, aceite do colaborador Write, existência dos ambientes e revisor de `production`.

Armazenar evidências reais, com data e contexto, conforme `docs/evidencias/README.md`. Não marcar um controle como atendido sem testá-lo.

## 9. Gestão de desvios
Mudanças urgentes também devem ter rastreabilidade. Se uma regra impedir o trabalho, registrar o motivo e corrigir a configuração sem desativar controles silenciosamente. Revisar este plano por Pull Request.

## 10. Critérios de aceite acadêmico
- [ ] Estrutura do repositório organizada e PGCS publicado.
- [ ] Link público acessível ao avaliador.
- [ ] Push direto na `main` efetivamente recusado e evidenciado.
- [ ] Par revisor com acesso Write aceito e evidenciado.
- [ ] `staging` e `production` criados.
- [ ] `production` com o responsável como revisor obrigatório.

## 11. Referências
- Material de aula de GCPSW, Prof. Luiz Carlos Camargo: conceitos de IC, baseline, repositório e controle de mudanças.
- Documentação oficial do GitHub: rulesets, Pull Requests e environments.
