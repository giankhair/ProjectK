from flask import Blueprint, render_template, redirect, url_for, jsonify, session, flash
from sqlalchemy.exc import SQLAlchemyError
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from form import AnggotaForm, BarangForm, BrgMasukForm, BrgOutForm, LoginForm
from models import AnggotaModel, BarangModel, BrgMasukModel, BrgOutModel, UserModel
from models import mysql

pages = Blueprint('pages', __name__, template_folder="templates", static_folder="static")

@pages.get('/')
@pages.route("/<_id>", methods=["GET", "POST"])
def index(_id=None):
    
    if session.get("id_user") is None:
        return redirect(url_for('.login'))
    
    getMsk = BrgMasukModel.get_all()
    getOut = BrgOutModel.get_all()
    
    total1 = sum(entry.qty for entry in getMsk)
    total2 = sum(entry.qty for entry in getOut)
    
    harga1 = sum(entry.harga_beli * entry.qty for entry in getMsk)
    harga2 = sum(entry.harga_jual * entry.qty for entry in getOut)
    
    return render_template( 'index.html',  side = 'Home', t1=total1, t2=total2, h1=harga1, h2=harga2 )

# login
@pages.route("/login", methods=['GET', 'POST'])
def login():
    if session.get("username"):
        return redirect(url_for(".index"))

    form = LoginForm()

    if form.validate_on_submit():
        user_data = UserModel.get_user(form.username.data)

        if not user_data:
            flash("Login credentials not correct", category="error")
            return redirect(url_for(".login"))
    
        if user_data and pbkdf2_sha256.verify(form.password.data, user_data.password):
            session["id_user"] = user_data.id_user
            session["username"] = user_data.username
            session["jabatan"] = user_data.jabatan

            return redirect(url_for(".index"))

        flash("Login credentials not correct", "error")

    return render_template("login.html", form=form, side= 'Login' )


# logout
@pages.get("/logout")
def logout():
    session.clear()
    return redirect(url_for(".login"))


# regis
@pages.route("/registration", methods=["GET","POST"])
def reg():
    
    get_all_user = UserModel.get_all()
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            password = pbkdf2_sha256.encrypt(form.password.data)
            new_data = UserModel (form.username.data, form.password.data, form.jabatan.data)
            mysql.session.add(new_data)
            mysql.session.commit()
            
            return redirect(url_for('.login'))
        except SQLAlchemyError as ex:
            print(ex)
            mysql.session.rollback()
            
    return render_template("reg.html", form=form, data=get_all_user)



#  Fungsi untuk menampilkan Tabel Anggota
@pages.route("/anggota", methods=["GET","POST"])
def anggota():
    get_all_data = AnggotaModel.get_all()
    form = AnggotaForm()
    
    if form.validate_on_submit():
        if get_all_data:
            for i in get_all_data:
                if i.kode_anggota == form.kode_anggota.data:

                    return jsonify({'message': 'Kode Anggota Sudah Dipakai'}), 400        
        try:
            new_data = AnggotaModel(form.kode_anggota.data, form.nama_anggota.data, form.status.data, form.nik.data, form.bidang.data, form.keterangan.data)
            mysql.session.add(new_data)
            mysql.session.commit()
            
            return redirect(url_for('.anggota'))
        except SQLAlchemyError as ex:
            print(ex)
            mysql.session.rollback()
    
    return render_template("anggota.html", side = 'Anggota', form=form, data=get_all_data)


# Delete anggota
@pages.get("/anggota")
@pages.route("/anggota/<_id>", methods=['GET','POST'])
def deleteAnggota(_id=None):
    get_data_anggota = AnggotaModel.get_all()
    if _id is not None:
        deleteAnggota = AnggotaModel.get_by_id(_id)
        mysql.session.delete(deleteAnggota)
        mysql.session.commit()
        
        return redirect(url_for(".anggota"))

    return render_template("anggota.html", data=get_data_anggota)


# Edit Anggota
@pages.route('/anggota/edit/<_id>', methods=['GET', 'POST'] )
def editAnggota(_id):
    form = AnggotaForm()
    get_anggota_id = AnggotaModel.get_by_id(_id)
    if form.validate_on_submit():
        try:
            if form.kode_anggota.data != get_anggota_id.kode_anggota and form.kode_anggota.data is not None: get_anggota_id.kode_anggota = form.kode_anggota.data
            if form.nama_anggota.data != get_anggota_id.nama_anggota and form.nama_anggota.data is not None: get_anggota_id.nama_anggota = form.nama_anggota.data
            if form.status.data != get_anggota_id.status and form.status.data is not None: get_anggota_id.status = form.status.data
            if form.nik.data != get_anggota_id.nik and form.nik.data is not None: get_anggota_id.nik = form.nik.data
            if form.bidang.data != get_anggota_id.bidang and form.bidang.data is not None: get_anggota_id.bidang = form.bidang.data
            if form.keterangan.data != get_anggota_id.keterangan and form.keterangan.data is not None: get_anggota_id.keterangan = form.keterangan.data

            mysql.session.commit()
            
            return redirect(url_for('.anggota'))
        except SQLAlchemyError as x:
            print(x)
            mysql.session.rollback()
    return render_template("edit/edit-anggota.html", data=get_anggota_id, form=form)


# Tabel barang
@pages.route('/barang', methods=["GET","POST"])
def barang():
    get_all_data = BarangModel.get_all()
    form = BarangForm()
    
    if form.validate_on_submit():
        if get_all_data:
            try:
                new_data = BarangModel(form.nama_barang.data, form.satuan.data, form.harga_beli.data, form.harga_jual.data, form.stok_awal.data, form.keterangan.data)
                mysql.session.add(new_data)
                mysql.session.commit()
                
                return redirect(url_for('.barang'))
            except SQLAlchemyError as ex:
                print(ex)
                mysql.session.rollback()
            
    return render_template("barang.html", side="Barang", form=form, data=get_all_data)


# Edit barang
@pages.route('/barang/edit/<_id>', methods=['GET','POST'])
def editBarang(_id):
    get_barang_id = BarangModel.get_by_id(_id)
    form = BarangForm()
    
    if form.validate_on_submit():
        try:
            if form.nama_barang.data != get_barang_id.nama_barang and form.nama_barang.data is not None:
                get_barang_id.nama_barang = form.nama_barang.data
            if form.satuan.data != get_barang_id.satuan and form.satuan.data is not None:
                get_barang_id.satuan = form.satuan.data
            if form.harga_beli.data != get_barang_id.harga_beli and form.harga_beli.data is not None:
                get_barang_id.harga_beli = form.harga_beli.data
            if form.harga_jual.data != get_barang_id.harga_jual and form.harga_jual.data is not None:
                get_barang_id.harga_jual = form.harga_jual.data
            if form.stok_awal.data != get_barang_id.stok_awal and form.stok_awal.data is not None:
                get_barang_id.stok_awal = form.stok_awal.data
            if form.keterangan.data != get_barang_id.keterangan and form.keterangan.data is not None:
                get_barang_id.keterangan = form.keterangan.data

            mysql.session.commit()
            
            return redirect(url_for('.barang'))
        except SQLAlchemyError as x:
            print(x)
            mysql.session.rollback()
            
    return render_template("edit/edit-barang.html", side="Barang", form=form, data=get_barang_id)


# Delete barang
@pages.get("/barang")
@pages.route("/barang/<_id>", methods=['GET','POST'])
def deleteBarang(_id=None):
    get_data_barang = BarangModel.get_all()
    if _id is not None:
        deleteBarang = BarangModel.get_by_id(_id)
        mysql.session.delete(deleteBarang)
        mysql.session.commit()
        
        return redirect(url_for(".barang"))

    return render_template("barang.html", data=get_data_barang)


# tabel barang masuk
@pages.route("/barang/masuk", methods=["GET","POST"])
def barang_masuk():
    get_all_data = BrgMasukModel.get_all()
    form = BrgMasukForm()
    
    if form.validate_on_submit():
        if get_all_data:
            try:
                new_data = BrgMasukModel(form.tanggal_masuk.data, form.nama_barang.data, form.satuan.data, form.qty.data, form.harga_beli.data, form.distributor.data, form.keterangan.data)
                mysql.session.add(new_data)
                mysql.session.commit()
                
                return redirect(url_for('.barang_masuk'))
            except SQLAlchemyError as ex:
                print(ex)
                mysql.session.rollback()
                
    return render_template("barang-masuk.html", side ="Barang Masuk", data=get_all_data, form=form)


# edit brg masuk
@pages.route('/barang/masuk/edit/<_id>',methods=['GET','POST'] )  
def editBrgMasuk (_id):
    get_brgMasuk_id = BrgMasukModel.get_by_id(_id)
    form = BrgMasukForm()
    
    if form.validate_on_submit():
        try:
            if form.tanggal_masuk.data != get_brgMasuk_id.tanggal_masuk and form.tanggal_masuk.data is not None:
                get_brgMasuk_id.tanggal_masuk = form.tanggal_masuk.data
            if form.nama_barang.data != get_brgMasuk_id.nama_barang and form.nama_barang.data is not None:
                get_brgMasuk_id.nama_barang = form.nama_barang.data
            if form.satuan.data != get_brgMasuk_id.satuan and form.satuan.data is not None:
                get_brgMasuk_id.satuan = form.satuan.data
            if form.qty.data != get_brgMasuk_id.qty and form.qty.data is not None:
                get_brgMasuk_id.qty = form.qty.data
            if form.harga_beli.data != get_brgMasuk_id.harga_beli and form.harga_beli.data is not None:
                get_brgMasuk_id.harga_beli = form.harga_beli.data
            if form.distributor.data != get_brgMasuk_id.distributor and form.distributor.data is not None:
                get_brgMasuk_id.distributor = form.distributor.data
            if form.keterangan.data != get_brgMasuk_id.keterangan and form.keterangan.data is not None:
                get_brgMasuk_id.keterangan = form.keterangan.data
                
            mysql.session.commit()
            
            return redirect(url_for('.barang_masuk'))
        except SQLAlchemyError as x:
            print(x)
            mysql.session.rollback()

    return render_template("edit/edit-brgmasuk.html", side="Barang", form=form, data=get_brgMasuk_id)


# Delete barang masuk
@pages.get("/barang/masuk")
@pages.route("/barang/masuk/<_id>", methods=['GET','POST'])
def deleteBrgMasuk(_id=None):
    get_data_barang_msk = BrgMasukModel.get_all()
    if _id is not None:
        deleteBarang_msk = BrgMasukModel.get_by_id(_id)
        mysql.session.delete(deleteBarang_msk)
        mysql.session.commit()
        
        return redirect(url_for(".barang_masuk"))

    return render_template("barang-masuk.html", data=get_data_barang_msk)


# barang out
@pages.route("/barang/out", methods=["GET","POST"])
def barang_out():
    get_all_data = BrgOutModel.get_all()
    form = BrgOutForm()
    
    if form.validate_on_submit():
        try:
            new_data = BrgOutModel(form.tanggal_keluar.data, form.nama_barang.data, form.satuan.data, form.qty.data, form.harga_jual.data, form.customer.data, form.pembayaran.data, form.keterangan.data)
            mysql.session.add(new_data)
            mysql.session.commit()
            
            return redirect(url_for('.barang_out'))
        except SQLAlchemyError as ex:
                print(ex)
                mysql.session.rollback()
            
    return render_template("barang-out.html", side ="Barang", form=form, data=get_all_data)


@pages.route('/barang/out/edit/<_id>',methods=['GET','POST'] )  
def editBrgOut (_id):
    get_brgOut_id = BrgOutModel.get_by_id(_id)
    form = BrgOutForm()
    
    if form.validate_on_submit():
        try:
            if form.tanggal_keluar.data != get_brgOut_id.tanggal_keluar and form.tanggal_keluar.data is not None:
                get_brgOut_id.tanggal_keluar = form.tanggal_keluar.data
            if form.nama_barang.data != get_brgOut_id.nama_barang and form.nama_barang.data is not None:
                get_brgOut_id.nama_barang = form.nama_barang.data
            if form.satuan.data != get_brgOut_id.satuan and form.satuan.data is not None:
                get_brgOut_id.satuan = form.satuan.data
            if form.qty.data != get_brgOut_id.qty and form.qty.data is not None:
                get_brgOut_id.qty = form.qty.data
            if form.harga_jual.data != get_brgOut_id.harga_jual and form.harga_jual.data is not None:
                get_brgOut_id.harga_jual = form.harga_jual.data
            if form.customer.data != get_brgOut_id.customer and form.customer.data is not None:
                get_brgOut_id.customer = form.customer.data
            if form.pembayaran.data != get_brgOut_id.pembayaran and form.pembayaran.data is not None:
                get_brgOut_id.pembayaran = form.pembayaran.data
            if form.keterangan.data != get_brgOut_id.keterangan and form.keterangan.data is not None:
                get_brgOut_id.keterangan = form.keterangan.data

                
            mysql.session.commit()
            
            return redirect(url_for('.barang_out'))
        except SQLAlchemyError as x:
            print(x)
            mysql.session.rollback()

    return render_template("edit/edit-brgout.html", side="Barang", form=form, data=get_brgOut_id)


# Delete barang out
@pages.get("/barang/out")
@pages.route("/barang/out/<_id>", methods=['GET','POST'])
def deleteBrgOut(_id=None):
    get_data_barang_out = BrgOutModel.get_all()
    if _id is not None:
        deleteBarang_out = BrgOutModel.get_by_id(_id)
        mysql.session.delete(deleteBarang_out)
        mysql.session.commit()
        
        return redirect(url_for(".barang_out"))

    return render_template("barang-out.html", data=get_data_barang_out)


@pages.route("/pembayaran")
def pembayaran():
    get_data_barang_out = BrgOutModel.get_all()
    return render_template("pembayaran.html", side ="Barang", data=get_data_barang_out)

@pages.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404

@pages.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


        