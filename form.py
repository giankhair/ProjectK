from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, MultipleFileField, TextAreaField
from wtforms.validators import InputRequired

class AnggotaForm(FlaskForm):
    kode_anggota = StringField("Kode Anggota", validators= [InputRequired()])
    nama_anggota = StringField("Nama Anggota", validators= [InputRequired()])
    status = StringField("Status", validators= [InputRequired()])
    nik = IntegerField("NIK/NIP/NIS", validators= [InputRequired()])
    bidang = StringField("Bidang", validators= [InputRequired()])
    keterangan = StringField("Keterangan", validators= [InputRequired()])
    submit = SubmitField("Submit")
    
    
class BarangForm(FlaskForm):
    nama_barang = StringField("Nama Barang", validators=[InputRequired()])
    satuan = StringField("Satuan", validators=[InputRequired()])
    harga_beli = IntegerField("Harga Beli", validators=[InputRequired()])
    harga_jual = IntegerField("Harga Jual", validators=[InputRequired()])
    stok_awal = IntegerField("Stok Awal", validators=[InputRequired()])
    keterangan = StringField("Keterangan", validators=[InputRequired()])
    submit = SubmitField("Submit")


class BrgMasukForm(FlaskForm):
    tanggal_masuk = StringField("Tanggal Masuk", validators=[InputRequired()])
    nama_barang = StringField("Nama Barang", validators=[InputRequired()])
    satuan = StringField("Satuan", validators=[InputRequired()])
    qty = IntegerField("Qty", validators=[InputRequired()])
    harga_beli = IntegerField("Harga Beli", validators=[InputRequired()])
    distributor = StringField("Distributor", validators=[InputRequired()])
    keterangan = StringField("Keterangan", validators=[InputRequired()])
    submit = SubmitField("Submit")
    
    
class BrgOutForm(FlaskForm):
    tanggal_keluar = StringField("Tanggal Keluar", validators=[InputRequired()])
    nama_barang = StringField("Nama Barang", validators=[InputRequired()])
    satuan = StringField("Satuan", validators=[InputRequired()])
    qty = IntegerField("Qty", validators=[InputRequired()])
    harga_jual = IntegerField("Harga Jual", validators=[InputRequired()])
    customer = StringField("Customer", validators=[InputRequired()])
    pembayaran = StringField("Pembayaran", validators=[InputRequired()])
    keterangan = StringField("Keterangan", validators=[InputRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = StringField("Password")
    jabatan = StringField("Jabatan")
    submit = SubmitField("Login")