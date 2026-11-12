import json

def tanya_user():
    fakta = {}

    print("=== SISTEM PAKAR STRATEGI PIT STOP F1 ===")
    print("Jawab pertanyaan berikut untuk memasukkan fakta:\n")

    print("1. Apakah saat ini sesi Balapan atau Kualifikasi?")
    print("   a. Balapan")
    print("   b. Kualifikasi")
    jawaban = input("Jawab (a/b): ").strip().lower()
    if jawaban == "b":
        fakta["Sesi"] = "Kualifikasi"
        print("\n   Fase Kualifikasi?")
        print("   1. Q1 / Q2")
        print("   2. Q3")
        q = input("   Jawab (1/2): ").strip()
        fakta["Fase Quali"] = "Q3" if q == "2" else "Q1/Q2"
    else:
        fakta["Sesi"] = "Balapan"

    print("\n2. Bagaimana kondisi lintasan saat ini?")
    print("   1. Kering")
    print("   2. Lembap")
    print("   3. Basah Deras")
    l = input("Jawab (1/2/3): ").strip()
    if l == "2":
        fakta["Kondisi Lintasan"] = "Lembap"
    elif l == "3":
        fakta["Kondisi Lintasan"] = "Basah Deras"
    else:
        fakta["Kondisi Lintasan"] = "Kering"

    if fakta["Sesi"] == "Balapan":
        print("\n3. Apakah FIA mendeklarasikan Wet Race (Basah)?")
        w = input("Jawab (y/n): ").strip().lower()
        fakta["Deklarasi Basah FIA"] = "Ya" if w == "y" else "Tidak"

        print("\n4. Berapa jenis ban kering yang sudah dipakai?")
        print("   1. Baru 1 Jenis")
        print("   2. Sudah 2 Jenis atau Lebih")
        c = input("Jawab (1/2): ").strip()
        fakta["Jumlah Compound Kering"] = "1 Jenis" if c == "1" else ">1 Jenis"

        print("\n5. Apakah sisa lap balapan kurang dari atau sama dengan batas stint ban?")
        lap = input("Jawab (y/n): ").strip().lower()
        fakta["Sisa Lap <= Batas Stint"] = True if lap == "y" else False

        print("\n6. Ban apa yang dipakai saat ini?")
        print("   1. Ban Kering (Soft/Medium/Hard)")
        print("   2. Intermediate")
        print("   3. Full Wet")
        b = input("Jawab (1/2/3): ").strip()
        if b == "2":
            fakta["Ban Saat Ini"] = "Intermediate"
        elif b == "3":
            fakta["Ban Saat Ini"] = "Full Wet"
        else:
            fakta["Ban Saat Ini"] = "Kering"

        print("\n7. Apakah ada ancaman Undercut dari rival?")
        u = input("Jawab (y/n): ").strip().lower()
        fakta["Ancaman Rival"] = "Ancaman Undercut" if u == "y" else "None"

    print("\n8. Bagaimana status Safety Car?")
    print("   1. Tidak ada (Normal)")
    print("   2. VSC / Safety Car")
    print("   3. Wajib Ban Basah SC")
    sc = input("Jawab (1/2/3): ").strip()
    if sc == "2":
        fakta["Status Safety Car"] = "VSC/SC"
    elif sc == "3":
        fakta["Status Safety Car"] = "Wajib Ban Basah SC"
    else:
        fakta["Status Safety Car"] = "None"

    if fakta["Kondisi Lintasan"] == "Kering":
        print("\n9. Apa target stint balapan?")
        print("   1. Hemat Panjang")
        print("   2. Sedang Seimbang")
        print("   3. Push Pendek")
        t = input("Jawab (1/2/3): ").strip()
        if t == "1":
            fakta["Target Stint"] = "Hemat Panjang"
        elif t == "3":
            fakta["Target Stint"] = "Push Pendek"
        else:
            fakta["Target Stint"] = "Sedang Seimbang"

    print("\n10. Bagaimana tingkat keausan / degradasi ban?")
    print("    1. Rendah")
    print("    2. Tinggi")
    print("    3. Aus Parah")
    deg = input("Jawab (1/2/3): ").strip()
    if deg == "2":
        fakta["Degradasi Ban"] = "Tinggi"
    elif deg == "3":
        fakta["Degradasi Ban"] = "Aus Parah"
    else:
        fakta["Degradasi Ban"] = "Rendah"

    return fakta

def proses_forward_chaining(fakta):
    aturan_terpakai = []
    fakta_baru_ada = True

    print("\n" + "=" * 50)
    print("PROSES INFERENSI FORWARD CHAINING")
    print("=" * 50)

    while fakta_baru_ada:
        fakta_baru_ada = False

        # R1
        if "R1" not in aturan_terpakai:
            if (fakta.get("Sesi") == "Balapan" and 
                fakta.get("Kondisi Lintasan") == "Kering" and 
                fakta.get("Deklarasi Basah FIA") == "Tidak" and 
                fakta.get("Jumlah Compound Kering") == "1 Jenis" and 
                fakta.get("Sisa Lap <= Batas Stint") == True):
                
                fakta["Mandat FIA"] = "Wajib Pit Ganti Ban Lain"
                aturan_terpakai.append("R1")
                fakta_baru_ada = True
                print("-> Aturan R1 cocok: Mandat FIA = Wajib Pit Ganti Ban Lain")

        # R2
        if "R2" not in aturan_terpakai:
            if fakta.get("Sesi") == "Balapan" and (fakta.get("Deklarasi Basah FIA") == "Ya" or fakta.get("Ban Saat Ini") in ["Intermediate", "Full Wet"]):
                fakta["Mandat FIA"] = "Bebas Aturan Dua Compound"
                aturan_terpakai.append("R2")
                fakta_baru_ada = True
                print("-> Aturan R2 cocok: Mandat FIA = Bebas Aturan Dua Compound")

        # R3
        if "R3" not in aturan_terpakai:
            if fakta.get("Status Safety Car") == "Wajib Ban Basah SC":
                fakta["Pilihan Ban"] = "Full Wet"
                fakta["Mandat FIA"] = "Wajib Full Wet"
                aturan_terpakai.append("R3")
                fakta_baru_ada = True
                print("-> Aturan R3 cocok: Pilihan Ban = Full Wet")

        # R4
        if "R4" not in aturan_terpakai:
            if fakta.get("Sesi") == "Kualifikasi" and fakta.get("Fase Quali") == "Q1/Q2" and fakta.get("Kondisi Lintasan") == "Kering":
                fakta["Pilihan Ban"] = "Soft"
                aturan_terpakai.append("R4")
                fakta_baru_ada = True
                print("-> Aturan R4 cocok: Pilihan Ban = Soft")

        # R5
        if "R5" not in aturan_terpakai:
            if fakta.get("Sesi") == "Kualifikasi" and fakta.get("Fase Quali") == "Q3" and fakta.get("Kondisi Lintasan") == "Kering":
                fakta["Pilihan Ban"] = "Soft Baru"
                aturan_terpakai.append("R5")
                fakta_baru_ada = True
                print("-> Aturan R5 cocok: Pilihan Ban = Soft Baru")

        # R6
        if "R6" not in aturan_terpakai:
            if fakta.get("Kondisi Lintasan") == "Basah Deras":
                fakta["Pilihan Ban"] = "Full Wet"
                aturan_terpakai.append("R6")
                fakta_baru_ada = True
                print("-> Aturan R6 cocok: Pilihan Ban = Full Wet")

        # R7
        if "R7" not in aturan_terpakai:
            if fakta.get("Kondisi Lintasan") == "Lembap":
                fakta["Pilihan Ban"] = "Intermediate"
                aturan_terpakai.append("R7")
                fakta_baru_ada = True
                print("-> Aturan R7 cocok: Pilihan Ban = Intermediate")

        # R8
        if "R8" not in aturan_terpakai:
            if fakta.get("Kondisi Lintasan") == "Kering" and fakta.get("Target Stint") == "Hemat Panjang":
                fakta["Pilihan Ban"] = "Hard"
                aturan_terpakai.append("R8")
                fakta_baru_ada = True
                print("-> Aturan R8 cocok: Pilihan Ban = Hard")

        # R9
        if "R9" not in aturan_terpakai:
            if fakta.get("Kondisi Lintasan") == "Kering" and fakta.get("Target Stint") == "Sedang Seimbang":
                fakta["Pilihan Ban"] = "Medium"
                aturan_terpakai.append("R9")
                fakta_baru_ada = True
                print("-> Aturan R9 cocok: Pilihan Ban = Medium")

        # R10
        if "R10" not in aturan_terpakai:
            if fakta.get("Kondisi Lintasan") == "Kering" and fakta.get("Target Stint") == "Push Pendek":
                fakta["Pilihan Ban"] = "Soft"
                aturan_terpakai.append("R10")
                fakta_baru_ada = True
                print("-> Aturan R10 cocok: Pilihan Ban = Soft")

        # R11
        if "R11" not in aturan_terpakai:
            if fakta.get("Degradasi Ban") == "Aus Parah":
                fakta["Keputusan Pit"] = "Masuk Pit Sekarang"
                aturan_terpakai.append("R11")
                fakta_baru_ada = True
                print("-> Aturan R11 cocok: Keputusan Pit = Masuk Pit Sekarang")

        # R12
        if "R12" not in aturan_terpakai:
            if fakta.get("Status Safety Car") == "VSC/SC" and fakta.get("Degradasi Ban") in ["Tinggi", "Aus Parah"]:
                fakta["Keputusan Pit"] = "Momen Pit Hemat Waktu"
                aturan_terpakai.append("R12")
                fakta_baru_ada = True
                print("-> Aturan R12 cocok: Keputusan Pit = Momen Pit Hemat Waktu")

        # R13
        if "R13" not in aturan_terpakai:
            if fakta.get("Ancaman Rival") == "Ancaman Undercut" and fakta.get("Degradasi Ban") in ["Tinggi", "Aus Parah"]:
                fakta["Keputusan Pit"] = "Tangkis Undercut"
                aturan_terpakai.append("R13")
                fakta_baru_ada = True
                print("-> Aturan R13 cocok: Keputusan Pit = Tangkis Undercut")

        # R14
        if "R14" not in aturan_terpakai:
            if fakta.get("Degradasi Ban") == "Rendah" and fakta.get("Mandat FIA") != "Wajib Pit Ganti Ban Lain":
                fakta["Keputusan Pit"] = "Stay Out"
                aturan_terpakai.append("R14")
                fakta_baru_ada = True
                print("-> Aturan R14 cocok: Keputusan Pit = Stay Out")

        # ATURAN GOAL

        # R15
        if "R15" not in aturan_terpakai:
            if fakta.get("Mandat FIA") == "Wajib Pit Ganti Ban Lain" and "Pilihan Ban" in fakta:
                ban = fakta["Pilihan Ban"]
                fakta["Goal"] = f"Box Box Box! Pasang Ban {ban} - Memenuhi Wajib Regulasi FIA"
                aturan_terpakai.append("R15")
                fakta_baru_ada = True
                print(f"-> Aturan R15 cocok: Goal Ditemukan!")

        # R16
        if "R16" not in aturan_terpakai:
            if fakta.get("Keputusan Pit") == "Momen Pit Hemat Waktu" and "Pilihan Ban" in fakta:
                ban = fakta["Pilihan Ban"]
                fakta["Goal"] = f"Box Lap Ini! Manfaatkan VSC/Safety Car -> Pasang Ban {ban}"
                aturan_terpakai.append("R16")
                fakta_baru_ada = True
                print(f"-> Aturan R16 cocok: Goal Ditemukan!")

        # R17
        if "R17" not in aturan_terpakai:
            if fakta.get("Keputusan Pit") == "Tangkis Undercut" and "Pilihan Ban" in fakta:
                ban = fakta["Pilihan Ban"]
                fakta["Goal"] = f"Box Lap Ini! Cover Undercut Rival -> Pasang Ban {ban}"
                aturan_terpakai.append("R17")
                fakta_baru_ada = True
                print(f"-> Aturan R17 cocok: Goal Ditemukan!")

        # R18
        if "R18" not in aturan_terpakai:
            if fakta.get("Sesi") == "Kualifikasi" and fakta.get("Pilihan Ban") == "Soft Baru":
                fakta["Goal"] = "Push Lap! Gas Pake Ban Soft Baru Buat Kualifikasi"
                aturan_terpakai.append("R18")
                fakta_baru_ada = True
                print("-> Aturan R18 cocok: Goal Ditemukan!")

        # R19
        if "R19" not in aturan_terpakai:
            if fakta.get("Keputusan Pit") == "Stay Out":
                fakta["Goal"] = "Stay Out! Ban Masih Bagus, Lanjut Push di Trek"
                aturan_terpakai.append("R19")
                fakta_baru_ada = True
                print("-> Aturan R19 cocok: Goal Ditemukan!")

    return fakta, aturan_terpakai

def tampilkan_hasil(fakta, aturan_terpakai):
    print("\n" + "=" * 50)
    print("HASIL REKOMENDASI STRATEGI PIT STOP")
    print("=" * 50)

    if "Goal" in fakta:
        print(f"\n[HASIL REKOMENDASI UTAMA / GOAL]:")
        print(f"-> \"{fakta['Goal']}\"")
    else:
        print("\n[INFO]: Tidak ada Goal khusus yang terpemicu.")

    print("\nFakta Akhir yang Diperoleh:")
    if "Mandat FIA" in fakta:
        print(f"- Mandat FIA    : {fakta['Mandat FIA']}")
    if "Pilihan Ban" in fakta:
        print(f"- Rekomendasi Ban: {fakta['Pilihan Ban']}")
    if "Keputusan Pit" in fakta:
        print(f"- Keputusan Pit : {fakta['Keputusan Pit']}")

    print("\nAturan yang Terpemicu secara Berurutan:")
    print(" -> ".join(aturan_terpakai))
    print("=" * 50)

if __name__ == "__main__":
    fakta_awal = tanya_user()
    fakta_akhir, aturan_terpakai = proses_forward_chaining(fakta_awal)
    tampilkan_hasil(fakta_akhir, aturan_terpakai)