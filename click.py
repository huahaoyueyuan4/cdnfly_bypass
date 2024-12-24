import json
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


def set_guardret_cookie(guard_value: str, data: dict) -> str:
    partial_key = guard_value[:8]
    json_str = json.dumps(data, separators=(',', ':'))
    xored = xor_encrypt(json_str, partial_key)
    b64_encoded = base64.b64encode(xored.encode('utf-8')).decode('utf-8')
    guardret = b64_encoded

    return guardret

if __name__ == "__main__":
    guard_cookie = "e213ebdbS0ic"
    test_data = {"x":496,"y":210,"a":708}

    ret_value = set_guardret_cookie(guard_cookie, test_data)
    print("guardret: ", ret_value)
