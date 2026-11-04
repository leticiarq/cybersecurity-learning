# Minha atividade prática: de HMAC a um JWT assinado

Esta atividade torna visíveis os elementos que a teoria costuma esconder. O primeiro script demonstra o núcleo criptográfico do HS256, o HMAC. O segundo monta e valida um JWT completo com RS256.

Os exemplos são didáticos. Em produção, use uma biblioteca JWT madura, uma política completa de validação de claims e gerenciamento seguro de chaves.

## Estrutura atual

```text
practical/
├── README.md
├── hs256-flow/
│   └── jwt_hs256.py
└── rs256-flow/
    └── main.py
```

- [Exemplo de HMAC-SHA-256](hs256-flow/jwt_hs256.py)
- [Fluxo completo de JWT com RS256](rs256-flow/main.py)

## Parte 1: entenda o HMAC usado pelo HS256

Execute:

```bash
python3 web-security/authentication/jwt/practical/hs256-flow/jwt_hs256.py
```

O script realiza três conversões:

```text
mensagem em texto -> bytes ---+
                              +-> HMAC-SHA-256 -> código hexadecimal
chave em texto ----> bytes ---+
```

Observe que:

1. a mensagem continua existindo; HMAC não a criptografa;
2. a chave participa do cálculo;
3. mudar um caractere da mensagem ou da chave muda o resultado;
4. quem não possui a mesma chave não consegue reproduzir o código esperado.

Para fixar, posso alterar `message` e `key`, uma por vez, e comparar as saídas. O valor hexadecimal impresso representa bytes do HMAC de forma legível; ele ainda não é um JWT.

No HS256, o conteúdo passado ao HMAC seria:

```text
base64url(header) + "." + base64url(payload)
```

## Parte 2: acompanhe um JWT RS256 completo

O exemplo depende do pacote `cryptography`:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install cryptography
python3 web-security/authentication/jwt/practical/rs256-flow/main.py
```

O programa gera pares de chaves temporários em memória. Nenhuma chave é gravada no disco.

### Etapa A: serialização

Header e payload começam como dicionários Python. O programa os transforma em JSON compacto e depois em bytes UTF-8:

```text
dicionário -> JSON -> bytes
```

### Etapa B: Base64URL

Os bytes são representados com Base64URL e o padding opcional `=` é removido:

```text
Header  -> JSON -> bytes -> Base64URL --+
                                          +-> signing input
Payload -> JSON -> bytes -> Base64URL --+
```

O resultado ainda pode ser decodificado. Nenhum segredo foi aplicado até aqui.

### Etapa C: assinatura

As duas partes são unidas com um ponto. A chave privada RSA assina exatamente esses bytes usando SHA-256 e PKCS #1 v1.5:

```text
signing input + chave privada -> assinatura
```

A assinatura é convertida para Base64URL e acrescentada ao token como terceira parte.

### Etapa D: verificação

O verificador separa as três partes, reconstrói o signing input original e usa a chave pública correspondente:

```text
signing input + assinatura + chave pública -> válida ou inválida
```

O script executa três casos:

1. token original com a chave pública correta: assinatura válida;
2. payload alterado com a assinatura antiga: assinatura inválida;
3. token original com outra chave pública: assinatura inválida.

## Conceitos que não devem ser misturados

| Conceito | O que faz | Usa segredo ou chave? |
|---|---|---|
| Base64URL | Muda a representação dos bytes | Não |
| Hash | Produz um resumo de tamanho fixo | Não |
| HMAC | Protege integridade com segredo compartilhado | Sim, um segredo |
| Criptografia | Busca esconder o conteúdo | Sim |
| Assinatura digital | Protege integridade e relaciona a origem à chave privada | Par de chaves |

Assinar não esconde. Nos exemplos de JWT, header e payload continuam legíveis.

## Meu roteiro de observação

Ao ler a saída do programa RS256, preciso localizar nesta ordem:

1. os objetos originais;
2. o JSON produzido;
3. as representações Base64URL;
4. o signing input;
5. a assinatura em bytes e Base64URL;
6. o token final;
7. o resultado de cada tentativa de validação.

## O que eu preciso conseguir explicar ao final

- por que Base64URL é reversível;
- qual conteúdo é assinado;
- por que mudar o payload invalida a assinatura;
- por que uma chave pública diferente falha;
- por que a chave pública verifica, mas não assina;
- por que uma assinatura válida não substitui a validação das claims.

Volte à teoria de [JWT](../jwt.md), [HS256](../hs256.md), [RS256](../rs256.md) e [comparação dos algoritmos](../hs256-vs-rs256.md) quando algum passo não estiver claro.

## Referências

- [RFC 7515 — JSON Web Signature](https://www.rfc-editor.org/rfc/rfc7515)
- [RFC 7518 — JSON Web Algorithms](https://www.rfc-editor.org/rfc/rfc7518)
- [Python — hmac](https://docs.python.org/3/library/hmac.html)
- [cryptography — RSA](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)
