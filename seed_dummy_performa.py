import random

from database import SessionLocal
import models

PRODUK_LIST = [
    "Keyboard Mekanik", "Mouse Wireless", "Monitor LED",
    "Teh Melati", "Kopi Hitam", "Headset Gaming",
    "Webcam HD", "Flashdisk 32GB", "Mousepad Gaming",
    "Speaker Bluetooth",
]

JUMLAH_DATA = 8000
DB_YANG_DIIZINKAN = "toko_db_test"


def main():
    db = SessionLocal()
    try:
        nama_db_aktif = db.bind.url.database
        if nama_db_aktif != DB_YANG_DIIZINKAN:
            print(
                f"DIBATALKAN: database yang tersambung sekarang adalah "
                f"'{nama_db_aktif}', bukan '{DB_YANG_DIIZINKAN}'."
            )
            return

        user_ids = [row[0] for row in db.query(models.User.id).all()]
        if not user_ids:
            print("Tidak ada user di database. Jalankan seed.py dulu untuk membuat user.")
            return

        print(f"Membuat {JUMLAH_DATA} baris data dummy di '{nama_db_aktif}'...")
        dummy_orders = []
        for _ in range(JUMLAH_DATA):
            jumlah = random.randint(1, 5)
            harga_satuan = random.randint(10000, 150000)
            dummy_orders.append({
                "user_id": random.choice(user_ids),
                "produk": random.choice(PRODUK_LIST),
                "jumlah": jumlah,
                "total": jumlah * harga_satuan,
            })

        db.bulk_insert_mappings(models.Order, dummy_orders)
        db.commit()
        print("Selesai. Data dummy berhasil ditambahkan.")

    finally:
        db.close()


if __name__ == "__main__":
    main()