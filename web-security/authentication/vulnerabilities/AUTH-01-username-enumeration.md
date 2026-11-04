# AUTH-01 — Enumeração de usuários

## O que eu entendi, em uma frase

A aplicação revela, por diferenças em suas respostas, se uma conta existe ou não.

## Exemplo para eu fixar

Durante o login, o sistema responde:

```text
ana@example.test       -> “Senha incorreta”
naoexiste@example.test -> “Conta não encontrada”
```

Nenhuma senha foi descoberta. Mesmo assim, a primeira mensagem confirmou que Ana possui uma conta. Essa informação reduz o trabalho necessário para ataques posteriores.

## Como entendo o vazamento da informação

```text
Identificador informado
          |
          v
  aplicação consulta a conta
       /             \
 existe             não existe
    |                   |
resposta A           resposta B
       \             /
        diferença observável
```

A diferença não precisa estar no texto. Ela pode aparecer no status HTTP, tamanho da resposta, cabeçalhos, redirecionamento ou próxima tela. Uma mensagem genérica não resolve o problema se os outros sinais continuam diferentes.

## Por que preciso prestar atenção

O impacto direto é divulgação de informação e possível perda de privacidade. Uma lista de contas válidas facilita phishing direcionado, password spraying e credential stuffing. A enumeração sozinha não fornece a senha e não causa automaticamente tomada da conta.

## Como eu reconheceria em ambiente autorizado

Compare uma conta de teste conhecida com identificadores certamente inexistentes nos fluxos de login, cadastro, convite e recuperação. Mantenha os outros campos iguais e observe se as diferenças são repetíveis.

O comportamento desejado é externamente equivalente. Se a diferença ocorrer apenas no tempo, consulte [AUTH-02](AUTH-02-timing-enumeration.md).

## Como corrigir ou prevenir

- use mensagens genéricas, como “credenciais inválidas”;
- mantenha status, formato e navegação equivalentes;
- na recuperação, diga que as instruções serão enviadas **caso** a conta exista;
- reduza diferenças de processamento observáveis;
- aplique limites e monitoramento a todos os fluxos de identidade;
- deixe detalhes diagnósticos somente em logs protegidos, sem credenciais.

## O que eu preciso lembrar

- Nome de usuário não é senha, mas confirmar sua existência ajuda outros ataques.
- Texto igual não basta se status, tamanho ou fluxo forem diferentes.
- O teste deve usar contas e limites autorizados.

## Referências técnicas

- [OWASP WSTG — Account Enumeration](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/03-Identity_Management/04-Account_Enumeration_and_Guessable_User_Account/)
- [OWASP Authentication Cheat Sheet — Authentication Responses](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#authentication-responses)
- [CWE-204 — Observable Response Discrepancy](https://cwe.mitre.org/data/definitions/204.html)
