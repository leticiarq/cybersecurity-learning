# AUTH-12 — Bypass de autenticação

## O que eu entendi, em uma frase

Uma função protegida pode ser usada sem concluir a prova de identidade exigida.

## Exemplo para eu fixar

A interface obriga o usuário a entrar antes de mostrar `/reports`. Porém, a API `/api/reports` foi publicada sem o middleware de autenticação. Digitar a rota diretamente contorna a tela e acessa os dados.

```text
requisição -> verificação de autenticação -> recurso protegido
                         |
             ausente ou controlada pelo cliente
                         |
                  acesso sem login
```

Outras causas incluem validação somente em JavaScript, endpoint antigo com política diferente e confiança em parâmetros como `authenticated=true`.

## Diferença que preciso lembrar: falha e bypass

Enumeração revela que uma conta existe. Senha fraca ainda exige acertar uma credencial. Bypass significa que uma verificação obrigatória foi ignorada, ausente ou satisfeita por informação não confiável.

Também é importante separar autenticação de autorização. Se o usuário fez login, mas acessou dados de outra pessoa, a raiz provavelmente está na autorização.

## Por que preciso prestar atenção

O impacto pode variar de leitura de dados sem login até execução de operações administrativas. Quando o bypass cria o contexto de outro usuário, pode resultar em tomada de conta.

## Como eu reconheceria em ambiente autorizado

Inventarie endpoints e estados de autenticação. Compare web, API, mobile e versões antigas. Com credenciais próprias, teste a ausência, expiração ou estado parcial da sessão e confirme se a rejeição ocorre no servidor.

## Como corrigir ou prevenir

- centralize o controle em middleware ou gateway testado;
- adote negação por padrão;
- valide sessão e fatores no servidor;
- não confie em flags, cookies ou headers sem integridade;
- mantenha política consistente entre canais e versões;
- teste automaticamente rotas novas e alternativas;
- aplique autenticação e autorização como decisões separadas.

## O que eu preciso lembrar

- Esconder um link não protege um endpoint.
- Toda rota protegida deve rejeitar estado ausente, parcial ou inválido.
- Login válido não substitui autorização.

## Referências técnicas

- [OWASP WSTG — Bypassing Authentication Schema](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication/04-Bypassing_Authentication_Schema/)
- [OWASP WSTG — Weaker Authentication in Alternative Channel](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication/10-Weaker_Authentication_in_Alternative_Channel/)
- [CWE-287 — Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
