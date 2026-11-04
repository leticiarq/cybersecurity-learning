# AUTH-03 — Política de senhas fraca

## O que eu entendi, em uma frase

A aplicação aceita senhas fáceis de adivinhar, reutilizadas ou já conhecidas em vazamentos.

## Exemplo para eu fixar

`Empresa2026!` contém maiúscula, número e símbolo, mas segue um padrão humano previsível. Cumprir uma regra visual de complexidade não torna uma senha automaticamente forte.

Atacantes não começam testando todas as combinações. Eles priorizam senhas vazadas, palavras comuns e transformações como adicionar o ano e um ponto de exclamação.

```text
senha comum ou reutilizada -> lista priorizada -> tentativa online
hash vazado                -> tentativa offline -> possível recuperação
```

Uma senha longa, única e gerada ou armazenada por um gerenciador costuma resistir melhor a esse tipo de priorização.

## Por que preciso prestar atenção

Senhas fracas aumentam a chance de tomada da conta por brute force, password spraying e credential stuffing. Se hashes forem vazados, também diminuem o custo das tentativas offline.

## Como eu reconheceria em ambiente autorizado

Em uma conta de teste, avalie:

- comprimentos mínimo e máximo;
- aceitação de valores comuns ou do próprio nome de usuário;
- truncamento silencioso;
- suporte a colagem e gerenciadores de senha;
- comportamento durante criação e troca de senha.

Não use credenciais reais vazadas no teste.

## Como corrigir ou prevenir

- permita senhas e frases-senha longas;
- bloqueie valores comuns e comprometidos por meio de uma lista apropriada;
- permita colagem e uso de gerenciadores de senha;
- não trunque silenciosamente;
- não exija troca periódica sem indício de comprometimento;
- ofereça MFA e proteção contra automação;
- armazene as senhas conforme [AUTH-05](AUTH-05-insecure-password-storage.md).

## Não confunda

Política de senha trata **o que o usuário pode escolher**. Armazenamento de senha trata **como o servidor protege essa escolha**. Os dois controles são necessários e resolvem problemas diferentes.

## O que eu preciso lembrar

- Complexidade aparente não substitui comprimento e imprevisibilidade.
- Uma senha única limita o efeito de vazamentos de outros serviços.
- Lista de bloqueio, MFA e rate limiting são camadas complementares.

## Referências técnicas

- [OWASP Authentication Cheat Sheet — Password Strength](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#implement-proper-password-strength-controls)
- [NIST SP 800-63B](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [CWE-521 — Weak Password Requirements](https://cwe.mitre.org/data/definitions/521.html)
