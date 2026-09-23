# AUTH-06 — Insecure Session Cookie

## Overview

Um **session cookie** transporta um identificador que permite ao servidor reconhecer uma sessão. Configuração insegura pode expor esse valor ou permitir que ele seja enviado em contextos indevidos.

Como o identificador representa temporariamente a autenticação do usuário, quem o obtém pode conseguir reutilizá-lo sem conhecer a senha.

## How It Works

```text
Login -> servidor cria sessão -> cookie com session ID
                                      |
                      navegador reenvia em requisições
```

- `Secure`: envia o cookie apenas por conexões seguras.
- `HttpOnly`: impede leitura pelas APIs JavaScript do navegador; não corrige XSS por completo.
- `SameSite`: controla envio em contextos cross-site e ajuda contra CSRF; não é um substituto universal para tokens anti-CSRF.
- `Domain` e `Path`: limitam onde o cookie é enviado.

IDs previsíveis, conteúdo sensível diretamente no cookie e escopos amplos criam riscos adicionais.

## Example

```http
Set-Cookie: session_id=12345; Path=/
```

O exemplo não usa `Secure`, `HttpOnly` ou `SameSite`, e o valor sequencial sugere baixa imprevisibilidade. Um cookie configurado com atributos corretos ainda precisa de um ID forte e validação server-side.

## Impact

Exposição ou previsão pode levar a **session hijacking**, afetando confidentiality e integrity conforme os privilégios da vítima. O atributo ausente determina o caminho de exposição; não se deve atribuir o mesmo impacto automaticamente a toda configuração.

## How to Identify

Em sessão própria e ambiente autorizado, inspecione `Set-Cookie`, escopo, persistência, conteúdo e comportamento em HTTP/HTTPS. Compare múltiplos IDs sem tentar prever sessões reais. Verifique se dados sensíveis ou privilégios são confiados ao conteúdo modificável.

## Mitigation

- use HTTPS em toda a sessão e marque cookies de autenticação como `Secure`;
- use `HttpOnly` quando JavaScript não precisar do cookie;
- selecione `SameSite` conforme o fluxo e mantenha proteção CSRF apropriada;
- restrinja `Domain` e `Path`; considere prefixos `__Host-` quando aplicável;
- gere IDs opacos com CSPRNG e entropia suficiente;
- não armazene senha nem dados sensíveis desnecessários no cookie;
- aplique rotação, expiração e invalidação server-side.

## Related Attacks

Cookies expostos favorecem session hijacking. A reutilização após logout é discutida em [AUTH-07](AUTH-07-session-invalidation.md); preservar o ID durante o login pode causar [AUTH-08](AUTH-08-session-fixation.md).

## CWE

[CWE-614 — Sensitive Cookie in HTTPS Session Without 'Secure' Attribute](https://cwe.mitre.org/data/definitions/614.html) e [CWE-1004 — Sensitive Cookie Without 'HttpOnly' Flag](https://cwe.mitre.org/data/definitions/1004.html) representam configurações específicas. “Insecure session cookie” é mais amplo e não possui uma única CWE que cubra todos os casos.

## OWASP Relationship

O OWASP Session Management Cheat Sheet detalha geração, transporte e atributos de cookies. O WSTG possui testes próprios para session management schema e cookie attributes.

## Key Takeaways

- O session ID deve ser tratado como credencial.
- Cada atributo de cookie resolve uma finalidade diferente.
- Atributos corretos não compensam um ID previsível.
- Cookie seguro depende também do ciclo de vida server-side.

## References

- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP WSTG — Cookie Attributes](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/02-Cookies_Attributes/)
- [RFC 6265 — HTTP State Management Mechanism](https://www.rfc-editor.org/rfc/rfc6265)
- [MITRE CWE-614](https://cwe.mitre.org/data/definitions/614.html)
- [MITRE CWE-1004](https://cwe.mitre.org/data/definitions/1004.html)
