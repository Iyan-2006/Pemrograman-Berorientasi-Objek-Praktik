# forms.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

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
        self.geometry("700x500")
        
        # Mapping pelanggan: "ID - Nama" -> ID
        self.pelanggan_map = {f"{p[0]} - {p[1]}": p[0] for p in self.db.get_all_pelanggan()}
 
        self.transaksi_items = []
        self.produk_map = {}
        self.create_widgets()
        self.refresh_produk_map()
        
    def refresh_produk_map(self):
        all_produk = self.db.get_all_produk()

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
        self.produk_cb['values'] = [row[2] for row in all_produk]

    def create_widgets(self):
        # Header Transaksi
        header_frame = ttk.LabelFrame(self, text="Detail Transaksi")
        header_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(header_frame, text="Tanggal:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tanggal_label = ttk.Label(header_frame, text=date.today().strftime("%Y-%m-%d"))
        self.tanggal_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(header_frame, text="Pelanggan:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.pelanggan_cb = ttk.Combobox(header_frame, values=list(self.pelanggan_map.keys()), width=40)
        self.pelanggan_cb.grid(row=0, column=3, padx=5, pady=5)

        # Input Item
        item_frame = ttk.LabelFrame(self, text="Tambah Item")
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

        # Daftar Item (Treeview)
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
        self.total_label = ttk.Label(total_frame, text="Total: 0", font=("Arial", 14, "bold"))
        self.total_label.pack(side="right", padx=10)

        # Tombol Aksi
        action_frame = ttk.Frame(self)
        action_frame.pack(pady=10)
        ttk.Button(action_frame, text="Simpan Transaksi", command=self.save_transaction).pack(side="left", padx=5)
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
            stok = produk['stok']

            if qty > stok:
                messagebox.showwarning("Stok Tidak Cukup", f"Stok tersedia hanya {stok}")
                return

            subtotal = qty * harga
            self.tree.insert('', 'end', values=(id_produk, produk_nama, qty, harga, subtotal))
            self.transaksi_items.append({
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
        total = sum([item['qty'] * item['harga'] for item in self.transaksi_items])
        self.total_label.config(text=f"Total: {total:.2f}")

    def save_transaction(self):
        if not self.transaksi_items:
            messagebox.showwarning("Peringatan", "Keranjang belanja kosong!")
            return
        
        id_pelanggan_str = self.pelanggan_cb.get()
        if not id_pelanggan_str:
            messagebox.showwarning("Peringatan", "Pilih pelanggan!")
            return
        id_pelanggan = self.pelanggan_map[id_pelanggan_str]
        total = sum([item['qty'] * item['harga'] for item in self.transaksi_items])
        id_karyawan = self.current_user["id"]

        try:
            id_penjualan = self.db.add_transaksi_penjualan(id_pelanggan, id_karyawan, total)
            for item in self.transaksi_items:
                self.db.add_detail_penjualan(id_penjualan, item['id_produk'], item['qty'], item['harga'])
            
            messagebox.showinfo("Sukses", f"Transaksi berhasil disimpan dengan ID: {id_penjualan}")
            self.refresh_produk_map()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan transaksi: {e}")


# --- Form Laporan ---
class LaporanForm(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("Laporan Penjualan")
        self.geometry("800x500")
        self.create_widgets()

    def create_widgets(self):
        # Treeview untuk laporan
        list_frame = ttk.Frame(self)
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ('id', 'tanggal', 'pelanggan', 'karyawan', 'total')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
        self.tree.pack(fill="both", expand=True)
        
        self.populate_treeview()

    def populate_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_laporan_penjualan():
            self.tree.insert('', 'end', values=row)
            
    # DATA TAMBAHAN
    # forms.py
# ... (kode yang sudah ada untuk semua form sebelumnya) ...

# --- Tambahkan kelas form baru di bawah ini ---

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

