# Authentication Vulnerabilities

**Authentication vulnerabilities** são falhas de projeto, implementação ou operação que enfraquecem a verificação de identidade ou a manutenção do estado autenticado. Elas podem revelar contas, facilitar tentativas automatizadas, expor credenciais, permitir bypass ou comprometer sessões.

Os códigos `AUTH-01` a `AUTH-15` são somente uma convenção interna deste repositório. Eles não são identificadores oficiais da OWASP, do MITRE CWE ou de outra organização.

## Índice

| ID | Vulnerability | Main Risk |
|---|---|---|
| AUTH-01 | [Username Enumeration](AUTH-01-username-enumeration.md) | User information disclosure |
| AUTH-02 | [Timing Enumeration](AUTH-02-timing-enumeration.md) | User information disclosure |
| AUTH-03 | [Weak Password Policy](AUTH-03-weak-password-policy.md) | Credential guessing |
| AUTH-04 | [Improper Restriction of Authentication Attempts](AUTH-04-authentication-attempts.md) | Automated authentication attacks |
| AUTH-05 | [Insecure Password Storage](AUTH-05-insecure-password-storage.md) | Credential compromise |
| AUTH-06 | [Insecure Session Cookie](AUTH-06-session-cookie.md) | Session hijacking |
| AUTH-07 | [Improper Session Invalidation](AUTH-07-session-invalidation.md) | Reuse of old sessions |
| AUTH-08 | [Session Fixation](AUTH-08-session-fixation.md) | Session takeover |
| AUTH-09 | [Weak Password Recovery](AUTH-09-weak-password-recovery.md) | Authentication bypass |
| AUTH-10 | [Predictable Recovery Tokens](AUTH-10-predictable-recovery-tokens.md) | Unauthorized password reset |
| AUTH-11 | [MFA Flaw](AUTH-11-mfa-flaw.md) | MFA bypass |
| AUTH-12 | [Authentication Bypass](AUTH-12-authentication-bypass.md) | Unauthenticated access |
| AUTH-13 | [Insecure Remember Me](AUTH-13-remember-me.md) | Persistent account access |
| AUTH-14 | [Credential Exposure](AUTH-14-credential-exposure.md) | Credential disclosure |
| AUTH-15 | [Default Credentials](AUTH-15-default-credentials.md) | Unauthorized administrative access |

## Grupos conceituais

### User Enumeration

[AUTH-01](AUTH-01-username-enumeration.md) trata diferenças no conteúdo e comportamento das respostas; [AUTH-02](AUTH-02-timing-enumeration.md) isola o canal lateral de tempo.

### Password Security

[AUTH-03](AUTH-03-weak-password-policy.md) aborda a escolha de senhas, enquanto [AUTH-05](AUTH-05-insecure-password-storage.md) aborda sua proteção no servidor.

### Authentication Attempts

[AUTH-04](AUTH-04-authentication-attempts.md) relaciona rate limiting, throttling e lockout a brute force, credential stuffing e password spraying.

### Session Security

[AUTH-06](AUTH-06-session-cookie.md), [AUTH-07](AUTH-07-session-invalidation.md), [AUTH-08](AUTH-08-session-fixation.md) e [AUTH-13](AUTH-13-remember-me.md) cobrem transporte, ciclo de vida, renovação e persistência de sessões.

### Password Recovery

[AUTH-09](AUTH-09-weak-password-recovery.md) analisa o fluxo completo; [AUTH-10](AUTH-10-predictable-recovery-tokens.md) aprofunda as propriedades do token.

### MFA and Authentication Bypass

[AUTH-11](AUTH-11-mfa-flaw.md) trata implementações defeituosas de MFA; [AUTH-12](AUTH-12-authentication-bypass.md) trata caminhos que contornam a autenticação.

### Credential Security

[AUTH-14](AUTH-14-credential-exposure.md) cobre exposição em trânsito, logs e configuração; [AUTH-15](AUTH-15-default-credentials.md) trata credenciais iniciais não substituídas.

## Avaliação responsável

Testes devem ocorrer somente em sistemas autorizados, com contas de teste, limites e procedimentos de recuperação acordados. Testes de login, recuperação e sessão podem bloquear usuários, enviar notificações, invalidar sessões ou causar indisponibilidade.

## Referências gerais

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/)
- [OWASP ASVS](https://owasp.org/projects/asvs)
