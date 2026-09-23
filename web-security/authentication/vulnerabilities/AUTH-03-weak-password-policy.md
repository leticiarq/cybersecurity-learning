# AUTH-03 — Weak Password Policy

## Overview

Uma **weak password policy** permite senhas que podem ser adivinhadas com baixo custo: valores comuns, curtos, previsíveis ou já comprometidos.

Políticas modernas priorizam comprimento, bloqueio de senhas conhecidas, liberdade para usar password managers e troca diante de comprometimento. Exigir combinações rígidas de maiúsculas, números e símbolos não garante força e pode incentivar padrões previsíveis.

## How It Works

Atacantes não começam por todas as combinações possíveis. Eles priorizam senhas de vazamentos, palavras comuns e transformações humanas. Reutilização permite que uma credencial vazada em outro serviço funcione no atual.

```text
Senha comum/reutilizada -> lista priorizada -> tentativa online
Hash de senha vazado    -> guessing offline -> credencial recuperada
```

Um limite máximo pequeno, truncamento silencioso ou bloqueio de colagem também prejudica senhas únicas e longas.

## Example

`Empresa2026!` satisfaz uma regra de “maiúscula, número e símbolo”, mas segue um padrão previsível. Uma passphrase longa e única gerada ou armazenada por um password manager pode ser mais resistente.

## Impact

Senhas fracas elevam a chance de **credential compromise** e account takeover por brute force, password spraying ou credential stuffing. Após vazamento de hashes, também reduzem o custo de ataque offline.

## How to Identify

Em conta de teste, avalie comprimento mínimo e máximo, senhas comuns, senhas que contêm o identificador, colagem, compatibilidade com password managers e mudança de senha. Não teste credenciais reais vazadas.

Comportamento esperado: bloqueio de valores conhecidamente fracos sem regras que reduzam a usabilidade segura. Comportamento vulnerável: aceitação de senhas triviais ou truncamento não informado.

## Mitigation

- permita senhas e passphrases longas;
- compare novas senhas com blocklists de valores comuns ou comprometidos;
- permita colagem, password managers e caracteres Unicode conforme o sistema;
- não trunque silenciosamente;
- não imponha troca periódica sem motivo; troque diante de comprometimento;
- ofereça MFA e controles contra automação;
- armazene senhas conforme [AUTH-05](AUTH-05-insecure-password-storage.md).

## Related Attacks

Políticas fracas aumentam o sucesso de [tentativas automatizadas](AUTH-04-authentication-attempts.md). Reutilização conecta credential stuffing à [exposição de credenciais](AUTH-14-credential-exposure.md).

## CWE

[CWE-521 — Weak Password Requirements](https://cwe.mitre.org/data/definitions/521.html) corresponde a requisitos que permitem credenciais facilmente adivinháveis.

## OWASP Relationship

O OWASP Authentication Cheat Sheet apresenta controles modernos de força de senha. O WSTG inclui **WSTG-ATHN-07 — Weak Authentication Methods** para avaliar comprimento, reutilização e valores comuns.

## Key Takeaways

- Complexidade visual não substitui comprimento e imprevisibilidade.
- Senha única reduz o efeito de vazamentos em outros serviços.
- Blocklists complementam, mas não substituem, rate limiting e MFA.
- Política e armazenamento são problemas distintos.

## References

- [OWASP Authentication Cheat Sheet — Password Strength Controls](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#implement-proper-password-strength-controls)
- [OWASP WSTG — Weak Authentication Methods](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication/07-Weak_Authentication_Methods/)
- [NIST SP 800-63B](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [MITRE CWE-521](https://cwe.mitre.org/data/definitions/521.html)
