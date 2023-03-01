import os
import binascii


# Bu Fonksiyon Metni  binary(ikili) string e dönüştürür.
def toBin(a):
    new = ""
    for ch in a:
        new += bin(ord(ch))[2:].zfill(8)
    return new


# Binary stringi metne dönüştürür
def toText(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)


# string i ikili metne dönüştürmeye yardımcı fonksiyon binascii kütüphanesi kullanıldı
def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


# metni 0 lar ile doldurarak 32 bit'li binary ye çevirir.
def to32Bit(x):
    if len(x) != 32:
        for i in range(0, 32 - len(x)):
            x += "0"
        return x
    return x


# metni 64 bit'li binary sayıya çevirir 0 ile doldurarak
def to64Bit(x):
    if (len(x) != 64):
        for i in range(0, 64 - len(x)):
            x += "0"
        return x
    return x


'''

metni 2 ye bölerek 1. kısım ve 2.kısım(ikiside 32 bitlik) arasında XOR işlemi yapılır.



'''


def xOR(x, y):
    new = ""
    for i in range(0, 32):
        if x[i] == "0" and y[i] == "0":
            new += "0"
        if x[i] == "0" and y[i] == "1":
            new += "1"
        if x[i] == "1" and y[i] == "0":
            new += "1"
        if x[i] == "1" and y[i] == "1":
            new += "0"
    return new


'''
Metni ve anahtarı argüman olarak olan bu şifreleme fonksiyonunda anahtar iki eşit parçaya bölünür.
anahtarın  ilk kısmı XOR işlemi için ikinci ise bayt miktarını ikiye katlamak için kullanılır.
Şifrele fonksiyonu  metni 32 bitlik parçalara bölerek çalışır.
metnin bölünen parçalarının miktarı 2 katına çıkarılır.
Daha sonra ilk kısmın parçalarına XOR İşlemi uygulanır.
Son olarak alınan metnin ilk kısmı ile ikinci kısmı yerdeğiştirilir.
Ve alınan metinden daha uzun ve şifrelenmiş metin sonuç olarak geriye döndürülür.

'''


def encrypt(msg, key):
    msg = toBin(msg)
    key = toBin(key)
    keyList = []
    addList = []
    temp = ""
    for i in range(0, len(key), 32):
        if i < len(key) / 2:
            temp = key[i:i + 32]
            keyList.append(temp)
        if i >= len(key) / 2:
            temp = key[i:i + 32]
            addList.append(temp)
    blockList = []
    for j in range(0, len(keyList)):
        for i in range(0, len(msg), 32):
            temp = ""
            temp += msg[i:i + 32]
            if len(temp) != 32:
                temp = to32Bit(temp)
            blockList.append(temp)
            blockList.append(addList[j])

        for i in range(0, len(blockList), 2):
            blockList[i] = xOR(blockList[i], keyList[j])
            temp = blockList[i]
            blockList[i] = blockList[i + 1]
            blockList[i + 1] = temp

    result = ""
    for i in range(0, len(blockList)):
        result += blockList[i]
    result = toText(result)
    return result


'''
Şifre çöz fonksiyonunda anahtar  iki eşit parçaya bölünür. ilk kısım XOR işlemine tabi tutulur.
ikinci kısmı bayt miktarını ikiye katlar.
Şifre çözme işlemi XOR' lanan key in kısmı ile ikinci kısmının yer değiştirmesi ile sonuçlanır.

'''


def decrypt(msg, key):
    msg = toBin(msg)
    key = toBin(key)
    keyList = []
    temp = ""
    for i in range(0, len(key), 32):
        if i < len(key) / 2:
            temp = key[i:i + 32]
            keyList.append(temp)
    blockList = []
    for i in range(0, len(msg), 32):
        temp = ""
        temp += msg[i:i + 32]
        blockList.append(temp)
    for j in range(0, len(keyList)):
        for i in range(0, len(blockList), 2):
            blockList[i + 1] = xOR(blockList[i + 1], keyList[j])
            temp = blockList[i + 1]
            blockList[i + 1] = blockList[i]
            blockList[i] = temp

    result = ""
    for i in range(0, len(blockList)):
        if i % 2 == 0:
            result += blockList[i]
    print(len(keyList) * 8)
    result = toText(result)
    tot = len(result) / len(keyList)
    result = result[0:int(tot)]
    return result


def main():
    msg = input('Sifrelenecek Metni Giriniz:::\n')
    key = input('UYARI : ANAHTAR DEGERI OLARAK IKILI YANI 1 VE 0 LARDAN OLUSAN  32 KARAKTERLİ SAYI DIZISI GIRINIZ '
                ':::\n  ANAHTAR  ICIN ORNEK SAYI DIZILERI:::: '
                '\n01111011011110110111101101111011\n01111010011110100111101001111010\n '
                '01111101011111010111110101111101  \n01111110011111100111111001111110\n')
    print(msg)

    result = encrypt(msg, key)
    print(key)
    print('Ascii ile Sifrelenmis Metin:::\n', repr(result))
    print('Şifrelenmis Metin::: \n' + result)
    result = decrypt(result, key)

    print('Ascii ile Sifresi Cozulmus Metin:::\n', repr(result))
    print('Sifresi Cozulmus Metin::: \n' + result)


main()

os.system("pause")
