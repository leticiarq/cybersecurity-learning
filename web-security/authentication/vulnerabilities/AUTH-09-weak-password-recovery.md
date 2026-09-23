# AUTH-09 — Weak Password Recovery

## Overview

Password recovery é um caminho alternativo para recuperar acesso à conta. Se esse fluxo exige evidência mais fraca que o login, ele pode contornar a autenticação principal.

Falhas incluem perguntas de segurança descobríveis, validação insuficiente, mudança de conta entre etapas, ausência de limites e suporte humano com verificação fraca.

## How It Works

```text
Identificação -> desafio/contato -> autorização do reset
                                         |
                          evidência fraca ou etapa pulável
                                         |
                               nova senha definida
```

Cada etapa precisa estar vinculada à mesma conta e transação. O backend deve validar o estado; controles apenas no frontend podem ser ignorados.

## Example

Uma aplicação pergunta “qual sua cidade natal?” e permite tentativas ilimitadas. A resposta aparece no perfil público da pessoa. Acertar a pergunta autoriza diretamente uma nova senha, tornando o fluxo mais fraco que o login.

## Impact

Pode causar authentication bypass e account takeover, alterando confidentiality e integrity dos dados da vítima. Também pode gerar denial of service se a senha for trocada sem controle e a vítima perder acesso.

## How to Identify

Com contas de teste, mapeie todas as etapas e transições. Verifique troca de identificador, repetição, bypass de telas, perguntas descobríveis, canais alternativos, limites, notificações e efeito sobre sessões existentes.

Comportamento esperado: respostas genéricas, evidência adequada, vínculo de transação e confirmação server-side. Vulnerável: uma etapa fraca ou manipulável autoriza o reset.

## Mitigation

- use canal de recuperação previamente verificado e token forte;
- não dependa de perguntas com respostas públicas ou estáticas;
- vincule cada etapa à conta e transação iniciadas;
- aplique limites e respostas que evitem enumeração;
- não altere a conta até a prova ser validada;
- notifique o usuário após reset e permita reportar abuso;
- considere encerrar sessões existentes após a mudança;
- proteja suporte e recuperação de MFA com controles equivalentes.

## Related Attacks

Recovery fraco pode explorar [username enumeration](AUTH-01-username-enumeration.md) ou [tokens previsíveis](AUTH-10-predictable-recovery-tokens.md). Quando pula totalmente uma barreira, torna-se um caminho de [authentication bypass](AUTH-12-authentication-bypass.md).

## CWE

[CWE-640 — Weak Password Recovery Mechanism for Forgotten Password](https://cwe.mitre.org/data/definitions/640.html) corresponde diretamente a mecanismos de recuperação cuja evidência pode ser descoberta ou contornada.

## OWASP Relationship

O OWASP Forgot Password Cheat Sheet descreve mensagens, tokens, vínculo de conta e pós-reset. O WSTG possui testes para weak security questions e weak password change/reset.

## Key Takeaways

- Recuperação faz parte da autenticação e não pode ser mais fraca.
- Perguntas pessoais frequentemente são descobríveis.
- Todas as etapas precisam ser validadas no servidor.
- Reset seguro inclui contenção e notificação posterior.

## References

- [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
- [OWASP WSTG — Weak Security Question Answer](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication/08-Weak_Security_Question_Answer/)
- [OWASP WSTG — Weak Password Change or Reset](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication/09-Weak_Password_Change_or_Reset_Functionalities/)
- [MITRE CWE-640](https://cwe.mitre.org/data/definitions/640.html)
