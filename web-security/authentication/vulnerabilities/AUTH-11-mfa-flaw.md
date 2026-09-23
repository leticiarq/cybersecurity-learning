# AUTH-11 — MFA Flaw

## Overview

Uma **MFA flaw** é uma falha na implementação de um fluxo que deveria exigir múltiplos fatores. O sistema anuncia MFA, mas uma etapa pode ser pulada, desvinculada da sessão ou validada apenas no cliente.

Isso é diferente de **ausência de MFA**. Um sistema single-factor pode ser inadequado ao risco, mas não possui necessariamente um bypass de uma implementação existente.

## How It Works

```text
Senha válida -> estado "primeiro fator"
                      |
              etapa MFA esperada
                      |
       rota direta / estado manipulável / validação fraca
                      |
             sessão totalmente autenticada
```

O backend pode conceder sessão completa antes do segundo fator, confiar que o frontend fará o redirecionamento ou não vincular o desafio ao usuário e à transação.

## Example

Após validar a senha, uma aplicação mostra `/mfa`. Em laboratório, acessar diretamente `/account` funciona porque o backend já marcou a sessão como autenticada. A interface tem MFA; o controle server-side não.

## Impact

O defeito remove a proteção esperada contra senha comprometida e pode permitir account takeover. O impacto depende de o atacante já possuir o primeiro fator ou conseguir contornar todo o fluxo.

## How to Identify

Com contas próprias, mapeie estados antes e depois de cada fator. Teste navegação direta, APIs, mobile, recuperação, “remember device”, troca e desativação de fator. Verifique se desafios pertencem à mesma conta e transação e se tentativas são limitadas.

Comportamento esperado: nenhuma rota sensível aceita estado parcial. Vulnerável: frontend ou parâmetro controlável decide que MFA foi concluído.

## Mitigation

- modele estados de autenticação no servidor;
- conceda sessão completa somente após todos os fatores;
- vincule desafio, conta, sessão e finalidade;
- limite tentativas e expire desafios;
- aplique MFA de modo consistente em todos os canais;
- proteja enrolment, troca, recovery e desativação;
- prefira fatores resistentes a phishing quando o risco justificar;
- monitore mudanças e bypasses sem registrar códigos.

## Related Attacks

Uma falha pode resultar em [authentication bypass](AUTH-12-authentication-bypass.md). [Weak recovery](AUTH-09-weak-password-recovery.md) frequentemente contorna MFA. Limites de códigos pertencem também a [AUTH-04](AUTH-04-authentication-attempts.md).

## CWE

Não existe uma CWE única para toda falha de MFA. [CWE-287 — Improper Authentication](https://cwe.mitre.org/data/definitions/287.html) pode corresponder quando a implementação aceita prova insuficiente. [CWE-308](https://cwe.mitre.org/data/definitions/308.html) descreve uso de single-factor onde múltiplos fatores eram necessários; não deve ser usado automaticamente para qualquer bug em MFA.

## OWASP Relationship

O OWASP Multifactor Authentication Cheat Sheet aborda enrolment, reset, fatores e bypasses. O OWASP ASVS contém requisitos de MFA no capítulo de Authentication.

## Key Takeaways

- Presença de uma tela MFA não prova enforcement.
- Estado parcial nunca deve acessar recursos finais.
- Recovery e canais alternativos fazem parte da implementação.
- Ausência de MFA e MFA vulnerável não são a mesma falha.

## References

- [OWASP Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [MITRE CWE-287](https://cwe.mitre.org/data/definitions/287.html)
- [MITRE CWE-308](https://cwe.mitre.org/data/definitions/308.html)
