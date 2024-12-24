import base64
import requests
import time


def xor_encrypt(plaintext: str) -> str:
    final_key = "qweabcPTNo2n3Ev5" + "PTNo2n3Ev5"

    output_chars = []
    key_len = len(final_key)
    for i, ch in enumerate(plaintext):
        p_char = ord(ch)
        k_char = ord(final_key[i % key_len])
        x_char = p_char ^ k_char  # XOR
        output_chars.append(chr(x_char))

    return ''.join(output_chars)

def encrypt(input_text: str) -> str:
    encrypted = xor_encrypt(input_text)
    encrypted_b64 = base64.b64encode(encrypted.encode('utf-8')).decode('utf-8')
    return encrypted_b64

if __name__ == "__main__":
    session = requests.Session()
    img = session.get(f"http://YOUR_DOMAIN/_guard/rotate.jpg?t={int(time.time()*1000)}")
    files = {
        'file': ('rotate.jpg', img.content, 'image/jpeg')
    }
    result = requests.post('http://127.0.0.1:8000/similar', files=files)
    angle = result.json()['most_similar_image'].split('.')[0].split('-')[-1]
    angle = 360-int(angle)
    session.cookies.set("guardret", encrypt(str(angle)))

    print(session.cookies.get('guardret'))

    result = session.get("http://YOUR_DOMAIN/")
    print(result.text)