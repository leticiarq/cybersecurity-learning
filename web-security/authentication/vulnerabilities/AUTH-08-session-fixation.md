# AUTH-08 — Session Fixation

## Overview

**Session fixation** ocorre quando a aplicação aceita, depois do login, um identificador de sessão que já existia antes da autenticação. Se outra pessoa conhece ou controla esse ID, pode reutilizá-lo após a vítima entrar.

Isso difere de **session hijacking**: hijacking é a tomada de uma sessão já autenticada; fixation prepara ou conhece o ID antes e espera que ele se torne autenticado.

## How It Works

```text
ID conhecido antes do login
            |
      vítima autentica
            |
servidor preserva o mesmo ID
            |
ID conhecido agora representa a vítima
```

A raiz é não regenerar o identificador na mudança de estado anônimo para autenticado, ou em mudanças relevantes de privilégio.

## Example

Uma loja cria um cookie para o carrinho anônimo. Após o login de Ana, o backend associa a identidade ao mesmo ID em vez de emitir outro. Em laboratório, uma cópia pré-login passa a acessar a área autenticada.

## Impact

Pode resultar em session takeover, com acesso à confidentiality e integrity da conta conforme seus privilégios. A senha não precisa ser descoberta.

## How to Identify

Com conta e navegador próprios, registre o ID antes do login, autentique-se e compare o valor depois. Verifique também MFA, reautenticação e elevação de privilégio. A simples igualdade é um sinal; confirme se a cópia anterior realmente recebe estado autenticado.

Comportamento esperado: o ID anterior é invalidado e outro é emitido. Vulnerável: o mesmo ID conserva continuidade e privilégios.

## Mitigation

- invalide a sessão anterior e gere novo ID após autenticação;
- regenere também após reautenticação e mudança de privilégio;
- gere IDs imprevisíveis;
- não aceite IDs de sessão por URL;
- use cookies com atributos defensivos e escopo restrito;
- evite copiar estado autenticado para um identificador controlável;
- teste todas as rotas e mecanismos de login.

## Related Attacks

Fixation pode levar a session hijacking, mas não é sinônimo dele. [Insecure session cookies](AUTH-06-session-cookie.md) podem facilitar a definição ou exposição do ID; [improper invalidation](AUTH-07-session-invalidation.md) prolonga sua utilidade.

## CWE

[CWE-384 — Session Fixation](https://cwe.mitre.org/data/definitions/384.html) é a correspondência direta.

## OWASP Relationship

O OWASP WSTG documenta **WSTG-SESS-03 — Session Fixation** e recomenda renovar o token após autenticação. O Session Management Cheat Sheet faz a mesma distinção de ciclo de vida.

## Key Takeaways

- O problema começa antes do login.
- O ID deve mudar quando a identidade ou privilégio muda.
- Fixation e hijacking estão relacionados, mas não são sinônimos.
- Gerar IDs fortes não elimina a necessidade de rotação.

## References

- [OWASP WSTG — Session Fixation](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/)
- [OWASP Session Management Cheat Sheet — Renew the Session ID](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#renew-the-session-id-after-any-privilege-level-change)
- [MITRE CWE-384](https://cwe.mitre.org/data/definitions/384.html)
