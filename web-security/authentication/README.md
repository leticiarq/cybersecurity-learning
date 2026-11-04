# Minhas anotações sobre segurança de autenticação

Neste módulo, organizo o que preciso entender sobre autenticação: como uma aplicação confirma uma identidade, mantém o usuário autenticado e protege esse acesso. Quando Ana informa seu e-mail e sua senha, o sistema precisa responder à pergunta: **“há evidência suficiente de que esta pessoa controla a conta de Ana?”**

Essa confirmação não termina na tela de login. Depois de entrar, a aplicação ainda precisa reconhecer Ana nas próximas requisições, proteger sua sessão, permitir uma recuperação segura da conta e encerrar o acesso quando necessário.

## Meu mapa mental do processo

```text
Pessoa apresenta uma credencial
              |
              v
Aplicação confirma a identidade       <- autenticação
              |
              v
Aplicação cria uma sessão ou token
              |
              v
Aplicação decide o que ela pode fazer <- autorização
```

Autenticação e autorização são controles diferentes. Um cliente pode estar corretamente autenticado e, ainda assim, não ter autorização para abrir a área administrativa.

## Minha ordem de estudo

1. [Fundamentos de autenticação](authentication-basics.md)
   Aprenda o vocabulário essencial e acompanhe o caminho completo entre o login e uma requisição autenticada.

2. [JSON Web Token (JWT)](jwt/README.md)
   Entenda a estrutura `header.payload.signature`, o que a assinatura protege e as diferenças entre HS256 e RS256.

3. [Atividade prática com JWT](jwt/practical/README.md)
   Observe no código como Base64URL, o conteúdo assinado e as chaves participam da criação e da validação do token.

4. [Vulnerabilidades de autenticação](vulnerabilities/README.md)
   Estude 15 falhas comuns, com exemplos, formas seguras de identificação e medidas de proteção.

Quando um termo em inglês ou uma sigla atrapalhar meu raciocínio, posso consultar o [glossário](glossary.md).

## Como vou revisar este módulo

Ao terminar cada página, eu devo conseguir responder sem consultar o texto:

- qual problema esse mecanismo resolve?
- em que momento a aplicação toma uma decisão de segurança?
- qual informação precisa permanecer secreta?
- o que um invasor ganharia se o controle falhasse?
- qual defesa atua na causa da falha?

Se essas respostas estiverem claras, os nomes técnicos deixam de ser apenas uma lista para memorizar e passam a representar mecanismos que eu realmente compreendi.

## Referências gerais

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Web Security Testing Guide — Authentication Testing](https://owasp.org/www-project-web-security-testing-guide/)
