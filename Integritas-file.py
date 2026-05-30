import hashlib
from datetime import datetime

def hitung_md5(konten: str) -> str:
    return hashlib.md5(konten.encode("utf-8")).hexdigest()

def hitung_sha256(konten: str) -> str:
    return hashlib.sha256(konten.encode("utf-8")).hexdigest()

def ambil_info_hash(label: str, konten: str) -> dict:
    return {
        "label"    : label,
        "md5"      : hitung_md5(konten),
        "sha256"   : hitung_sha256(konten),
        "ukuran"   : len(konten.encode("utf-8")),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

def bandingkan_hash(asli: dict, modifikasi: dict) -> dict:
    md5_sama    = asli["md5"]    == modifikasi["md5"]
    sha256_sama = asli["sha256"] == modifikasi["sha256"]
    return {
        "md5_sama"      : md5_sama,
        "sha256_sama"   : sha256_sama,
        "integritas_ok" : md5_sama and sha256_sama,
    }

def buat_konten(data: dict) -> str:
    return (
        f"Nama Dokumen       : {data['nama_dokumen']}\n"
        f"ID Dokumen         : {data['id_dokumen']}\n"
        f"Tanggal            : {data['tanggal']}\n"
        f"Perihal            : {data['perihal']}\n"
        f"\n"
        f"Rincian Pengadaan IT:\n"
        f"  Lisensi Software : Rp {data['lisensi_software']}\n"
        f"  Sewa Server      : Rp {data['sewa_server']}\n"
        f"  Registrasi Domain: Rp {data['registrasi_domain']}\n"
        f"Total              : Rp {data['total']}\n"
        f"\n"
        f"Disetujui oleh     : {data['disetujui']}\n"
        f"Status             : {data['status']}\n"
    )

def input_dokumen(judul: str) -> dict:
    LEBAR = 68
    print("\n" + "=" * LEBAR)
    print(f"  INPUT {judul}")
    print("=" * LEBAR)
    data = {}
    data["nama_dokumen"]       = input("  Nama Dokumen        : ")
    data["id_dokumen"]         = input("  ID Dokumen          : ")
    data["tanggal"]            = input("  Tanggal             : ")
    data["perihal"]            = input("  Perihal             : ")
    print("  ---")
    data["lisensi_software"]   = input("  Lisensi Software(Rp): ")
    data["sewa_server"]        = input("  Sewa Server     (Rp): ")
    data["registrasi_domain"]  = input("  Reg. Domain     (Rp): ")
    data["total"]              = input("  Total           (Rp): ")
    print("  ---")
    data["disetujui"]          = input("  Disetujui oleh      : ")
    data["status"]             = input("  Status              : ")
    return data

def main():
    LEBAR = 68

    print("=" * LEBAR)
    print("  APLIKASI PENGECEKAN INTEGRITAS FILE — MD5 & SHA-256")
    print(f"  Waktu : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * LEBAR)

    data_asli  = input_dokumen("FILE ASLI")
    data_modif = input_dokumen("FILE YANG DIMODIFIKASI")

    konten_asli  = buat_konten(data_asli)
    konten_modif = buat_konten(data_modif)

    info_asli  = ambil_info_hash("file_asli.txt",       konten_asli)
    info_modif = ambil_info_hash("file_modifikasi.txt", konten_modif)

    print("\n" + "=" * LEBAR)
    print("  ISI DOKUMEN")
    print("=" * LEBAR)

    print("\n  [ FILE ASLI ]")
    print("-" * LEBAR)
    for baris in konten_asli.strip().splitlines():
        print(f"  {baris}")

    print("\n  [ FILE DIMODIFIKASI ]")
    print("-" * LEBAR)
    for baris in konten_modif.strip().splitlines():
        print(f"  {baris}")

    print("\n" + "=" * LEBAR)
    print("  HASIL HASHING")
    print("=" * LEBAR)

    print("\n" + "-" * LEBAR)
    print("  FILE ASLI")
    print("-" * LEBAR)
    print(f"  Nama      : {info_asli['label']}")
    print(f"  Ukuran    : {info_asli['ukuran']} bytes")
    print(f"  Timestamp : {info_asli['timestamp']}")
    print(f"  MD5       : {info_asli['md5']}")
    print(f"  SHA-256   : {info_asli['sha256']}")

    print("\n" + "-" * LEBAR)
    print("  FILE DIMODIFIKASI")
    print("-" * LEBAR)
    print(f"  Nama      : {info_modif['label']}")
    print(f"  Ukuran    : {info_modif['ukuran']} bytes")
    print(f"  Timestamp : {info_modif['timestamp']}")
    print(f"  MD5       : {info_modif['md5']}")
    print(f"  SHA-256   : {info_modif['sha256']}")

    hasil   = bandingkan_hash(info_asli, info_modif)
    md5_st  = "COCOK   " if hasil["md5_sama"]    else "BERBEDA "
    sha_st  = "COCOK   " if hasil["sha256_sama"] else "BERBEDA "
    verdict = " FILE TIDAK BERUBAH — INTEGRITAS TERJAGA" \
              if hasil["integritas_ok"] \
              else " FILE TELAH DIMODIFIKASI — INTEGRITAS RUSAK"

    print("\n" + "=" * LEBAR)
    print("  HASIL PERBANDINGAN")
    print("=" * LEBAR)
    print(f"\n  {'Algoritma':<10}  {'Status':<16}  Panjang Digest")
    print("  " + "-" * 50)
    print(f"  {'MD5':<10}  {md5_st:<16}  128-bit (32 hex)")
    print(f"  {'SHA-256':<10}  {sha_st:<16}  256-bit (64 hex)")
    print("\n  " + "-" * LEBAR)
    print(f"  KESIMPULAN: {verdict}")
    print("  " + "-" * LEBAR)
    
    print(f"\n  MD5 Asli       : {info_asli['md5']}")
    print(f"  MD5 Modifikasi : {info_modif['md5']}")
    print(f"\n  SHA-256 Asli   :\n    {info_asli['sha256']}")
    print(f"  SHA-256 Modif  :\n    {info_modif['sha256']}")

    print("\n" + "=" * LEBAR)
    print("  SELESAI")
    print("=" * LEBAR)

if __name__ == "__main__":
    main()