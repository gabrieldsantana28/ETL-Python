# Guia prático de configuração e avaliação N2-P2

## A. Publicação
Adicione os arquivos deste pacote sem sobrescrever arquivos existentes. Acrescente ao README principal do repositório um link para `docs/PLANO_GCS.md` e para este guia.

## B. Proteção da `main`
No GitHub: Settings > Rules > Rulesets > New branch ruleset. Nome sugerido: `protecao-main`; status `Active`; target branch `main`. Ative `Require a pull request before merging`, `Required approvals: 1`, bloqueio de force pushes e de exclusões. Não conceda bypass ao proprietário. Confira se a regra está ativa.

## C. Evidência de push recusado
Depois de publicar as alterações por PR, faça um teste não destrutivo em clone local atualizado:

```bash
git switch main
git pull --ff-only origin main
git commit --allow-empty -m "test: verifica bloqueio de push direto"
git push origin main
```

O último comando deve ser recusado pelo GitHub. Capture a saída com o comando e o erro. Para remover **somente o commit vazio local que você acabou de criar**, depois da recusa e antes de qualquer outro trabalho, execute `git reset --hard origin/main` (isso descarta alterações locais: confirme que não há trabalho pendente). Se o push for aceito, a proteção não está correta: ajuste a regra e refaça o teste com outro commit vazio.

## D. Par de revisão
Settings > Collaborators (ou Collaborators and teams) > Add people. Convide o colega, garanta acesso Write e peça que aceite. Capture a tela que comprove o acesso. No GitHub, o proprietário de repositório pessoal pode ter opções de permissões diferentes das de uma organização: confirme o acesso efetivo exibido.

## E. Ambientes
Settings > Environments > New environment. Crie `staging` e `production`. Em `production`, habilite `Required reviewers` e selecione `gabrieldsantana28`; habilite `Prevent self-review` se disponível. Guarde captura da configuração. Em Actions, execute manualmente `Demonstracao de ambientes GCS`; a etapa de production deverá aguardar a aprovação conforme as regras. Se o próprio usuário iniciar o workflow e `Prevent self-review` estiver ativo, ele não poderá aprovar a própria execução: peça ao colaborador que inicie o workflow.

## F. Evidências
Confira `docs/evidencias/README.md`. Capturas devem mostrar situações reais, não imagens simuladas. Evite expor tokens, emails privados ou credenciais.

## G. Entrega
Envie o link https://github.com/gabrieldsantana28/ETL-Python e confirme que o professor consegue consultar o plano, as evidências e as configurações acessíveis.
