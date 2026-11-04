# AUTH-10 — Token de recuperação previsível

## O que eu entendi, em uma frase

O valor que autoriza a troca de senha pode ser adivinhado, reutilizado ou aplicado à conta errada.

## Quatro propriedades que preciso avaliar separadamente

Um token de recuperação seguro precisa ser:

| Propriedade | Pergunta |
|---|---|
| Imprevisível | Outra pessoa consegue adivinhar o valor? |
| Vinculado | Ele vale somente para aquela conta e ação? |
| Temporário | Expira em pouco tempo? |
| De uso único | Deixa de funcionar após o reset? |

Ter uma propriedade não compensa a ausência de outra. Um token aleatório ainda é inseguro se puder ser reutilizado indefinidamente.

## Exemplo para eu fixar

```text
reset-1042
reset-1043
reset-1044
```

Uma sequência permite estimar valores seguintes. Timestamp, ID incremental e gerador pseudoaleatório não criptográfico produzem o mesmo tipo de risco. Em outro caso, o valor pode ser forte, mas continuar válido depois de usado.

```text
pedido de reset -> token -> canal verificado -> nova senha
                       |
           previsível, sem vínculo ou sem expiração
```

## Por que preciso prestar atenção

Quem obtém um token válido pode trocar a senha e assumir a conta. Como links de recuperação aparecem em URLs, eles também podem vazar em histórico, logs ou cabeçalho `Referer`.

## Como eu reconheceria em ambiente autorizado

Use apenas contas próprias. Compare tokens sem tentar valores de terceiros. Observe comprimento, padrão aparente, conta vinculada, finalidade, expiração, uso único e invalidação depois de um novo pedido. Em revisão de código, confira o gerador e o armazenamento.

## Como corrigir ou prevenir

- gere valores com CSPRNG e entropia suficiente;
- aplique validade curta e consumo atômico de uso único;
- vincule token, usuário, ação e transação;
- invalide tokens anteriores quando apropriado;
- armazene uma representação protegida quando possível;
- entregue somente por canal verificado e HTTPS;
- nunca registre o valor completo;
- use rate limiting como camada adicional, não como compensação por baixa entropia.

## O que eu preciso lembrar

- O token funciona como uma credencial temporária.
- Entropia, vínculo, validade e uso único são controles diferentes.
- Valor forte também precisa ser protegido contra vazamento.

## Referências técnicas

- [OWASP Forgot Password Cheat Sheet — URL Tokens](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html#url-tokens)
- [CWE-330 — Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html)
- [CWE-640 — Weak Password Recovery Mechanism](https://cwe.mitre.org/data/definitions/640.html)
