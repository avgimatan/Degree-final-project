import re
from urlextract import URLExtract


def bitcoin(text):
    res = re.findall("([13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[ac-hj-np-zAC-HJ-NP-Z02-9]{11,71})\s", text)
    # lis = re.findall("[1,3,bc]", text)
    return res


def url(text):
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    for m in re.finditer(r'(?:https?://)?(?:www)?(\S*?\.onion)\b', text, re.M | re.IGNORECASE):
        urls.append(m.group(0))
    return urls


def email(text):
    lis = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    return lis


if __name__ == '__main__':
    text = "BTC Address: 1JHwenDp9A98XdjfYkHKyiE3R99Q72K9X4 " \
         "BTC Address: 1Unoc4af6gCq3xzdDFmGLpq18jbTW1nZD " \
         "BTC Address: 1A8Ad7VbWDqwmRY6nSHtFcTqfW2XioXNmj " \
         "BTC Address: 12CZYvgNZ2ze3fGPFzgbSCELBJ6zzp2cWc " \
         "BTC Address: bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"

    print(bitcoin(text))
    print(email("fddsf https://google.com dormaniak@gmail.com blala dffdfd.onion asdasdsadsadsa@tut.com"))
    print(url("fddsf http://google.com dormaniak@gmail.com blala http://dffdfd.onion asdasdsadsadsa@tut.com"))
