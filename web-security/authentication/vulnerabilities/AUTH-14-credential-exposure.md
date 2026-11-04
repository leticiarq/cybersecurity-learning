# AUTH-14 — Exposição de credenciais

## O que eu entendi, em uma frase

Uma senha, token, chave de API ou ID de sessão aparece em um local acessível a quem não deveria vê-lo.

## O que considero uma credencial

Qualquer valor que conceda acesso precisa de proteção. Isso inclui:

- senhas e códigos temporários;
- tokens de acesso e recuperação;
- cookies e IDs de sessão;
- chaves de API e chaves privadas.

## Onde preciso procurar vazamentos

```text
credencial -> componente legítimo
                  |
             cópia secundária
                  |
     URL / log / trace / analytics / erro / código
```

Considere `GET /login?password=exemplo`. Mesmo com HTTPS, a URL pode aparecer em histórico, logs de servidor e ferramentas intermediárias. HTTPS protege o transporte; não impede que os próprios componentes registrem o endereço.

Segredos versionados no código também se propagam por clones, caches e backups. Apagar apenas o arquivo visível não torna a credencial secreta novamente.

## Por que preciso prestar atenção

Quem obtém uma credencial pode usar os privilégios associados a ela. O alcance depende de validade, escopo, reutilização e possibilidade de revogação.

## Como eu reconheceria em ambiente autorizado

Use credenciais fictícias para rastrear propagação em requisições, respostas, logs sanitizados, traces, analytics, relatórios de erro, repositórios e configuração. Não copie segredos reais para relatórios.

## Como corrigir ou prevenir

- use TLS e nunca envie credenciais em URLs;
- envie senhas no corpo apropriado de uma requisição HTTPS;
- aplique redação em logs, traces e mensagens de erro;
- use gerenciador de segredos e menor privilégio;
- não versione segredos e adote detecção preventiva;
- reduza escopo e validade de tokens;
- proteja backups e ambientes de suporte;
- tenha mecanismos de rotação e revogação.

Se ocorrer exposição, trate-a como incidente: revogue ou rotacione o segredo e investigue o uso. Apagar uma cópia não desfaz as demais.

## O que eu preciso lembrar

- Tokens e IDs de sessão são credenciais.
- HTTPS não impede vazamento em URL, log ou código.
- Minimização e redação reduzem a propagação.

## Referências técnicas

- [OWASP Logging Cheat Sheet — Data to Exclude](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude)
- [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- [CWE-522 — Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html)
