import base64


def xor_decrypt(ciphertext: str, key: str) -> str:
    final_key = key + "PTNo2n3Ev5"

    output_chars = []
    key_len = len(final_key)
    for i, ch in enumerate(ciphertext):
        c_char = ord(ch)
        k_char = ord(final_key[i % key_len])
        x_char = c_char ^ k_char  # XOR
        output_chars.append(chr(x_char))

    return ''.join(output_chars)

if __name__ == "__main__":
    s = "QkFV"
    partial_key = "qweabcPTNo2n3Ev5"
    xored_bytes = base64.b64decode(s)
    xored_str = xored_bytes.decode('utf-8')
    print(xor_decrypt(xored_str, partial_key))