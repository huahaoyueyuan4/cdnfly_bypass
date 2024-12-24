import requests
import base64,time

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

if __name__ == "__main__":
    session = requests.Session()
    result = session.get("http://YOUR_DOMAIN/")
    print(result.text)
    guard = result.cookies.get("guard")
    partial_key = guard[:8]
    time_num_plain = guard[12:]
    time_num = int(time_num_plain[10:])
    num_calc = (time_num * 2) + 17
    num_calc -= 2
    str_val = str(num_calc)
    encrypted = xor_encrypt(str_val, partial_key)
    encrypted_bas64 = base64.b64encode(encrypted.encode('utf-8')).decode('utf-8')
    session.cookies.set("guardret", encrypted_bas64)
    print(encrypted_bas64)
    time.sleep(5)
    result = session.get("http://YOUR_DOMAIN/")
    print(result.text)