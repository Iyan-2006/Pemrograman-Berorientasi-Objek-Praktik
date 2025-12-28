# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from forms import (
    PelangganForm, ProdukForm, KategoriForm, SupplierForm, KaryawanForm,
    PenjualanForm, LaporanForm,PembelianForm, ReturPenjualanForm
)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_user = {
            "id": 1,
            "nama": "Admin"
        }

        self.title("Sistem Manajemen Toko Sederhana")
        self.geometry("400x300")
        
        # Konsep Enkapsulasi: Objek db menyembunyikan detail koneksi dan query
        self.db = Database(db_name="toko.db")

        self.create_menu()
        self.create_main_layout()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Menu Data Master
        master_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Data Master", menu=master_menu)
        master_menu.add_command(label="Master Pelanggan", command=lambda: PelangganForm(self, self.db))
        master_menu.add_command(label="Master Produk", command=lambda: ProdukForm(self, self.db))
        master_menu.add_command(label="Master Kategori", command=lambda: KategoriForm(self, self.db))
        master_menu.add_command(label="Master Supplier", command=lambda: SupplierForm(self, self.db))
        master_menu.add_command(label="Master Karyawan", command=lambda: KaryawanForm(self, self.db))

        # Menu Transaksi
        transaksi_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Transaksi", menu=transaksi_menu)
        transaksi_menu.add_command(label="Penjualan", command=lambda: PenjualanForm(self, self.db, self.current_user))
        
        transaksi_menu.add_command(label="Pembelian", command=lambda: PembelianForm(self, self.db, self.current_user))

        transaksi_menu.add_command(label="Retur Penjualan", command=lambda: ReturPenjualanForm(self, self.db, self.current_user))

        # Menu Laporan
        laporan_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Laporan", menu=laporan_menu)
        laporan_menu.add_command(label="Laporan Penjualan", command=lambda: LaporanForm(self, self.db))
        # laporan_menu.add_command(label="Laporan Pembelian", command=lambda: LaporanPembelianForm(self, self.db))

        # Menu Keluar
        menubar.add_command(label="Keluar", command=self.quit_app)

    def create_main_layout(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        label = ttk.Label(main_frame, text="Selamat Datang di Sistem Manajemen Toko", font=("Helvetica", 16))
        label.pack(pady=20, expand=True)
        
        info_label = ttk.Label(main_frame, text="Silakan pilih menu di atas untuk memulai.")
        info_label.pack()

    def quit_app(self):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?"):
            self.db.close()
            self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()