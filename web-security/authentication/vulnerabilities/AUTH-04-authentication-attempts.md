# AUTH-04 — Improper Restriction of Authentication Attempts

## Overview

Esta vulnerabilidade ocorre quando o sistema não restringe adequadamente tentativas de autenticação. Em termos simples, a aplicação permite testar credenciais rápido demais ou por tempo demais.

O problema também existe quando um controle é fácil de contornar ou causa efeitos perigosos, como lockout permanente acionável por qualquer pessoa.

## How It Works

```text
Muitas tentativas -> endpoint de autenticação
                           |
                sem limite efetivo
                           |
              guessing em escala
```

Limitar somente por IP pode falhar diante de origens distribuídas. Limitar somente por conta pode facilitar denial of service. APIs, mobile, MFA e recuperação esquecidos criam canais alternativos.

## Example

Em homologação, uma conta descartável recebe uma sequência pequena e previamente acordada de senhas incorretas. As respostas continuam sem atraso progressivo, limite, desafio ou alerta. O objetivo é observar o controle, não encontrar uma senha.

## Impact

- maior viabilidade de account takeover;
- adivinhação de senhas e códigos de curta duração;
- **availability** afetada se lockout puder ser abusado para bloquear vítimas;
- aumento de carga e ruído operacional.

## How to Identify

Mapeie login web, APIs, mobile, protocolos legados, MFA e recuperação. Em teste autorizado, observe limites por conta, origem, dispositivo e comportamento agregado; verifique concorrência e janelas de tempo sem exceder o escopo.

Comportamento esperado: redução progressiva da taxa, correlação e alerta. Vulnerável: volume significativo aceito ou limites reiniciáveis/isolados por canal.

## Mitigation

- aplique rate limiting e throttling com múltiplos sinais;
- associe contadores à conta, não apenas ao IP;
- use atrasos progressivos e controles adaptativos;
- projete lockout temporário e recuperação para resistir a DoS;
- proteja cada fator e canal;
- registre eventos sem credenciais e gere alertas;
- combine com senhas fortes e MFA; CAPTCHA não deve ser a única defesa.

## Related Attacks

**Brute force** testa muitos candidatos; **credential stuffing** reutiliza pares vazados; **password spraying** distribui poucas senhas por muitas contas. [Username enumeration](AUTH-01-username-enumeration.md) fornece alvos e [weak password policy](AUTH-03-weak-password-policy.md) aumenta a chance de sucesso.

## CWE

[CWE-307 — Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html) é a correspondência direta para restrições ausentes ou inadequadas.

## OWASP Relationship

O Authentication Cheat Sheet trata proteção contra ataques automatizados. O WSTG v4.2 possui o teste **WSTG-ATHN-03 — Testing for Weak Lock Out Mechanism**.

## Key Takeaways

- Um único contador por IP ou usuário raramente é suficiente.
- Lockout mal projetado pode virar denial of service.
- Todos os canais precisam aplicar política consistente.
- Rate limiting é uma camada, não a solução completa.

## References

- [OWASP Authentication Cheat Sheet — Protect Against Automated Attacks](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#protect-against-automated-attacks)
- [OWASP WSTG v4.2 — Weak Lock Out Mechanism](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism/)
- [OWASP Credential Stuffing Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html)
- [MITRE CWE-307](https://cwe.mitre.org/data/definitions/307.html)
