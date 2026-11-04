import hashlib
import hmac

message = "Hello, world!"
key = "SUPER"

message_bytes= message.encode("utf-8")
key_bytes =  key.encode("utf-8")

signature = hmac.new(
    key_bytes,
    message_bytes,
    hashlib.sha256

    ).hexdigest()

print("Original message:", message)
print("HMAC-SHA256 signature:", signature)
