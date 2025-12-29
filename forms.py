# forms.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime 

# --- Konsep Inheritansi dan Polimorfisme ---
# Kelas induk untuk semua form Data Master
class BaseMasterForm(tk.Toplevel):
    def __init__(self, parent, db, title):
        super().__init__(parent)
        self.db = db
        self.title(title)
        self.geometry("800x500")
        self.create_widgets()
        self.populate_treeview()

    def create_widgets(self):
        # Frame untuk input
        self.input_frame = ttk.LabelFrame(self, text="Input Data")
        self.input_frame.pack(pady=10, padx=10, fill="x")

        # Entri data akan dibuat di kelas anak (Polimorfisme)
        self.entries = {}
        self.create_input_fields()

        # Frame untuk tombol
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=5)

        ttk.Button(self.button_frame, text="Tambah", command=self.add_data).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Ubah", command=self.update_data).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Hapus", command=self.delete_data).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Clear", command=self.clear_form).pack(side="left", padx=5)

        # Frame untuk Treeview
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview akan dibuat di kelas anak (Polimorfisme)
        self.tree = self.create_treeview()
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

    # Metode abstrak (akan dioverride di kelas anak)
    def create_input_fields(self):
        raise NotImplementedError

    def create_treeview(self):
        raise NotImplementedError

    def get_form_data(self):
        raise NotImplementedError

    def clear_form(self):
        raise NotImplementedError

    def populate_treeview(self):
        raise NotImplementedError

    # Logika umum untuk CRUD
    def add_data(self):
        data = self.get_form_data()
        if not data:
            return
        try:
            self.insert_data(data)
            self.populate_treeview()
            self.clear_form()
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan data: {e}")

    def update_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diubah!")
            return
        item_id = self.tree.item(selected_item[0])['values'][0]
        data = self.get_form_data()
        if not data:
            return
        try:
            self.update_data_in_db(item_id, data)
            self.populate_treeview()
            self.clear_form()
            messagebox.showinfo("Sukses", "Data berhasil diubah!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengubah data: {e}")

    def delete_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?"):
            item_id = self.tree.item(selected_item[0])['values'][0]
            try:
                self.delete_data_from_db(item_id)
                self.populate_treeview()
                self.clear_form()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def on_item_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        values = self.tree.item(selected_item[0])['values']
        self.fill_form_from_selection(values)

    # Metode CRUD abstrak
    def insert_data(self, data):
        raise NotImplementedError
    def update_data_in_db(self, item_id, data):
        raise NotImplementedError
    def delete_data_from_db(self, item_id):
        raise NotImplementedError
    def fill_form_from_selection(self, values):
        raise NotImplementedError


# --- Kelas Anak (Implementasi Polimorfisme) ---
class PelangganForm(BaseMasterForm):
    def __init__(self, parent, db):
        super().__init__(parent, db, "Master Pelanggan")

    def create_input_fields(self):
        ttk.Label(self.input_frame, text="Nama Pelanggan:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entries['nama'] = ttk.Entry(self.input_frame, width=40)
        self.entries['nama'].grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Alamat:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entries['alamat'] = ttk.Entry(self.input_frame, width=40)
        self.entries['alamat'].grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Telepon:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entries['telepon'] = ttk.Entry(self.input_frame, width=40)
        self.entries['telepon'].grid(row=2, column=1, padx=5, pady=5)

    def create_treeview(self):
        columns = ('id', 'nama', 'alamat', 'telepon')
        tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        tree.heading('id', text='ID')
        tree.heading('nama', text='Nama Pelanggan')
        tree.heading('alamat', text='Alamat')
        tree.heading('telepon', text='Telepon')
        tree.column('id', width=40, anchor='center')
        tree.column('nama', width=150)
        tree.column('alamat', width=200)
        tree.column('telepon', width=120)
        return tree

    def get_form_data(self):
        nama = self.entries['nama'].get()
        if not nama:
            messagebox.showwarning("Peringatan", "Nama pelanggan harus diisi!")
            return None
        return {
            'nama': nama,
            'alamat': self.entries['alamat'].get(),
            'telepon': self.entries['telepon'].get()
        }

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def populate_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_all_pelanggan():
            self.tree.insert('', 'end', values=row)

    def insert_data(self, data):
        self.db.add_pelanggan(data['nama'], data['alamat'], data['telepon'])
    
    def update_data_in_db(self, item_id, data):
        self.db.update_pelanggan(item_id, data['nama'], data['alamat'], data['telepon'])

    def delete_data_from_db(self, item_id):
        self.db.delete_pelanggan(item_id)

    def fill_form_from_selection(self, values):
        self.clear_form()
        self.entries['nama'].insert(0, values[1])
        self.entries['alamat'].insert(0, values[2])
        self.entries['telepon'].insert(0, values[3])

class KategoriForm(BaseMasterForm):
    def __init__(self, parent, db):
        super().__init__(parent, db, "Master Kategori")

    def create_input_fields(self):
        ttk.Label(self.input_frame, text="Nama Kategori:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entries['nama_kategori'] = ttk.Entry(self.input_frame, width=40)
        self.entries['nama_kategori'].grid(row=0, column=1, padx=5, pady=5)

    def create_treeview(self):
        columns = ('id', 'nama_kategori')
        tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        tree.heading('id', text='ID')
        tree.heading('nama_kategori', text='Nama Kategori')
        tree.column('id', width=40, anchor='center')
        tree.column('nama_kategori', width=200)
        return tree

    def get_form_data(self):
        nama = self.entries['nama_kategori'].get()
        if not nama:
            messagebox.showwarning("Peringatan", "Nama kategori harus diisi!")
            return None
        return {'nama_kategori': nama}

    def clear_form(self):
        self.entries['nama_kategori'].delete(0, tk.END)

    def populate_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_all_kategori():
            self.tree.insert('', 'end', values=row)

    def insert_data(self, data):
        self.db.add_kategori(data['nama_kategori'])
    
    def update_data_in_db(self, item_id, data):
        self.db.update_kategori(item_id, data['nama_kategori'])

    def delete_data_from_db(self, item_id):
        self.db.delete_kategori(item_id)

    def fill_form_from_selection(self, values):
        self.clear_form()
        self.entries['nama_kategori'].insert(0, values[1])

class SupplierForm(BaseMasterForm):
    def __init__(self, parent, db):
        super().__init__(parent, db, "Master Supplier")

    def create_input_fields(self):
        ttk.Label(self.input_frame, text="Nama Supplier:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entries['nama'] = ttk.Entry(self.input_frame, width=40)
        self.entries['nama'].grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Alamat:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entries['alamat'] = ttk.Entry(self.input_frame, width=40)
        self.entries['alamat'].grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Telepon:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entries['telepon'] = ttk.Entry(self.input_frame, width=40)
        self.entries['telepon'].grid(row=2, column=1, padx=5, pady=5)

    def create_treeview(self):
        columns = ('id', 'nama', 'alamat', 'telepon')
        tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        tree.heading('id', text='ID')
        tree.heading('nama', text='Nama Supplier')
        tree.heading('alamat', text='Alamat')
        tree.heading('telepon', text='Telepon')
        tree.column('id', width=40, anchor='center')
        tree.column('nama', width=150)
        tree.column('alamat', width=200)
        tree.column('telepon', width=120)
        return tree

    def get_form_data(self):
        nama = self.entries['nama'].get()
        if not nama:
            messagebox.showwarning("Peringatan", "Nama supplier harus diisi!")
            return None
        return {
            'nama': nama,
            'alamat': self.entries['alamat'].get(),
            'telepon': self.entries['telepon'].get()
        }

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def populate_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_all_supplier():
            self.tree.insert('', 'end', values=row)

    def insert_data(self, data):
        self.db.add_supplier(data['nama'], data['alamat'], data['telepon'])
    
    def update_data_in_db(self, item_id, data):
        self.db.update_supplier(item_id, data['nama'], data['alamat'], data['telepon'])

    def delete_data_from_db(self, item_id):
        self.db.delete_supplier(item_id)

    def fill_form_from_selection(self, values):
        self.clear_form()
        self.entries['nama'].insert(0, values[1])
        self.entries['alamat'].insert(0, values[2])
        self.entries['telepon'].insert(0, values[3])

class KaryawanForm(BaseMasterForm):
    def __init__(self, parent, db):
        super().__init__(parent, db, "Master Karyawan")

    def create_input_fields(self):
        ttk.Label(self.input_frame, text="Nama Karyawan:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entries['nama'] = ttk.Entry(self.input_frame, width=40)
        self.entries['nama'].grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Alamat:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entries['alamat'] = ttk.Entry(self.input_frame, width=40)
        self.entries['alamat'].grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Telepon:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entries['telepon'] = ttk.Entry(self.input_frame, width=40)
        self.entries['telepon'].grid(row=2, column=1, padx=5, pady=5)

    def create_treeview(self):
        columns = ('id', 'nama', 'alamat', 'telepon')
        tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        tree.heading('id', text='ID')
        tree.heading('nama', text='Nama Karyawan')
        tree.heading('alamat', text='Alamat')
        tree.heading('telepon', text='Telepon')
        tree.column('id', width=40, anchor='center')
        tree.column('nama', width=150)
        tree.column('alamat', width=200)
        tree.column('telepon', width=120)
        return tree

    def get_form_data(self):
        nama = self.entries['nama'].get()
        if not nama:
            messagebox.showwarning("Peringatan", "Nama karyawan harus diisi!")
            return None
        return {
            'nama': nama,
            'alamat': self.entries['alamat'].get(),
            'telepon': self.entries['telepon'].get()
        }

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def populate_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_all_karyawan():
            self.tree.insert('', 'end', values=row)

    def insert_data(self, data):
        self.db.add_karyawan(data['nama'], data['alamat'], data['telepon'])
    
    def update_data_in_db(self, item_id, data):
        self.db.update_karyawan(item_id, data['nama'], data['alamat'], data['telepon'])

    def delete_data_from_db(self, item_id):
        self.db.delete_karyawan(item_id)

    def fill_form_from_selection(self, values):
        self.clear_form()
        self.entries['nama'].insert(0, values[1])
        self.entries['alamat'].insert(0, values[2])
        self.entries['telepon'].insert(0, values[3])

# ProdukForm yang sudah diperbaiki
# forms.py

# ... (kode sebelumnya tidak berubah) ...

class ProdukForm(BaseMasterForm):
    def __init__(self, parent, db):
        # --- PERBAIKAN: Inisialisasi peta (map) dengan penanganan jika data kosong ---
        # Ambil data dari database
        all_kategori = db.get_all_kategori()
        all_supplier = db.get_all_supplier()

        # Buat peta (map) hanya jika data ada, jika tidak, gunakan dictionary kosong
        if all_kategori:
            self.kategori_map = {str(k[1]): k[0] for k in all_kategori}
        else:
            self.kategori_map = {}
            
        if all_supplier:
            self.supplier_map = {str(s[1]): s[0] for s in all_supplier}
        else:
            self.supplier_map = {}
        
        super().__init__(parent, db, "Master Produk")

    def create_input_fields(self):
        ttk.Label(self.input_frame, text="Kode Produk:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entries['kode'] = ttk.Entry(self.input_frame, width=40)
        self.entries['kode'].grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Nama Produk:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entries['nama'] = ttk.Entry(self.input_frame, width=40)
        self.entries['nama'].grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Kategori:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entries['kategori'] = ttk.Combobox(self.input_frame, values=list(self.kategori_map.keys()), width=38)
        self.entries['kategori'].grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Supplier:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entries['supplier'] = ttk.Combobox(self.input_frame, values=list(self.supplier_map.keys()), width=38)
        self.entries['supplier'].grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Harga Beli:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entries['harga_beli'] = ttk.Entry(self.input_frame, width=40)
        self.entries['harga_beli'].grid(row=4, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Harga Jual:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entries['harga_jual'] = ttk.Entry(self.input_frame, width=40)
        self.entries['harga_jual'].grid(row=5, column=1, padx=5, pady=5)
        ttk.Label(self.input_frame, text="Stok:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entries['stok'] = ttk.Entry(self.input_frame, width=40)
        self.entries['stok'].grid(row=6, column=1, padx=5, pady=5)

    def create_treeview(self):
        columns = ('id', 'kode', 'nama', 'kategori', 'supplier','harga_beli', 'harga_jual', 'stok')
        tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col.replace('_', ' ').title())
        tree.column('id', width=40, anchor='center')
        return tree

    def get_form_data(self):
        if not self.entries['kode'].get() or not self.entries['nama'].get():
            messagebox.showwarning("Peringatan", "Kode dan Nama Produk harus diisi!")
            return None
        try:
            return {
                'kode': self.entries['kode'].get(),
                'nama': self.entries['nama'].get(),
                'id_kategori': self.kategori_map.get(self.entries['kategori'].get()),
                'id_supplier': self.supplier_map.get(self.entries['supplier'].get()),
                'harga_beli': float(self.entries['harga_beli'].get() or 0),
                'harga_jual': float(self.entries['harga_jual'].get() or 0),
                'stok': int(self.entries['stok'].get() or 0)
            }
        except ValueError:
            messagebox.showerror("Error", "Harga dan stok harus berupa angka!")
            return None

    def clear_form(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, ttk.Combobox):
                entry.set('')

    def populate_treeview(self):
        # --- REFRESH KATEGORI & SUPPLIER ---
        all_kategori = self.db.get_all_kategori()
        all_supplier = self.db.get_all_supplier()

        self.kategori_map = {str(k[1]): k[0] for k in all_kategori} if all_kategori else {}
        self.supplier_map = {str(s[1]): s[0] for s in all_supplier} if all_supplier else {}

        # Update combobox values
        self.entries['kategori']['values'] = list(self.kategori_map.keys())
        self.entries['supplier']['values'] = list(self.supplier_map.keys())

        # --- REFRESH TREEVIEW ---
        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in self.db.get_all_produk():
            self.tree.insert('', 'end', values=row)


    def insert_data(self, data):
        self.db.add_produk(data['kode'], data['nama'], data['id_kategori'], data['id_supplier'], data['harga_beli'], data['harga_jual'], data['stok'])
    
    def update_data_in_db(self, item_id, data):
        self.db.update_produk(item_id, data['kode'], data['nama'], data['id_kategori'], data['id_supplier'], data['harga_beli'], data['harga_jual'], data['stok'])

    def delete_data_from_db(self, item_id):
        self.db.delete_produk(item_id)

    def fill_form_from_selection(self, values):
        self.clear_form()
        self.entries['kode'].insert(0, values[1])
        self.entries['nama'].insert(0, values[2])
        self.entries['kategori'].set(values[3])
        self.entries['supplier'].set(values[4])
        self.entries['harga_beli'].insert(0, values[5])   # ⬅ TAMBAHAN
        self.entries['harga_jual'].insert(0, values[6])   # ⬅ INDEX BERGESER
        self.entries['stok'].insert(0, values[7])

class PenjualanForm(tk.Toplevel):
    def __init__(self, parent, db, current_user):
        super().__init__(parent)
        self.db = db
        self.current_user = current_user

        self.title("Transaksi Penjualan")
        self.geometry("900x600")
        
        # Mapping pelanggan: "ID - Nama" -> ID
        self.pelanggan_map = {f"{p[0]} - {p[1]}": p[0] for p in self.db.get_all_pelanggan()}
 
        self.transaksi_items = []
        self.produk_map = {}
        self.produk_data = []
        self.selected_product_id = None
        
        style = ttk.Style(self)
        style.theme_use("default")   # paksa theme netral

        style.configure(
            "Treeview",
            foreground="black",
            background="white",
            fieldbackground="white"
        )

        style.map(
            "Treeview",
            background=[("selected", "#cce5ff")],
            foreground=[("selected", "black")]
        )

        self.create_widgets()
        self.refresh_produk_map()
        self.create_stok_window()
        
    def create_stok_window(self):
        """Membuat jendela kecil untuk menampilkan stok"""
        self.stok_window = tk.Toplevel(self)
        self.stok_window.title("Info Stok")
        self.stok_window.geometry("300x200")
        self.stok_window.withdraw()  # Sembunyikan awalnya
        
        # Frame untuk info stok
        stok_frame = ttk.LabelFrame(self.stok_window, text="Informasi Stok")
        stok_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.stok_label = ttk.Label(stok_frame, text="Pilih produk untuk melihat stok", font=("Arial", 10))
        self.stok_label.pack(pady=10)
        
        ttk.Label(stok_frame, text="Stok Tersedia:").pack(pady=5)
        self.stok_value_label = ttk.Label(stok_frame, text="0", font=("Arial", 14, "bold"), foreground="blue")
        self.stok_value_label.pack(pady=5)
        
        ttk.Label(stok_frame, text="Harga Jual:").pack(pady=5)
        self.harga_value_label = ttk.Label(stok_frame, text="Rp 0", font=("Arial", 12))
        self.harga_value_label.pack(pady=5)
        
        ttk.Button(stok_frame, text="Tutup", command=self.stok_window.withdraw).pack(pady=10)

    def refresh_produk_map(self):
        all_produk = self.db.get_all_produk()
        self.produk_data = all_produk  # Simpan data lengkap untuk referensi

        # Key = nama produk
        self.produk_map = {
            row[2]: {       # row[2] = nama_produk
                'id': row[0],
                'nama': row[2],
                'harga': row[6],  # harga_jual
                'stok': row[7]
            }
            for row in all_produk
        }

        # Combobox menampilkan nama produk saja
        self.produk_cb['values'] = [row[2] for row in all_produk] if hasattr(self, 'produk_cb') else []
        
        # Update treeview stok jika sudah dibuat
        if hasattr(self, 'stok_tree'):
            self.update_stok_treeview()

    def update_stok_treeview(self):
        """Update treeview untuk menampilkan stok produk"""
        # Hapus data lama
        for item in self.stok_tree.get_children():
            self.stok_tree.delete(item)
        
        # Tambah data baru
        for row in self.produk_data:
            produk_id = row[0]
            kode = row[1]
            nama = row[2]
            kategori = row[3]
            stok = row[7]
            
            # Tentukan warna teks berdasarkan stok
            tags = ('stok_rendah',) if stok <= 5 else ()
            
            self.stok_tree.insert('', 'end', values=(kode, nama, kategori, stok), tags=tags)

    def create_widgets(self):
        # Frame utama dengan 2 kolom
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Kolom kiri: Form transaksi
        left_frame = ttk.LabelFrame(main_frame, text="Form Transaksi")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Kolom kanan: Info stok
        right_frame = ttk.LabelFrame(main_frame, text="Daftar Stok Produk")
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # --- KOLOM KIRI: FORM TRANSAKSI ---
        # Header Transaksi
        header_frame = ttk.LabelFrame(left_frame, text="Detail Transaksi")
        header_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(header_frame, text="Tanggal:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        from datetime import date
        self.tanggal_label = ttk.Label(header_frame, text=date.today().strftime("%Y-%m-%d"))
        self.tanggal_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(header_frame, text="Kasir:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.kasir_label = ttk.Label(header_frame, text=self.current_user["nama"])
        self.kasir_label.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(header_frame, text="Pelanggan:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.pelanggan_cb = ttk.Combobox(header_frame, values=list(self.pelanggan_map.keys()), width=40)
        self.pelanggan_cb.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="ew")
        self.pelanggan_cb.set("1 - Umum" if "1 - Umum" in self.pelanggan_map else list(self.pelanggan_map.keys())[0] if self.pelanggan_map else "")

        # Input Item
        item_frame = ttk.LabelFrame(left_frame, text="Tambah Item")
        item_frame.pack(pady=10, padx=10, fill="x")

        # Baris 1: Produk dan tombol lihat stok
        ttk.Label(item_frame, text="Produk:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.produk_cb = ttk.Combobox(item_frame, values=[], width=30)
        self.produk_cb.grid(row=0, column=1, padx=5, pady=5)
        self.produk_cb.bind("<<ComboboxSelected>>", self.on_produk_select)
        self.produk_cb.bind("<KeyRelease>", self.on_produk_search)
        
        # Tombol lihat stok
        ttk.Button(item_frame, text="Lihat Stok", command=self.show_stok_info, 
                  width=10).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(item_frame, text="Qty:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.qty_entry = ttk.Entry(item_frame, width=15)
        self.qty_entry.grid(row=1, column=1, padx=5, pady=5)
        self.qty_entry.insert(0, "1")  # Default qty = 1
        
        # Label info stok tersedia
        self.stok_info_label = ttk.Label(item_frame, text="Stok tersedia: -", foreground="blue")
        self.stok_info_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        ttk.Label(item_frame, text="Harga:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.harga_entry = ttk.Entry(item_frame, width=15)
        self.harga_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.subtotal_label = ttk.Label(item_frame, text="Subtotal: Rp 0", font=("Arial", 10, "bold"))
        self.subtotal_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        ttk.Button(item_frame, text="Tambah ke Keranjang", command=self.add_to_cart,
                  style="Accent.TButton").grid(row=3, column=0, columnspan=3, pady=10)

        # Daftar Item (Treeview)
        list_frame = ttk.LabelFrame(left_frame, text="Keranjang Belanja")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Scrollbar untuk treeview
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ('no', 'nama', 'qty', 'harga', 'subtotal')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', 
                                yscrollcommand=scrollbar.set, height=8)
        scrollbar.config(command=self.tree.yview)
        
        # Konfigurasi kolom
        self.tree.heading('no', text='No')
        self.tree.heading('nama', text='Nama Produk')
        self.tree.heading('qty', text='Qty')
        self.tree.heading('harga', text='Harga')
        self.tree.heading('subtotal', text='Subtotal')
        
        self.tree.column('no', width=40, anchor='center')
        self.tree.column('nama', width=150)
        self.tree.column('qty', width=60, anchor='center')
        self.tree.column('harga', width=100, anchor='e')
        self.tree.column('subtotal', width=120, anchor='e')
        
        self.tree.pack(fill="both", expand=True)
        
        # Tombol hapus item
        ttk.Button(list_frame, text="Hapus Item Terpilih", 
                  command=self.remove_selected_item).pack(pady=5)
        
        # Total dan tombol aksi
        bottom_frame = ttk.Frame(left_frame)
        bottom_frame.pack(pady=10, padx=10, fill="x")
        
        self.total_label = ttk.Label(bottom_frame, text="Total: Rp 0", 
                                    font=("Arial", 14, "bold"), foreground="green")
        self.total_label.pack(side="left", padx=10)
        
        action_frame = ttk.Frame(bottom_frame)
        action_frame.pack(side="right")
        
        ttk.Button(action_frame, text="Simpan Transaksi", 
                  command=self.save_transaction, style="Success.TButton").pack(side="left", padx=5)
        ttk.Button(action_frame, text="Batal", 
                  command=self.destroy).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Clear", 
                  command=self.clear_cart).pack(side="left", padx=5)
        
        # --- KOLOM KANAN: INFO STOK ---
        # Treeview untuk stok
        columns_stok = ('kode', 'nama', 'kategori', 'stok')
        self.stok_tree = ttk.Treeview(right_frame, columns=columns_stok, show='headings', height=15)
        
        self.stok_tree.heading('kode', text='Kode')
        self.stok_tree.heading('nama', text='Nama Produk')
        self.stok_tree.heading('kategori', text='Kategori')
        self.stok_tree.heading('stok', text='Stok')
        
        self.stok_tree.column('kode', width=80)
        self.stok_tree.column('nama', width=150)
        self.stok_tree.column('kategori', width=100)
        self.stok_tree.column('stok', width=60, anchor='center')
        
        self.stok_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Konfigurasi tag untuk stok rendah
        self.stok_tree.tag_configure('stok_rendah', foreground='red')
        
        # Tombol refresh stok
        ttk.Button(right_frame, text="Refresh Stok", 
                  command=self.refresh_produk_map).pack(pady=5)
        
        # Styling
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))
        style.configure("Success.TButton", font=("Arial", 10, "bold"), foreground="white", background="green")
        
        # Update treeview stok dengan data awal
        self.update_stok_treeview()
        
    def on_produk_search(self, event):
        """Filter produk berdasarkan input pencarian"""
        search_term = self.produk_cb.get().lower()
        filtered_products = [p[2] for p in self.produk_data if search_term in p[2].lower()]
        self.produk_cb['values'] = filtered_products
    
    def on_produk_select(self, event):
        selected_nama = self.produk_cb.get()
        if not selected_nama or selected_nama not in self.produk_map:
            return

        produk = self.produk_map[selected_nama]
        self.selected_product_id = produk['id']
        
        harga = produk['harga']
        self.harga_entry.delete(0, tk.END)
        self.harga_entry.insert(0, str(harga))
        
        # Update info stok
        stok = produk['stok']
        self.stok_info_label.config(text=f"Stok tersedia: {stok}")
        
        # Update warna info stok
        if stok <= 5:
            self.stok_info_label.config(foreground="red")
        elif stok <= 10:
            self.stok_info_label.config(foreground="orange")
        else:
            self.stok_info_label.config(foreground="blue")
        
        # Hitung subtotal awal
        self.calculate_subtotal()
        
        # Tampilkan info stok di jendela terpisah
        self.update_stok_window_info(produk)
    
    def update_stok_window_info(self, produk_info):
        """Update info di jendela stok"""
        if hasattr(self, 'stok_window'):
            self.stok_label.config(text=f"Produk: {produk_info['nama']}")
            self.stok_value_label.config(text=str(produk_info['stok']))
            self.harga_value_label.config(text=f"Rp {produk_info['harga']:,.2f}")
            
            # Tentukan warna berdasarkan stok
            if produk_info['stok'] <= 5:
                self.stok_value_label.config(foreground="red")
            elif produk_info['stok'] <= 10:
                self.stok_value_label.config(foreground="orange")
            else:
                self.stok_value_label.config(foreground="blue")
    
    def show_stok_info(self):
        """Tampilkan jendela info stok"""
        if self.selected_product_id:
            self.stok_window.deiconify()  # Tampilkan jendela
            self.stok_window.lift()  # Bawa ke depan
        else:
            messagebox.showinfo("Info", "Pilih produk terlebih dahulu!")
    
    def calculate_subtotal(self):
        """Hitung subtotal berdasarkan qty dan harga"""
        try:
            qty = int(self.qty_entry.get() or 1)
            harga = float(self.harga_entry.get() or 0)
            subtotal = qty * harga
            self.subtotal_label.config(text=f"Subtotal: Rp {subtotal:,.2f}")
        except ValueError:
            self.subtotal_label.config(text="Subtotal: Rp 0")
    
    def add_to_cart(self):
        produk_nama = self.produk_cb.get()
        qty_str = self.qty_entry.get()
        harga_str = self.harga_entry.get()
        
        if not all([produk_nama, qty_str]):
            messagebox.showwarning("Peringatan", "Lengkapi data item!")
            return

        if produk_nama not in self.produk_map:
            messagebox.showwarning("Peringatan", "Produk tidak valid!")
            return

        try:
            qty = int(qty_str)
            produk = self.produk_map[produk_nama]
            id_produk = produk['id']
            harga = produk['harga']
            stok = produk['stok']

            # VALIDASI STOK: Periksa apakah stok mencukupi
            if qty <= 0:
                messagebox.showwarning("Peringatan", "Jumlah harus lebih dari 0!")
                return
            
            if qty > stok:
                messagebox.showwarning(
                    "Stok Tidak Cukup", 
                    f"Stok produk '{produk_nama}' tidak mencukupi!\n"
                    f"Stok tersedia: {stok}\n"
                    f"Jumlah diminta: {qty}"
                )
                return

            # Cek apakah produk sudah ada di keranjang
            item_found = None
            for item in self.transaksi_items:
                if item['id_produk'] == id_produk:
                    item_found = item
                    break
            
            if item_found:
                # Tanyakan apakah ingin menggabungkan atau membuat baru
                response = messagebox.askyesno(
                    "Produk Sudah Ada",
                    f"Produk '{produk_nama}' sudah ada di keranjang.\n"
                    f"Apakah ingin menambah jumlahnya?"
                )
                if response:
                    # Validasi stok untuk penambahan
                    new_total_qty = item_found['qty'] + qty
                    if new_total_qty > stok:
                        messagebox.showwarning(
                            "Stok Tidak Cukup",
                            f"Stok tidak mencukupi untuk penambahan!\n"
                            f"Stok tersedia: {stok}\n"
                            f"Jumlah di keranjang: {item_found['qty']}\n"
                            f"Jumlah tambahan: {qty}\n"
                            f"Total menjadi: {new_total_qty}"
                        )
                        return
                    
                    # Update jumlah di keranjang
                    item_found['qty'] = new_total_qty
                    
                    # Update treeview
                    for child in self.tree.get_children():
                        values = self.tree.item(child)['values']
                        if values[1] == produk_nama:
                            new_subtotal = new_total_qty * harga
                            self.tree.item(child, values=(
                                values[0], values[1], new_total_qty, 
                                f"Rp {harga:,.2f}", f"Rp {new_subtotal:,.2f}"
                            ))
                            break
                    
                    self.update_total()
                    self.clear_item_form()
                    return
                # Jika tidak ingin menggabungkan, lanjutkan menambah item baru

            # Jika produk belum ada atau tidak ingin digabungkan
            subtotal = qty * harga
            
            # Nomor urut
            item_no = len(self.transaksi_items) + 1
            
            # Tambah ke treeview
            self.tree.insert('', 'end', values=(
                item_no, 
                produk_nama, 
                qty, 
                f"Rp {harga:,.2f}", 
                f"Rp {subtotal:,.2f}"
            ))
            
            # Tambah ke list transaksi
            self.transaksi_items.append({
                'id_produk': id_produk,
                'qty': qty,
                'harga': harga
            })

            self.update_total()
            
            # Kurangi stok di tampilan (hanya tampilan)
            produk['stok'] -= qty
            self.stok_info_label.config(text=f"Stok tersedia: {produk['stok']}")
            
            # Update harga entry jika kosong
            if not harga_str:
                self.harga_entry.delete(0, tk.END)
                self.harga_entry.insert(0, str(harga))

            self.produk_cb.set('')
            self.qty_entry.delete(0, tk.END)
            self.qty_entry.insert(0, "1")
            self.harga_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Qty harus berupa angka!")
    
    def remove_selected_item(self):
        """Menghapus item terpilih dari keranjang"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Peringatan", "Pilih item yang akan dihapus!")
            return
        
        for item in selected_items:
            values = self.tree.item(item)['values']
            produk_nama = values[1]
            qty = int(values[2])
            
            # Hapus dari treeview
            self.tree.delete(item)
            
            # Hapus dari list transaksi
            # PERBAIKAN: Syntax list comprehension yang benar
            self.transaksi_items = [
                i for i in self.transaksi_items 
                if not (
                    produk_nama in self.produk_map and 
                    i['id_produk'] == self.produk_map[produk_nama]['id']
                )
            ]
            
            # Kembalikan stok di tampilan
            if produk_nama in self.produk_map:
                self.produk_map[produk_nama]['stok'] += qty
                if self.produk_cb.get() == produk_nama:
                    self.stok_info_label.config(
                        text=f"Stok tersedia: {self.produk_map[produk_nama]['stok']}"
                    )
        
        # Update nomor urut
        self.renumber_items()
        self.update_total()
    
    def renumber_items(self):
        """Mengatur ulang nomor urut item"""
        children = self.tree.get_children()
        for idx, child in enumerate(children, 1):
            values = list(self.tree.item(child)['values'])
            values[0] = idx
            self.tree.item(child, values=values)
    
    def update_total(self):
        total = sum([item['qty'] * item['harga'] for item in self.transaksi_items])
        self.total_label.config(text=f"Total: Rp {total:,.2f}")
    
    def clear_item_form(self):
        """Mengosongkan form input item"""
        self.produk_cb.set('')
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")
        self.harga_entry.delete(0, tk.END)
        self.stok_info_label.config(text="Stok tersedia: -", foreground="blue")
        self.subtotal_label.config(text="Subtotal: Rp 0")
        self.selected_product_id = None
    
    def clear_cart(self):
        """Mengosongkan seluruh keranjang"""
        if not self.transaksi_items:
            return
        
        if messagebox.askyesno("Konfirmasi", "Apakah yakin ingin mengosongkan keranjang?"):
            # Hapus semua item dari treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Reset list transaksi
            self.transaksi_items = []
            
            # Reset total
            self.update_total()
            
            # Refresh stok display
            self.refresh_produk_map()
    
    def save_transaction(self):
        if not self.transaksi_items:
            messagebox.showwarning("Peringatan", "Keranjang belanja kosong!")
            return
        
        id_pelanggan_str = self.pelanggan_cb.get()
        if not id_pelanggan_str:
            messagebox.showwarning("Peringatan", "Pilih pelanggan!")
            return
        
        id_pelanggan = self.pelanggan_map.get(id_pelanggan_str)
        if not id_pelanggan:
            messagebox.showwarning("Peringatan", "Pelanggan tidak valid!")
            return
        
        total = sum([item['qty'] * item['harga'] for item in self.transaksi_items])
        id_karyawan = self.current_user["id"]

        # Konfirmasi sebelum simpan
        if not messagebox.askyesno("Konfirmasi", 
                                 f"Simpan transaksi dengan total Rp {total:,.2f}?"):
            return
        
        try:
            id_penjualan = self.db.add_transaksi_penjualan(id_pelanggan, id_karyawan, total)
            for item in self.transaksi_items:
                self.db.add_detail_penjualan(id_penjualan, item['id_produk'], item['qty'], item['harga'])
            
            # Tampilkan struk
            self.show_receipt(id_penjualan, total)
            
            messagebox.showinfo("Sukses", f"Transaksi berhasil disimpan dengan ID: {id_penjualan}")
            
            # Reset form setelah sukses
            self.transaksi_items = []
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            self.update_total()
            self.refresh_produk_map()
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan transaksi: {e}")
    
    def show_receipt(self, transaction_id, total):
        """Menampilkan struk transaksi"""
        receipt_window = tk.Toplevel(self)
        receipt_window.title(f"Struk Transaksi #{transaction_id}")
        receipt_window.geometry("400x500")
        
        # Frame untuk struk
        receipt_frame = ttk.Frame(receipt_window, padding=20)
        receipt_frame.pack(fill="both", expand=True)
        
        # Header struk
        ttk.Label(receipt_frame, text="TOKO KITA", 
                 font=("Courier", 16, "bold")).pack()
        ttk.Label(receipt_frame, text="Jl. Contoh No. 123", 
                 font=("Courier", 10)).pack()
        ttk.Label(receipt_frame, text="=" * 40, 
                 font=("Courier", 10)).pack()
        
        # Info transaksi
        ttk.Label(receipt_frame, 
                 text=f"ID Transaksi: {transaction_id}",
                 font=("Courier", 10)).pack(anchor="w")
        from datetime import date, datetime
        ttk.Label(receipt_frame, 
                 text=f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                 font=("Courier", 10)).pack(anchor="w")
        ttk.Label(receipt_frame, 
                 text=f"Kasir: {self.current_user['nama']}",
                 font=("Courier", 10)).pack(anchor="w")
        pelanggan_nama = self.pelanggan_cb.get().split(' - ')[1] if ' - ' in self.pelanggan_cb.get() else self.pelanggan_cb.get()
        ttk.Label(receipt_frame, 
                 text=f"Pelanggan: {pelanggan_nama}",
                 font=("Courier", 10)).pack(anchor="w")
        
        ttk.Label(receipt_frame, text="-" * 40, 
                 font=("Courier", 10)).pack()
        
        # Daftar item
        ttk.Label(receipt_frame, text="ITEM", 
                 font=("Courier", 10, "bold")).pack(anchor="w")
        
        for item in self.transaksi_items:
            produk_nama = ""
            for produk_id, info in self.produk_map.items():
                if info['id'] == item['id_produk']:
                    produk_nama = info['nama']
                    break
            
            item_text = f"{produk_nama[:20]:20} {item['qty']:3} x Rp {item['harga']:,.0f}"
            ttk.Label(receipt_frame, text=item_text, 
                     font=("Courier", 9)).pack(anchor="w")
        
        ttk.Label(receipt_frame, text="-" * 40, 
                 font=("Courier", 10)).pack()
        
        # Total
        ttk.Label(receipt_frame, 
                 text=f"TOTAL: Rp {total:,.2f}",
                 font=("Courier", 12, "bold")).pack(anchor="w")
        
        ttk.Label(receipt_frame, text="=" * 40, 
                 font=("Courier", 10)).pack()
        ttk.Label(receipt_frame, text="Terima kasih atas kunjungan Anda!", 
                 font=("Courier", 10)).pack()
        
        # Tombol cetak/tutup
        ttk.Button(receipt_window, text="Cetak", 
                  command=lambda: self.print_receipt(receipt_window)).pack(pady=10)
        ttk.Button(receipt_window, text="Tutup", 
                  command=receipt_window.destroy).pack(pady=5)
    
    def print_receipt(self, window):
        """Fungsi untuk mencetak struk (simulasi)"""
        messagebox.showinfo("Info", "Struk berhasil dicetak!")
        window.destroy()

class PembelianForm(tk.Toplevel):
    def __init__(self, parent, db, current_user):
        super().__init__(parent)
        self.db = db
        self.current_user = current_user

        self.title("Transaksi Pembelian")
        self.geometry("700x500")
        
        self.supplier_map = {f"{s[0]} - {s[1]}": s[0] for s in self.db.get_all_supplier()}
        self.produk_map = {
            f"{p[0]} - {p[2]}": {
                'id': p[0],
                'nama': p[2],
                'harga': p[5],   # harga_beli
                'stok': p[7]
            }
            for p in self.db.get_all_produk()
        }

        
        self.transaksi_items = []
        self.create_widgets()

    def create_widgets(self):
        header_frame = ttk.LabelFrame(self, text="Detail Transaksi")
        header_frame.pack(pady=10, padx=10, fill="x")
        ttk.Label(header_frame, text="Tanggal:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tanggal_label = ttk.Label(header_frame, text=date.today().strftime("%Y-%m-%d"))
        self.tanggal_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(header_frame, text="Supplier:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.supplier_cb = ttk.Combobox(header_frame, values=list(self.supplier_map.keys()), width=40)
        self.supplier_cb.grid(row=0, column=3, padx=5, pady=5)

        item_frame = ttk.LabelFrame(self, text="Tambah Item")
        item_frame.pack(pady=10, padx=10, fill="x")
        ttk.Label(item_frame, text="Produk:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.produk_cb = ttk.Combobox(item_frame, values=list(self.produk_map.keys()), width=40)
        self.produk_cb.grid(row=0, column=1, padx=5, pady=5)
        self.produk_cb.bind("<<ComboboxSelected>>", self.on_produk_select)
        ttk.Label(item_frame, text="Qty:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.qty_entry = ttk.Entry(item_frame, width=10)
        self.qty_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(item_frame, text="Harga Beli:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.harga_entry = ttk.Entry(item_frame, width=15)
        self.harga_entry.grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(item_frame, text="Tambah ke Keranjang", command=self.add_to_cart).grid(row=0, column=6, padx=10, pady=5)

        list_frame = ttk.Frame(self)
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        columns = ('id_produk', 'nama', 'qty', 'harga', 'subtotal')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.tree.heading('id_produk', text='ID Produk')
        self.tree.heading('nama', text='Nama Produk')
        self.tree.heading('qty', text='Qty')
        self.tree.heading('harga', text='Harga Beli')
        self.tree.heading('subtotal', text='Subtotal')
        self.tree.pack(fill="both", expand=True)
        
        total_frame = ttk.Frame(self)
        total_frame.pack(pady=5, padx=10, fill="x")
        self.total_label = ttk.Label(total_frame, text="Total: 0", font=("Arial", 14, "bold"))
        self.total_label.pack(side="right", padx=10)

        action_frame = ttk.Frame(self)
        action_frame.pack(pady=10)
        ttk.Button(action_frame, text="Simpan Transaksi", command=self.save_transaction).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Batal", command=self.destroy).pack(side="left", padx=5)

    def on_produk_select(self, event):
        selected_produk = self.produk_cb.get()
        harga = self.produk_map[selected_produk]['harga']
        self.harga_entry.delete(0, tk.END)
        self.harga_entry.insert(0, str(harga))

    def add_to_cart(self):
        produk_str = self.produk_cb.get()
        qty_str = self.qty_entry.get()

        if not all([produk_str, qty_str]):
            messagebox.showwarning("Peringatan", "Lengkapi data item!")
            return

        produk = self.produk_map.get(produk_str)
        if not produk:
            messagebox.showwarning("Peringatan", "Produk tidak valid!")
            return

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError



            id_produk = produk['id']
            harga = produk['harga']
            subtotal = qty * harga
            nama_produk = produk['nama']

            self.tree.insert('', 'end', values=(id_produk,nama_produk, qty, harga, subtotal))
            self.transaksi_items.append({'id_produk': id_produk, 'qty': qty, 'harga': harga})

            self.update_total()
            self.produk_cb.set('')
            self.qty_entry.delete(0, tk.END)
            self.harga_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Qty harus berupa angka positif!")

    def update_total(self):
        total = sum([item['qty'] * item['harga'] for item in self.transaksi_items])
        self.total_label.config(text=f"Total: {total:.2f}")

    def save_transaction(self):
        if not self.transaksi_items: messagebox.showwarning("Peringatan", "Keranjang belanja kosong!"); return
        id_supplier_str = self.supplier_cb.get()
        if not id_supplier_str: messagebox.showwarning("Peringatan", "Pilih supplier!"); return
        id_supplier = self.supplier_map[id_supplier_str]
        total = sum([item['qty'] * item['harga'] for item in self.transaksi_items])
        if not self.current_user:
            messagebox.showerror("Error", "User belum login!")
            return

        id_karyawan = self.current_user["id"]

        try:
            id_pembelian = self.db.add_transaksi_pembelian(id_supplier, id_karyawan, total)
            for item in self.transaksi_items:
                self.db.add_detail_pembelian(id_pembelian, item['id_produk'], item['qty'], item['harga'])
            messagebox.showinfo("Sukses", f"Transaksi Pembelian berhasil disimpan dengan ID: {id_pembelian}")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan transaksi: {e}")

class ReturPenjualanForm(tk.Toplevel):
    def __init__(self, parent, db, current_user):
        super().__init__(parent)
        self.db = db
        self.current_user = current_user

        self.title("Retur Penjualan")
        self.geometry("700x500")

        # Mapping pelanggan
        self.pelanggan_map = {f"{p[0]} - {p[1]}": p[0] for p in self.db.get_all_pelanggan()}

        # Data transaksi retur
        self.retur_items = []
        self.produk_map = {}

        self.create_widgets()
        self.refresh_produk_map()

    def refresh_produk_map(self):
        all_produk = self.db.get_all_produk()
        self.produk_map = {
            row[2]: {  # row[2] = nama_produk
                'id': row[0],
                'nama': row[2],
                'harga': row[6],  # harga_jual
                'stok': row[7]
            }
            for row in all_produk
        }
        self.produk_cb['values'] = [row[2] for row in all_produk]

    def create_widgets(self):
        # Header Retur
        header_frame = ttk.LabelFrame(self, text="Detail Retur")
        header_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(header_frame, text="Tanggal:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tanggal_label = ttk.Label(header_frame, text=date.today().strftime("%Y-%m-%d"))
        self.tanggal_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(header_frame, text="Pelanggan:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.pelanggan_cb = ttk.Combobox(header_frame, values=list(self.pelanggan_map.keys()), width=40)
        self.pelanggan_cb.grid(row=0, column=3, padx=5, pady=5)

        # Input Item Retur
        item_frame = ttk.LabelFrame(self, text="Tambah Item Retur")
        item_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(item_frame, text="Produk:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.produk_cb = ttk.Combobox(item_frame, values=[], width=40)
        self.produk_cb.grid(row=0, column=1, padx=5, pady=5)
        self.produk_cb.bind("<<ComboboxSelected>>", self.on_produk_select)

        ttk.Label(item_frame, text="Qty:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.qty_entry = ttk.Entry(item_frame, width=10)
        self.qty_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(item_frame, text="Harga:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.harga_entry = ttk.Entry(item_frame, width=15)
        self.harga_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(item_frame, text="Tambah ke Keranjang", command=self.add_to_cart).grid(row=0, column=6, padx=10, pady=5)

        # Treeview
        list_frame = ttk.Frame(self)
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        columns = ('id_produk', 'nama', 'qty', 'harga', 'subtotal')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.tree.heading('id_produk', text='ID Produk')
        self.tree.heading('nama', text='Nama Produk')
        self.tree.heading('qty', text='Qty')
        self.tree.heading('harga', text='Harga')
        self.tree.heading('subtotal', text='Subtotal')
        self.tree.pack(fill="both", expand=True)

        # Total
        total_frame = ttk.Frame(self)
        total_frame.pack(pady=5, padx=10, fill="x")
        self.total_label = ttk.Label(total_frame, text="Total Retur: 0", font=("Arial", 14, "bold"))
        self.total_label.pack(side="right", padx=10)

        # Tombol Aksi
        action_frame = ttk.Frame(self)
        action_frame.pack(pady=10)
        ttk.Button(action_frame, text="Simpan Retur", command=self.save_transaction).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Batal", command=self.destroy).pack(side="left", padx=5)

    def on_produk_select(self, event):
        selected_nama = self.produk_cb.get()
        if not selected_nama or selected_nama not in self.produk_map:
            return
        harga = self.produk_map[selected_nama]['harga']
        self.harga_entry.delete(0, tk.END)
        self.harga_entry.insert(0, str(harga))

    def add_to_cart(self):
        produk_nama = self.produk_cb.get()
        qty_str = self.qty_entry.get()
        if not all([produk_nama, qty_str]):
            messagebox.showwarning("Peringatan", "Lengkapi data item!")
            return
        if produk_nama not in self.produk_map:
            messagebox.showwarning("Peringatan", "Produk tidak valid!")
            return
        try:
            qty = int(qty_str)
            produk = self.produk_map[produk_nama]
            id_produk = produk['id']
            harga = produk['harga']

            subtotal = qty * harga
            self.tree.insert('', 'end', values=(id_produk, produk_nama, qty, harga, subtotal))
            self.retur_items.append({
                'id_produk': id_produk,
                'qty': qty,
                'harga': harga
            })

            self.update_total()

            self.produk_cb.set('')
            self.qty_entry.delete(0, tk.END)
            self.harga_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Qty harus berupa angka!")

    def update_total(self):
        total = sum([item['qty'] * item['harga'] for item in self.retur_items])
        self.total_label.config(text=f"Total Retur: {total:.2f}")

    def save_transaction(self):
        if not self.retur_items:
            messagebox.showwarning("Peringatan", "Keranjang retur kosong!")
            return

        id_pelanggan_str = self.pelanggan_cb.get()
        if not id_pelanggan_str:
            messagebox.showwarning("Peringatan", "Pilih pelanggan!")
            return
        id_pelanggan = self.pelanggan_map[id_pelanggan_str]
        total = sum([item['qty'] * item['harga'] for item in self.retur_items])
        id_karyawan = self.current_user["id"]

        try:
            # Simpan header retur
            id_retur = self.db.add_transaksi_retur_penjualan(None, id_pelanggan, id_karyawan, total)
            for item in self.retur_items:
                self.db.add_detail_retur_penjualan(id_retur, item['id_produk'], item['qty'], item['harga'])
            messagebox.showinfo("Sukses", f"Retur berhasil disimpan dengan ID: {id_retur}")
            self.refresh_produk_map()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan retur: {e}")

# forms.py - Tambahkan class LaporanForm

class LaporanPenjualanForm(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("Laporan Penjualan")
        self.geometry("1000x600")
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        # Frame untuk filter
        filter_frame = ttk.LabelFrame(self, text="Filter Laporan", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        # Tanggal awal
        ttk.Label(filter_frame, text="Tanggal Awal:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tanggal_awal_entry = ttk.Entry(filter_frame, width=15)
        self.tanggal_awal_entry.grid(row=0, column=1, padx=5, pady=5)
        self.tanggal_awal_entry.insert(0, datetime.now().strftime("%Y-%m-01"))  # Awal bulan
        
        # Tanggal akhir
        ttk.Label(filter_frame, text="Tanggal Akhir:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.tanggal_akhir_entry = ttk.Entry(filter_frame, width=15)
        self.tanggal_akhir_entry.grid(row=0, column=3, padx=5, pady=5)
        self.tanggal_akhir_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Hari ini
        
        # Tombol filter
        ttk.Button(filter_frame, text="Filter", command=self.load_data).grid(row=0, column=4, padx=10, pady=5)
        ttk.Button(filter_frame, text="Reset", command=self.reset_filter).grid(row=0, column=5, padx=5, pady=5)
        
        # Tombol cetak/export
        ttk.Button(filter_frame, text="Cetak Laporan", command=self.cetak_laporan).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(filter_frame, text="Export Excel", command=self.export_excel).grid(row=0, column=7, padx=5, pady=5)
        
        # Frame untuk treeview
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Treeview dengan scrollbar
        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side="right", fill="y")
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        
        columns = ('id', 'tanggal', 'waktu', 'pelanggan', 'karyawan', 'total')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Konfigurasi kolom
        self.tree.heading('id', text='ID')
        self.tree.heading('tanggal', text='Tanggal')
        self.tree.heading('waktu', text='Waktu')
        self.tree.heading('pelanggan', text='Pelanggan')
        self.tree.heading('karyawan', text='Kasir')
        self.tree.heading('total', text='Total')
        
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('tanggal', width=100, anchor='center')
        self.tree.column('waktu', width=80, anchor='center')
        self.tree.column('pelanggan', width=150)
        self.tree.column('karyawan', width=100)
        self.tree.column('total', width=120, anchor='e')
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Frame untuk total
        total_frame = ttk.Frame(self)
        total_frame.pack(fill="x", padx=10, pady=5)
        
        self.total_transaksi_label = ttk.Label(total_frame, text="Total Transaksi: 0", font=("Arial", 10, "bold"))
        self.total_transaksi_label.pack(side="left", padx=20)
        
        self.total_penjualan_label = ttk.Label(total_frame, text="Total Penjualan: Rp 0", font=("Arial", 10, "bold"))
        self.total_penjualan_label.pack(side="left", padx=20)
        
        self.rata_rata_label = ttk.Label(total_frame, text="Rata-rata per Transaksi: Rp 0", font=("Arial", 10, "bold"))
        self.rata_rata_label.pack(side="left", padx=20)
        
    def load_data(self):
        """Memuat data laporan penjualan"""
        # Ambil filter tanggal
        tanggal_awal = self.tanggal_awal_entry.get().strip()
        tanggal_akhir = self.tanggal_akhir_entry.get().strip()
        
        # Validasi tanggal
        if not tanggal_awal:
            tanggal_awal = None
        if not tanggal_akhir:
            tanggal_akhir = None
        
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ambil data dari database
        data = self.db.get_laporan_penjualan(tanggal_awal, tanggal_akhir)
        
        # Hitung total
        total_transaksi = len(data)
        total_penjualan = 0
        
        # Tambah data ke treeview
        for row in data:
            self.tree.insert('', 'end', values=row)
            total_penjualan += row[5] if row[5] else 0
        
        # Update label total
        self.total_transaksi_label.config(text=f"Total Transaksi: {total_transaksi}")
        self.total_penjualan_label.config(text=f"Total Penjualan: Rp {total_penjualan:,.2f}")
        
        if total_transaksi > 0:
            rata_rata = total_penjualan / total_transaksi
            self.rata_rata_label.config(text=f"Rata-rata per Transaksi: Rp {rata_rata:,.2f}")
        else:
            self.rata_rata_label.config(text="Rata-rata per Transaksi: Rp 0")
    
    def reset_filter(self):
        """Reset filter ke default"""
        from datetime import datetime
        self.tanggal_awal_entry.delete(0, tk.END)
        self.tanggal_awal_entry.insert(0, datetime.now().strftime("%Y-%m-01"))
        self.tanggal_akhir_entry.delete(0, tk.END)
        self.tanggal_akhir_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.load_data()
    
    def cetak_laporan(self):
        """Cetak laporan (simulasi)"""
        from tkinter import Toplevel, Text, Scrollbar
        
        # Ambil data terfilter
        tanggal_awal = self.tanggal_awal_entry.get()
        tanggal_akhir = self.tanggal_akhir_entry.get()
        
        # Buat window preview cetak
        print_window = Toplevel(self)
        print_window.title("Preview Cetak Laporan")
        print_window.geometry("600x700")
        
        # Text widget untuk preview
        frame = ttk.Frame(print_window, padding=10)
        frame.pack(fill="both", expand=True)
        
        text = Text(frame, wrap="word", font=("Courier", 10))
        
        # Header laporan
        header = f"""
{'='*60}
{'LAPORAN PENJUALAN'.center(60)}
{'='*60}
Periode: {tanggal_awal} s/d {tanggal_akhir}
Tanggal Cetak: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
{'NO'.center(5)} {'TANGGAL'.center(12)} {'PELANGGAN'.center(20)} {'KASIR'.center(15)} {'TOTAL'.center(15)}
{'='*60}
"""
        text.insert("1.0", header)
        
        # Data laporan
        data = self.db.get_laporan_penjualan(tanggal_awal, tanggal_akhir)
        total_penjualan = 0
        
        for idx, row in enumerate(data, 1):
            no = str(idx).center(5)
            tanggal = row[1].center(12)
            pelanggan = row[3][:18].ljust(20)
            kasir = row[4][:13].ljust(15)
            total = f"Rp {row[5]:,.2f}".rjust(15)
            
            text.insert("end", f"{no} {tanggal} {pelanggan} {kasir} {total}\n")
            total_penjualan += row[5] if row[5] else 0
        
        # Footer laporan
        footer = f"""
{'='*60}
{'Total Transaksi:'.ljust(40)} {len(data):>20}
{'Total Penjualan:'.ljust(40)} {'Rp ' + f'{total_penjualan:,.2f}'.rjust(18)}
{'='*60}
{'TERIMA KASIH'.center(60)}
{'='*60}
"""
        text.insert("end", footer)
        
        text.config(state="disabled")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tombol
        button_frame = ttk.Frame(print_window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Cetak", command=lambda: messagebox.showinfo("Info", "Mengirim ke printer...")).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Tutup", command=print_window.destroy).pack(side="left", padx=5)
    
    def export_excel(self):
        """Export ke Excel (simulasi)"""
        messagebox.showinfo("Info", "Fitur export Excel akan diimplementasikan pada versi selanjutnya.\n"
                                  "Gunakan fitur cetak untuk saat ini.")

# Alias untuk backward compatibility
LaporanForm = LaporanPenjualanForm
