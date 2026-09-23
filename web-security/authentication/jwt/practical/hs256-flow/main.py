"""Demonstração didática de criação e validação de um JWT com HS256.

Não use esta implementação como substituta de uma biblioteca JWT madura.
Ela verifica a assinatura, mas não implementa uma política completa de claims.
"""

import base64
import hashlib
import hmac
import json
from typing import Any


def json_bytes(value: dict[str, Any]) -> bytes:
    """Serializa JSON compacto e determinístico como UTF-8."""
    return json.dumps(
        value,
        separators=(",", ":"),
        sort_keys=True,
        ensure_ascii=False,
    ).encode("utf-8")


def base64url_encode(data: bytes) -> str:
    """Codifica bytes em Base64URL sem o padding opcional '='."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def base64url_decode(value: str) -> bytes:
    """Restaura o padding e decodifica Base64URL estritamente."""
    padding = "=" * (-len(value) % 4)
    return base64.b64decode(
        value + padding,
        altchars=b"-_",
        validate=True,
    )


def create_jwt(header: dict[str, Any], payload: dict[str, Any], secret: bytes) -> str:
    """Monta header.payload.signature explicitamente."""
    header_json = json_bytes(header)
    payload_json = json_bytes(payload)
    encoded_header = base64url_encode(header_json)
    encoded_payload = base64url_encode(payload_json)
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")

    signature = hmac.new(secret, signing_input, hashlib.sha256).digest()
    encoded_signature = base64url_encode(signature)

    print("\n=== CRIAÇÃO HS256 ===")
    print("1. Header:                 ", header)
    print("2. Header JSON:            ", header_json.decode())
    print("3. Header Base64URL:       ", encoded_header)
    print("4. Payload:                ", payload)
    print("5. Payload JSON:           ", payload_json.decode())
    print("6. Payload Base64URL:      ", encoded_payload)
    print("7. Signing Input:          ", signing_input.decode())
    print("8. HMAC-SHA-256 (hex):     ", signature.hex())
    print("9. Signature Base64URL:    ", encoded_signature)

    token = f"{signing_input.decode()}.{encoded_signature}"
    print("10. JWT:                   ", token)
    return token


def validate_jwt(token: str, secret: bytes, label: str) -> bool:
    """Recalcula o HMAC e faz uma comparação segura das assinaturas."""
    print(f"\n=== VALIDAÇÃO: {label} ===")
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
        received_signature = base64url_decode(encoded_signature)
    except (ValueError, UnicodeEncodeError) as error:
        print("Token malformado:", error)
        return False

    calculated_signature = hmac.new(
        secret,
        signing_input,
        hashlib.sha256,
    ).digest()
    valid = hmac.compare_digest(received_signature, calculated_signature)

    print("Header codificado:         ", encoded_header)
    print("Payload codificado:        ", encoded_payload)
    print("Signature recebida (hex):  ", received_signature.hex())
    print("Signing Input reconstruído:", signing_input.decode())
    print("Signature calculada (hex): ", calculated_signature.hex())
    print("Assinatura válida?         ", valid)
    return valid


def replace_payload_without_signing(token: str, payload: dict[str, Any]) -> str:
    """Altera somente o payload para demonstrar que a assinatura falha."""
    encoded_header, _, original_signature = token.split(".")
    changed_payload = base64url_encode(json_bytes(payload))
    return f"{encoded_header}.{changed_payload}.{original_signature}"


def main() -> None:
    # Em produção, gere e armazene este segredo em um secret manager.
    secret = b"didactic-secret-with-at-least-32-bytes"
    wrong_secret = b"another-secret-that-does-not-match!!"
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "aud": "learning-api",
        "iat": 1710000000,
        "name": "Ana",
        "sub": "user-123",
    }

    token = create_jwt(header, payload, secret)
    assert validate_jwt(token, secret, "token original + chave correta")

    tampered_token = replace_payload_without_signing(
        token,
        {**payload, "name": "Mallory"},
    )
    assert not validate_jwt(
        tampered_token,
        secret,
        "Experimento A — payload alterado + assinatura original",
    )
    assert not validate_jwt(
        token,
        wrong_secret,
        "Experimento B — token original + chave incorreta",
    )


if __name__ == "__main__":
    main()
