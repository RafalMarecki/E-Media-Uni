import codecs
import struct


class Chunk:
    DLUGOSC = 4


    def __init__(self, dlugosc, dane, typ, crc):
        self.dlugosc = dlugosc
        self.dane = dane
        self.typ = typ
        self.crc = crc

    def __str__(self):
        print("Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("    Lenght: " + str(int.from_bytes(self.dlugosc, 'big')))
        # print("    dane: " + str(self.dane))
        print("    CRC: " + self.crc.hex())


class IHDR(Chunk):
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)

        wartosci = struct.unpack('>iibbbbb', self.dane)
        self.width = str(wartosci[0])
        self.height = str(wartosci[1])
        self.bit_depth = str(wartosci[2])
        self.color_type = str(wartosci[3])
        self.compression_method = str(wartosci[4])
        self.filter_method = str(wartosci[5])
        self.interlace_method = str(wartosci[6])

    def __str__(self):
        print("Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("    Width: " + self.width)
        print("    Height: " + self.height)
        print("    Bit_depth: " + self.bit_depth)
        print("    Color_type: " + self.color_type)
        print("    Compression_method: " + self.compression_method)
        print("    Filter_method: " + self.filter_method)
        print("    Interlace_method: " + self.interlace_method)


class IDAT(Chunk):
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)


class IEND(Chunk):
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)


class gAMA(Chunk):
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)

    def __str__(self):
        gamma = int.from_bytes(self.dane, 'big') / 100000
        print("Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("    Gamma number:" + str(gamma))


class cHRM(Chunk):
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)

    def __str__(self):
        wartosci = struct.unpack('>iiiiiiii', self.dane)
        WPx = wartosci[0] / 100000
        WPy = wartosci[1] / 100000
        Rx = wartosci[2] / 100000
        Ry = wartosci[3] / 100000
        Gx = wartosci[4] / 100000
        Gy = wartosci[5] / 100000
        Bx = wartosci[6] / 100000
        By = wartosci[7] / 100000
        print("Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("    WhitePointX: " + str(WPx))
        print("    WhitePointY: " + str(WPy))
        print("    RedX: " + str(Rx))
        print("    RedY: " + str(Ry))
        print("    GreenX: " + str(Gx))
        print("    GreenY: " + str(Gy))
        print("    BlueX: " + str(Bx))
        print("    BlueY: " + str(By))


class tIME(Chunk):
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)

    def __str__(self):
        wartosci = struct.unpack('>hbbbbb', self.dane)
        rok = wartosci[0]
        miesiac = wartosci[1]
        dzien = wartosci[2]
        godzina = wartosci[3]
        minuta = wartosci[4]
        sekunda = wartosci[5]
        print("Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("    Ostatnia modyfikacja: "
              + str(rok) + '/' + str(miesiac) + '/' + str(dzien)
              + ' ' + str(godzina) + ':' + str(minuta) + ':' + str(sekunda))


class pHYs(Chunk):
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)

    def __str__(self):
        wartosci = struct.unpack('>iib', self.dane)
        pixX = wartosci[0]
        pixY = wartosci[1]
        unit = wartosci[2]
        print("Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("    X: " + str(pixX))
        print("    Y: " + str(pixY))
        print("    Unit: " + str(unit))


# Does not work
# class PLTE(Chunk):
#     def __init__(self, dlugosc, typ, dane, crc):
#         super().__init__(dlugosc, typ, dane, crc)

#     def __str__(self):
#         wartosci = struct.unpack('>bbb', self.dane)
#         red = wartosci[0]
#         green = wartosci[1]
#         blue = wartosci[2]
#         print("Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
#         print(self.dane)
#         print("    Red: " + str(red))
#         print("    Green: " + str(green))
#         print("    Blue: " + str(blue))

NIEZBEDNE_CHUNKI = [b'IHDR', b'IDAT', b'IEND']

RODZAJE_CHUNKOW = {
    b'IHDR': IHDR,
    # b'PLTE': PLTE,
    b'IDAT': IDAT,
    b'IEND': IEND,
    b'tIME': tIME,
    b'gAMA': gAMA,
    b'pHYs': pHYs,
    b'cHRM': cHRM
}

