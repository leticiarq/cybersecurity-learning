# AUTH-10 — Predictable Recovery Tokens

## Overview

Um recovery token é uma credencial temporária que autoriza uma ação sensível. Se for previsível, reutilizável, duradouro ou mal vinculado, outra pessoa pode redefinir a senha da vítima.

Um token seguro deve ser aleatório, de uso único, ter validade curta, ser armazenado com proteção adequada e estar vinculado à conta e finalidade corretas.

## How It Works

```text
Pedido de reset -> token gerado -> canal verificado
                       |
       baixa entropia / sem expiração / reuse
                       |
             reset não autorizado
```

Timestamp, ID sequencial e PRNG não criptográfico tornam tokens adivinháveis. Trocar o `user_id` mantendo o token indica vínculo incompleto.

## Example

Uma aplicação cria `reset-1042`, depois `reset-1043`. Em teste controlado, a sequência revela o próximo valor. Outro sistema gera token forte, mas aceita o mesmo link várias vezes após o primeiro reset.

## Impact

Predição ou replay pode levar diretamente a account takeover. Tokens em URLs também podem vazar por logs, histórico ou referrer, ampliando o risco de credential exposure.

## How to Identify

Use apenas contas próprias. Compare tokens sem tentar valores de terceiros; observe comprimento, distribuição aparente, vínculo, expiração, uso único e invalidação após novo pedido ou reset. Revise o gerador e armazenamento em análise de código.

Comportamento esperado: valores imprevisíveis, escopo único e rejeição após uso/expiração. Vulnerável: padrões, reutilização ou troca de conta/finalidade.

## Mitigation

- gere tokens com CSPRNG e entropia suficiente;
- aplique validade curta e uso único com atualização atômica;
- vincule ao usuário, ação e transação;
- invalide tokens anteriores quando apropriado;
- armazene apenas representação protegida quando possível;
- entregue por canal previamente verificado e HTTPS;
- não registre tokens completos;
- aplique rate limiting sem depender dele para compensar baixa entropia.

## Related Attacks

É uma forma específica de [weak password recovery](AUTH-09-weak-password-recovery.md) e pode se combinar com [credential exposure](AUTH-14-credential-exposure.md) ou [username enumeration](AUTH-01-username-enumeration.md).

## CWE

[CWE-330 — Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html) aplica-se à previsibilidade. [CWE-640](https://cwe.mitre.org/data/definitions/640.html) representa o mecanismo de recuperação fraco de forma mais ampla.

## OWASP Relationship

O OWASP Forgot Password Cheat Sheet requer tokens aleatórios, suficientemente longos, vinculados ao usuário, de uso único e com expiração. O WSTG cobre análise de tokens no teste de password reset.

## Key Takeaways

- Recovery token deve ser tratado como credencial temporária.
- Entropia, vínculo, expiração e uso único são propriedades independentes.
- Token forte ainda pode vazar por transporte ou logs.
- Rate limiting não transforma token previsível em token seguro.

## References

- [OWASP Forgot Password Cheat Sheet — URL Tokens](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html#url-tokens)
- [OWASP WSTG — Weak Password Change or Reset](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication/09-Weak_Password_Change_or_Reset_Functionalities/)
- [MITRE CWE-330](https://cwe.mitre.org/data/definitions/330.html)
- [MITRE CWE-640](https://cwe.mitre.org/data/definitions/640.html)
