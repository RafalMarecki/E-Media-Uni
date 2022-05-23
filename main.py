from PlikPng import *

sciezka = "images/android_tIME_cHRM_gAMA.png"

png = PlikPng(sciezka)
print("\n<==========================================>\nWszystkie chunki:")
png.wczytaj_wszystkie_chunki()
png.wypisz_chunki()
png.wyczysc_tablice_chunkow()
print("\n<==========================================>\nNiezbedne chunki:")
png.wczytaj_niezbedne_chunki()
png.wypisz_chunki()
png.wyswietl_orginal_z_oczyszczonym('wyczyszczony_obraz')
png.wyswietl_transformate_fouriera()