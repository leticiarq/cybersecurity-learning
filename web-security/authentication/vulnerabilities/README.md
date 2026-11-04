# Minhas anotações sobre vulnerabilidades de autenticação

Uma vulnerabilidade de autenticação enfraquece a confirmação da identidade ou a forma como a aplicação mantém essa identidade depois do login. Algumas falhas apenas revelam que uma conta existe; outras permitem assumir uma sessão ou ignorar completamente o login.

Organizei as falhas com os códigos `AUTH-01` a `AUTH-15` para facilitar minha revisão. Eles não são identificadores oficiais da OWASP ou do MITRE.

## Como eu enxergo o fluxo completo

```text
Descobrir a conta -> apresentar credenciais -> concluir MFA
        |                    |                   |
        v                    v                   v
     AUTH-01/02          AUTH-03/04/05         AUTH-11

Recuperar acesso -> criar e usar sessão -> encerrar acesso
        |                    |                   |
        v                    v                   v
     AUTH-09/10         AUTH-06/08/13          AUTH-07

Em qualquer etapa: bypass, exposição ou credencial padrão
                   AUTH-12/14/15
```

## Minha ordem de revisão

| Grupo | Conteúdo | Ideia central |
|---|---|---|
| Descoberta de contas | [AUTH-01](AUTH-01-username-enumeration.md) e [AUTH-02](AUTH-02-timing-enumeration.md) | Respostas podem revelar quais usuários existem |
| Senhas e tentativas | [AUTH-03](AUTH-03-weak-password-policy.md), [AUTH-04](AUTH-04-authentication-attempts.md) e [AUTH-05](AUTH-05-insecure-password-storage.md) | Senha forte também precisa de limite de tentativas e armazenamento seguro |
| Sessões | [AUTH-06](AUTH-06-session-cookie.md), [AUTH-07](AUTH-07-session-invalidation.md), [AUTH-08](AUTH-08-session-fixation.md) e [AUTH-13](AUTH-13-remember-me.md) | O acesso precisa ser protegido do início ao encerramento |
| Recuperação | [AUTH-09](AUTH-09-weak-password-recovery.md) e [AUTH-10](AUTH-10-predictable-recovery-tokens.md) | Recuperar a conta não pode ser mais fácil que entrar nela |
| MFA e bypass | [AUTH-11](AUTH-11-mfa-flaw.md) e [AUTH-12](AUTH-12-authentication-bypass.md) | Toda etapa obrigatória deve ser aplicada no servidor |
| Credenciais | [AUTH-14](AUTH-14-credential-exposure.md) e [AUTH-15](AUTH-15-default-credentials.md) | Um segredo só protege enquanto não é exposto ou conhecido |

## Três ataques que parecem iguais, mas não são

| Ataque | Estratégia |
|---|---|
| Brute force | Muitas senhas contra uma ou mais contas |
| Password spraying | Poucas senhas comuns contra muitas contas |
| Credential stuffing | Pares de usuário e senha vazados de outro serviço |

Essa diferença ajuda a entender por que um único limite por endereço IP ou por conta não resolve todos os cenários.

## Como organizei cada página

Em cada vulnerabilidade, procuro responder às mesmas perguntas:

1. qual é a falha em uma frase?
2. como ela aparece em um exemplo concreto?
3. que decisão do sistema está incorreta?
4. qual impacto ela produz?
5. como identificá-la de forma autorizada?
6. quais controles corrigem a causa?

## Regra para meus testes

Só devo testar sistemas próprios ou explicitamente autorizados, usando contas descartáveis e limites previamente combinados. Testes de login, recuperação e sessão podem bloquear usuários, disparar notificações, invalidar sessões ou causar indisponibilidade.

## Referências gerais

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/)
- [OWASP ASVS](https://owasp.org/projects/asvs)
