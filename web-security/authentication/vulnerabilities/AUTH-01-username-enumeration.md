# AUTH-01 — Username Enumeration

## Overview

**Username enumeration** ocorre quando respostas da aplicação permitem distinguir contas existentes de inexistentes. Em termos simples, o sistema confirma indiretamente “essa pessoa tem uma conta aqui”.

Tecnicamente, a diferença pode estar na mensagem, status HTTP, tamanho do corpo, redirecionamento, cabeçalhos ou sequência de telas. O código `AUTH-01` é apenas a convenção interna deste repositório.

## How It Works

Fluxos de login, cadastro, convite e recuperação consultam o cadastro de usuários. Quando seus caminhos externos não são equivalentes, a resposta funciona como um oráculo:

```text
Identificador -> Mecanismo de autenticação
                         |
             +-----------+-----------+
             |                       |
       Conta existente         Conta inexistente
             |                       |
      Resposta diferente -> Informação revelada
```

Uma mensagem genérica não basta se outros elementos continuam diferentes.

## Example

Uma aplicação fictícia responde `401 "Senha incorreta"` para `ana@example.test`, mas `404 "Conta não encontrada"` para um endereço inexistente. A senha de Ana não foi descoberta, porém sua conta foi confirmada.

## Impact

O impacto direto é **information disclosure** e possível perda de privacidade. A lista de contas válidas reduz a incerteza de ataques posteriores, como phishing direcionado, password spraying e credential stuffing. Account takeover não é automático: depende de outra fraqueza ou credencial comprometida.

## How to Identify

Em avaliação autorizada, compare uma conta de teste conhecida com identificadores certamente inexistentes em todos os fluxos de identidade. Observe mensagem, status, comprimento, headers, redirecionamento e etapas seguintes.

Comportamento esperado: respostas externas equivalentes. Comportamento vulnerável: diferenças repetíveis que classificam a existência da conta. Variações exclusivamente temporais são tratadas em [AUTH-02](AUTH-02-timing-enumeration.md).

## Mitigation

- use mensagens genéricas, como “credenciais inválidas”;
- mantenha status, formato e navegação equivalentes;
- em recuperação, informe que instruções serão enviadas *caso* a conta exista;
- reduza diferenças de processamento observáveis;
- aplique rate limiting e monitoramento em todos os fluxos de identidade;
- mantenha detalhes diagnósticos apenas em logs protegidos, sem credenciais.

## Related Attacks

Enumeração pode fornecer alvos para [password spraying e brute force](AUTH-04-authentication-attempts.md), exploração de [senhas fracas](AUTH-03-weak-password-policy.md) e tentativas com [credenciais padrão](AUTH-15-default-credentials.md).

## CWE

[CWE-204 — Observable Response Discrepancy](https://cwe.mitre.org/data/definitions/204.html) descreve respostas diferentes que revelam estado interno. A correspondência é direta quando a existência da conta é inferida por diferenças observáveis.

## OWASP Relationship

O OWASP WSTG documenta o teste **WSTG-IDNT-04 — Account Enumeration and Guessable User Account**. O OWASP Authentication Cheat Sheet recomenda respostas genéricas e equivalentes para falhas de autenticação.

## Key Takeaways

- Username geralmente não é a senha, mas sua confirmação reduz o espaço de ataque.
- Mensagem igual não resolve diferenças de status, tamanho ou fluxo.
- Timing enumeration é um canal específico e possui análise própria.
- Testes devem usar contas e limites autorizados.

## References

- [OWASP WSTG — Account Enumeration and Guessable User Account](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/03-Identity_Management/04-Account_Enumeration_and_Guessable_User_Account/)
- [OWASP Authentication Cheat Sheet — Authentication Responses](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#authentication-responses)
- [MITRE CWE-204](https://cwe.mitre.org/data/definitions/204.html)
