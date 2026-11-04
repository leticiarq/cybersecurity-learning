# Meu glossário de autenticação e segurança web

Aqui registro os termos que preciso consultar durante o estudo. Mantenho as expressões em inglês porque elas aparecem com frequência em documentação, ferramentas e relatórios de segurança.

| Termo | Significado neste módulo |
|---|---|
| Account takeover | Tomada de uma conta por alguém que não é seu titular |
| Authentication (AuthN) | Confirmação de uma identidade |
| Authorization (AuthZ) | Decisão sobre o que uma identidade pode fazer |
| Bearer token | Token cuja posse normalmente é suficiente para apresentá-lo |
| Brute force | Teste de muitos candidatos até encontrar uma credencial válida |
| Claim | Afirmação transportada por um token, como emissor, usuário ou expiração |
| Credential | Evidência usada na autenticação, como senha, token ou chave |
| Credential stuffing | Uso de pares de usuário e senha vazados de outros serviços |
| CSPRNG | Gerador de números pseudoaleatórios adequado para uso criptográfico |
| Encoding | Mudança reversível de representação, como Base64URL; não é criptografia |
| Hash | Resumo de tamanho fixo calculado a partir de dados |
| HMAC | Código de autenticação calculado com uma função de hash e um segredo |
| Identity Provider (IdP) | Serviço que autentica identidades e pode emitir tokens |
| MFA | Autenticação que exige fatores de categorias independentes |
| Password hashing | Função deliberadamente custosa criada para armazenar/verificar senhas |
| Password spraying | Teste de poucas senhas comuns contra muitas contas |
| Rate limiting | Restrição da quantidade de operações permitidas em um intervalo |
| Revocation | Invalidação de uma credencial antes de sua expiração natural |
| Salt | Valor único combinado com a senha durante o password hashing |
| Session hijacking | Uso indevido de uma sessão autenticada obtida de outra pessoa |
| Session ID | Identificador temporário usado pelo servidor para localizar uma sessão |
| Signing input | Bytes exatos de header e payload sobre os quais a assinatura é calculada |
| Token | Valor que representa identidade, autorização ou estado |

## Uma distinção que eu preciso lembrar

Os termos descrevem mecanismos diferentes. Por exemplo, Base64URL representa bytes, hashing produz um resumo, criptografia busca confidencialidade e assinatura protege integridade e origem. Trocar os nomes entre si costuma levar a decisões de segurança incorretas.
