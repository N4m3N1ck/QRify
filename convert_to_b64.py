import base64


def string_to_b64(s: str):
    s_bytes = s.encode('utf-8')
    b64 = base64.b64encode(s_bytes)
    return str(b64)[2:-1]


if __name__ == "__main__":
    s = input("Enter string to encode: ")
    print(string_to_b64(s))
