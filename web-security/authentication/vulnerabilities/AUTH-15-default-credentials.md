# AUTH-15 — Default Credentials

## Overview

**Default credentials** são usernames, senhas ou chaves iniciais fornecidos com software, dispositivo ou implantação. A vulnerabilidade surge quando permanecem ativos e conhecidos ou iguais entre instalações.

O risco é especialmente alto em contas administrativas e interfaces de infraestrutura, pois combina descoberta fácil com privilégios elevados.

## How It Works

```text
Produto/deployment -> credencial inicial conhecida
                              |
                     não alterada/desativada
                              |
                  login não autorizado
```

O problema inclui contas de demonstração, credenciais de fabricante, senhas temporárias previsíveis e backdoors de manutenção esquecidos.

## Example

Um painel recém-instalado aceita `admin` com a senha documentada no manual público. A implantação foi exposta antes da etapa de hardening, permitindo acesso administrativo.

## Impact

Pode produzir acesso não autorizado, frequentemente administrativo, afetando confidentiality, integrity e availability. O impacto real depende do privilégio e da exposição da interface.

## How to Identify

Em escopo autorizado, inventarie produtos, contas iniciais e procedimento de instalação. Consulte documentação oficial e configuração, usando tentativas mínimas para evitar lockout. Verifique contas de demonstração, templates e imagens de deployment.

Comportamento esperado: segredo único é definido na instalação ou a conta fica desabilitada até configuração. Vulnerável: credencial pública, compartilhada ou previsível permanece funcional.

## Mitigation

- não forneça credenciais universais;
- exija segredo único e forte no primeiro uso;
- bloqueie operação normal até a configuração segura;
- desative ou remova contas de demonstração e manutenção;
- use provisioning seguro para secrets por instalação;
- limite interfaces administrativas por rede e privilégio;
- inclua verificação no processo de deployment;
- rotacione imediatamente credenciais encontradas e investigue uso.

## Related Attacks

[Username enumeration](AUTH-01-username-enumeration.md) pode revelar contas administrativas. [AUTH-04](AUTH-04-authentication-attempts.md) reduz tentativas automatizadas, mas não corrige uma credencial padrão conhecida.

## CWE

[CWE-1392 — Use of Default Credentials](https://cwe.mitre.org/data/definitions/1392.html) corresponde diretamente ao uso de credenciais padrão. Quando a credencial também está fixa no código, [CWE-798](https://cwe.mitre.org/data/definitions/798.html) pode ser relevante, mas os conceitos não são idênticos.

## OWASP Relationship

O OWASP WSTG documenta **WSTG-ATHN-02 — Testing for Default Credentials** e inclui tanto produtos instalados quanto senhas iniciais previsíveis de novas contas.

## Key Takeaways

- Credenciais públicas não devem sobreviver ao deployment.
- Segredos iniciais devem ser únicos por instalação.
- Contas administrativas ampliam o impacto.
- Rate limiting não compensa uma senha já conhecida.

## References

- [OWASP WSTG v4.2 — Testing for Default Credentials](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Default_Credentials/)
- [MITRE CWE-1392](https://cwe.mitre.org/data/definitions/1392.html)
- [MITRE CWE-798](https://cwe.mitre.org/data/definitions/798.html)
