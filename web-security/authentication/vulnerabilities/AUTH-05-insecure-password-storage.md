# AUTH-05 — Insecure Password Storage

## Overview

**Insecure password storage** deixa senhas recuperáveis ou baratas de adivinhar após acesso ao banco de dados. A senha normalmente não precisa ser recuperada: o servidor deve apenas verificar uma tentativa.

Por isso, plaintext, encoding e encryption reversível não são substitutos de **password hashing**.

## How It Works

| Técnica | Propriedade | Adequação para senhas |
|---|---|---|
| Plaintext | Valor original armazenado | Inadequada |
| Encoding | Representação reversível sem chave | Inadequada |
| Encryption | Reversível com chave | Normalmente inadequada |
| Hash geral rápido | Irreversível, mas barato de testar | Inadequada isoladamente |
| Password hashing | Salt e custo configurável | Projetada para este uso |

```text
Cadastro: senha + salt único -> password hashing -> hash armazenado
Login: tentativa + salt      -> password hashing -> comparação
```

O `salt` é único e não secreto; impede que senhas iguais gerem registros iguais e reduz o valor de tabelas pré-computadas. Argon2id, scrypt, bcrypt e PBKDF2 são construções específicas, com escolha e parâmetros dependentes da plataforma e dos requisitos.

## Example

Uma aplicação armazena `base64(password)`. Após uma leitura indevida do banco, qualquer pessoa reverte Base64 imediatamente. Em outro caso, SHA-256 sem salt permite guesses muito rápidos. Ambos são diferentes de password hashing deliberadamente custoso.

## Impact

Uma violação do banco pode causar **credential compromise** em massa, account takeover local e impacto em outros serviços devido à reutilização. Encryption concentra o risco adicional na chave de descriptografia.

## How to Identify

Em revisão autorizada de código e arquitetura, identifique algoritmo, salt, parâmetros, truncamento, migração e localização de secrets. Nunca solicite ou exponha senhas reais. Um hash de comprimento fixo não prova armazenamento seguro.

## Mitigation

- prefira Argon2id quando disponível; use alternativas maduras conforme requisitos;
- gere salt único automaticamente;
- calibre custo e reavalie ao longo do tempo;
- use APIs de frameworks e bibliotecas mantidas;
- compare resultados com função apropriada;
- faça rehash gradual após login quando os parâmetros mudarem;
- mantenha eventual `pepper` separado do banco; ele não substitui salt;
- nunca implemente primitivas criptográficas manualmente.

## Related Attacks

Armazenamento inseguro viabiliza password cracking offline. [Políticas fracas](AUTH-03-weak-password-policy.md) e [credential exposure](AUTH-14-credential-exposure.md) ampliam o impacto.

## CWE

[CWE-256 — Plaintext Storage of a Password](https://cwe.mitre.org/data/definitions/256.html) aplica-se diretamente ao caso plaintext. [CWE-916 — Use of Password Hash With Insufficient Computational Effort](https://cwe.mitre.org/data/definitions/916.html) cobre hashes ou parâmetros baratos. Nenhuma das duas, isoladamente, representa todas as formas possíveis do problema.

## OWASP Relationship

O OWASP Password Storage Cheat Sheet fornece seleção e operação de password hashing. O OWASP ASVS inclui requisitos de armazenamento de credenciais no capítulo de Authentication.

## Key Takeaways

- Base64 é encoding, não proteção.
- Encryption é reversível e normalmente desnecessária para senhas.
- SHA-256 isolado é rápido demais para password storage.
- Salt, algoritmo e parâmetros devem ser avaliados em conjunto.

## References

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [MITRE CWE-256](https://cwe.mitre.org/data/definitions/256.html)
- [MITRE CWE-916](https://cwe.mitre.org/data/definitions/916.html)
