# Minhas anotações sobre JSON Web Token (JWT)

Um JWT é um formato para transportar afirmações (*claims*) entre sistemas. Na forma assinada estudada aqui, ele se parece com uma sequência de três blocos separados por pontos:

```text
header.payload.signature
```

A assinatura permite detectar alterações e verificar quem tinha a chave capaz de produzir o token. Ela **não esconde** o header nem o payload.

## Minha ordem de estudo

1. [Como um JWT funciona](jwt.md) — estrutura, Base64URL, claims, assinatura e validação.
2. [HS256](hs256.md) — o mesmo segredo assina e verifica.
3. [RS256](rs256.md) — a chave privada assina e a chave pública verifica.
4. [HS256 ou RS256?](hs256-vs-rs256.md) — escolha baseada na fronteira de confiança.
5. [Atividade prática](practical/README.md) — observe HMAC e um JWT RS256 funcionando no código.

Antes de avançar, preciso guardar esta ideia: **JWT é um formato, não uma solução completa de autenticação**. Expiração, revogação, transporte, armazenamento e autorização continuam sendo responsabilidades da aplicação.

## Referências

- [RFC 7519 — JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519)
- [RFC 7518 — JSON Web Algorithms](https://www.rfc-editor.org/rfc/rfc7518)
