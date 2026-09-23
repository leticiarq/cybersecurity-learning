# Atividade prática — Fluxo de JWT com HS256 e RS256

Esta atividade constrói e valida JWSs compactos sem uma biblioteca JWT. O objetivo é tornar visíveis JSON, Base64URL, signing input e assinatura. Os exemplos são didáticos: não implementam toda a validação de claims, gestão de chaves e tratamento de erros exigidos em produção.

## Estrutura

```text
practical/
├── README.md
├── hs256-flow/
│   └── main.py
└── rs256-flow/
    └── main.py
```

- [Código HS256](hs256-flow/main.py)
- [Código RS256](rs256-flow/main.py)
- Teoria: [JWT](../jwt.md), [HS256](../hs256.md), [RS256](../rs256.md) e [HS256 vs RS256](../hs256-vs-rs256.md)

## Pré-requisitos e execução

HS256 usa somente a biblioteca padrão:

```bash
python3 web-security/authentication/jwt/practical/hs256-flow/main.py
```

RS256 usa o pacote `cryptography` para executar RSA com primitivas seguras. O programa ainda monta e separa o JWT explicitamente:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install cryptography
python3 web-security/authentication/jwt/practical/rs256-flow/main.py
```

As chaves RSA são geradas em memória a cada execução e não são gravadas. Em produção, private keys exigem armazenamento protegido, controle de acesso e rotação.

## Base comum: serialização e Base64URL

Os dois programas:

1. criam dicionários Python para header e payload;
2. serializam JSON de forma compacta e determinística;
3. convertem os bytes com Base64URL;
4. removem o padding `=` da representação;
5. unem as duas partes com ponto.

```text
Header -> JSON -> bytes -> Base64URL --+
                                         +-> signing_input
Payload -> JSON -> bytes -> Base64URL --+
```

O código assina exatamente os bytes ASCII de:

```text
base64url(header) + "." + base64url(payload)
```

O JSON decodificado pode parecer igual e ainda ter outra representação de bytes. Na validação, usam-se as duas partes originais recebidas.

## Parte 1 — HS256

```text
Header -> JSON -> Base64URL
Payload -> JSON -> Base64URL
                 |
                 v
       Header codificado + "." + Payload codificado
                 |
          Secret Key + HMAC-SHA-256
                 |
                 v
       Signature -> Base64URL -> JWT
```

Na validação:

1. o token é separado em três partes;
2. o signing input é reconstruído sem alterar as partes;
3. HMAC-SHA-256 é executado com o mesmo segredo;
4. a assinatura recebida é decodificada;
5. `hmac.compare_digest` compara bytes sem encerramento antecipado baseado no primeiro byte diferente.

A mesma secret key assina e verifica. Consequentemente, todo verificador que conhece o segredo também consegue gerar tokens aceitos.

### Experimentos A e B

O programa cria um token válido e depois:

- **A — altera o payload**, preservando a assinatura original. O signing input muda e a assinatura falha;
- **B — usa uma chave incorreta**. O HMAC calculado é diferente e a validação falha.

## Parte 2 — RS256

```text
Header + Payload -> Base64URL -> Signing Input
                                      |
                            RSA/SHA-256 + Private Key
                                      |
                                      v
                              Signature -> JWT
```

Na validação:

```text
JWT -> partes -> Signing Input + Signature
                              + Public Key
                                      |
                           RSA/SHA-256 Verification
                                      |
                                Valid / Invalid
```

A **private key assina**; a **public key verifica**. A public key pode ser distribuída porque não contém a capacidade necessária para criar uma assinatura válida. O pacote `cryptography` aplica RSASSA-PKCS1-v1_5 com SHA-256; o código não tenta implementar RSA manualmente.

O payload não é criptografado. RSA está sendo usado como esquema de assinatura digital.

### Experimentos A e C

O programa:

- altera o payload e mantém a assinatura, que deixa de corresponder;
- verifica com a public key do par correto, com sucesso;
- verifica com a public key de outro par, sem sucesso.

## Comparação final

```text
HS256                         RS256

Secret Key                    Private Key
    |                              |
    v                              v
Assina JWT                     Assina JWT
    |                              |
    v                              v
Secret Key                    Public Key
    |                              |
    v                              v
Verifica JWT                  Verifica JWT
```

HS256 é simétrico porque o mesmo segredo concede as capacidades de criar e verificar o MAC. RS256 usa assinatura assimétrica porque essas capacidades são separadas entre private key e public key.

## Conceitos que não devem ser confundidos

| Conceito | Finalidade | Reversível? | Usa chave? |
|---|---|---|---|
| Codificação | Representar dados em outro alfabeto, como Base64URL | Sim | Não |
| Hashing | Produzir resumo de tamanho fixo | Não por projeto | Não |
| HMAC | Integridade e autenticação com segredo compartilhado | Não | Uma secret key |
| Criptografia | Proteger confidencialidade | Sim, com a chave apropriada | Sim |
| Assinatura digital | Integridade e autenticidade com par assimétrico | Não “desfaz” para obter a mensagem | Private key assina; public key verifica |

Assinar não esconde. Em ambos os exemplos, qualquer pessoa com o token pode decodificar header e payload.

## Resultado esperado

Ao acompanhar a saída e o código, verifique se você consegue explicar:

- como as três partes são construídas;
- o que forma o signing input;
- por que Base64URL pode ser revertido;
- por que mudar header ou payload invalida a assinatura;
- quais chaves assinam e verificam em cada algoritmo;
- por que validação de assinatura não substitui validação de claims.

## Referências

- [RFC 7515 — JSON Web Signature](https://www.rfc-editor.org/rfc/rfc7515)
- [RFC 7518 — JSON Web Algorithms](https://www.rfc-editor.org/rfc/rfc7518)
- [Python — hmac](https://docs.python.org/3/library/hmac.html)
- [cryptography — RSA](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)
