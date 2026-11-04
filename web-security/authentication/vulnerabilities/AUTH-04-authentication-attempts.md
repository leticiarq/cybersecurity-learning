# AUTH-04 — Tentativas de autenticação sem restrição adequada

## O que eu entendi, em uma frase

A aplicação permite testar credenciais rápido demais, por tempo demais ou por um canal que não aplica os limites esperados.

## Três estratégias que preciso diferenciar

| Ataque | O que é testado |
|---|---|
| Brute force | Muitas senhas contra uma conta |
| Password spraying | Poucas senhas comuns contra muitas contas |
| Credential stuffing | Pares de usuário e senha obtidos em vazamentos |

Sem restrições, o atacante consegue ampliar o volume:

```text
muitas tentativas -> login/API/MFA/recuperação
                           |
                    sem limite efetivo
                           |
                 adivinhação em escala
```

## Por que um único limite não basta

Limitar somente por IP pode falhar quando as requisições vêm de várias origens. Limitar somente por conta permite que qualquer pessoa bloqueie repetidamente a conta de uma vítima. Além disso, API, aplicativo móvel, MFA e recuperação podem formar canais alternativos.

## Por que preciso prestar atenção

O volume aumenta a chance de adivinhar senhas e códigos curtos. Um bloqueio mal planejado também pode causar indisponibilidade ao permitir que terceiros travem contas legítimas.

## Como eu reconheceria em ambiente autorizado

Use uma conta descartável e uma quantidade pequena, previamente acordada, de tentativas incorretas. Observe se existem atraso progressivo, limitação, desafio ou alerta. Mapeie separadamente web, API, mobile, MFA e recuperação.

O objetivo é avaliar o controle, não descobrir uma senha. Não exceda os limites do escopo.

## Como corrigir ou prevenir

- combine sinais de conta, origem, dispositivo e comportamento agregado;
- use limitação de taxa e atrasos progressivos;
- projete bloqueios temporários que resistam a abuso de negação de serviço;
- aplique política consistente a todos os fatores e canais;
- registre eventos sem gravar credenciais e gere alertas;
- combine o controle com senhas fortes e MFA;
- não trate CAPTCHA como única defesa.

## O que eu preciso lembrar

- Limite por IP e limite por usuário têm pontos cegos diferentes.
- Bloqueio permanente pode virar uma ferramenta de ataque.
- Rate limiting reduz escala, mas não corrige senha fraca ou vazada.

## Referências técnicas

- [OWASP Authentication Cheat Sheet — Automated Attacks](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#protect-against-automated-attacks)
- [OWASP Credential Stuffing Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html)
- [CWE-307 — Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html)
