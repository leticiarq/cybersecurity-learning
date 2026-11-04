# AUTH-07 — Sessão não invalidada corretamente

## O que eu entendi, em uma frase

Uma sessão que deveria ter terminado continua sendo aceita pelo servidor.

## Exemplo para eu fixar

Ana copia o cookie de sua própria sessão em um ambiente de teste e clica em “Sair”. Depois, reapresenta a cópia antiga à API. Se a requisição ainda for aceita, o logout removeu o cookie do navegador, mas não invalidou a sessão no servidor.

```text
ID válido -> logout
               |
      navegador apaga o cookie
               |
      servidor mantém a sessão válida
               |
cópia antiga ainda funciona
```

Fechar uma aba ou apagar um cookie não altera automaticamente o estado mantido no backend.

## Quando espero que uma sessão termine

- logout;
- tempo ocioso ou tempo máximo atingido;
- troca ou recuperação de senha;
- desativação da conta;
- encerramento administrativo;
- suspeita de comprometimento.

Sessões armazenadas no servidor podem ser removidas ou marcadas como inválidas. Tokens autocontidos exigem outra estratégia, como validade curta, versão, lista de revogação ou rotação de refresh token.

## Por que preciso prestar atenção

Uma sessão copiada anteriormente continua concedendo acesso. Isso prolonga uma invasão e dificulta a contenção mesmo depois de a vítima trocar a senha ou usar “sair de todos os dispositivos”.

## Como eu reconheceria em ambiente autorizado

Com uma conta própria, guarde identificadores antes do logout e de outros eventos de segurança. Reapresente-os somente no ambiente autorizado e confirme se recursos protegidos os rejeitam. Avalie também timeout ocioso, timeout absoluto e sessões concorrentes.

## Como corrigir ou prevenir

- invalide a sessão no servidor durante o logout;
- defina tempos ocioso e absoluto proporcionais ao risco;
- encerre ou reavalie sessões depois de reset de senha e eventos críticos;
- permita ao usuário encerrar outras sessões;
- rotacione refresh tokens e detecte reutilização quando aplicável;
- mantenha relógios e armazenamento de sessão consistentes;
- não dependa apenas de apagar o cookie no cliente.

## Uma diferença que preciso lembrar

Expiração encerra uma credencial quando o tempo acaba. Revogação a encerra antes desse momento. Uma estratégia segura costuma precisar das duas.

## Referências técnicas

- [OWASP Session Management Cheat Sheet — Session Expiration](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#session-expiration)
- [OWASP WSTG — Logout Functionality](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/06-Logout_Functionality/)
- [CWE-613 — Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)
