import cv2
from matplotlib import image as mpimg, pyplot as plt
import numpy as np

from Chunk import *

PNG_MAGIC_NUMBER = b'\x89PNG\r\n\x1a\n'

class PlikPng:
    # Konstruktor
    def __init__(self, sciezka): 
        try:
            self.plik = open(sciezka, 'rb')
        except IOError as e:
            raise e

        if self.plik.read(len(PNG_MAGIC_NUMBER)) != PNG_MAGIC_NUMBER:
            raise Exception('To nie plik PNG!')

        self.sciezka = sciezka    
        self.tablica_chunkow = []

    # Wyswietla pojedynczy obraz
    def wyswietl_obraz(self):            
        tmp_png = self.plik
        tmp_png.seek(0)
        img = mpimg.imread(tmp_png)
        plt.imshow(img)
        plt.show()
        tmp_png.seek(len(PNG_MAGIC_NUMBER))     # Omijamy magic nuber

    # Wyswietla obraz oryginalny i obraz tylko z niezbędnymi chunkami side-by-side
    def wyswietl_orginal_z_oczyszczonym(self, plik):
        img = mpimg.imread(self.sciezka)

        sciezka = 'images/' + plik + '.png'
        self.stworz_plik_z_niezbednymi_chunkami(sciezka)
        img2 = mpimg.imread(sciezka)

        plt.subplot(121), plt.imshow(img)
        plt.title('Obrazek oryginalny'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img2)
        plt.title('Obrazek oczyszczony'), plt.xticks([]), plt.yticks([])
        plt.show()

    # Przeprowadza fazowa i amplitudowa transformatę fouriera na obrazie i wyswietla je side-by-side
    def wyswietl_transformate_fouriera(self):
        img = cv2.imread(self.sciezka, 0)
        f = np.fft.fft2(img)            # Fourier dyskretny dwuwymiarowy
        fshift = np.fft.fftshift(f)     # Shift skladowej stalej na srodek

        widmo_amplitudowe = 20 * np.log(np.abs(fshift))     
        widmo_fazowe = np.asarray(np.angle(fshift))

        plt.subplot(141), plt.imshow(img, cmap='gray')
        plt.title('Obrazek oryginalny'), plt.xticks([]), plt.yticks([])
        plt.subplot(142), plt.imshow(widmo_amplitudowe, cmap='gray')
        plt.title('Widmo amplitudowe'), plt.xticks([]), plt.yticks([])
        plt.subplot(143), plt.imshow(widmo_fazowe, cmap='gray')
        plt.title('Widmo fazowe'), plt.xticks([]), plt.yticks([])

        transformata_odwrotna = np.fft.ifft2(f)
        plt.subplot(144), plt.imshow(np.abs(transformata_odwrotna), cmap='gray')
        plt.title('Odwrotna transformata fouriera'), plt.xticks([]), plt.yticks([])
        plt.show()

    # Wypisz tablice chunkow
    def wypisz_chunki(self):
        print("----------------------")
        for chunk in self.tablica_chunkow:
            chunk.__str__()
            print("----------------------")

    # Wyczysc tablice chunkow
    def wyczysc_tablice_chunkow(self):
        self.plik.seek(len(PNG_MAGIC_NUMBER))
        self.tablica_chunkow.clear()

    # Wczytaj wszystkie chunki do tablicy 
    def wczytaj_wszystkie_chunki(self):
        self.tablica_chunkow = []
        while True:
            dlugosc = self.plik.read(Chunk.DLUGOSC)
            typ = self.plik.read(Chunk.DLUGOSC)
            dane = self.plik.read(int.from_bytes(dlugosc, 'big'))
            crc = self.plik.read(Chunk.DLUGOSC)

            specific_chunk = RODZAJE_CHUNKOW.get(typ, Chunk)
            chunk = specific_chunk(dlugosc, dane, typ, crc)
            self.tablica_chunkow.append(chunk)

            if typ == b'IEND':
                self.plik.seek(len(PNG_MAGIC_NUMBER))
                break

    # Wczytaj tylko niezbedne chunki do tablicy
    def wczytaj_niezbedne_chunki(self):
        self.tablica_chunkow = []
        while True:
            dlugosc = self.plik.read(Chunk.DLUGOSC)
            typ = self.plik.read(Chunk.DLUGOSC)
            dane = self.plik.read(int.from_bytes(dlugosc, 'big'))
            crc = self.plik.read(Chunk.DLUGOSC)

            if typ in NIEZBEDNE_CHUNKI:
                specific_chunk = RODZAJE_CHUNKOW.get(typ, Chunk)
                chunk = specific_chunk(dlugosc, dane, typ, crc)
                self.tablica_chunkow.append(chunk)

            if typ == b'IEND':
                self.plik.seek(len(PNG_MAGIC_NUMBER))
                break

    # Stworz plik z niezbednymi chunkami
    def stworz_plik_z_niezbednymi_chunkami(self, sciezka):
        plik = open(sciezka, 'wb')
        plik.write(PNG_MAGIC_NUMBER)

        for chunk in self.tablica_chunkow:
            if chunk.typ in NIEZBEDNE_CHUNKI:
                plik.write(chunk.dlugosc)
                plik.write(chunk.typ)
                plik.write(chunk.dane)
                plik.write(chunk.crc)

        plik.close()
