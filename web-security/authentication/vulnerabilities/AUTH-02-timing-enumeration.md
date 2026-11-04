# AUTH-02 — Enumeração por tempo de resposta

## O que eu entendi, em uma frase

Mesmo com mensagens idênticas, o tempo de resposta permite inferir se uma conta existe.

## Exemplo para eu fixar

Para uma conta existente, o servidor calcula um hash de senha deliberadamente custoso. Para uma conta inexistente, ele encerra o processamento imediatamente:

```text
Conta inexistente -> consulta --------------------> resposta
Conta existente   -> consulta -> hash de senha ---> resposta
                                      |
                              diferença de tempo
```

Uma requisição lenta não prova nada. Redes, filas e carga do servidor produzem variação. A indicação aparece quando várias amostras revelam uma diferença consistente entre os dois grupos.

## Por que preciso prestar atenção

O efeito direto é o mesmo da enumeração por conteúdo: descobrir contas válidas. Isso melhora a eficiência de ataques direcionados, mas não revela a senha nem toma a conta por si só.

## Como eu reconheceria em ambiente autorizado

Alterne requisições entre uma conta de teste conhecida e identificadores inexistentes, mantendo todos os demais campos iguais. Colete várias amostras e compare distribuições, não somente uma média.

Considere fatores como cache, balanceador, rate limiting, localização, aquecimento da aplicação e carga. Uma diferença só é relevante quando permanece depois de controlar essas variáveis.

## Como corrigir ou prevenir

- execute uma verificação de custo comparável para contas existentes e inexistentes;
- use um hash fictício válido quando o usuário não existir;
- evite caminhos com encerramento antecipado observável;
- mantenha também texto, status e formato equivalentes;
- trate chamadas externas de forma assíncrona quando for adequado;
- combine o tratamento com limites e monitoramento.

Atrasos fixos ou aleatórios apenas mascaram o sintoma e podem continuar distinguíveis com amostras suficientes.

## O que eu preciso lembrar

- O canal lateral é o tempo, não o conteúdo.
- É necessário medir um conjunto de respostas, não uma requisição isolada.
- Caminhos de processamento equivalentes são melhores que atrasos cosméticos.

## Referências técnicas

- [OWASP WSTG — Account Enumeration](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/03-Identity_Management/04-Account_Enumeration_and_Guessable_User_Account/)
- [OWASP Authentication Cheat Sheet — Authentication Responses](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#authentication-responses)
- [CWE-208 — Observable Timing Discrepancy](https://cwe.mitre.org/data/definitions/208.html)
