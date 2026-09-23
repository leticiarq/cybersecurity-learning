# Authentication Basics

## O que é autenticação?

**Authentication** é o processo de verificar uma alegação de identidade. Digitar um e-mail identifica a conta pretendida; apresentar a senha correta fornece evidência de que a pessoa controla uma credencial associada a essa conta. A autenticação não prova necessariamente a identidade civil do usuário: dentro de um serviço, uma identidade digital pode representar apenas uma conta.

Uma **identidade** é a representação de um sujeito no sistema, normalmente associada a um identificador único e a atributos. Uma **credencial** é algo usado para sustentar a alegação de identidade: senha, chave criptográfica, código temporário ou dado biométrico, por exemplo. O identificador de usuário geralmente não é secreto; a credencial deve ser protegida.

## Authentication vs authorization

| Questão | Authentication (AuthN) | Authorization (AuthZ) |
|---|---|---|
| Pergunta | Quem é você? | O que você pode fazer? |
| Exemplo | Validar senha e MFA de Ana | Permitir que Ana leia apenas os próprios pedidos |
| Momento | Estabelece ou confirma a identidade | Deve ser verificada em cada operação protegida |

Estar autenticado não significa poder acessar qualquer recurso. Um usuário comum autenticado continua sem autorização para executar funções administrativas.

## Fluxo básico de login

```text
Usuário -> envia identificador e credencial por HTTPS
Servidor -> localiza a conta e verifica a credencial
Servidor -> aplica MFA e controles de risco, quando necessários
Servidor -> cria uma sessão ou emite tokens
Cliente  -> apresenta o identificador de sessão/token nas próximas requisições
Servidor -> autentica o contexto e aplica autorização ao recurso solicitado
```

Falhas devem produzir mensagens suficientemente genéricas, ser registradas com cuidado e alimentar controles contra abuso. Credenciais e tokens não devem aparecer em logs.

## Sessões e cookies de sessão

HTTP não mantém estado por si só. Na autenticação baseada em sessão, o servidor cria um registro de sessão e entrega ao navegador um identificador aleatório. Um cookie pode transportá-lo automaticamente:

```http
Set-Cookie: session_id=valor-aleatorio; Secure; HttpOnly; SameSite=Lax
```

Nas requisições seguintes, o navegador devolve o cookie. O servidor consulta o estado da sessão e reconhece o usuário. `Secure` restringe o envio a HTTPS; `HttpOnly` impede acesso pelo JavaScript da página; `SameSite` ajuda a limitar envios entre sites. Esses atributos são camadas de defesa e precisam ser combinados com proteção contra CSRF, rotação após login ou mudança de privilégio, expiração e invalidação no logout.

O identificador de sessão funciona temporariamente como uma credencial. Se for roubado, pode permitir **session hijacking** mesmo sem conhecimento da senha.

## Tokens

Um token é um valor que representa autorização, identidade ou estado. Na autenticação baseada em tokens, o cliente apresenta o token a cada chamada, frequentemente no cabeçalho:

```http
Authorization: Bearer <token>
```

Alguns tokens são opacos e precisam ser consultados no servidor; outros, como JWTs, carregam claims verificáveis. “Stateless” não significa “sem estado em todo o sistema”: revogação, refresh tokens, dispositivos e logout podem exigir estado. A forma segura de armazenar e transportar tokens depende da arquitetura e das ameaças; exposição a XSS, CSRF e vazamentos deve ser considerada.

| Aspecto | Sessão no servidor | Token autocontido assinado |
|---|---|---|
| Estado principal | Registro mantido pelo servidor | Claims no token |
| Revogação imediata | Geralmente direta | Pode exigir lista, versão ou validade curta |
| Escala/distribuição | Pode exigir armazenamento compartilhado | Verificação pode ser distribuída |
| Risco central | Roubo/fixação do ID de sessão | Roubo, validação incorreta ou chave comprometida |

Consulte [JSON Web Tokens](jwt/jwt.md) para estudar um formato de token assinado.

## Fatores de autenticação

- **Something you know**: algo que a pessoa sabe, como senha ou PIN.
- **Something you have**: algo que possui, como security key, smart card ou aplicativo autenticador.
- **Something you are**: característica biométrica, como impressão digital ou reconhecimento facial.

**MFA** (multi-factor authentication) exige fatores de categorias independentes. Senha mais PIN continua sendo apenas um fator de conhecimento. **2FA** é o caso específico de MFA que usa exatamente dois fatores; MFA pode usar dois ou mais. A independência importa: comprometer um fator não deveria comprometer automaticamente o outro.

Recuperação de conta, troca e desativação de fatores precisam ser tão protegidas quanto o login, pois podem virar caminhos de bypass.

## Armazenamento seguro de senhas

O servidor não precisa recuperar a senha original: precisa verificar se uma tentativa corresponde ao valor cadastrado. Por isso, senhas não devem ser armazenadas em texto puro nem com criptografia reversível. Deve-se usar uma função própria para **password hashing**, com `salt` único e custo configurável, como Argon2id, scrypt, bcrypt ou PBKDF2 conforme a plataforma e seus requisitos.

Fluxo simplificado:

```text
cadastro: senha + salt único -> password hash -> banco de dados
login:    tentativa + salt armazenado -> novo hash -> comparação segura
```

Um hash criptográfico comum e rápido, como SHA-256 isolado, não é adequado para armazenar senhas: rapidez favorece tentativas offline em massa. O `salt` não precisa ser secreto; ele impede que hashes iguais revelem senhas iguais e dificulta tabelas pré-computadas. Um `pepper` opcional é um segredo separado do banco e não substitui `salt` nem uma função adequada.

## Principais riscos

- enumeração de usuários por mensagens ou tempos diferentes;
- senhas fracas, reutilizadas ou vazadas;
- brute force, password spraying e credential stuffing;
- ausência ou bypass de MFA;
- recuperação de conta mais fraca que o login;
- sessões previsíveis, não rotacionadas ou que continuam válidas após logout;
- tokens expostos, excessivamente longos ou validados de forma incompleta;
- armazenamento inadequado de senhas e segredos;
- falhas de autorização após um login válido;
- falta de monitoramento, alertas e resposta a atividades anômalas.

Veja o [índice de vulnerabilidades](vulnerabilities/README.md) para aprofundar esses problemas.

## Referências

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)
