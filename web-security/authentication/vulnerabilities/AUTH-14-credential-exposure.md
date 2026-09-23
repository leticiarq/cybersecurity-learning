# AUTH-14 — Credential Exposure

## Overview

**Credential exposure** ocorre quando senha, token, API key, session ID ou outro autenticador fica acessível a pessoas ou sistemas que não deveriam vê-lo.

A exposição pode acontecer em trânsito, URLs, logs, respostas, analytics, código-fonte, repositórios, arquivos de configuração, backups ou mensagens de erro.

## How It Works

```text
Credencial -> componente legítimo
                  |
        canal ou armazenamento secundário
                  |
      log / URL / rede / resposta / código
                  |
             divulgação
```

Credenciais em query strings podem aparecer no histórico, logs de proxy e referrer. Sem TLS, dados em trânsito podem ser observados ou alterados. Secrets em configuração versionada se propagam por clones e backups.

## Example

Uma API recebe `GET /login?password=exemplo`. Mesmo usando HTTPS, o servidor e intermediários podem registrar a URL. Isso é exposição em canais auxiliares, diferente de armazenar hashes de senha incorretamente no banco.

## Impact

Pode resultar em credential compromise, account takeover e acesso aos privilégios associados. O alcance depende do tipo de credencial, validade, escopo, reutilização e capacidade de revogação.

## How to Identify

Em avaliação autorizada, revise requisições, respostas, logs sanitizados, tracing, analytics, crash reports, repositórios e configuração. Use credenciais fictícias para rastrear propagação. Não copie secrets reais para relatórios.

Comportamento esperado: secrets aparecem apenas nos pontos estritamente necessários e são redigidos. Vulnerável: valores completos persistem em sistemas auxiliares ou canais inseguros.

## Mitigation

- use TLS e nunca envie credenciais em URLs;
- transmita senhas no corpo apropriado por HTTPS;
- aplique redaction em logs, traces e erros;
- use secret manager e menor privilégio;
- não versione secrets; use scanning preventivo;
- reduza escopo e validade de tokens;
- implemente rotação e revogação;
- proteja backups e ambientes de suporte;
- responda a exposição como incidente, não apenas apagando a cópia visível.

## Related Attacks

Exposição pode fornecer material para credential stuffing, session hijacking e account takeover. [Insecure password storage](AUTH-05-insecure-password-storage.md) é um caso de proteção inadequada no repositório primário; este documento enfatiza divulgação por canais e sistemas diversos.

## CWE

[CWE-522 — Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html) é uma classificação ampla para credenciais transmitidas ou armazenadas sem proteção suficiente. Casos específicos podem exigir uma CWE mais precisa.

## OWASP Relationship

O OWASP Authentication Cheat Sheet recomenda transporte seguro de credenciais. O Logging Cheat Sheet especifica dados que não devem ser registrados, e o Transport Layer Security Cheat Sheet cobre proteção em trânsito.

## Key Takeaways

- Tokens e session IDs são credenciais, assim como senhas.
- HTTPS não impede vazamento por URL ou logs.
- Redação e minimização reduzem propagação.
- Exposição exige rotação, revogação e investigação.

## References

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Logging Cheat Sheet — Data to Exclude](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude)
- [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- [MITRE CWE-522](https://cwe.mitre.org/data/definitions/522.html)
