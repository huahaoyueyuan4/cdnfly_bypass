import base64
import time
import json
import requests
def generate_slider_track(new_total_time=None):

    old_track = {
        "move": [
            {"timestamp": 1734779000109, "x": 186, "y": 256},
            {"timestamp": 1734779000400, "x": 654, "y": 266},
            {"timestamp": 1734779000401, "x": 655, "y": 268},
            {"timestamp": 1734779000402, "x": 659, "y": 268},
            {"timestamp": 1734779000406, "x": 666, "y": 268}
        ],
        "btn": 52,
        "slider": 529,
        "page_width": 855,
        "page_height": 1361
    }

    timestamps = [pt["timestamp"] for pt in old_track["move"]]
    old_min = min(timestamps)
    old_max = max(timestamps)
    old_duration = old_max - old_min

    base_time = int(time.time() * 1000)

    if new_total_time is not None and old_duration != 0:
        scale = float(new_total_time) / old_duration
    else:
        scale = 1.0

    new_move = []
    for pt in old_track["move"]:
        relative_t = pt["timestamp"] - old_min
        new_t = int(base_time + relative_t * scale)

        new_move.append({
            "timestamp": new_t,
            "x": pt["x"],
            "y": pt["y"]
        })

    new_track = {
        "move": new_move,
        "btn": old_track["btn"],
        "slider": old_track["slider"],
        "page_width": old_track["page_width"],
        "page_height": old_track["page_height"]
    }

    return new_track

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

    track = generate_slider_track()
    guard_value = result.cookies.get("guard")
    partial_key = guard_value[:8]
    print(partial_key)
    encrypted = xor_encrypt(json.dumps(track), partial_key)
    guard_encrypted = encrypted.strip()
    guard_encrypted_b64 = base64.b64encode(guard_encrypted.encode("utf-8")).decode("utf-8")
    print(guard_encrypted_b64)
    session.cookies.set("guardret", guard_encrypted_b64)
    time.sleep(1)
    result = session.get("http://YOUR_DOMAIN/")
    print(result.text)