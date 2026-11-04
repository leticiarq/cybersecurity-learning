# AUTH-13 — “Lembrar de mim” inseguro

## O que eu entendi, em uma frase

O mecanismo de acesso persistente usa um token previsível, contém a senha ou não pode ser revogado.

## Como entendo o fluxo correto

“Lembrar de mim” mantém o acesso por mais tempo que uma sessão comum. Para isso, o navegador recebe uma credencial persistente própria:

```text
login + “lembrar de mim” -> token persistente aleatório
                                      |
                            visita futura apresenta o token
                                      |
                              servidor cria sessão curta
```

Esse token não deve ser a senha nem uma transformação reversível de `usuário:senha`.

## Exemplo para eu fixar

Uma aplicação grava Base64 de `email:senha` em um cookie por um ano. Base64 pode ser revertido e revela a senha. Em outro sistema, o valor é aleatório, mas a mesma cópia ainda funciona depois de “sair de todos os dispositivos”. Nesse caso, a falha está na revogação.

O risco também aumenta quando o token nunca expira ou não é renovado depois do uso.

## Por que preciso prestar atenção

Uma cópia roubada pode conceder acesso persistente. Se o token contiver a senha, o vazamento ainda pode atingir outros serviços onde ela foi reutilizada.

## Como eu reconheceria em ambiente autorizado

Com sua própria conta, inspecione formato, atributos e validade. Teste revogação após logout, troca de senha e encerramento de dispositivos. Observe se o token é rotacionado e se cria uma nova sessão curta.

## Como corrigir ou prevenir

- gere um valor aleatório com alta entropia;
- armazene no servidor apenas uma representação protegida quando possível;
- vincule o token a usuário, finalidade e registro de dispositivo;
- rotacione depois do uso e detecte reutilização quando aplicável;
- aplique expiração e revogação;
- invalide em eventos de risco;
- use cookie com `Secure`, `HttpOnly` e `SameSite` adequado;
- exija reautenticação em operações sensíveis;
- nunca armazene a senha no token.

## O que eu preciso lembrar

- Token persistente é uma credencial diferente da senha.
- Persistência aumenta a janela de uso depois de um vazamento.
- O mecanismo precisa de expiração, rotação e revogação.

## Referências técnicas

- [OWASP WSTG — Vulnerable Remember Password](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/04-Authentication_Testing/05-Testing_for_Vulnerable_Remember_Password/)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [CWE-539 — Persistent Cookies Containing Sensitive Information](https://cwe.mitre.org/data/definitions/539.html)
- [CWE-613 — Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)
