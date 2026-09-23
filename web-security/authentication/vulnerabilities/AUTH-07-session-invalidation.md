# AUTH-07 — Improper Session Invalidation

## Overview

**Improper session invalidation** ocorre quando uma sessão que deveria terminar continua aceita pelo servidor. Fechar a tela ou apagar o cookie no navegador não revoga, por si só, o estado server-side.

Eventos como logout, troca ou reset de senha, desativação de conta e detecção de comprometimento precisam ter regras explícitas de invalidação.

## How It Works

```text
Session ID válido -> logout no cliente
                         |
             registro permanece válido
                         |
       cópia antiga do ID ainda funciona
```

Sessões stateful exigem remover ou marcar o registro como inválido. Tokens autocontidos podem exigir expiração curta, versionamento, revocation list ou outro mecanismo arquitetural.

## Example

Ana copia o próprio cookie em um ambiente de teste, realiza logout e depois reapresenta a cópia. Se a API ainda aceita o identificador, o logout alterou apenas o navegador e não encerrou a sessão no servidor.

## Impact

Uma sessão obtida anteriormente pode continuar permitindo acesso, causando session hijacking persistente, perda de confidentiality e ações não autorizadas. Sessões antigas após troca de senha dificultam contenção de account takeover.

## How to Identify

Com uma conta própria, capture identificadores antes de logout e eventos de segurança. Reapresente-os apenas no ambiente autorizado e confirme se recursos protegidos os rejeitam. Avalie timeout ocioso, timeout absoluto, sessões concorrentes e revogação administrativa.

Comportamento esperado: rejeição server-side. Vulnerável: o token antigo mantém os mesmos privilégios até uma expiração excessivamente distante ou indefinida.

## Mitigation

- invalide sessões server-side no logout;
- defina timeouts ocioso e absoluto proporcionais ao risco;
- encerre ou reavalie sessões após reset de senha e eventos críticos;
- ofereça encerramento de outras sessões;
- rotacione refresh tokens e detecte reuse quando aplicável;
- mantenha relógios e armazenamento de sessão consistentes;
- não dependa apenas da remoção do cookie.

## Related Attacks

A falha prolonga os efeitos de [session cookie exposure](AUTH-06-session-cookie.md), [remember-me inseguro](AUTH-13-remember-me.md) e credential compromise. Não é sinônimo de [session fixation](AUTH-08-session-fixation.md), que ocorre quando um ID conhecido é preservado durante a autenticação.

## CWE

[CWE-613 — Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html) descreve sessões antigas reutilizáveis por expiração ou término insuficiente.

## OWASP Relationship

O OWASP Session Management Cheat Sheet aborda logout, expiração e encerramento. O OWASP ASVS possui um capítulo específico de Session Management, incluindo requisitos de término e validade.

## Key Takeaways

- Logout precisa alterar o estado aceito pelo servidor.
- Expiração e revogação são controles diferentes.
- Troca de senha deve participar da estratégia de contenção.
- Tokens stateless ainda precisam de política de ciclo de vida.

## References

- [OWASP Session Management Cheat Sheet — Session Expiration](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#session-expiration)
- [OWASP WSTG — Testing for Logout Functionality](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/06-Logout_Functionality/)
- [MITRE CWE-613](https://cwe.mitre.org/data/definitions/613.html)
