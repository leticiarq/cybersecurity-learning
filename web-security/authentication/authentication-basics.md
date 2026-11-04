# Fundamentos de autenticação — minhas anotações

## A ideia central

Imagine que Ana deseja ver seus pedidos em uma loja virtual. Informar `ana@example.com` apenas diz **qual conta** ela quer usar. A senha fornece uma evidência de que ela controla essa conta. Se a evidência for aceita, a aplicação cria uma forma temporária de reconhecer Ana nas próximas páginas.

Esse exemplo contém quatro conceitos diferentes:

| Conceito | Pergunta que responde | Exemplo |
|---|---|---|
| Identidade | Quem é representado no sistema? | A conta de Ana |
| Identificador | Qual conta está sendo solicitada? | `ana@example.com` |
| Credencial | Que evidência será apresentada? | Senha, chave de acesso ou código temporário |
| Autenticação (AuthN) | A evidência é suficiente? | Conferir a senha e o segundo fator |

O identificador geralmente não é secreto. A credencial deve ser protegida, pois outra pessoa pode usá-la para se passar pelo titular da conta.

## Autenticação não é autorização

Depois de confirmar quem está fazendo a requisição, a aplicação ainda precisa decidir o que essa identidade pode fazer. Essa segunda decisão é a **autorização (AuthZ)**.

| Situação | Controle aplicado |
|---|---|
| Conferir a senha de Ana | Autenticação |
| Permitir que Ana veja os próprios pedidos | Autorização |
| Impedir Ana de abrir o painel de administrador | Autorização |

Uma forma simples de lembrar:

```text
Autenticação: quem está pedindo?
Autorização:  essa pessoa pode fazer isso?
```

A autorização deve ser verificada em toda operação protegida. O fato de alguém ter feito login não concede acesso a todos os recursos.

## O que acontece durante um login

```text
1. Ana envia identificador e senha por HTTPS
2. O servidor localiza a conta
3. O servidor verifica a senha armazenada de forma segura
4. Se necessário, solicita um segundo fator
5. O servidor cria uma sessão ou emite tokens
6. Nas próximas requisições, reconhece Ana por essa sessão ou token
7. Para cada recurso, verifica também a autorização
```

Uma falha pode ocorrer em qualquer etapa. Mensagens diferentes podem revelar quais contas existem; tentativas ilimitadas podem facilitar adivinhação; uma sessão mal protegida pode ser roubada mesmo que a senha seja forte.

## Como a aplicação “lembra” do login

O protocolo HTTP não se lembra automaticamente de uma requisição anterior. Por isso, a aplicação precisa estabelecer um contexto autenticado. Duas abordagens comuns são sessões mantidas no servidor e tokens autocontidos.

### Sessão mantida no servidor

Após o login, o servidor cria um registro parecido com este:

```text
ID da sessão: r4nd0m...
Usuário:      Ana
Criada em:    10:00
Expira em:    10:30
```

O navegador recebe apenas o identificador aleatório, normalmente em um cookie:

```http
Set-Cookie: session_id=r4nd0m...; Secure; HttpOnly; SameSite=Lax
```

Nas requisições seguintes, o navegador devolve o cookie. O servidor procura o registro correspondente e recupera a identidade de Ana.

O ID da sessão passa a funcionar como uma credencial temporária. Quem roubar uma cópia válida poderá tentar reutilizá-la sem conhecer a senha. Por isso, ele precisa ser imprevisível, protegido durante o transporte, renovado depois do login e invalidado no logout.

Os atributos do cookie têm funções diferentes:

- `Secure`: envia o cookie somente por HTTPS;
- `HttpOnly`: impede que JavaScript leia diretamente seu valor;
- `SameSite`: limita alguns envios iniciados por outros sites e ajuda na defesa contra CSRF.

Esses atributos são camadas de proteção. Eles não substituem expiração, invalidação, renovação do ID nem controles específicos contra CSRF.

### Token apresentado pelo cliente

Em outra arquitetura, o cliente recebe um token e o apresenta a cada chamada:

```http
Authorization: Bearer <token>
```

Um token opaco é apenas um valor que o servidor precisa consultar. Um token autocontido, como um JWT assinado, carrega afirmações que podem ser verificadas pelo destinatário.

| Aspecto | Sessão no servidor | Token autocontido assinado |
|---|---|---|
| Onde fica o estado principal | No armazenamento do servidor | Dentro das afirmações do token |
| Como o servidor reconhece o usuário | Consulta o ID da sessão | Valida assinatura e afirmações |
| Revogação imediata | Em geral, simples | Pode exigir lista, versão ou validade curta |
| Risco se for roubado | Reutilização da sessão | Reutilização do token até expirar ou ser revogado |

“Autocontido” não significa “sem estado em todo o sistema”. Logout, refresh tokens, dispositivos conectados e revogação frequentemente exigem algum estado no servidor.

Veja [JSON Web Token](jwt/jwt.md) para estudar esse formato em detalhes.

## Fatores de autenticação e MFA

Um fator é o tipo de evidência apresentado:

- **algo que você sabe**: senha ou PIN;
- **algo que você possui**: chave física, smart card ou aplicativo autenticador;
- **algo que você é**: característica biométrica.

**MFA** exige fatores de categorias independentes. Senha mais PIN são dois segredos, mas pertencem à mesma categoria (“algo que você sabe”); portanto, não formam MFA por si só. **2FA** é o caso de MFA com exatamente dois fatores.

O segundo fator só é útil se não puder ser facilmente ignorado. Cadastro, troca, recuperação e desativação do MFA precisam de proteção equivalente à do login.

## Como senhas devem ser armazenadas

O servidor não precisa recuperar a senha original. Ele precisa apenas verificar se a tentativa atual corresponde à senha cadastrada. Por isso, senhas não devem ser salvas em texto puro, Base64 ou criptografia reversível.

O fluxo correto usa uma função própria para **password hashing**:

```text
Cadastro:
senha + salt único -> função de password hashing -> hash armazenado

Login:
tentativa + salt armazenado -> mesma função -> comparação com o hash
```

- o `salt` é um valor único para cada senha e pode ser armazenado junto com o hash;
- a função deve ser deliberadamente custosa, para reduzir a velocidade de tentativas offline;
- algoritmos apropriados incluem Argon2id, scrypt, bcrypt e PBKDF2, conforme a plataforma;
- SHA-256 isolado é rápido demais e não é adequado para esse uso;
- um `pepper` opcional é um segredo guardado fora do banco, mas não substitui o `salt` nem o algoritmo correto.

## Onde as falhas costumam aparecer

| Etapa | Exemplo de falha |
|---|---|
| Identificação da conta | Respostas revelam quais usuários existem |
| Verificação da senha | Tentativas ilimitadas ou senhas fracas |
| Segundo fator | Etapa de MFA pode ser ignorada |
| Recuperação | Link previsível ou pergunta fácil de descobrir |
| Criação da sessão | ID antigo não é renovado após o login |
| Uso da sessão | Cookie ou token é exposto |
| Encerramento | Logout não invalida a sessão no servidor |
| Autorização | Usuário autenticado acessa recurso que não lhe pertence |

O [catálogo de vulnerabilidades](vulnerabilities/README.md) aprofunda cada caso.

## Perguntas para minha revisão

Antes de avançar, eu devo conseguir explicar:

1. por que informar um e-mail não prova identidade;
2. por que um session ID precisa ser protegido como uma senha temporária;
3. por que dois segredos de conhecimento não formam MFA;
4. por que SHA-256 puro é inadequado para armazenar senhas;
5. por que login válido não elimina a necessidade de autorização.

## Referências

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)
