import uuid
import requests


def toBinary(text: str):
    result = ""
    for c in text:
        val = ord(c)
        for i in range(8):
            result += str(0 if (val & 128) == 0 else 1)
            val = val << 1
    return result


def xor(text1: str, text2: str):
    result = ""
    for i in range(min(len(text1), len(text2))):
        result += str(int(text1[i]) ^ int(text2[i]))
    return result


class AdvancedLicense:
    def __init__(self, server: str):
        self.server = server
        self.security_key = "YecoF0I6M05thxLeokoHuW8iUhTdIUInjkfF"

    def is_valid(self, key: str):
        rand = toBinary(str(uuid.uuid4()))
        secK = toBinary(self.security_key)
        key = toBinary(key)
        resp = self.__request(xor(rand, secK), xor(rand, key))
        return self.__get_status(resp, rand, key, secK)


    def __request(self, v1: str, v2: str, name: str = None):
        URL = self.server + "?v1=" + v1 + "&v2=" + v2 + ("" if name is None else f"&pl={name}")
        resp = requests.get(URL, headers={
            "User-Agent": "Mozilla/5.0"
        }).content.decode("utf-8")
        return resp


    def __get_status(self, resp, rand, key, secKey):
        if resp[0] != "0" and resp[0] != "1":
            return resp.strip()
        else:
            stat = xor(xor(resp, key), secKey)
            if rand[:len(stat)] == stat:
                return "VALID"
            else:
                return "WRONG_RESPONSE"
