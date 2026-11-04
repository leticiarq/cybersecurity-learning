# AUTH-08 — Fixação de sessão

## O que eu entendi, em uma frase

A aplicação mantém, depois do login, um ID de sessão que já era conhecido antes da autenticação.

## Sequência que preciso visualizar

```text
1. Um ID de sessão é conhecido antes do login
2. A vítima autentica usando esse mesmo ID
3. O servidor associa a identidade ao ID antigo
4. Quem já conhecia o ID tenta reutilizá-lo
```

Imagine uma loja que cria uma sessão anônima para o carrinho. Ana faz login, mas o backend apenas acrescenta sua identidade ao mesmo registro em vez de emitir um novo ID. Uma cópia anterior daquele ID passa a representar a conta autenticada.

## Diferença que preciso lembrar: fixação e sequestro

- **Fixação de sessão:** o ID é preparado ou conhecido antes do login e não é renovado.
- **Sequestro de sessão:** um ID que já estava autenticado é roubado.

A fixação pode terminar em sequestro, mas o momento em que o ID se torna conhecido é diferente.

## Por que preciso prestar atenção

A falha pode permitir acesso à conta sem descobrir a senha. O impacto depende dos privilégios que a sessão recebe.

## Como eu reconheceria em ambiente autorizado

Em uma conta e navegador próprios, registre o ID antes do login e compare com o valor depois. Repita a observação em MFA, reautenticação e elevação de privilégio.

A igualdade dos valores é um sinal, mas confirme se a cópia anterior realmente ganhou o estado autenticado. Algumas aplicações mantêm um identificador externo e renovam com segurança outro valor interno.

## Como corrigir ou prevenir

- invalide a sessão anônima e gere um novo ID após autenticação;
- renove também após reautenticação e mudança de privilégio;
- gere IDs imprevisíveis;
- não aceite IDs de sessão em URLs;
- use cookies com atributos defensivos e escopo restrito;
- teste todos os mecanismos e canais de login.

## O que eu preciso lembrar

- O problema começa antes do login.
- ID forte ainda precisa ser renovado quando a identidade ou o privilégio muda.
- A sessão antiga deve deixar de ser aceita.

## Referências técnicas

- [OWASP WSTG — Session Fixation](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/)
- [OWASP Session Management Cheat Sheet — Renew the Session ID](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#renew-the-session-id-after-any-privilege-level-change)
- [CWE-384 — Session Fixation](https://cwe.mitre.org/data/definitions/384.html)
