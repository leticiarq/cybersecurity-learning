# Authentication Security

**Authentication** (autenticação, ou AuthN) é o processo de verificar se uma entidade é quem afirma ser. Em uma aplicação web, isso normalmente significa relacionar uma requisição a uma identidade por meio de credenciais, como senha, chave de acesso ou fator biométrico.

Autenticação é uma fronteira de segurança: uma falha pode permitir que outra pessoa assuma uma conta e acesse dados ou ações protegidas. Ela não deve ser confundida com **authorization** (autorização, ou AuthZ). Autenticação responde *“quem é você?”*; autorização responde *“o que essa identidade pode fazer?”*. Uma aplicação precisa aplicar as duas verificações.

## Trilha de estudos

1. [Authentication Basics](authentication-basics.md) — identidades, credenciais, login, sessões, tokens, fatores, MFA e senhas.
2. [JWT](jwt/README.md) — índice do conteúdo sobre JSON Web Tokens.
   - [Como um JWT funciona](jwt/jwt.md)
   - [HS256](jwt/hs256.md)
   - [RS256](jwt/rs256.md)
   - [HS256 vs RS256](jwt/hs256-vs-rs256.md)
   - [Atividade prática](jwt/practical/README.md)
3. [Authentication Vulnerabilities](vulnerabilities/README.md) — catálogo numerado com 15 falhas de autenticação, identificação autorizada, impactos e mitigações.

## Objetivos de aprendizagem

Ao concluir este módulo, o leitor deverá conseguir descrever um fluxo de login, diferenciar sessão de token, reconhecer fatores de autenticação, explicar como JWTs assinados são construídos e identificar controles defensivos contra falhas de autenticação.

## Referências gerais

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Web Security Testing Guide — Authentication Testing](https://owasp.org/www-project-web-security-testing-guide/)
