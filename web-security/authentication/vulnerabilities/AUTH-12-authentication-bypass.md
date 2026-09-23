# AUTH-12 — Authentication Bypass

## Overview

**Authentication bypass** permite acessar total ou parcialmente uma função protegida sem completar a prova de identidade exigida.

Nem toda vulnerabilidade de autenticação é um bypass. Enumeração apenas revela contas; senha fraca ainda exige uma credencial. Bypass significa que uma validação necessária foi ausente, ignorada ou satisfeita por dado não confiável.

## How It Works

```text
Requisição -> deveria verificar autenticação -> recurso protegido
                         |
          validação ausente ou controlada pelo cliente
                         |
                  acesso concedido
```

Causas comuns incluem middleware ausente em uma rota, validação apenas em JavaScript, endpoints alternativos com política diferente ou confiança em parâmetros como `authenticated=true`.

## Example

A interface exige login antes de abrir `/reports`, mas a API `/api/reports` não executa o middleware de autenticação. Ocultar o link no frontend não protege o endpoint.

## Impact

Pode causar acesso não autenticado a dados e operações, afetando confidentiality e integrity. Account takeover é uma possibilidade quando o bypass concede contexto de outro usuário, mas não é consequência obrigatória de todo caso.

## How to Identify

Em avaliação autorizada, inventarie endpoints e estados de autenticação. Compare web, API, mobile e versões antigas; remova ou altere credenciais próprias e confirme enforcement server-side. Diferencie falha de autenticação de falha de autorização após login.

Comportamento esperado: toda rota protegida rejeita estado ausente, parcial ou inválido. Vulnerável: uma variação de endpoint ou estado controlável concede acesso.

## Mitigation

- centralize enforcement em middleware ou gateway testado;
- aplique deny by default;
- valide sessão e fatores no servidor;
- não confie em flags, headers ou cookies controláveis sem integridade;
- mantenha política consistente entre canais;
- teste rotas novas e alternativas automaticamente;
- separe autenticação de autorização e aplique ambas.

## Related Attacks

[MFA flaws](AUTH-11-mfa-flaw.md) e [weak recovery](AUTH-09-weak-password-recovery.md) podem criar bypasses. Session prediction e fixation são mecanismos diferentes, ainda que também resultem em acesso indevido.

## CWE

[CWE-287 — Improper Authentication](https://cwe.mitre.org/data/definitions/287.html) descreve prova de identidade insuficiente ou incorretamente validada. É apropriada quando a raiz está na autenticação; falhas puramente de autorização exigem classificação diferente.

## OWASP Relationship

O OWASP WSTG documenta **WSTG-ATHN-04 — Bypassing Authentication Schema** e **WSTG-ATHN-10 — Weaker Authentication in Alternative Channel**.

## Key Takeaways

- Navegação no frontend não é controle de segurança.
- Todos os endpoints devem aplicar a mesma política.
- Authentication bypass não é rótulo para qualquer falha de login.
- Autenticação válida não substitui autorização.

## References

- [OWASP WSTG — Bypassing Authentication Schema](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication/04-Bypassing_Authentication_Schema/)
- [OWASP WSTG — Weaker Authentication in Alternative Channel](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication/10-Weaker_Authentication_in_Alternative_Channel/)
- [MITRE CWE-287](https://cwe.mitre.org/data/definitions/287.html)
