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
        print(" > Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("     - Lenght: " + str(int.from_bytes(self.dlugosc, 'big')))
        # print("    dane: " + str(self.dane))
        print("     - CRC: " + self.crc.hex())


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
        print(" > Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("     - Dimensions: " + self.width + " x " + self.height)
        print("     - Bit_depth: " + self.bit_depth)
        print("     - Color_type: " + self.color_type)
        print("     - Compression_method: " + self.compression_method)
        print("     - Filter_method: " + self.filter_method)
        print("     - Interlace_method: " + self.interlace_method)


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
        print(" > Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("     - Gamma number:" + str(gamma))


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
        print(" > Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("     - WhitePointX: " + str(WPx))
        print("     - WhitePointY: " + str(WPy))
        print("     - RedX: " + str(Rx))
        print("     - RedY: " + str(Ry))
        print("     - GreenX: " + str(Gx))
        print("     - GreenY: " + str(Gy))
        print("     - BlueX: " + str(Bx))
        print("     - BlueY: " + str(By))


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
        print(" > Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("     - Ostatnia modyfikacja: "
              + str(rok) + '/' + str(miesiac) + '/' + str(dzien)
              + ' ' + str(godzina) + ':' + str(minuta) + ':' + str(sekunda))

class sRGB(Chunk):
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)

    def __str__(self):
        wartosci = struct.unpack('>b', self.dane)
        color = wartosci[0]
        colors_dic = {
            0: "Perceptual",
            1: "Relative colorimetric",
            2: "Saturation",
            3: "Absolute colorimetric"
        }

        print(" > Nazwa chunka: "  + codecs.decode(self.typ, 'UTF-8'))
        print("     - Color space: " + str(color))
        print("     - Type: " + colors_dic.get(color))



class pHYs(Chunk):
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)

    def __str__(self):
        wartosci = struct.unpack('>iib', self.dane)
        pixele_X = wartosci[0]
        pixele_Y = wartosci[1]
        jedn = wartosci[2]
        print(" > Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        print("     - Pixel per: " + str(jedn) + ", X axis: " + str(pixele_X))
        print("     - Pixel per: " + str(jedn) + ", Y axis: " + str(pixele_Y))

# Does not work
class PLTE(Chunk):
    palette = []
    def __init__(self, dlugosc, typ, dane, crc):
        super().__init__(dlugosc, typ, dane, crc)

    def parse_data(self):
        for i in range(0, len(self.dane), 3):
            part_pix = self.dane[i:i + 3]
            full_pixel = (part_pix[0], part_pix[1], part_pix[2])
            if not self.palette.__contains__(full_pixel):
                self.palette.append(full_pixel)

    def __str__(self):
        self.parse_data()
        print("Nazwa chunka: " + codecs.decode(self.typ, 'UTF-8'))
        for color in self.palette:
            print('[', color[0], ';', color[1], ';', color[2], ']', '->', colored(color[0], color[1], color[2], (str)("KOLOR")))


def colored(r, g, b, text): # Koloruje 
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


NIEZBEDNE_CHUNKI = [b'IHDR', b'IDAT', b'IEND', b'PLTE']

RODZAJE_CHUNKOW = {
    b'IHDR': IHDR,####################################################################################
    b'PLTE': PLTE,####################################################################################
    b'IDAT': IDAT,####################################################################################
    b'IEND': IEND,####################################################################################
    b'tIME': tIME,
    b'sRGB': sRGB,####################################################################################
    b'gAMA': gAMA,
    b'pHYs': pHYs,####################################################################################
    b'cHRM': cHRM
}

