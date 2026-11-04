"""Demonstração didática de criação e validação de um JWT com RS256.

O código monta o JWT manualmente, mas delega RSA ao pacote cryptography.
Não use esta implementação como substituta de uma biblioteca JWT madura.
"""

import base64
import json
from typing import Any

try:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
except ImportError as error:
    raise SystemExit(
        "Dependência ausente. Instale com: python3 -m pip install cryptography"
    ) from error


def json_bytes(value: dict[str, Any]) -> bytes:
    """Serializa JSON compacto e determinístico como UTF-8."""
    return json.dumps(
        value,
        separators=(",", ":"),
        sort_keys=True,
        ensure_ascii=False,
    ).encode("utf-8")


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def base64url_decode(value: str) -> bytes:
    padding_length = "=" * (-len(value) % 4)
    return base64.b64decode(
        value + padding_length,
        altchars=b"-_",
        validate=True,
    )


def create_jwt(
    header: dict[str, Any],
    payload: dict[str, Any],
    private_key: rsa.RSAPrivateKey,
) -> str:
    """Monta o JWS e assina o signing input com a private key."""
    header_json = json_bytes(header)
    payload_json = json_bytes(payload)
    encoded_header = base64url_encode(header_json)
    encoded_payload = base64url_encode(payload_json)
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")

    # RS256 = RSASSA-PKCS1-v1_5 com SHA-256.
    signature = private_key.sign(
        signing_input,
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    encoded_signature = base64url_encode(signature)

    print("\n=== CRIAÇÃO RS256 ===")
    print("1. Header:                 ", header)
    print("2. Header JSON:            ", header_json.decode())
    print("3. Header Base64URL:       ", encoded_header)
    print("4. Payload:                ", payload)
    print("5. Payload JSON:           ", payload_json.decode())
    print("6. Payload Base64URL:      ", encoded_payload)
    print("7. Signing Input:          ", signing_input.decode())
    print("8. Assinatura RSA (hex):   ", signature.hex())
    print("9. Signature Base64URL:    ", encoded_signature)

    token = f"{signing_input.decode()}.{encoded_signature}"
    print("10. JWT:                   ", token)
    return token


def validate_jwt(
    token: str,
    public_key: rsa.RSAPublicKey,
    label: str,
) -> bool:
    """Verifica a assinatura com a public key correspondente."""
    print(f"\n=== VALIDAÇÃO: {label} ===")
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
        signature = base64url_decode(encoded_signature)
    except (ValueError, UnicodeEncodeError) as error:
        print("Token malformado:", error)
        return False

    print("Header codificado:         ", encoded_header)
    print("Payload codificado:        ", encoded_payload)
    print("Signing Input reconstruído:", signing_input.decode())
    print("Signature recebida (hex):  ", signature.hex())

    try:
        public_key.verify(
            signature,
            signing_input,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    except InvalidSignature:
        print("Assinatura válida?          False")
        return False

    print("Assinatura válida?          True")
    return True


def replace_payload_without_signing(token: str, payload: dict[str, Any]) -> str:
    encoded_header, _, original_signature = token.split(".")
    changed_payload = base64url_encode(json_bytes(payload))
    return f"{encoded_header}.{changed_payload}.{original_signature}"


def generate_key_pair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Gera um par temporário; a public key não oferece método de assinatura."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key, private_key.public_key()


def main() -> None:
    private_key, public_key = generate_key_pair()
    _, wrong_public_key = generate_key_pair()

    header = {"alg": "RS256", "typ": "JWT"}
    payload = {
        "aud": "learning-api",
        "iat": 1710000000,
        "name": "Ana",
        "sub": "user-123",
    }

    token = create_jwt(header, payload, private_key)
    assert validate_jwt(
        token,
        public_key,
        "token original + public key correspondente",
    )

    tampered_token = replace_payload_without_signing(
        token,
        {**payload, "name": "Mallory"},
    )
    assert not validate_jwt(
        tampered_token,
        public_key,
        "Experimento A — payload alterado + assinatura original",
    )
    assert not validate_jwt(
        token,
        wrong_public_key,
        "Experimento C — token original + public key incorreta",
    )

    print(
        "\nA public key apenas verifica; somente a private key correspondente assina."
    )
    print("Header e payload continuam legíveis: RS256 não os criptografa.")


if __name__ == "__main__":
    main()
