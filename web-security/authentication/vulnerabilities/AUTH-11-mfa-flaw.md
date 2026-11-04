# AUTH-11 — Falha na autenticação multifator (MFA)

## O que eu entendi, em uma frase

A aplicação exibe ou solicita um segundo fator, mas permite ignorá-lo ou validá-lo de forma incorreta.

## Ponto essencial: uma tela não prova proteção

Considere este fluxo:

```text
senha correta -> sessão parcialmente autenticada -> tela de MFA
                            |
                  acesso direto a /account
                            |
              servidor libera o recurso protegido
```

A interface mostrou o MFA, mas o servidor já concedeu uma sessão completa depois da senha. Ocultar a navegação no frontend não aplica o controle.

Outras falhas aparecem quando o desafio não está vinculado à mesma conta e sessão, quando um parâmetro controlado pelo cliente marca o fator como concluído ou quando recuperação e “lembrar dispositivo” oferecem um desvio mais fraco.

## Diferença que preciso lembrar: ausência e falha de MFA

Um sistema que usa somente senha pode estar inadequado ao risco, mas não possui necessariamente um bug de bypass. Aqui, a vulnerabilidade está em uma implementação que deveria exigir múltiplos fatores e não aplica essa exigência corretamente.

## Por que preciso prestar atenção

A falha remove a proteção esperada contra uma senha comprometida. Dependendo do fluxo, quem possui apenas o primeiro fator pode conseguir assumir a conta.

## Como eu reconheceria em ambiente autorizado

Com contas próprias, mapeie os estados antes e depois de cada fator. Confira navegação direta, APIs, aplicativo móvel, recuperação, “lembrar dispositivo”, troca e desativação do fator. Verifique também vínculo do desafio, expiração e limite de tentativas.

Nenhuma rota sensível deve aceitar um estado parcialmente autenticado.

## Como corrigir ou prevenir

- mantenha os estados de autenticação no servidor;
- conceda sessão completa somente depois de todos os fatores;
- vincule desafio, conta, sessão e finalidade;
- limite tentativas e expire desafios;
- aplique MFA de forma consistente em todos os canais;
- proteja cadastro, troca, recuperação e desativação dos fatores;
- prefira fatores resistentes a phishing quando o risco justificar;
- monitore mudanças sem registrar códigos secretos.

## O que eu preciso lembrar

- MFA precisa ser aplicado no backend, não apenas mostrado na interface.
- Estado parcial não deve alcançar recursos finais.
- Recuperação e canais alternativos fazem parte do mesmo controle.

## Referências técnicas

- [OWASP Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)
- [CWE-287 — Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- [CWE-308 — Use of Single-factor Authentication](https://cwe.mitre.org/data/definitions/308.html)
