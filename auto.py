import base64


def xor_encrypt(plaintext: str, key: str) -> str:
    final_key = key + "PTNo2n3Ev5"

    output_chars = []
    key_len = len(final_key)
    for i, ch in enumerate(plaintext):
        p_char = ord(ch)
        k_char = ord(final_key[i % key_len])
        x_char = p_char ^ k_char  # XOR
        output_chars.append(chr(x_char))

    return ''.join(output_chars)

def setRet(param: str) -> str:
    key = param[0:8]
    num_str = param[12:]
    num_val = int(num_str)
    val_56549e = (num_val * 2 + 18) - 2
    encrypted = xor_encrypt(str(val_56549e), key)
    guard_encrypted = encrypted.strip()
    guard_encrypted_b64 = base64.b64encode(guard_encrypted.encode("utf-8")).decode("utf-8")
    return guard_encrypted_b64


if __name__ == "__main__":
    test_input = "3ec4e8a4Jh4760"
    cookie_value = setRet(test_input)
    print(cookie_value)