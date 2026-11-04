# Como um JWT funciona — minhas anotações

## Primeiro eu preciso entender a finalidade

Suponha que um serviço de login confirme a identidade de Ana e precise informar a uma API que ela é a usuária `123`. Em vez de a API perguntar ao serviço de login a cada requisição, Ana pode apresentar um token assinado com essa informação.

O token carrega afirmações, por exemplo:

```text
“O emissor login.example afirma que o usuário 123
pode usar a API pedidos.example até as 10:30.”
```

Essas afirmações são chamadas de **claims**. Um JSON Web Token (JWT) define uma forma compacta de transportá-las. Quando o JWT é assinado, a API consegue verificar se o conteúdo foi alterado e se foi produzido por alguém que controla a chave esperada.

## As três partes

Um JWT assinado normalmente usa a serialização compacta de JWS:

```text
base64url(header).base64url(payload).base64url(signature)
```

### 1. Header: como o token foi processado

O header contém metadados. Um exemplo com HS256 é:

```json
{"alg":"HS256","typ":"JWT"}
```

- `alg` informa o algoritmo usado;
- `typ` indica o tipo do objeto.

O header ajuda no processamento, mas não deve decidir sozinho quais algoritmos são aceitos. O verificador precisa ter uma lista segura configurada previamente.

### 2. Payload: quais afirmações estão sendo feitas

```json
{
  "iss": "login.example",
  "sub": "user-123",
  "aud": "pedidos.example",
  "exp": 1710001800
}
```

Esse conteúdo afirma quem emitiu o token, quem é o sujeito, qual serviço deve aceitá-lo e até quando ele vale. O payload não deve conter senha, chave, documento ou qualquer dado que precise permanecer secreto.

### 3. Signature: proteção contra alteração

Primeiro, header e payload são convertidos para Base64URL e unidos por um ponto:

```text
signing_input = base64url(header) + "." + base64url(payload)
```

O algoritmo usa esse texto e uma chave para gerar a terceira parte. Se alguém alterar um caractere do header ou do payload, o conteúdo assinado muda. A assinatura antiga deixa de corresponder.

## Base64URL não é criptografia

Base64URL apenas representa bytes com caracteres adequados para URLs. Qualquer pessoa que receba o token consegue decodificar as duas primeiras partes.

```text
Codificação:  muda a representação; pode ser revertida sem segredo.
Criptografia: busca esconder o conteúdo; exige a chave apropriada.
Assinatura:   permite detectar alterações e verificar a origem.
```

Portanto:

> Um JWT assinado protege a integridade do conteúdo, mas não sua confidencialidade.

JWTs também podem ser usados dentro de estruturas criptografadas, como JWE, mas isso é um mecanismo diferente do JWS assinado estudado aqui.

## Claims mais comuns

| Claim | Pergunta respondida |
|---|---|
| `iss` (*issuer*) | Quem emitiu o token? |
| `sub` (*subject*) | Sobre qual usuário ou entidade o token fala? |
| `aud` (*audience*) | Qual serviço deve aceitar o token? |
| `exp` (*expiration time*) | A partir de quando o token está expirado? |
| `nbf` (*not before*) | A partir de quando o token pode ser usado? |
| `iat` (*issued at*) | Quando ele foi emitido? |
| `jti` (*JWT ID*) | Qual é o identificador deste token? |

Os tempos usam **NumericDate**: quantidade de segundos desde `1970-01-01T00:00:00Z`. A presença de uma claim não garante nada sozinha. O destinatário precisa verificar se o valor corresponde à sua política.

Exemplo: uma assinatura pode ser válida, mas a API ainda deve rejeitar um token cujo `aud` aponta para outro serviço.

## Construção passo a passo

```text
Header  -> JSON -> bytes -> Base64URL --+
                                          +-> conteúdo a assinar
Payload -> JSON -> bytes -> Base64URL --+          |
                                                     v
                                              algoritmo + chave
                                                     |
                                                     v
                                                assinatura
```

Em detalhes:

1. o emissor cria o header e o payload;
2. serializa os dois objetos como JSON;
3. codifica seus bytes com Base64URL;
4. une os resultados com `.`;
5. assina exatamente esses bytes;
6. codifica a assinatura com Base64URL;
7. une as três partes com pontos.

A assinatura cobre as representações originais recebidas. O verificador não deve reconstruir outro JSON “equivalente”, pois espaços, ordem e codificação podem produzir bytes diferentes.

## Como o token chega à API

Um access token costuma ser enviado no cabeçalho HTTP:

```http
GET /pedidos HTTP/1.1
Host: pedidos.example
Authorization: Bearer eyJ...
```

`Bearer` significa que quem possui o valor pode apresentá-lo. Por isso, o token deve ser protegido como uma credencial: usar HTTPS, não aparecer em URLs e não ser registrado em logs.

## Validação passo a passo

Receber um token não significa confiar nele. O destinatário deve:

1. limitar o tamanho e conferir a estrutura esperada;
2. interpretar header e payload com segurança;
3. exigir o algoritmo configurado para aquele contexto;
4. selecionar uma chave proveniente de fonte confiável;
5. verificar a assinatura sobre as partes originais;
6. validar `iss`, `aud`, `exp`, `nbf` e todas as claims obrigatórias;
7. aplicar autorização depois de validar a identidade e o contexto.

Uma pequena tolerância de relógio pode ser necessária, mas não deve prolongar excessivamente a validade do token.

## O que a assinatura garante — e o que não garante

| A assinatura pode ajudar a garantir | Ela não garante sozinha |
|---|---|
| O conteúdo não foi alterado | O conteúdo permaneceu secreto |
| Alguém com a chave apropriada produziu o token | Quem apresenta o token é seu usuário original |
| As claims podem ser verificadas sem nova consulta ao emissor | O token não foi roubado ou copiado |
| O token corresponde aos bytes assinados | Logout, revogação e autorização |

Um token roubado pode ser reutilizado até expirar ou ser revogado. Uma assinatura válida também não torna verdadeiras claims que a aplicação deixou de validar.

## Exemplo de alteração

Considere um payload com `"role":"user"`. Se alguém decodificar o token, trocar para `"role":"admin"` e mantiver a assinatura antiga, a verificação falhará. Para criar uma assinatura que corresponda ao novo conteúdo, seria necessário controlar a chave de assinatura.

Isso é integridade. O conteúdo continuou legível durante todo o processo.

## Perguntas para minha revisão

- Por que Base64URL não protege um segredo?
- Qual parte exata do token é assinada?
- Por que assinatura válida não dispensa a validação de `aud` e `exp`?
- Por que um token roubado ainda pode funcionar sem nenhuma alteração?

Continue com [HS256](hs256.md) e [RS256](rs256.md).

## Referências

- [RFC 7519 — JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519)
- [RFC 7515 — JSON Web Signature](https://www.rfc-editor.org/rfc/rfc7515)
- [RFC 8725 — JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725)
