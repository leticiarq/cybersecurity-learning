# AUTH-09 — Recuperação de senha fraca

## O que eu entendi, em uma frase

O caminho para recuperar a conta exige uma prova mais fraca que o login normal.

## Como entendo a recuperação de conta

Quem conclui a recuperação pode escolher uma nova senha e assumir a conta. Portanto, esse fluxo é uma forma alternativa de provar identidade, não apenas uma função auxiliar.

```text
identificar a conta -> comprovar controle -> autorizar reset -> definir senha
                              |
                 evidência fraca ou etapa ignorada
                              |
                     tomada da conta
```

## Exemplo para eu fixar

Uma aplicação pergunta “qual é sua cidade natal?” e permite tentativas ilimitadas. A resposta aparece no perfil público da pessoa. Se acertar essa pergunta for suficiente para definir uma senha nova, o caminho de recuperação é muito mais fraco que o login.

Outras causas incluem troca da conta entre etapas, validação apenas no frontend, suporte humano com verificação insuficiente e ausência de limites.

## Por que preciso prestar atenção

A falha pode contornar a autenticação principal e permitir tomada da conta. Também pode causar indisponibilidade ao trocar a senha e remover o acesso do titular legítimo.

## Como eu reconheceria em ambiente autorizado

Com contas de teste, desenhe todas as etapas e transições. Verifique:

- se a conta pode ser trocada no meio do fluxo;
- se uma tela pode ser pulada por acesso direto ao endpoint;
- se perguntas usam informação pública;
- se tentativas são limitadas;
- se canais alternativos aplicam a mesma política;
- se o titular é notificado;
- o que acontece com sessões já abertas.

## Como corrigir ou prevenir

- use um canal previamente verificado e um token forte;
- não dependa de perguntas com respostas públicas ou estáticas;
- vincule cada etapa à mesma conta e transação;
- valide todo o estado no servidor;
- aplique limites e respostas que evitem enumeração;
- notifique o usuário após a mudança;
- encerre ou reavalie sessões existentes conforme o risco;
- proteja recuperação de MFA e atendimento humano com controles equivalentes.

## O que eu preciso lembrar

- Recuperação não pode ser uma “porta dos fundos” mais fraca.
- Cada etapa precisa pertencer à mesma conta e transação.
- O fluxo seguro também considera notificação e contenção após o reset.

## Referências técnicas

- [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
- [OWASP WSTG — Weak Password Change or Reset](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/04-Authentication/09-Weak_Password_Change_or_Reset_Functionalities/)
- [CWE-640 — Weak Password Recovery Mechanism](https://cwe.mitre.org/data/definitions/640.html)
