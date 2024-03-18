from app import mysql
from passlib.hash import pbkdf2_sha256


class AnggotaModel(mysql.Model):
    __tablename__ = 'anggota'
    
    id = mysql.Column(mysql.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    kode_anggota = mysql.Column(mysql.String, nullable=False, unique=True)
    nama_anggota = mysql.Column(mysql.String, nullable=False)
    status = mysql.Column(mysql.String, nullable=False)
    nik = mysql.Column(mysql.Integer, nullable=False)
    bidang = mysql.Column(mysql.String, nullable=False)
    keterangan = mysql.Column(mysql.String, nullable=False)
    
    def __init__(self, kode_anggota, nama_anggota, status, nik, bidang, keterangan):
        self.kode_anggota = kode_anggota
        self.nama_anggota = nama_anggota
        self.status = status
        self.nik = nik
        self.bidang = bidang
        self.keterangan = keterangan
        
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    

class BarangModel(mysql.Model):
    __tablename__ = "persedia_brg"
    
    id = mysql.Column(mysql.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    nama_barang = mysql.Column(mysql.String, nullable=False, unique=True)
    satuan = mysql.Column(mysql.String, nullable=False)
    harga_beli = mysql.Column(mysql.Integer, nullable=False)
    harga_jual = mysql.Column(mysql.Integer, nullable=False)
    stok_awal = mysql.Column(mysql.Integer, nullable=False)
    keterangan = mysql.Column(mysql.String, nullable=False)

    def __init__(self, nama_barang, satuan, harga_beli, harga_jual, stok_awal, keterangan):
        self.nama_barang = nama_barang
        self.satuan = satuan
        self.harga_beli = harga_beli
        self.harga_jual = harga_jual
        self.stok_awal = stok_awal
        self.keterangan = keterangan
        
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    
class BrgMasukModel(mysql.Model):
    __tablename__ = 'brg_masuk'
    
    id = mysql.Column(mysql.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    tanggal_masuk = mysql.Column(mysql.String, nullable=False)
    nama_barang = mysql.Column(mysql.String, nullable=False, unique=True)
    satuan = mysql.Column(mysql.String, nullable=False)
    qty = mysql.Column(mysql.Integer, nullable=False)
    harga_beli = mysql.Column(mysql.Integer, nullable=False)
    distributor = mysql.Column(mysql.String, nullable=False)
    keterangan = mysql.Column(mysql.String, nullable=False)
    
    def __init__(self, tanggal_masuk, nama_barang, satuan, qty, harga_beli, distributor, keterangan):
        self.tanggal_masuk = tanggal_masuk
        self.nama_barang = nama_barang
        self.satuan = satuan
        self.qty = qty
        self.harga_beli = harga_beli
        self.distributor = distributor
        self.keterangan = keterangan

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    
class BrgOutModel(mysql.Model):
    __tablename__= 'brg_out'
    
    id = mysql.Column(mysql.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    tanggal_keluar = mysql.Column(mysql.String, nullable=False)
    nama_barang = mysql.Column(mysql.String, nullable=False, unique=True)
    satuan = mysql.Column(mysql.String, nullable=False)
    qty = mysql.Column(mysql.Integer, nullable=False)
    harga_jual = mysql.Column(mysql.Integer, nullable=False)
    customer = mysql.Column(mysql.String, nullable=False)
    pembayaran = mysql.Column(mysql.String, nullable=False)
    keterangan = mysql.Column(mysql.String, nullable=False)
    
    def __init__(self, tanggal_keluar, nama_barang, satuan, qty, harga_jual, customer, pembayaran, keterangan):
        self.tanggal_keluar = tanggal_keluar
        self.nama_barang = nama_barang
        self.satuan = satuan
        self.qty = qty
        self.harga_jual = harga_jual
        self.customer = customer
        self.pembayaran = pembayaran
        self.keterangan = keterangan

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    

class UserModel(mysql.Model):
    __tablename__ = "user"

    id_user = mysql.Column(mysql.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    username = mysql.Column(mysql.String, nullable=False)
    password = mysql.Column(mysql.String, nullable=False)
    jabatan = mysql.Column(mysql.String)
    
    def __init__(self, username, password, jabatan):
        self.username = username
        self.password = pbkdf2_sha256.hash(password)
        self.jabatan = jabatan
        

    @classmethod
    def check_user(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    
