import json
import datetime

# --- VERİ YÖNETİMİ ---
def verileri_yukle():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"uyeler": [], "gorevler": [], "toplantilar": []}

def verileri_kaydet(veri):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(veri, f, indent=4, ensure_ascii=False)

# --- İŞLEVSEL FONKSİYONLAR (MODÜLLER) ---

def toplanti_planla(data):
    print("\n--- YENİ TOPLANTI PLANLA ---")
    konu = input("Toplantı Konusu: ")
    tarih = input("Tarih (GG.AA.YYYY): ")
    saat = input("Saat (SS:DD): ")
    yeni_toplanti = {"konu": konu, "tarih": tarih, "saat": saat, "olusturma_tarihi": str(datetime.datetime.now())}
    data["toplantilar"].append(yeni_toplanti)
    verileri_kaydet(data)
    print(f"-> '{konu}' toplantısı başarıyla planlandı.")

def toplantilari_listele(data):
    print("\n--- PLANLANMIŞ TOPLANTILAR ---")
    if not data.get("toplantilar"):
        print("Henüz planlanmış bir toplantı yok.")
    else:
        for i, t in enumerate(data["toplantilar"], 1):
            print(f"{i}. {t['tarih']} saat {t['saat']} -> Konu: {t['konu']}")

def istatistikleri_goster(data):
    print("\n--- KULÜP GENEL İSTATİSTİKLERİ ---")
    toplam_uye = len(data["uyeler"])
    toplam_gorev = len(data["gorevler"])
    tamamlanan = len([g for g in data["gorevler"] if g["durum"] == "TAMAMLANDI"])
    yuzde = (tamamlanan / toplam_gorev * 100) if toplam_gorev > 0 else 0
    print(f"👥 Üye: {toplam_uye} | 📋 Görev: {toplam_gorev} | ✅ Başarı: %{yuzde:.1f}")

def gorevleri_filtrele(data):
    print("\n--- GÖREV FİLTRELEME ---")
    print("1- Sorumlu Kişiye Göre Ara")
    print("2- Duruma Göre Filtrele (T: Tamamlandı / D: Devam Ediyor)")
    alt_secim = input("Seçiminiz: ")
    bulunanlar = []

    if alt_secim == "1":
        isim = input("Aranan üye ismi: ").lower()
        bulunanlar = [g for g in data["gorevler"] if isim in g["sorumlu"].lower()]
    elif alt_secim == "2":
        durum = input("Durum (T/D): ").upper()
        hedef_durum = "TAMAMLANDI" if durum == "T" else "Devam Ediyor"
        bulunanlar = [g for g in data["gorevler"] if g["durum"] == hedef_durum]

    print("\n--- ARAMA SONUÇLARI ---")
    if not bulunanlar:
        print("Kriterlere uygun görev bulunamadı.")
    else:
        for i, g in enumerate(bulunanlar, 1):
            print(f"{i}. [{g['durum']}] {g['baslik']} - Sorumlu: {g['sorumlu']}")

# --- ANA PROGRAM DÖNGÜSÜ ---
def ana_menu():
    data = verileri_yukle()
    while True:
        print("\n--- UNITY MANAGER: GÖNÜLLÜ YÖNETİM PANELİ ---")
        print("1- Üye Ekle\n2- Yeni Görev Ata\n3- Görevleri Görüntüle\n4- Görev Durumu Güncelle")
        print("5- Yeni Toplantı Planla\n6- Toplantıları Listele\n7- Görevleri Filtrele/Ara\n8- İstatistikler\n0- Çıkış")
        
        secim = input("\nSeçiminiz: ")
        
        if secim == "1":
            ad = input("Üye Adı: ")
            data["uyeler"].append({"ad": ad, "kayit_tarihi": str(datetime.date.today())})
            verileri_kaydet(data)
        elif secim == "2":
            baslik = input("Görev: "); sorumlu = input("Sorumlu: ")
            data["gorevler"].append({"baslik": baslik, "sorumlu": sorumlu, "durum": "Devam Ediyor", "tarih": str(datetime.date.today())})
            verileri_kaydet(data)
        elif secim == "3":
            for i, g in enumerate(data["gorevler"], 1):
                print(f"{i}. [{g['durum']}] {g['baslik']} ({g['sorumlu']})")
        elif secim == "4":
            try:
                idx = int(input("Güncellemek istediğiniz görev no: ")) - 1
                data["gorevler"][idx]["durum"] = "TAMAMLANDI"
                verileri_kaydet(data)
                print("Güncellendi!")
            except:
                print("Hatalı giriş!")
        elif secim == "5":
            toplanti_planla(data)
        elif secim == "6":
            toplantilari_listele(data)
        elif secim == "7":
            gorevleri_filtrele(data)
        elif secim == "8":
            istatistikleri_goster(data)
        elif secim == "0":
            break

if __name__ == "__main__":
    ana_menu()
    