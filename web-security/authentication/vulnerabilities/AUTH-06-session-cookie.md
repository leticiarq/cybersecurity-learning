# AUTH-06 — Cookie de sessão inseguro

## O que eu entendi, em uma frase

O cookie que identifica a sessão pode ser exposto, enviado ao destino errado ou ter um valor fácil de prever.

## Por que o cookie é sensível

Depois do login, o navegador costuma receber um ID de sessão:

```http
Set-Cookie: session_id=r4nd0m...; Secure; HttpOnly; SameSite=Lax
```

Nas requisições seguintes, o navegador devolve esse valor. O servidor encontra a sessão e reconhece o usuário. Portanto, uma cópia do ID pode permitir reutilizar a sessão sem conhecer a senha.

```text
login -> servidor cria sessão -> navegador recebe o ID
                                      |
                           cada requisição envia o ID
```

## O que preciso saber sobre cada atributo

| Atributo | Proteção oferecida | Limite |
|---|---|---|
| `Secure` | Envia o cookie somente por HTTPS | Não impede outros vazamentos |
| `HttpOnly` | Impede leitura direta por JavaScript | Não corrige todas as consequências de XSS |
| `SameSite` | Restringe certos envios entre sites | Não substitui sempre a proteção contra CSRF |
| `Domain` e `Path` | Limitam onde o cookie é enviado | Precisam de escopo mínimo adequado |

Considere este exemplo:

```http
Set-Cookie: session_id=12345; Path=/
```

Além de não declarar os três atributos defensivos, o valor sequencial sugere previsibilidade. Atributos corretos também não compensariam um ID fraco.

## Por que preciso prestar atenção

Se outra pessoa obtiver ou prever um ID válido, poderá tentar assumir a sessão (*session hijacking*). O impacto acompanha os privilégios da vítima.

## Como eu reconheceria em ambiente autorizado

Inspecione cookies da sua própria sessão. Verifique atributos, escopo, duração, conteúdo e comportamento em HTTP e HTTPS. Compare IDs apenas para avaliar formato e aleatoriedade; não tente prever sessões reais de terceiros.

## Como corrigir ou prevenir

- use HTTPS durante toda a sessão e marque o cookie como `Secure`;
- use `HttpOnly` quando JavaScript não precisar do valor;
- escolha `SameSite` de acordo com o fluxo e mantenha defesa contra CSRF;
- restrinja `Domain` e `Path` e considere o prefixo `__Host-`;
- gere IDs opacos e imprevisíveis com CSPRNG;
- não coloque senha ou dados sensíveis desnecessários no cookie;
- aplique renovação, expiração e invalidação no servidor.

## O que eu preciso lembrar

- ID de sessão é uma credencial temporária.
- Cada atributo resolve uma parte diferente do problema.
- Segurança do cookie também depende do ciclo de vida no servidor.

## Referências técnicas

- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP WSTG — Cookie Attributes](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/02-Cookies_Attributes/)
- [CWE-614 — Cookie Without Secure](https://cwe.mitre.org/data/definitions/614.html)
- [CWE-1004 — Cookie Without HttpOnly](https://cwe.mitre.org/data/definitions/1004.html)
