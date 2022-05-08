import cv2
from matplotlib import image as mpimg, pyplot as plt
import numpy as np

from Chunk import *

PNG_MAGIC_NUMBER = b'\x89PNG\r\n\x1a\n'

class PlikPng:
    # Konstruktor
    def __init__(self, path): 
        try:
            self.file = open(path, 'rb')
        except IOError as e:
            raise e

        if self.file.read(len(PNG_MAGIC_NUMBER)) != PNG_MAGIC_NUMBER:
            raise Exception('To nie plik PNG!')

        self.path = path    
        self.chunks = []

    # Wyswietla pojedynczy obraz
    def wyswietl_obraz(self):            
        tmp_png = self.file
        tmp_png.seek(0)
        img = mpimg.imread(tmp_png)
        plt.imshow(img)
        plt.show()
        tmp_png.seek(len(PNG_MAGIC_NUMBER))

    # Wyswietla obraz oryginalny i obraz tylko z niezbędnymi chunkami side-by-side
    def wyswietl_orginal_z_oczyszczonym(self, file_name):
        img = mpimg.imread(self.path)

        file_path = 'images/' + file_name + '.png'
        self.stworz_plik_z_niezbednymi_chunkami(file_path)
        img2 = mpimg.imread(file_path)

        plt.subplot(121), plt.imshow(img)
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img2)
        plt.title('Cleaned Image'), plt.xticks([]), plt.yticks([])
        plt.show()

    # Przeprowadza fazowa i amplitudowa transformatę fouriera na obrazie i wyswietla je side-by-side
    def wyswietl_transformate_fouriera(self):
        img = cv2.imread(self.path, 0)
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift))
        phase_spectrum = np.asarray(np.angle(fshift))

        plt.subplot(131), plt.imshow(img, cmap='gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(132), plt.imshow(magnitude_spectrum, cmap='gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.subplot(133), plt.imshow(phase_spectrum, cmap='gray')
        plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])
        plt.show()

    # Wypisz tablice chunkow
    def wypisz_chunki(self):
        print("----------------------")
        for chunk in self.chunks:
            chunk.__str__()
            print("----------------------")

    # Wyczysc tablice chunkow
    def wyczysc_tablice_chunkow(self):
        self.file.seek(len(PNG_MAGIC_NUMBER))
        self.chunks.clear()

    # Wczytaj wszystkie chunki do tablicy 
    def wczytaj_wszystkie_chunki(self):
        self.chunks = []
        while True:
            dlugosc = self.file.read(Chunk.DLUGOSC)
            typ = self.file.read(Chunk.DLUGOSC)
            dane = self.file.read(int.from_bytes(dlugosc, 'big'))
            crc = self.file.read(Chunk.DLUGOSC)
            specific_chunk = RODZAJE_CHUNKOW.get(typ, Chunk)
            chunk = specific_chunk(dlugosc, dane, typ, crc)
            self.chunks.append(chunk)
            if typ == b'IEND':
                self.file.seek(len(PNG_MAGIC_NUMBER))
                break

    # Wczytaj tylko niezbedne chunki do tablicy
    def wczytaj_niezbedne_chunki(self):
        self.chunks = []
        while True:
            dlugosc = self.file.read(Chunk.DLUGOSC)
            typ = self.file.read(Chunk.DLUGOSC)
            dane = self.file.read(int.from_bytes(dlugosc, 'big'))
            crc = self.file.read(Chunk.DLUGOSC)
            if typ in NIEZBEDNE_CHUNKI:
                specific_chunk = RODZAJE_CHUNKOW.get(typ, Chunk)
                chunk = specific_chunk(dlugosc, dane, typ, crc)
                self.chunks.append(chunk)
            if typ == b'IEND':
                self.file.seek(len(PNG_MAGIC_NUMBER))
                break

    # Stworz plik z niezbednymi chunkami
    def stworz_plik_z_niezbednymi_chunkami(self, file_path):
        new_file = open(file_path, 'wb')
        new_file.write(PNG_MAGIC_NUMBER)

        for chunk in self.chunks:
            if chunk.typ in NIEZBEDNE_CHUNKI:
                new_file.write(chunk.dlugosc)
                new_file.write(chunk.typ)
                new_file.write(chunk.dane)
                new_file.write(chunk.crc)

        new_file.close()
