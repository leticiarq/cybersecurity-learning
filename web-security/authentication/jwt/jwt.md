# JSON Web Tokens (JWT)

## O que é e para que serve

**JSON Web Token (JWT)** é um formato compacto definido pela RFC 7519 para transportar **claims** entre partes. Claims são afirmações como “o sujeito deste token é o usuário 42” ou “este token expira em determinado instante”.

JWT descreve o formato, não uma estratégia completa de autenticação. Em APIs, um JWT assinado pode ser usado como access token porque o destinatário consegue verificar sua integridade e procedência. Ele também aparece em protocolos como OpenID Connect. Nem todo token é JWT, e nem todo JWT deve ser usado como credencial.

Neste estudo, “JWT assinado” representa um JWS em serialização compacta:

```text
base64url(header).base64url(payload).base64url(signature)
```

Um JWT também pode ser criptografado como JWE, mas esse é outro formato e não é o foco aqui.

## As três partes

### Header

Metadados que orientam o processamento. Em um token HS256:

```json
{"alg":"HS256","typ":"JWT"}
```

`alg` declara o algoritmo usado. O verificador não deve aceitar cegamente esse valor: a aplicação deve manter uma lista explícita de algoritmos esperados para aquele contexto.

### Payload

Objeto JSON com claims:

```json
{"sub":"1234567890","name":"Ana","iat":1710000000}
```

O payload não é um local seguro para senhas, chaves, documentos ou outros dados secretos.

### Signature

A assinatura é calculada sobre os textos Base64URL exatos do header e do payload, incluindo o ponto:

```text
signing_input = base64url(header) + "." + base64url(payload)
```

O algoritmo combina esse conteúdo com a chave apropriada. A assinatura resultante também é convertida para Base64URL e anexada ao token.

## Base64URL não é criptografia

Base64URL representa bytes usando caracteres seguros para URLs. Em relação ao Base64 tradicional, usa `-` e `_` no lugar de `+` e `/`, e normalmente omite `=` de preenchimento. Qualquer pessoa que receba o token consegue reverter essa codificação.

> O payload de um JWT comum assinado **não está criptografado** apenas porque aparece em Base64URL.

Codificação muda a representação; criptografia procura garantir confidencialidade com uma chave. A assinatura fornece integridade e autenticação da origem conforme o controle da chave, mas não esconde o conteúdo.

## Claims

A RFC define nomes de **registered claims**, cujo uso é opcional e dependente do perfil da aplicação:

| Claim | Nome | Finalidade |
|---|---|---|
| `iss` | Issuer | Identifica quem emitiu o token |
| `sub` | Subject | Identifica o sujeito do token |
| `aud` | Audience | Identifica o destinatário pretendido |
| `exp` | Expiration Time | Instante a partir do qual o token não deve ser aceito |
| `nbf` | Not Before | Instante antes do qual o token não deve ser aceito |
| `iat` | Issued At | Instante em que o token foi emitido |
| `jti` | JWT ID | Identificador do token, útil em alguns controles de replay/revogação |

Os valores de tempo são **NumericDate**, isto é, segundos desde 1970-01-01T00:00:00Z, desconsiderando leap seconds. Além dos registered claims, há claims públicos e privados definidos pelas partes. Um claim apenas informa algo; o verificador precisa conferir se ele satisfaz sua política.

## Exemplo decomposto

Para o header e o payload anteriores, as duas primeiras partes ficam:

```text
Header:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9

Payload:
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFuYSIsImlhdCI6MTcxMDAwMDAwMH0

Signature:
<resultado-base64url-da-assinatura>
```

O token final une as três partes com pontos:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFuYSIsImlhdCI6MTcxMDAwMDAwMH0.<assinatura>
```

A assinatura real depende do algoritmo e da chave; portanto, o marcador não é um token utilizável. A [atividade prática](practical/README.md) gera tokens completos.

## Criação e envio

1. O emissor cria header e payload.
2. Serializa cada objeto como JSON.
3. Converte ambos para Base64URL.
4. Concatena as partes com `.` para formar o signing input.
5. Assina esse conjunto com o algoritmo e a chave configurados.
6. codifica a assinatura em Base64URL e monta o token.

Em uma API, um access token frequentemente é enviado assim:

```http
GET /profile HTTP/1.1
Host: api.example
Authorization: Bearer eyJ...
```

`Bearer` significa que a posse do valor permite usá-lo. HTTPS é obrigatório para protegê-lo em trânsito, e o token não deve aparecer em URLs.

## Processo de validação

O recebimento de um token deve levar a uma sequência controlada:

1. impor limites de tamanho e exigir exatamente três partes para um JWS compacto;
2. decodificar e interpretar header e payload com segurança;
3. exigir o algoritmo previamente configurado, sem aceitar `none` nem troca inesperada de família;
4. selecionar uma chave confiável — nunca uma URL ou chave arbitrária controlada pelo token;
5. verificar a assinatura sobre as duas primeiras partes originais;
6. validar `iss`, `aud`, `exp`, `nbf` e demais claims exigidos pelo contexto;
7. aplicar autorização usando dados validados, e não somente decodificados.

Pode existir pequena tolerância de relógio (*clock skew*) configurada, mas ela não deve ampliar desnecessariamente a validade. O token deve ser rejeitado se expirado, ainda não válido, destinado a outra audiência ou emitido por uma fonte não confiável.

## Por que uma alteração invalida a assinatura?

Header e payload codificados fazem parte do signing input. Alterar um caractere muda a entrada do algoritmo. Sem a chave de assinatura, não é possível produzir a assinatura correspondente ao novo conteúdo. Reaproveitar a assinatura antiga faz a verificação falhar.

Isso detecta modificação, mas não impede leitura, cópia ou replay de um token válido. Um token roubado pode continuar utilizável até expirar ou ser revogado.

## O que um JWT protege — e o que não protege

| Pode oferecer | Não oferece automaticamente |
|---|---|
| Integridade do header e payload | Confidencialidade do conteúdo |
| Autenticidade vinculada ao controle da chave | Prova de que quem apresenta o token é o usuário original |
| Claims verificáveis sem consultar o emissor em cada requisição | Revogação, logout, autorização ou transporte seguro |

## Cuidados de segurança

- Use biblioteca madura em produção; o código deste repositório é didático.
- Fixe algoritmos aceitos e use a chave correta para cada emissor e finalidade.
- Valide assinatura **e** claims obrigatórios.
- Use chaves fortes, armazenamento seguro, rotação e identificadores de chave confiáveis.
- Mantenha access tokens curtos e minimize claims.
- Planeje revogação e rotação antes de adotar tokens autocontidos.
- Não misture tokens de ambientes, clientes ou finalidades diferentes.
- Evite registrar tokens; trate-os como credenciais.

Continue em [HS256](hs256.md), [RS256](rs256.md) e [HS256 vs RS256](hs256-vs-rs256.md).

## Referências

- [RFC 7519 — JSON Web Token (JWT)](https://www.rfc-editor.org/rfc/rfc7519)
- [RFC 7515 — JSON Web Signature (JWS)](https://www.rfc-editor.org/rfc/rfc7515)
- [RFC 8725 — JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725)
