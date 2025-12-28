# database.py
import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Tabel Kategori
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS kategori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_kategori TEXT NOT NULL UNIQUE
            )
        """)

        # Tabel Supplier
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS supplier (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_supplier TEXT NOT NULL,
                alamat TEXT,
                telepon TEXT
            )
        """)

        # Tabel Karyawan
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS karyawan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_karyawan TEXT NOT NULL,
                alamat TEXT,
                telepon TEXT
            )
        """)
        
        # Tabel Pelanggan
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pelanggan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_pelanggan TEXT NOT NULL,
                alamat TEXT,
                telepon TEXT
            )
        """)
        
        # Tabel Produk
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produk (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode_produk TEXT NOT NULL UNIQUE,
                nama_produk TEXT NOT NULL,
                id_kategori INTEGER,
                id_supplier INTEGER,
                harga_beli REAL,
                harga_jual REAL,
                stok INTEGER DEFAULT 0,
                FOREIGN KEY (id_kategori) REFERENCES kategori(id),
                FOREIGN KEY (id_supplier) REFERENCES supplier(id)
            )
        """)

        # Tabel Penjualan
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS penjualan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pelanggan INTEGER,
                id_karyawan INTEGER,
                tanggal_penjualan TEXT NOT NULL,
                total_harga REAL,
                FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id),
                FOREIGN KEY (id_karyawan) REFERENCES karyawan(id)
            )
        """)

        # Tabel Detail Penjualan
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detail_penjualan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_penjualan INTEGER,
                id_produk INTEGER,
                jumlah INTEGER,
                harga_satuan REAL,
                FOREIGN KEY (id_penjualan) REFERENCES penjualan(id),
                FOREIGN KEY (id_produk) REFERENCES produk(id)
            )
        """)
        
        # Tabel Pembelian
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pembelian (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_supplier INTEGER,
                id_karyawan INTEGER,
                tanggal_pembelian TEXT NOT NULL,
                total_harga REAL,
                FOREIGN KEY (id_supplier) REFERENCES supplier(id),
                FOREIGN KEY (id_karyawan) REFERENCES karyawan(id)
            )
        """)

        # Tabel Detail Pembelian
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detail_pembelian (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pembelian INTEGER,
                id_produk INTEGER,
                jumlah INTEGER,
                harga_satuan REAL,
                FOREIGN KEY (id_pembelian) REFERENCES pembelian(id),
                FOREIGN KEY (id_produk) REFERENCES produk(id)
            )
        """)

        # Tabel Retur Penjualan
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS retur_penjualan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_penjualan INTEGER,
                id_pelanggan INTEGER,
                id_karyawan INTEGER,
                tanggal_retur TEXT,
                total_retur REAL,
                FOREIGN KEY (id_penjualan) REFERENCES penjualan(id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detail_retur_penjualan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_retur INTEGER,
                id_produk INTEGER,
                qty INTEGER,
                harga REAL,
                FOREIGN KEY (id_retur) REFERENCES retur_penjualan(id)
            )
        """)

        self.conn.commit()

    # --- Metode CRUD Umum ---
    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def execute_fetch_query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    # --- Metode untuk Pelanggan ---
    def add_pelanggan(self, nama, alamat, telepon):
        self.execute_query("INSERT INTO pelanggan (nama_pelanggan, alamat, telepon) VALUES (?, ?, ?)", (nama, alamat, telepon))

    def get_all_pelanggan(self):
        return self.execute_fetch_query("SELECT id, nama_pelanggan, alamat, telepon FROM pelanggan")

    def update_pelanggan(self, id, nama, alamat, telepon):
        self.execute_query("UPDATE pelanggan SET nama_pelanggan=?, alamat=?, telepon=? WHERE id=?", (nama, alamat, telepon, id))

    def delete_pelanggan(self, id):
        self.execute_query("DELETE FROM pelanggan WHERE id=?", (id,))

    # --- Metode untuk Produk ---
    def add_produk(self, kode, nama, id_kategori, id_supplier, harga_beli, harga_jual, stok):
        self.execute_query("INSERT INTO produk (kode_produk, nama_produk, id_kategori, id_supplier, harga_beli, harga_jual, stok) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (kode, nama, id_kategori, id_supplier, harga_beli, harga_jual, stok))

    def get_all_produk(self):
        return self.execute_fetch_query("""
            SELECT p.id, p.kode_produk, p.nama_produk, 
            k.nama_kategori, s.nama_supplier,
            p.harga_beli, 
            p.harga_jual, p.stok 
            FROM produk p
            LEFT JOIN kategori k ON p.id_kategori = k.id
            LEFT JOIN supplier s ON p.id_supplier = s.id
        """)

    def update_produk(self, id, kode, nama, id_kategori, id_supplier, harga_beli, harga_jual, stok):
        self.execute_query("UPDATE produk SET kode_produk=?, nama_produk=?, id_kategori=?, id_supplier=?, harga_beli=?, harga_jual=?, stok=? WHERE id=?",
                           (kode, nama, id_kategori, id_supplier, harga_beli, harga_jual, stok, id))

    def delete_produk(self, id):
        self.execute_query("DELETE FROM produk WHERE id=?", (id,))

    # --- Metode untuk Kategori ---
    def add_kategori(self, nama):
        self.execute_query("INSERT INTO kategori (nama_kategori) VALUES (?)", (nama,))

    def get_all_kategori(self):
        return self.execute_fetch_query("SELECT id, nama_kategori FROM kategori")

    def update_kategori(self, id, nama):
        self.execute_query("UPDATE kategori SET nama_kategori=? WHERE id=?", (nama, id))

    def delete_kategori(self, id):
        self.execute_query("DELETE FROM kategori WHERE id=?", (id,))

    # --- Metode untuk Supplier ---
    def add_supplier(self, nama, alamat, telepon):
        self.execute_query("INSERT INTO supplier (nama_supplier, alamat, telepon) VALUES (?, ?, ?)", (nama, alamat, telepon))

    def get_all_supplier(self):
        return self.execute_fetch_query("SELECT id, nama_supplier, alamat, telepon FROM supplier")

    def update_supplier(self, id, nama, alamat, telepon):
        self.execute_query("UPDATE supplier SET nama_supplier=?, alamat=?, telepon=? WHERE id=?", (nama, alamat, telepon, id))

    def delete_supplier(self, id):
        self.execute_query("DELETE FROM supplier WHERE id=?", (id,))

    # --- Metode untuk Karyawan ---
    def add_karyawan(self, nama, alamat, telepon):
        self.execute_query("INSERT INTO karyawan (nama_karyawan, alamat, telepon) VALUES (?, ?, ?)", (nama, alamat, telepon))

    def get_all_karyawan(self):
        return self.execute_fetch_query("SELECT id, nama_karyawan, alamat, telepon FROM karyawan")

    def update_karyawan(self, id, nama, alamat, telepon):
        self.execute_query("UPDATE karyawan SET nama_karyawan=?, alamat=?, telepon=? WHERE id=?", (nama, alamat, telepon, id))

    def delete_karyawan(self, id):
        self.execute_query("DELETE FROM karyawan WHERE id=?", (id,))
    
    # --- Metode untuk Transaksi ---
    def add_transaksi_penjualan(self, id_pelanggan, id_karyawan, total):
        # Mendapatkan tanggal hari ini
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        self.execute_query("INSERT INTO penjualan (id_pelanggan, id_karyawan, tanggal_penjualan, total_harga) VALUES (?, ?, ?, ?)",
                           (id_pelanggan, id_karyawan, today, total))
        return self.cursor.lastrowid # Mengembalikan ID transaksi yang baru dibuat

    def add_detail_penjualan(self, id_penjualan, id_produk, jumlah, harga):
        self.execute_query("INSERT INTO detail_penjualan (id_penjualan, id_produk, jumlah, harga_satuan) VALUES (?, ?, ?, ?)",
                           (id_penjualan, id_produk, jumlah, harga))
        # Kurangi stok produk
        self.execute_query("UPDATE produk SET stok = stok - ? WHERE id = ?", (jumlah, id_produk))

    def add_transaksi_pembelian(self, id_supplier, id_karyawan, total):
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        self.execute_query("""
            INSERT INTO pembelian (id_supplier, id_karyawan, tanggal_pembelian, total_harga)
            VALUES (?, ?, ?, ?)
        """, (id_supplier, id_karyawan, today, total))
        return self.cursor.lastrowid

    def add_detail_pembelian(self, id_pembelian, id_produk, jumlah, harga):
        self.execute_query("""
            INSERT INTO detail_pembelian (id_pembelian, id_produk, jumlah, harga_satuan)
            VALUES (?, ?, ?, ?)
        """, (id_pembelian, id_produk, jumlah, harga))

        # ⬆ TAMBAH STOK
        self.execute_query(
            "UPDATE produk SET stok = stok + ? WHERE id = ?",
            (jumlah, id_produk)
        )
        
    def get_detail_penjualan_by_id(self, id_penjualan):
        return self.execute_fetch_query("""
            SELECT dp.id, p.id, p.nama_produk, dp.jumlah, dp.harga_satuan
            FROM detail_penjualan dp
            JOIN produk p ON dp.id_produk = p.id
            WHERE dp.id_penjualan = ?
        """, (id_penjualan,))
        
    def add_transaksi_retur_penjualan(self, id_penjualan, id_pelanggan, id_karyawan, total):
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        self.execute_query("""
            INSERT INTO retur_penjualan (id_penjualan, id_pelanggan, id_karyawan, tanggal_retur, total_retur)
            VALUES (?, ?, ?, ?, ?)
        """, (id_penjualan, id_pelanggan, id_karyawan, today, total))
        return self.cursor.lastrowid
    
    def add_detail_retur_penjualan(self, id_retur, id_produk, qty, harga):
        self.execute_query("""
            INSERT INTO detail_retur_penjualan (id_retur, id_produk, qty, harga)
            VALUES (?, ?, ?, ?)
        """, (id_retur, id_produk, qty, harga))

        # ⬆ KEMBALIKAN STOK
        self.execute_query(
            "UPDATE produk SET stok = stok + ? WHERE id = ?",
            (qty, id_produk)
        )




    def get_laporan_penjualan(self):
        return self.execute_fetch_query("""
            SELECT p.id, p.tanggal_penjualan, pel.nama_pelanggan, kar.nama_karyawan, p.total_harga
            FROM penjualan p
            JOIN pelanggan pel ON p.id_pelanggan = pel.id
            JOIN karyawan kar ON p.id_karyawan = kar.id
            ORDER BY p.tanggal_penjualan DESC
        """)

    def close(self):
        self.conn.close()