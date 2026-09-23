# AUTH-13 — Insecure Remember Me

## Overview

“Remember Me” mantém acesso por um período maior que a sessão comum. Uma implementação insegura usa tokens previsíveis, permanentes, não revogáveis ou derivados diretamente de credenciais.

O mecanismo deve usar uma credencial persistente própria. Ele não deve guardar a senha do usuário no navegador nem construir um token reversível com username e password.

## How It Works

```text
Login + opção Remember Me -> token persistente
                                  |
                 retorna em visita futura
                                  |
              servidor cria nova sessão curta
```

O risco aumenta quando o mesmo token funciona indefinidamente, permanece válido após logout ou troca de senha, ou não é rotacionado depois do uso.

## Example

Uma aplicação grava Base64 de `email:password` em cookie por um ano. Base64 pode ser revertido e expõe a senha. Outra aplicação usa valor aleatório, mas aceita a mesma cópia após “sair de todos os dispositivos”, indicando falha de revogação.

## Impact

Roubo do token pode conceder acesso persistente e account takeover. Armazenar senha no cookie também causa credential compromise que pode atingir outros serviços.

## How to Identify

Com conta própria, inspecione formato, atributos e validade. Teste revogação após logout, mudança de senha e encerramento de dispositivos; observe rotação e criação de nova sessão. Não tente tokens pertencentes a terceiros.

Comportamento esperado: token opaco, aleatório, revogável e separado da senha. Vulnerável: dados previsíveis, credenciais incorporadas ou persistência sem controle.

## Mitigation

- gere token aleatório de alta entropia;
- armazene representação protegida server-side;
- associe token a usuário, finalidade e registro de dispositivo;
- rotacione após uso e detecte reuse quando possível;
- aplique expiração e revogação;
- invalide em eventos de risco;
- use cookie `Secure`, `HttpOnly` e `SameSite` adequado;
- exija reautenticação para operações sensíveis;
- nunca armazene a senha no token.

## Related Attacks

O mecanismo amplia a janela de [session cookie exposure](AUTH-06-session-cookie.md) e depende de [session invalidation](AUTH-07-session-invalidation.md). Token previsível se relaciona aos princípios de [recovery token](AUTH-10-predictable-recovery-tokens.md), embora a finalidade seja diferente.

## CWE

Não há uma única CWE para toda implementação de Remember Me. [CWE-539 — Use of Persistent Cookies Containing Sensitive Information](https://cwe.mitre.org/data/definitions/539.html) aplica-se quando o cookie persistente contém informação sensível. Falhas de expiração podem se relacionar a [CWE-613](https://cwe.mitre.org/data/definitions/613.html).

## OWASP Relationship

O OWASP WSTG contém **Testing for Vulnerable Remember Password**. O Session Management Cheat Sheet fornece controles para cookies e ciclo de vida.

## Key Takeaways

- Remember Me não deve armazenar a senha.
- Token persistente deve ser revogável e rotacionável.
- Sessões de longa duração elevam o custo de um vazamento.
- Operações sensíveis ainda podem exigir reautenticação.

## References

- [OWASP WSTG v4.2 — Testing for Vulnerable Remember Password](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/04-Authentication_Testing/05-Testing_for_Vulnerable_Remember_Password/)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [MITRE CWE-539](https://cwe.mitre.org/data/definitions/539.html)
- [MITRE CWE-613](https://cwe.mitre.org/data/definitions/613.html)
