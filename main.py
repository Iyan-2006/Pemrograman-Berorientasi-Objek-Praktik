# main.py
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
from database import Database
from forms import (
    PelangganForm, ProdukForm, KategoriForm, SupplierForm, KaryawanForm,
    PenjualanForm, PembelianForm, ReturPenjualanForm
)

class LoginWindow(tk.Toplevel):
    """Window untuk login"""
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.parent = parent
        self.result = None
        
        self.title("Login - Sistem Toko")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Handle window close (X button)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # tombol login
        style = ttk.Style(self)
        style.configure(
            "Login.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10
        )

        self.create_widgets()
        self.bind("<Return>", lambda e: self.login())

        self.center_window()
        
        # Focus ke username entry
        self.username_entry.focus()
        
    def center_window(self):
        """Menempatkan window di tengah layar"""
        self.update_idletasks()
        width = 400
        height = 300
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Membuat widget untuk form login"""
        # Frame utama
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(fill="both", expand=True)
        
        # Judul
        title_label = ttk.Label(main_frame, 
                               text="SISTEM MANAJEMEN TOKO",
                               font=("Helvetica", 16, "bold"),
                               foreground="#2c3e50")
        title_label.pack(pady=(0, 30))
        
        # Sub judul
        sub_title = ttk.Label(main_frame,
                             text="Silakan login untuk melanjutkan",
                             font=("Helvetica", 10),
                             foreground="#7f8c8d")
        sub_title.pack(pady=(0, 20))
        
        # Form login
        login_frame = ttk.LabelFrame(main_frame, text="Login", padding=20)
        login_frame.pack(fill="x", pady=10)
        
        # Username
        ttk.Label(login_frame, text="Username:", 
                 font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.username_entry = ttk.Entry(login_frame, width=25, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, padx=5, pady=10)
        self.username_entry.insert(0, "admin")  # Default username
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Password
        ttk.Label(login_frame, text="Password:", 
                 font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.password_entry = ttk.Entry(login_frame, width=25, show="•", font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)
        self.password_entry.insert(0, "admin123")  # Default password
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Tombol
        button_frame = tk.Frame(main_frame, bg=self["bg"])
        button_frame.pack(pady=20)

        
        # Tombol Login dengan styling
        self.login_btn = tk.Button(
            button_frame,
            text="LOGIN",
            font=("Segoe UI", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            width=18,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.login
        )
        self.login_btn.pack(pady=10)

        
        # Tombol Keluar
        exit_btn = ttk.Button(button_frame, 
                             text="Keluar", 
                             command=self.on_close,
                             style="Exit.TButton",
                             width=12)
        exit_btn.pack(side="left", padx=5)
        
        # Info default login
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", pady=10)
        
        info_text = "Default login:\nUsername: admin\nPassword: admin123"
        info_label = ttk.Label(info_frame, 
                              text=info_text,
                              font=("Arial", 8),
                              foreground="#95a5a6",
                              justify="center")
        info_label.pack()
        
        # Styling untuk tombol
        style = ttk.Style()
        style.configure("Login.TButton", 
                       font=("Arial", 10, "bold"),
                       foreground="white",
                       background="#3498db",
                       padding=8)
        style.map("Login.TButton",
                 background=[('active', '#2980b9')])
        
        style.configure("Exit.TButton",
                       font=("Arial", 10),
                       foreground="white",
                       background="#95a5a6",
                       padding=8)
        style.map("Exit.TButton",
                 background=[('active', '#7f8c8d')])
    
    def login(self):
        """Proses login ketika tombol Login diklik"""
        self.login_btn.config(state="disabled", text="Memeriksa...")
        self.update_idletasks()

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validasi input
        if not username:
            messagebox.showwarning("Peringatan", "Username harus diisi!")
            self.login_btn.config(state="normal", text="Login")
            self.username_entry.focus()
            return

        if not password:
            messagebox.showwarning("Peringatan", "Password harus diisi!")
            self.login_btn.config(state="normal", text="Login")
            self.password_entry.focus()
            return

        print(f"Login attempt: {username}")
        
        # Gunakan method baru yang return dictionary
        user_data = self.db.verify_login_dict(username, password)
        
        if user_data:
            print(f"Login successful: {user_data}")
            self.result = user_data
            self.destroy()
        else:
            # Fallback ke default admin
            if username == "admin" and password == "admin123":
                print("Using default admin login")
                self.result = {
                    "id": 1,
                    "username": "admin",
                    "nama": "Admin",
                    "level": "admin",
                    "id_karyawan": 1
                }
                self.destroy()
            else:
                messagebox.showerror("Login Gagal", 
                                "Username atau password salah!\n\n"
                                "Coba dengan:\nUsername: admin\nPassword: admin123")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
                self.login_btn.config(state="normal", text="Login")

        
    def on_close(self):
        """Handle ketika tombol keluar atau X diklik"""
        self.result = None
        self.destroy()
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistem Manajemen Toko")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        # Inisialisasi database
        self.db = Database(db_name="toko.db")
        
        # User belum login
        self.current_user = None
        
        # Tampilkan login window
        self.withdraw()        # SEMBUNYIKAN ROOT
        self.show_login()

    
    def show_login(self):
        """Menampilkan window login"""
        print("Showing login window...")
        
        # Buat window login
        self.login_window = LoginWindow(self, self.db)
        
        # Tunggu sampai window login ditutup
        self.wait_window(self.login_window)
        
        # Cek hasil login
        if hasattr(self.login_window, 'result') and self.login_window.result:
            self.current_user = self.login_window.result
            print(f"User logged in: {self.current_user['username']}")
            self.deiconify()   # TAMPILKAN ROOT
            self.initialize_app()
        else:
            print("Login cancelled or failed")
            self.quit_app()
    
    def initialize_app(self):
        """Inisialisasi aplikasi setelah login berhasil"""
        print("Initializing application...")
        
        try:
            # Clear window jika ada widget sebelumnya
            for widget in self.winfo_children():
                widget.destroy()
            
            # Buat menu dan layout
            self.create_menu()
            self.create_main_layout()
            
            # Update title dengan nama user
            self.title(f"Sistem Manajemen Toko - {self.current_user['nama']} ({self.current_user['level'].title()})")
            
            # Tampilkan welcome message
            messagebox.showinfo("Login Berhasil", 
                              f"Selamat datang, {self.current_user['nama']}!\n"
                              f"Akses level: {self.current_user['level'].title()}")
            
            print("Application initialized successfully")
            
        except Exception as e:
            print(f"Error initializing app: {e}")
            messagebox.showerror("Error", f"Gagal menginisialisasi aplikasi: {e}")
            self.destroy()
    
    # ... (sisa kode App tetap sama)s
        
    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menu Dashboard
        dashboard_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dashboard", menu=dashboard_menu)
        dashboard_menu.add_command(label="Refresh Dashboard", command=self.refresh_dashboard)
        dashboard_menu.add_separator()
        dashboard_menu.add_command(label="Logout", command=self.logout)
        dashboard_menu.add_command(label="Keluar", command=self.quit_app)

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
        transaksi_menu.add_command(label="Penjualan", 
                                  command=lambda: PenjualanForm(self, self.db, self.current_user))
        transaksi_menu.add_command(label="Pembelian", 
                                  command=lambda: PembelianForm(self, self.db, self.current_user))
        transaksi_menu.add_command(label="Retur Penjualan", 
                                  command=lambda: ReturPenjualanForm(self, self.db, self.current_user))

        # Menu Laporan
        laporan_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Laporan", menu=laporan_menu)
        laporan_menu.add_command(label="Laporan Penjualan", command=self.show_laporan_sederhana)
        laporan_menu.add_command(label="Laporan Stok", command=self.show_laporan_stok)
        laporan_menu.add_command(label="Produk Terlaris", command=self.show_produk_terlaris)
        
        # Menu Tools
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Backup Database", command=self.backup_database)
        tools_menu.add_command(label="Restore Database", command=self.restore_database)
        
        # Menu Bantuan
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bantuan", menu=help_menu)
        help_menu.add_command(label="Tentang", command=self.show_about)
        help_menu.add_command(label="Panduan Penggunaan", command=self.show_help)

    def show_laporan_sederhana(self):
        """Menampilkan laporan penjualan sederhana"""
        from tkinter import Toplevel
        import tkinter.ttk as ttk
        
        laporan_window = Toplevel(self)
        laporan_window.title("Laporan Penjualan")
        laporan_window.geometry("800x500")
        
        # Treeview
        frame = ttk.Frame(laporan_window, padding=10)
        frame.pack(fill="both", expand=True)
        
        columns = ('id', 'tanggal', 'pelanggan', 'karyawan', 'total')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        tree.heading('id', text='ID')
        tree.heading('tanggal', text='Tanggal')
        tree.heading('pelanggan', text='Pelanggan')
        tree.heading('karyawan', text='Kasir')
        tree.heading('total', text='Total')
        
        tree.column('id', width=50, anchor='center')
        tree.column('tanggal', width=100)
        tree.column('pelanggan', width=150)
        tree.column('karyawan', width=100)
        tree.column('total', width=120, anchor='e')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load data
        try:
            data = self.db.get_laporan_penjualan()
            for row in data:
                formatted_row = list(row)

                # total_harga ada di index ke-5
                if len(formatted_row) > 5:
                    total = formatted_row[5]
                    try:
                        total = float(total)
                    except:
                        total = 0
                    formatted_row[5] = f"Rp {total:,.2f}"

                tree.insert('', 'end', values=formatted_row)

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")
            
    def create_main_layout(self):
        """Membuat layout dashboard utama"""
        try:
            # Frame utama dengan dua bagian
            main_frame = ttk.Frame(self)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Bagian kiri: Info user dan menu cepat
            left_frame = ttk.Frame(main_frame, width=200)
            left_frame.pack(side="left", fill="y", padx=(0, 10))
            
            # Bagian kanan: Dashboard utama
            right_frame = ttk.Frame(main_frame)
            right_frame.pack(side="right", fill="both", expand=True)
            
            # --- Bagian Kiri: Info User ---
            user_frame = ttk.LabelFrame(left_frame, text="Informasi User", padding=10)
            user_frame.pack(fill="x", pady=(0, 10))
            
            # Avatar/icon
            avatar_label = ttk.Label(user_frame, text="👤", font=("Arial", 24))
            avatar_label.pack(pady=5)
            
            # Nama user
            user_name_label = ttk.Label(user_frame, text=self.current_user['nama'], 
                                       font=("Arial", 12, "bold"))
            user_name_label.pack()
            
            # Level user
            user_level_label = ttk.Label(user_frame, text=f"Level: {self.current_user['level'].title()}", 
                                        font=("Arial", 10))
            user_level_label.pack()
            
            # Tanggal login
            login_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            login_label = ttk.Label(user_frame, text=f"Login: {login_date}", 
                                   font=("Arial", 9))
            login_label.pack(pady=5)
            
            # Tombol logout
            ttk.Button(user_frame, text="Logout", command=self.logout, 
                      width=15).pack(pady=10)
            
            # --- Menu Cepat ---
            quick_menu_frame = ttk.LabelFrame(left_frame, text="Menu Cepat", padding=10)
            quick_menu_frame.pack(fill="x")
            
            # PERBAIKAN: Ganti LaporanForm dengan show_laporan_sederhana
            ttk.Button(quick_menu_frame, text="📦 Transaksi Penjualan", 
                      command=lambda: PenjualanForm(self, self.db, self.current_user),
                      style="Quick.TButton").pack(fill="x", pady=5)
            
            ttk.Button(quick_menu_frame, text="📊 Laporan Penjualan", 
                      command=self.show_laporan_sederhana,  # PERBAIKAN DI SINI
                      style="Quick.TButton").pack(fill="x", pady=5)
            
            ttk.Button(quick_menu_frame, text="📋 Master Produk", 
                      command=lambda: ProdukForm(self, self.db),
                      style="Quick.TButton").pack(fill="x", pady=5)
            
            ttk.Button(quick_menu_frame, text="📈 Produk Terlaris", 
                      command=self.show_produk_terlaris,
                      style="Quick.TButton").pack(fill="x", pady=5)
            
            # --- Bagian Kanan: Dashboard ---
            # Header dashboard
            header_frame = ttk.Frame(right_frame)
            header_frame.pack(fill="x", pady=(0, 10))
            
            welcome_label = ttk.Label(header_frame, 
                                     text=f"Selamat datang, {self.current_user['nama']}!",
                                     font=("Helvetica", 16, "bold"))
            welcome_label.pack(side="left")
            
            date_label = ttk.Label(header_frame, 
                                  text=datetime.now().strftime("%A, %d %B %Y"),
                                  font=("Helvetica", 10))
            date_label.pack(side="right")
            
            # Statistik cards
            stats_frame = ttk.Frame(right_frame)
            stats_frame.pack(fill="x", pady=10)
            
            # Card 1: Total Pelanggan
            try:
                total_pelanggan = self.db.get_total_pelanggan()
                card1 = self.create_stat_card(stats_frame, "Total Pelanggan", 
                                             total_pelanggan, "👥", 0)
                card1.pack(side="left", padx=5, fill="both", expand=True)
            except:
                card1 = self.create_stat_card(stats_frame, "Total Pelanggan", 
                                             "Error", "👥", 0)
                card1.pack(side="left", padx=5, fill="both", expand=True)
            
            # Card 2: Total Produk
            try:
                total_produk = self.db.get_total_produk()
                card2 = self.create_stat_card(stats_frame, "Total Produk", 
                                             total_produk, "📦", 1)
                card2.pack(side="left", padx=5, fill="both", expand=True)
            except:
                card2 = self.create_stat_card(stats_frame, "Total Produk", 
                                             "Error", "📦", 1)
                card2.pack(side="left", padx=5, fill="both", expand=True)
            
            # Card 3: Total Stok
            try:
                total_stok = self.db.get_total_stok() or 0
                card3 = self.create_stat_card(stats_frame, "Total Stok", 
                                             total_stok, "📊", 2)
                card3.pack(side="left", padx=5, fill="both", expand=True)
            except:
                card3 = self.create_stat_card(stats_frame, "Total Stok", 
                                             "Error", "📊", 2)
                card3.pack(side="left", padx=5, fill="both", expand=True)
            
            # Card 4: Penjualan Hari Ini
            try:
                penjualan_hari_ini = self.db.get_total_penjualan_hari_ini() or 0
                card4 = self.create_stat_card(stats_frame, "Penjualan Hari Ini", 
                                             f"Rp {penjualan_hari_ini:,.0f}", "💰", 3)
                card4.pack(side="left", padx=5, fill="both", expand=True)
            except:
                card4 = self.create_stat_card(stats_frame, "Penjualan Hari Ini", 
                                             "Rp 0", "💰", 3)
                card4.pack(side="left", padx=5, fill="both", expand=True)
            
            # --- Produk Stok Rendah ---
            stok_frame = ttk.LabelFrame(right_frame, text="⚠️ Produk Stok Rendah", padding=10)
            stok_frame.pack(fill="both", expand=True, pady=10)
            
            # Treeview untuk produk stok rendah
            columns = ('kode', 'nama', 'stok', 'harga')
            self.stok_tree = ttk.Treeview(stok_frame, columns=columns, show='headings', height=8)
            
            self.stok_tree.heading('kode', text='Kode')
            self.stok_tree.heading('nama', text='Nama Produk')
            self.stok_tree.heading('stok', text='Stok')
            self.stok_tree.heading('harga', text='Harga Jual')
            
            self.stok_tree.column('kode', width=80)
            self.stok_tree.column('nama', width=200)
            self.stok_tree.column('stok', width=60, anchor='center')
            self.stok_tree.column('harga', width=100, anchor='e')
            
            scrollbar = ttk.Scrollbar(stok_frame, orient="vertical", command=self.stok_tree.yview)
            self.stok_tree.configure(yscrollcommand=scrollbar.set)
            
            self.stok_tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Load data stok rendah
            self.load_stok_rendah()
            
            # --- Recent Activity ---
            activity_frame = ttk.LabelFrame(right_frame, text="📝 Aktifitas Terakhir", padding=10)
            activity_frame.pack(fill="x", pady=(10, 0))
            
            activity_text = tk.Text(activity_frame, height=4, font=("Arial", 9))
            activity_text.pack(fill="x")
            activity_text.insert("1.0", 
                                f"• Login berhasil pada {datetime.now().strftime('%H:%M:%S')}\n"
                                f"• User: {self.current_user['nama']}\n"
                                f"• Level akses: {self.current_user['level'].title()}\n"
                                f"• Sistem siap digunakan...")
            activity_text.config(state="disabled")
            
            # Styling
            style = ttk.Style()
            style.configure("Quick.TButton", font=("Arial", 10))
            style.configure("Card.TLabel", font=("Arial", 12))
            style.configure("CardValue.TLabel", font=("Arial", 18, "bold"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat layout: {e}")
            self.destroy()
    
    def create_stat_card(self, parent, title, value, icon, color_index):
        """Membuat card statistik"""
        colors = ["#4CAF50", "#2196F3", "#FF9800", "#F44336"]
        
        card = ttk.Frame(parent, relief="solid", borderwidth=1)
        
        # Warna header
        header_frame = tk.Frame(card, bg=colors[color_index], height=5)
        header_frame.pack(fill="x")
        
        # Konten card
        content_frame = ttk.Frame(card, padding=10)
        content_frame.pack(fill="both", expand=True)
        
        # Icon dan value
        icon_label = ttk.Label(content_frame, text=icon, font=("Arial", 24))
        icon_label.pack()
        
        value_label = ttk.Label(content_frame, text=str(value), 
                               font=("Arial", 18, "bold"))
        value_label.pack(pady=5)
        
        title_label = ttk.Label(content_frame, text=title, font=("Arial", 10))
        title_label.pack()
        
        return card
    
    def load_stok_rendah(self):
        """Memuat data produk dengan stok rendah"""
        try:
            # Hapus data lama
            for item in self.stok_tree.get_children():
                self.stok_tree.delete(item)
            
            produk_stok_rendah = self.db.get_produk_dengan_stok_rendah(batas=10)
            
            if produk_stok_rendah:
                for produk in produk_stok_rendah:

                    # AMANKAN harga
                    harga = produk[5] if len(produk) > 5 else 0
                    try:
                        harga = float(harga)
                    except:
                        harga = 0

                    self.stok_tree.insert('', 'end', values=(
                        produk[1] if len(produk) > 1 else "",  # kode
                        produk[2] if len(produk) > 2 else "",  # nama
                        produk[3] if len(produk) > 3 else 0,   # stok
                        f"Rp {harga:,.0f}"
                    ))
            else:
                self.stok_tree.insert('', 'end', values=("", "Tidak ada produk stok rendah", "", ""))

        except Exception as e:
            self.stok_tree.insert('', 'end', values=("", "Error memuat data", "", ""))

    
    def refresh_dashboard(self):
        """Refresh data dashboard"""
        # Untuk sekarang, cukup reload stok rendah
        self.load_stok_rendah()
        messagebox.showinfo("Refresh", "Dashboard telah di-refresh!")
    
    def show_laporan_stok(self):
        """Menampilkan laporan stok"""
        from tkinter import Toplevel
        import tkinter.ttk as ttk
        
        laporan_window = Toplevel(self)
        laporan_window.title("Laporan Stok Produk")
        laporan_window.geometry("800x500")
        
        # Treeview
        frame = ttk.Frame(laporan_window, padding=10)
        frame.pack(fill="both", expand=True)
        
        columns = ('kode', 'nama', 'kategori', 'supplier', 'harga_beli', 'harga_jual', 'stok', 'nilai_stok')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        headings = ['Kode', 'Nama', 'Kategori', 'Supplier', 'Harga Beli', 'Harga Jual', 'Stok', 'Nilai Stok']
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, width=100)
        
        tree.column('nama', width=150)
        tree.column('kategori', width=100)
        tree.column('nilai_stok', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load data
        try:
            data = self.db.get_laporan_stok()
            if data:
                for row in data:
                    tree.insert('', 'end', values=row)
            
            # Total
            total_frame = ttk.Frame(laporan_window)
            total_frame.pack(fill="x", padx=10, pady=5)
            
            if data:
                total_stok = sum(row[6] for row in data if len(row) > 6 and row[6])
                total_nilai = sum(row[7] for row in data if len(row) > 7 and row[7])
                
                ttk.Label(total_frame, text=f"Total Produk: {len(data)}", 
                         font=("Arial", 10)).pack(side="left", padx=10)
                ttk.Label(total_frame, text=f"Total Stok: {total_stok}", 
                         font=("Arial", 10)).pack(side="left", padx=10)
                ttk.Label(total_frame, text=f"Total Nilai Stok: Rp {total_nilai:,.0f}", 
                         font=("Arial", 10, "bold")).pack(side="left", padx=10)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat laporan stok: {e}")
    
    def show_produk_terlaris(self):
        """Menampilkan produk terlaris"""
        from tkinter import Toplevel
        import tkinter.ttk as ttk
        
        laporan_window = Toplevel(self)
        laporan_window.title("Laporan Produk Terlaris")
        laporan_window.geometry("600x400")
        
        # Treeview
        frame = ttk.Frame(laporan_window, padding=10)
        frame.pack(fill="both", expand=True)
        
        columns = ('nama', 'terjual', 'pendapatan')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        tree.heading('nama', text='Nama Produk')
        tree.heading('terjual', text='Jumlah Terjual')
        tree.heading('pendapatan', text='Total Pendapatan')
        
        tree.column('nama', width=250)
        tree.column('terjual', width=100, anchor='center')
        tree.column('pendapatan', width=150, anchor='e')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load data
        try:
            data = self.db.get_produk_terlaris(limit=20)
            if data:
                for row in data:
                    # amankan nilai pendapatan
                    pendapatan = row[2] if len(row) > 2 else 0
                    try:
                        pendapatan = float(pendapatan)
                    except:
                        pendapatan = 0

                    tree.insert('', 'end', values=(
                        row[0] if len(row) > 0 else "",           # nama
                        int(row[1]) if len(row) > 1 and row[1] else 0,  # terjual
                        f"Rp {pendapatan:,.0f}"                  # pendapatan
                    ))

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat produk terlaris: {e}")
    
    def backup_database(self):
        """Backup database"""
        from datetime import datetime
        import os
        
        try:
            if not os.path.exists("backup"):
                os.makedirs("backup")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backup/toko_backup_{timestamp}.db"
            
            if self.db.backup_database(backup_file):
                messagebox.showinfo("Backup Berhasil", 
                                  f"Database berhasil di-backup ke:\n{backup_file}")
            else:
                messagebox.showerror("Backup Gagal", "Gagal melakukan backup database")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal backup: {e}")
    
    def restore_database(self):
        """Restore database (simulasi)"""
        messagebox.showinfo("Info", 
                          "Fitur restore database akan diimplementasikan pada versi selanjutnya.\n"
                          "Untuk saat ini, backup otomatis tersimpan di folder 'backup'.")
    
    def show_about(self):
        """Menampilkan about dialog"""
        about_text = """
SISTEM MANAJEMEN TOKO
Versi 1.0

Fitur:
• Manajemen Data Master
• Transaksi Penjualan & Pembelian
• Manajemen Stok
• Laporan dan Analisis
• Multi-user dengan Level Akses

Dibangun dengan Python, Tkinter, dan SQLite

© 2023 - Sistem Toko v1.0
        """
        messagebox.showinfo("Tentang Aplikasi", about_text)
    
    def show_help(self):
        """Menampilkan help dialog"""
        help_text = """
PANDUAN PENGGUNAAN:

1. Data Master:
   - Pelanggan: Kelola data pelanggan
   - Produk: Kelola data produk dan stok
   - Kategori: Kelola kategori produk
   - Supplier: Kelola data supplier
   - Karyawan: Kelola data karyawan

2. Transaksi:
   - Penjualan: Transaksi penjualan dengan validasi stok
   - Pembelian: Transaksi pembelian barang
   - Retur: Pengembalian barang yang dijual

3. Laporan:
   - Laporan Penjualan: Histori transaksi penjualan
   - Laporan Stok: Monitoring stok produk
   - Produk Terlaris: Analisis penjualan produk

4. Tools:
   - Backup: Backup database secara manual
   - Restore: Restore dari backup (coming soon)

Catatan:
• Stok otomatis berkurang saat penjualan
• Stok otomatis bertambah saat pembelian/retur
• Validasi stok mencegah penjualan melebihi stok tersedia
        """
        from tkinter import Toplevel, Text, Scrollbar
        import tkinter.ttk as ttk
        
        help_window = Toplevel(self)
        help_window.title("Panduan Penggunaan")
        help_window.geometry("600x400")
        
        frame = ttk.Frame(help_window, padding=10)
        frame.pack(fill="both", expand=True)
        
        text = Text(frame, wrap="word", font=("Arial", 10))
        text.insert("1.0", help_text)
        text.config(state="disabled")
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Button(help_window, text="Tutup", command=help_window.destroy).pack(pady=10)
    
    def logout(self):
        """Logout dari sistem"""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin logout?"):
            self.current_user = None
            # Hapus semua widget
            for widget in self.winfo_children():
                try:
                    widget.destroy()
                except:
                    pass
            # Tampilkan login kembali
            self.after(100, self.show_login)
    
    def quit_app(self):
        """Keluar dari aplikasi"""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            try:
                self.db.close()
            except:
                pass
            self.after(100, self.destroy)

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Aplikasi error: {str(e)}")
