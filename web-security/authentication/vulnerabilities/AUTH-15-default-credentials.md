# AUTH-15 — Credenciais padrão

## O que eu entendi, em uma frase

Uma conta continua usando o usuário, a senha ou a chave inicial conhecida do produto.

## Exemplo para eu fixar

Um painel recém-instalado aceita `admin` com a senha publicada no manual. A equipe expôs o serviço antes de concluir a configuração. Qualquer pessoa que conheça a documentação pode tentar entrar com privilégios administrativos.

```text
produto instalado -> credencial inicial conhecida
                              |
                   não foi trocada ou desativada
                              |
                       acesso indevido
```

Também entram nessa categoria contas de demonstração, senhas temporárias previsíveis e contas de manutenção esquecidas.

## Por que preciso prestar atenção

Credenciais padrão combinam baixo esforço de descoberta com, frequentemente, privilégios elevados. O resultado pode incluir leitura, alteração ou indisponibilidade de todo o sistema.

## Como eu reconheceria em ambiente autorizado

Inventarie produtos, contas iniciais e procedimentos de instalação. Consulte documentação oficial e configuração. Use o menor número possível de tentativas para evitar bloqueios e verifique também imagens, templates e automações de implantação.

O comportamento seguro exige um segredo único durante a instalação ou mantém a conta desabilitada até que seja configurada.

## Como corrigir ou prevenir

- não forneça uma credencial universal entre instalações;
- exija um segredo único e forte no primeiro uso;
- bloqueie a operação normal até a configuração segura;
- remova ou desative contas de demonstração e manutenção;
- use provisionamento seguro de segredos por instalação;
- restrinja interfaces administrativas por rede e privilégio;
- inclua a verificação no processo de implantação;
- ao encontrar uma credencial padrão, rotacione-a e investigue o uso.

## Uma diferença que preciso lembrar

Rate limiting reduz o volume de tentativas, mas não corrige uma senha que já é pública. O problema é a permanência de uma credencial conhecida.

## O que eu preciso lembrar

- Credencial inicial não deve sobreviver à implantação.
- Cada instalação precisa de segredo próprio.
- Contas administrativas aumentam o impacto.

## Referências técnicas

- [OWASP WSTG — Default Credentials](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Default_Credentials/)
- [CWE-1392 — Use of Default Credentials](https://cwe.mitre.org/data/definitions/1392.html)
- [CWE-798 — Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
