# AUTH-02 — Timing Enumeration

## Overview

**Timing enumeration** identifica contas por diferenças mensuráveis no tempo de resposta. A mensagem pode ser idêntica, mas uma categoria de usuário demora sistematicamente mais.

Ela difere de [Username Enumeration](AUTH-01-username-enumeration.md) baseada em conteúdo: aqui, a informação está no **tempo**, um canal lateral afetado por ruído de rede.

## How It Works

Uma aplicação pode encerrar cedo quando o usuário não existe, mas executar um password hash custoso quando a conta existe:

```text
Usuário inexistente -> consulta -> resposta
Usuário existente   -> consulta -> password hashing -> resposta
                                              |
                                    diferença estatística
```

Outro exemplo é enviar e-mail apenas para contas válidas. Mesmo com texto e status iguais, trabalho adicional pode alterar a distribuição dos tempos.

## Example

Em homologação, respostas para uma conta de teste conhecida se concentram em torno de uma faixa maior, enquanto identificadores inexistentes respondem mais rápido. Uma única requisição lenta não comprova nada; a indicação só aparece em amostras repetidas e controladas.

## Impact

O impacto direto é **information disclosure** sobre contas. Isso torna ataques direcionados mais eficientes, mas não fornece a senha nem causa account takeover isoladamente.

## How to Identify

Com autorização, alterne requisições entre casos conhecido e inexistente, mantenha os demais campos iguais e colete várias amostras. Compare distribuições, não apenas médias. Considere aquecimento de cache, balanceadores, filas, rate limiting, jitter, localização e carga do servidor.

Comportamento vulnerável: diferença consistente que persiste após controlar variáveis. Comportamento esperado: caminhos com custo comparável ou variação insuficiente para classificar contas com confiança.

## Mitigation

- execute verificação de custo equivalente para usuários existentes e inexistentes;
- use um hash fictício válido quando a conta não existe;
- não dependa apenas de atrasos fixos ou aleatórios;
- mantenha mensagens e demais propriedades equivalentes;
- trate chamadas externas de forma assíncrona quando adequado;
- combine com rate limiting e monitoramento.

## Related Attacks

Timing enumeration pode preparar [password spraying](AUTH-04-authentication-attempts.md) e ataques a [password recovery](AUTH-09-weak-password-recovery.md). É um caso específico de discrepância observável, mas merece tratamento separado pela necessidade de análise estatística.

## CWE

[CWE-208 — Observable Timing Discrepancy](https://cwe.mitre.org/data/definitions/208.html) descreve diferenças temporais que expõem informação sobre estado interno.

## OWASP Relationship

O **WSTG-IDNT-04** inclui análise de response times como forma de enumerar contas. O Authentication Cheat Sheet alerta que mensagens genéricas ainda podem vazar informação por tempos distintos.

## Key Takeaways

- O canal de informação é o tempo, não o texto.
- Latência e carga produzem falsos positivos; uma amostra não basta.
- Caminhos equivalentes são melhores que atrasos cosméticos.
- O resultado confirma uma conta, não sua credencial.

## References

- [OWASP WSTG — Account Enumeration and Guessable User Account](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/03-Identity_Management/04-Account_Enumeration_and_Guessable_User_Account/)
- [OWASP Authentication Cheat Sheet — Authentication Responses](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#authentication-responses)
- [MITRE CWE-208](https://cwe.mitre.org/data/definitions/208.html)
