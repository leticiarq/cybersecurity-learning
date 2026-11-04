# AUTH-05 — Armazenamento inseguro de senhas

## O que eu entendi, em uma frase

Depois de obter o banco de dados, um invasor consegue ler as senhas ou testar candidatos com custo muito baixo.

## A pergunta que orienta meu entendimento

O servidor precisa recuperar a senha original? Normalmente, não. Ele só precisa responder: “a tentativa atual corresponde à senha cadastrada?”. Por isso, deve armazenar um resultado de **password hashing**, e não a senha reversível.

| Forma de armazenamento | Problema |
|---|---|
| Texto puro | A senha fica imediatamente visível |
| Base64 ou outro encoding | Qualquer pessoa pode reverter sem chave |
| Criptografia | Quem obtém a chave pode recuperar todas as senhas |
| SHA-256 puro | Tentativas offline são rápidas demais |
| Password hashing com salt e custo | Construído especificamente para verificar senhas |

## Como a verificação funciona

```text
Cadastro:
senha + salt único -> Argon2id/scrypt/bcrypt/PBKDF2 -> hash armazenado

Login:
tentativa + salt armazenado -> mesma função -> comparação
```

O `salt` é diferente para cada senha e não precisa ser secreto. Ele evita que senhas iguais produzam registros iguais e reduz a utilidade de tabelas pré-calculadas. O custo configurável torna cada tentativa mais cara.

## Exemplo para eu fixar

Se a aplicação salva `base64(senha)`, basta decodificar o texto. Se salva SHA-256 sem salt, o valor não é diretamente reversível, mas um invasor pode calcular milhões de candidatos rapidamente. Os dois casos são inadequados por motivos diferentes.

## Por que preciso prestar atenção

Uma leitura indevida do banco pode comprometer muitas contas ao mesmo tempo. Como usuários reutilizam senhas, o dano pode alcançar outros serviços.

## Como eu reconheceria em ambiente autorizado

Em revisão de arquitetura e código, identifique algoritmo, parâmetros, salt, truncamento, estratégia de migração e localização de segredos. Não solicite nem exponha senhas reais. A aparência de um hash não prova que o mecanismo seja adequado.

## Como corrigir ou prevenir

- prefira Argon2id quando disponível ou outra alternativa madura adequada à plataforma;
- gere um salt único automaticamente;
- calibre e reavalie o custo ao longo do tempo;
- use APIs mantidas de frameworks e bibliotecas;
- faça *rehash* gradual quando os parâmetros mudarem;
- mantenha um `pepper` opcional separado do banco;
- nunca crie primitivas criptográficas próprias.

O `pepper` é uma camada adicional; não substitui o salt nem a função apropriada.

## O que eu preciso lembrar

- Base64 é representação, não proteção.
- Criptografia reversível normalmente não é necessária para senhas.
- SHA-256 puro é rápido demais para esse uso.
- Algoritmo, salt e parâmetros precisam ser avaliados juntos.

## Referências técnicas

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [CWE-256 — Plaintext Storage of a Password](https://cwe.mitre.org/data/definitions/256.html)
- [CWE-916 — Password Hash With Insufficient Computational Effort](https://cwe.mitre.org/data/definitions/916.html)
