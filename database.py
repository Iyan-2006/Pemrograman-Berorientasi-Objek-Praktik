# database.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_default_data()

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
                harga_beli REAL DEFAULT 0,
                harga_jual REAL DEFAULT 0,
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
                waktu_penjualan TEXT NOT NULL,
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
                subtotal REAL,
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
                waktu_pembelian TEXT NOT NULL,
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
                subtotal REAL,
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
                tanggal_retur TEXT NOT NULL,
                waktu_retur TEXT NOT NULL,
                total_retur REAL,
                alasan_retur TEXT,
                FOREIGN KEY (id_penjualan) REFERENCES penjualan(id),
                FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id),
                FOREIGN KEY (id_karyawan) REFERENCES karyawan(id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detail_retur_penjualan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_retur INTEGER,
                id_produk INTEGER,
                qty INTEGER,
                harga REAL,
                subtotal REAL,
                FOREIGN KEY (id_retur) REFERENCES retur_penjualan(id),
                FOREIGN KEY (id_produk) REFERENCES produk(id)
            )
        """)

        # Tabel Pengguna (untuk login)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pengguna (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                id_karyawan INTEGER,
                level TEXT DEFAULT 'kasir',
                FOREIGN KEY (id_karyawan) REFERENCES karyawan(id)
            )
        """)

        self.conn.commit()

    def insert_default_data(self):
        """Insert data default untuk aplikasi"""
        try:
            # Cek apakah sudah ada data pelanggan umum
            result = self.cursor.execute("SELECT COUNT(*) FROM pelanggan WHERE id = 1").fetchone()
            if result[0] == 0:
                self.cursor.execute(
                    "INSERT INTO pelanggan (id, nama_pelanggan, alamat, telepon) VALUES (1, 'Umum', '-', '-')"
                )
            
            # Cek apakah sudah ada karyawan admin
            result = self.cursor.execute("SELECT COUNT(*) FROM karyawan WHERE id = 1").fetchone()
            if result[0] == 0:
                self.cursor.execute(
                    "INSERT INTO karyawan (id, nama_karyawan, alamat, telepon) VALUES (1, 'Admin', '-', '-')"
                )
            
            # Cek apakah sudah ada pengguna
            result = self.cursor.execute("SELECT COUNT(*) FROM pengguna WHERE id = 1").fetchone()
            if result[0] == 0:
                self.cursor.execute(
                    "INSERT INTO pengguna (id, username, password, id_karyawan, level) VALUES (1, 'admin', 'admin123', 1, 'admin')"
                )
            
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting default data: {e}")

    # --- Metode CRUD Umum ---
    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Query Error: {e}")
            return False

    def execute_fetch_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Fetch Query Error: {e}")
            return []

    # --- Metode untuk Pelanggan ---
    def add_pelanggan(self, nama, alamat="", telepon=""):
        return self.execute_query(
            "INSERT INTO pelanggan (nama_pelanggan, alamat, telepon) VALUES (?, ?, ?)", 
            (nama, alamat, telepon)
        )

    def get_all_pelanggan(self):
        return self.execute_fetch_query("SELECT id, nama_pelanggan, alamat, telepon FROM pelanggan ORDER BY nama_pelanggan")

    def get_pelanggan_by_id(self, id):
        result = self.execute_fetch_query("SELECT id, nama_pelanggan, alamat, telepon FROM pelanggan WHERE id = ?", (id,))
        return result[0] if result else None

    def update_pelanggan(self, id, nama, alamat, telepon):
        return self.execute_query(
            "UPDATE pelanggan SET nama_pelanggan=?, alamat=?, telepon=? WHERE id=?", 
            (nama, alamat, telepon, id)
        )

    def delete_pelanggan(self, id):
        return self.execute_query("DELETE FROM pelanggan WHERE id=?", (id,))

    # --- Metode untuk Produk ---
    def add_produk(self, kode, nama, id_kategori=None, id_supplier=None, harga_beli=0, harga_jual=0, stok=0):
        return self.execute_query(
            """INSERT INTO produk (kode_produk, nama_produk, id_kategori, id_supplier, 
               harga_beli, harga_jual, stok) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (kode, nama, id_kategori, id_supplier, harga_beli, harga_jual, stok)
        )

    def get_all_produk(self):
        return self.execute_fetch_query("""
            SELECT p.id, p.kode_produk, p.nama_produk, 
                   k.nama_kategori, s.nama_supplier,
                   p.harga_beli, p.harga_jual, p.stok 
            FROM produk p
            LEFT JOIN kategori k ON p.id_kategori = k.id
            LEFT JOIN supplier s ON p.id_supplier = s.id
            ORDER BY p.nama_produk
        """)

    def get_produk_by_id(self, id):
        result = self.execute_fetch_query("""
            SELECT p.id, p.kode_produk, p.nama_produk, 
                   k.nama_kategori, s.nama_supplier,
                   p.harga_beli, p.harga_jual, p.stok 
            FROM produk p
            LEFT JOIN kategori k ON p.id_kategori = k.id
            LEFT JOIN supplier s ON p.id_supplier = s.id
            WHERE p.id = ?
        """, (id,))
        return result[0] if result else None

    def get_produk_by_kode(self, kode):
        result = self.execute_fetch_query("SELECT * FROM produk WHERE kode_produk = ?", (kode,))
        return result[0] if result else None

    def update_produk(self, id, kode, nama, id_kategori, id_supplier, harga_beli, harga_jual, stok):
        return self.execute_query(
            """UPDATE produk SET kode_produk=?, nama_produk=?, id_kategori=?, id_supplier=?, 
               harga_beli=?, harga_jual=?, stok=? WHERE id=?""",
            (kode, nama, id_kategori, id_supplier, harga_beli, harga_jual, stok, id)
        )

    def delete_produk(self, id):
        return self.execute_query("DELETE FROM produk WHERE id=?", (id,))

    # --- Metode untuk Kategori ---
    def add_kategori(self, nama):
        return self.execute_query("INSERT INTO kategori (nama_kategori) VALUES (?)", (nama,))

    def get_all_kategori(self):
        return self.execute_fetch_query("SELECT id, nama_kategori FROM kategori ORDER BY nama_kategori")

    def get_kategori_by_id(self, id):
        result = self.execute_fetch_query("SELECT id, nama_kategori FROM kategori WHERE id = ?", (id,))
        return result[0] if result else None

    def update_kategori(self, id, nama):
        return self.execute_query("UPDATE kategori SET nama_kategori=? WHERE id=?", (nama, id))

    def delete_kategori(self, id):
        return self.execute_query("DELETE FROM kategori WHERE id=?", (id,))

    # --- Metode untuk Supplier ---
    def add_supplier(self, nama, alamat="", telepon=""):
        return self.execute_query(
            "INSERT INTO supplier (nama_supplier, alamat, telepon) VALUES (?, ?, ?)", 
            (nama, alamat, telepon)
        )

    def get_all_supplier(self):
        return self.execute_fetch_query("SELECT id, nama_supplier, alamat, telepon FROM supplier ORDER BY nama_supplier")

    def get_supplier_by_id(self, id):
        result = self.execute_fetch_query("SELECT id, nama_supplier, alamat, telepon FROM supplier WHERE id = ?", (id,))
        return result[0] if result else None

    def update_supplier(self, id, nama, alamat, telepon):
        return self.execute_query(
            "UPDATE supplier SET nama_supplier=?, alamat=?, telepon=? WHERE id=?", 
            (nama, alamat, telepon, id)
        )

    def delete_supplier(self, id):
        return self.execute_query("DELETE FROM supplier WHERE id=?", (id,))

    # --- Metode untuk Karyawan ---
    def add_karyawan(self, nama, alamat="", telepon=""):
        return self.execute_query(
            "INSERT INTO karyawan (nama_karyawan, alamat, telepon) VALUES (?, ?, ?)", 
            (nama, alamat, telepon)
        )

    def get_all_karyawan(self):
        return self.execute_fetch_query("SELECT id, nama_karyawan, alamat, telepon FROM karyawan ORDER BY nama_karyawan")

    def get_karyawan_by_id(self, id):
        result = self.execute_fetch_query("SELECT id, nama_karyawan, alamat, telepon FROM karyawan WHERE id = ?", (id,))
        return result[0] if result else None

    def update_karyawan(self, id, nama, alamat, telepon):
        return self.execute_query(
            "UPDATE karyawan SET nama_karyawan=?, alamat=?, telepon=? WHERE id=?", 
            (nama, alamat, telepon, id)
        )

    def delete_karyawan(self, id):
        return self.execute_query("DELETE FROM karyawan WHERE id=?", (id,))

    # --- Metode untuk Pengguna (Login) ---
    def add_pengguna(self, username, password, id_karyawan, level="kasir"):
        return self.execute_query(
            "INSERT INTO pengguna (username, password, id_karyawan, level) VALUES (?, ?, ?, ?)",
            (username, password, id_karyawan, level)
        )

    def get_pengguna_by_username(self, username):
        result = self.execute_fetch_query(
            "SELECT p.*, k.nama_karyawan FROM pengguna p JOIN karyawan k ON p.id_karyawan = k.id WHERE username = ?",
            (username,)
        )
        return result[0] if result else None

   # database.py - Perbaiki method verify_login

    def verify_login(self, username, password):
        """Memverifikasi login user"""
        try:
            # Query yang lebih sederhana dan jelas
            result = self.execute_fetch_query(
                """SELECT p.id, p.username, p.password, p.id_karyawan, p.level, 
                    k.nama_karyawan 
                FROM pengguna p 
                LEFT JOIN karyawan k ON p.id_karyawan = k.id 
                WHERE p.username = ? AND p.password = ?""",
                (username, password)
            )
            
            if result:
                # Pastikan result memiliki 6 kolom
                row = result[0]
                if len(row) >= 6:
                    return row
                else:
                    # Jika tidak ada nama karyawan, gunakan username
                    return (row[0], row[1], row[2], row[3], row[4], row[1])  # username sebagai nama
            return None
        except Exception as e:
            print(f"Login error: {e}")
            return None
        
    # database.py - tambahkan method ini
    def verify_login_dict(self, username, password):
        """Memverifikasi login dan return dictionary"""
        try:
            # Query yang lebih aman
            result = self.execute_fetch_query(
                """SELECT 
                    p.id, 
                    p.username, 
                    p.id_karyawan, 
                    p.level,
                    COALESCE(k.nama_karyawan, p.username) as nama
                FROM pengguna p 
                LEFT JOIN karyawan k ON p.id_karyawan = k.id 
                WHERE p.username = ? AND p.password = ?""",
                (username, password)
            )
            
            if result:
                row = result[0]
                return {
                    "id": row[0],
                    "username": row[1],
                    "id_karyawan": row[2],
                    "level": row[3],
                    "nama": row[4]
                }
            return None
        except Exception as e:
            print(f"Login error: {e}")
            return None

    # --- Metode untuk Transaksi Penjualan ---
    def add_transaksi_penjualan(self, id_pelanggan, id_karyawan, total):
        """Menambah transaksi penjualan baru"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            waktu = datetime.now().strftime("%H:%M:%S")
            
            self.cursor.execute(
                """INSERT INTO penjualan (id_pelanggan, id_karyawan, tanggal_penjualan, 
                   waktu_penjualan, total_harga) VALUES (?, ?, ?, ?, ?)""",
                (id_pelanggan, id_karyawan, today, waktu, total)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding penjualan: {e}")
            return None

    def add_detail_penjualan(self, id_penjualan, id_produk, jumlah, harga_satuan):
        """Menambah detail penjualan dan mengurangi stok"""
        try:
            subtotal = jumlah * harga_satuan
            
            # Kurangi stok produk
            if not self.update_stok_produk(id_produk, -jumlah):
                return False
            
            # Tambah detail penjualan
            self.cursor.execute(
                """INSERT INTO detail_penjualan (id_penjualan, id_produk, jumlah, 
                   harga_satuan, subtotal) VALUES (?, ?, ?, ?, ?)""",
                (id_penjualan, id_produk, jumlah, harga_satuan, subtotal)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding detail penjualan: {e}")
            return False

    def get_detail_penjualan_by_id(self, id_penjualan):
        return self.execute_fetch_query("""
            SELECT dp.id, p.id, p.nama_produk, dp.jumlah, dp.harga_satuan, dp.subtotal
            FROM detail_penjualan dp
            JOIN produk p ON dp.id_produk = p.id
            WHERE dp.id_penjualan = ?
        """, (id_penjualan,))
        
    # --- Metode untuk Transaksi Pembelian ---
    def add_transaksi_pembelian(self, id_supplier, id_karyawan, total):
        """Menambah transaksi pembelian baru"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            waktu = datetime.now().strftime("%H:%M:%S")
            
            self.cursor.execute(
                """INSERT INTO pembelian (id_supplier, id_karyawan, tanggal_pembelian, 
                   waktu_pembelian, total_harga) VALUES (?, ?, ?, ?, ?)""",
                (id_supplier, id_karyawan, today, waktu, total)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding pembelian: {e}")
            return None

    def add_detail_pembelian(self, id_pembelian, id_produk, jumlah, harga_satuan):
        """Menambah detail pembelian dan menambah stok"""
        try:
            subtotal = jumlah * harga_satuan
            
            # Tambah stok produk
            if not self.update_stok_produk(id_produk, jumlah):
                return False
            
            # Tambah detail pembelian
            self.cursor.execute(
                """INSERT INTO detail_pembelian (id_pembelian, id_produk, jumlah, 
                   harga_satuan, subtotal) VALUES (?, ?, ?, ?, ?)""",
                (id_pembelian, id_produk, jumlah, harga_satuan, subtotal)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding detail pembelian: {e}")
            return False

    # --- Metode untuk Retur Penjualan ---
    def add_transaksi_retur_penjualan(self, id_penjualan, id_pelanggan, id_karyawan, total, alasan=""):
        """Menambah transaksi retur penjualan"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            waktu = datetime.now().strftime("%H:%M:%S")
            
            self.cursor.execute(
                """INSERT INTO retur_penjualan (id_penjualan, id_pelanggan, id_karyawan, 
                   tanggal_retur, waktu_retur, total_retur, alasan_retur) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (id_penjualan, id_pelanggan, id_karyawan, today, waktu, total, alasan)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding retur penjualan: {e}")
            return None
    
    def add_detail_retur_penjualan(self, id_retur, id_produk, qty, harga):
        """Menambah detail retur penjualan dan menambah stok kembali"""
        try:
            subtotal = qty * harga
            
            # Tambah stok produk kembali
            if not self.update_stok_produk(id_produk, qty):
                return False
            
            # Tambah detail retur
            self.cursor.execute(
                """INSERT INTO detail_retur_penjualan (id_retur, id_produk, qty, 
                   harga, subtotal) VALUES (?, ?, ?, ?, ?)""",
                (id_retur, id_produk, qty, harga, subtotal)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding detail retur: {e}")
            return False

    # --- Metode untuk Stok ---
    def get_produk_stok(self, produk_id):
        """Mendapatkan stok produk berdasarkan ID"""
        result = self.execute_fetch_query("SELECT stok FROM produk WHERE id = ?", (produk_id,))
        return result[0][0] if result else 0

    def check_stok_cukup(self, produk_id, qty_dibutuhkan):
        """Memeriksa apakah stok mencukupi"""
        stok_tersedia = self.get_produk_stok(produk_id)
        return stok_tersedia >= qty_dibutuhkan, stok_tersedia

    def update_stok_produk(self, produk_id, perubahan):
        """Update stok produk (bisa positif untuk tambah, negatif untuk kurang)"""
        try:
            self.cursor.execute(
                "UPDATE produk SET stok = stok + ? WHERE id = ?",
                (perubahan, produk_id)
            )
            self.conn.commit()
            
            # Verifikasi stok tidak negatif
            self.cursor.execute("SELECT stok FROM produk WHERE id = ?", (produk_id,))
            stok_sekarang = self.cursor.fetchone()[0]
            
            if stok_sekarang < 0:
                # Rollback jika stok negatif
                self.cursor.execute(
                    "UPDATE produk SET stok = stok - ? WHERE id = ?",
                    (perubahan, produk_id)
                )
                self.conn.commit()
                return False
                
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False

    def get_produk_dengan_stok_rendah(self, batas=5):
        """Mendapatkan produk dengan stok di bawah batas tertentu"""
        return self.execute_fetch_query("""
            SELECT p.id, p.kode_produk, p.nama_produk, p.stok, 
                   k.nama_kategori, p.harga_jual
            FROM produk p
            LEFT JOIN kategori k ON p.id_kategori = k.id
            WHERE p.stok <= ?
            ORDER BY p.stok ASC
        """, (batas,))

    # --- Metode untuk Laporan ---
    def get_laporan_penjualan(self, tanggal_awal=None, tanggal_akhir=None):
        """Mendapatkan laporan penjualan dengan filter tanggal"""
        query = """
            SELECT p.id, p.tanggal_penjualan, p.waktu_penjualan, 
                   pel.nama_pelanggan, kar.nama_karyawan, p.total_harga
            FROM penjualan p
            JOIN pelanggan pel ON p.id_pelanggan = pel.id
            JOIN karyawan kar ON p.id_karyawan = kar.id
        """
        
        params = []
        if tanggal_awal and tanggal_akhir:
            query += " WHERE p.tanggal_penjualan BETWEEN ? AND ?"
            params.extend([tanggal_awal, tanggal_akhir])
        
        query += " ORDER BY p.tanggal_penjualan DESC, p.waktu_penjualan DESC"
        
        return self.execute_fetch_query(query, tuple(params))

    def get_laporan_pembelian(self, tanggal_awal=None, tanggal_akhir=None):
        """Mendapatkan laporan pembelian dengan filter tanggal"""
        query = """
            SELECT pb.id, pb.tanggal_pembelian, pb.waktu_pembelian,
                   s.nama_supplier, k.nama_karyawan, pb.total_harga
            FROM pembelian pb
            JOIN supplier s ON pb.id_supplier = s.id
            JOIN karyawan k ON pb.id_karyawan = k.id
        """
        
        params = []
        if tanggal_awal and tanggal_akhir:
            query += " WHERE pb.tanggal_pembelian BETWEEN ? AND ?"
            params.extend([tanggal_awal, tanggal_akhir])
        
        query += " ORDER BY pb.tanggal_pembelian DESC, pb.waktu_pembelian DESC"
        
        return self.execute_fetch_query(query, tuple(params))

    def get_laporan_stok(self):
        """Mendapatkan laporan stok semua produk"""
        return self.execute_fetch_query("""
            SELECT p.kode_produk, p.nama_produk, k.nama_kategori,
                   s.nama_supplier, p.harga_beli, p.harga_jual, p.stok,
                   (p.stok * p.harga_jual) as nilai_stok
            FROM produk p
            LEFT JOIN kategori k ON p.id_kategori = k.id
            LEFT JOIN supplier s ON p.id_supplier = s.id
            ORDER BY p.nama_produk
        """)

    def get_ringkasan_penjualan_harian(self, tanggal=None):
        """Mendapatkan ringkasan penjualan harian"""
        if not tanggal:
            tanggal = datetime.now().strftime("%Y-%m-%d")
        
        return self.execute_fetch_query("""
            SELECT 
                COUNT(*) as jumlah_transaksi,
                SUM(total_harga) as total_penjualan,
                AVG(total_harga) as rata_rata_transaksi
            FROM penjualan
            WHERE tanggal_penjualan = ?
        """, (tanggal,))

    def get_produk_terlaris(self, limit=10):
        """Mendapatkan produk terlaris berdasarkan jumlah penjualan"""
        return self.execute_fetch_query("""
            SELECT 
                p.nama_produk,
                SUM(dp.jumlah) as total_terjual,
                SUM(dp.subtotal) as total_pendapatan
            FROM detail_penjualan dp
            JOIN produk p ON dp.id_produk = p.id
            GROUP BY dp.id_produk
            ORDER BY total_terjual DESC
            LIMIT ?
        """, (limit,))

    # --- Metode Utility ---
    def get_total_pelanggan(self):
        result = self.execute_fetch_query("SELECT COUNT(*) FROM pelanggan")
        return result[0][0] if result else 0

    def get_total_produk(self):
        result = self.execute_fetch_query("SELECT COUNT(*) FROM produk")
        return result[0][0] if result else 0

    def get_total_stok(self):
        result = self.execute_fetch_query("SELECT SUM(stok) FROM produk")
        return result[0][0] if result else 0

    def get_total_penjualan_hari_ini(self):
        today = datetime.now().strftime("%Y-%m-%d")
        result = self.execute_fetch_query(
            "SELECT SUM(total_harga) FROM penjualan WHERE tanggal_penjualan = ?", 
            (today,)
        )
        return result[0][0] if result and result[0][0] else 0

    def backup_database(self, backup_path):
        """Membuat backup database"""
        try:
            import shutil
            shutil.copy2("toko.db", backup_path)
            return True
        except Exception as e:
            print(f"Backup error: {e}")
            return False

    def close(self):
        """Menutup koneksi database"""
        try:
            self.conn.close()
        except:
            pass
