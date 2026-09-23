# JSON Web Token (JWT)

JWT é um formato compacto para transportar um conjunto de claims entre partes. Um JWT pode ser assinado e/ou criptografado; nesta trilha, o foco está em **JWS compact serialization**, isto é, tokens assinados no formato `header.payload.signature`.

## Conteúdos

- [JWT: estrutura, claims e validação](jwt.md)
- [HS256: assinatura simétrica com HMAC-SHA-256](hs256.md)
- [RS256: assinatura assimétrica com RSA e SHA-256](rs256.md)
- [Comparação HS256 vs RS256](hs256-vs-rs256.md)
- [Atividade prática: construção e validação sem biblioteca JWT](practical/README.md)

Antes de escolher um algoritmo, é necessário definir emissores, verificadores, fronteiras de confiança, rotação de chaves e requisitos de revogação. A escolha do algoritmo não corrige validação incompleta de claims ou transporte inseguro.

## Referências

- [RFC 7519 — JSON Web Token (JWT)](https://www.rfc-editor.org/rfc/rfc7519)
- [RFC 7518 — JSON Web Algorithms (JWA)](https://www.rfc-editor.org/rfc/rfc7518)
