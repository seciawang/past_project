from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont
import locale
#import json
import mysql.connector
from datetime import *

DATABASE_HOST = "localhost"
DATABASE_USER = "root"
DATABASE_NAME = "Enyi_App_Database"
DATABASE_PASSWORD = "87654321"

try:
    db = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
    print("Connection to SQL established!\nConnection to Enyi_App_Database established!")

except Exception as error:
    print("Something happened! No connection to Database.\nAbort...")
    eexxiitt = input()
    exit()    

db_cursor = db.cursor()

def query_execute(query, val):

    db_cursor.reset()
    #db_cursor.reset()

    try:
        db_cursor.execute(query, val)
        return None
    except Exception as error:
        print("################\n", error, "\n################")
        return error

def query_executemany(query, val):

    try:
        db_cursor.executemany(query, val)
        return None
    except Exception as error:
        return error

#!!!except Exception as error:
#   create_window.database_error_toplevel(error)


#START AT 15 July 2023
#----Search Engine


locale.setlocale(locale.LC_ALL, 'en_US.utf8')

class Status:

    def __init__ (self,
                  capital_barang, capital_uang, uang_pribadi,
                  perputaran_toko_harian, perputaran_toko_bulanan, gross_profit,
                  pengeluaran_harian, pengeluaran_bulanan,
                  jumlah_prive):
        
        self.capital_barang = capital_barang
        self.capital_uang = capital_uang
        self.uang_pribadi = uang_pribadi
        self.perputaran_toko_harian =perputaran_toko_harian
        self.perputaran_toko_bulanan = perputaran_toko_bulanan
        self.gross_profit = gross_profit
        self.pengeluaran_harian = pengeluaran_harian
        self.pengeluaran_bulanan = pengeluaran_bulanan
        self.jumlah_prive = jumlah_prive

    def update(self):

        #Capital Barang
        loadfile("barang")
        self.capital_barang = 0
        for i in range(len(list_barang)):
            self.capital_barang = self.capital_barang + (list_barang[i].harga_pokok*list_barang[i].stock_sekarang)

    

class Barang:
    
    def __init__(self, id_barang, barang, kategori, harga_pokok, harga_jual, stock_sekarang, stock_reminder):

        self.id_barang = id_barang
        self.barang = barang
        self.kategori = kategori
        self.harga_pokok = harga_pokok
        self.harga_jual = harga_jual
        self.stock_sekarang = stock_sekarang
        self.stock_reminder = stock_reminder

    def print(self):

        print("id_barang: ", self.id_barang,
              "barang: ", self.barang,
              "kategori: ", self.kategori,
              "harga_pokok: ", self.harga_pokok,
              "harga_jual: ", self.harga_jual,
              "stock_sekarang: ", self.stock_sekarang,
              "stock_reminder: ", self.stock_reminder)

    def update_stock(self, quantity): #quantity can be - or +
        self.stock_sekarang += quantity

        #MENARIK UNTUK print(varBarang)... it will return that return.
        #def __str__(self):
        #    return f"{self.name}({self.age})"

class Kategori:

    def __init__(self, tipe, kategori):
        self.tipe = tipe
        self.kategori = kategori

class TRX_Toko:

    #constructor for classmethod
    def __init__(self, id_trx_toko, tipe, nama_barang, quantity, jumlah, tanggal):
        self.id_trx_toko = id_trx_toko
        self.tipe = tipe #Jual_Offline #Jual_Online #Beli #Operational
        self.nama_barang = nama_barang #bukan Class Barang
        self.quantity = quantity
        self.jumlah = jumlah
        self.tanggal = tanggal

    #init - jual/beli
    @classmethod
    def toko(cls, id_trx_toko, tipe, nama_barang, quantity, jumlah, tanggal):
        return cls(id_trx_toko, tipe, nama_barang, quantity, jumlah, tanggal)

    #init - operational (beli)
    @classmethod
    def operational(cls, id_trx_toko, tipe, nama_barang, jumlah, tanggal):
        return cls(id_trx_toko, tipe, nama_barang, None, jumlah, tanggal)

    #init - Incoming_Toko
    @classmethod
    def incoming_toko(cls, tipe, nama_barang, quantity, jumlah):
        return cls(None, tipe, nama_barang, quantity, jumlah, None)

    #init - Incoming_Operational
    @classmethod
    def incoming_operational(cls, tipe, nama_barang, jumlah):
        return cls(None, tipe, nama_barang, None, jumlah, None)
        

class Incoming_Toko:

    def __init__(self, id_incoming_toko, trx_toko, tanggal_incoming):
        self.id_incoming_toko = id_incoming_toko
        self.trx_toko = trx_toko #class TRX_Toko, tapi tidak punya [id_trx_toko, tanggal] (untuk Toko), dan tidak punya [id_trx_toko, quantity, tanggal] (untuk operational)
        
class Pengeluaran:

    def __init__(self, id_pengeluaran, pengeluaran):
        self.id_pengeluaran = id_pengeluaran
        self.pengeluaran = pengeluaran

class TRX_Pengeluaran:

    def __init__(self, id_trx_pengeluaran, nama_pengeluaran, jumlah, tanggal):
        self.id_trx_pengeluaran = id_trx_pengeluaran
        self.nama_pengeluaran = nama_pengeluaran #bukan Class Pengeluaran
        self.jumlah = jumlah
        self.tanggal = tanggal

    @classmethod
    def incoming(cls, nama_pengeluaran, jumlah):
        return cls(None, nama_pengeluaran, jumlah, None)

class Incoming_Pengeluaran:

    def __init__(self, id_incoming_pengeluaran, trx_pengeluaran, tanggal_incoming):
        self.id_incoming_pengeluaran = id_incoming_pengeluaran
        self.trx_pengeluaran = trx_pengeluaran #class TRX_Pengeluaran, tapi tidak ada [id_trx_pengeluaran, tanggal]
        self.tanggal_incoming = tanggal_incoming

#################
######################
######################
#################

def convert_id(id_barang_number, zero_count):

    str_id_barang_number = str(id_barang_number)

    while(len(str_id_barang_number)!=zero_count):
        str_id_barang_number = '0' + str_id_barang_number

    return str_id_barang_number


def backupfile(nama_file):

    date_now = datetime.now()
    date_file = str(date_now.year) + "_" + str(date_now.month) + "_" + str(date_now.day) + "--" + str(date_now.hour) + "_" + str(date_now.minute) + ".txt"

    if(nama_file == "all"):
        pass

    elif(nama_file == "status"):
        pass
    
    elif(nama_file == "barang"):

        #global list_barang
        #global FOLDER_DATA
        print("masuk backup barang")

        list_obj = list_barang

        file_str = nama_file + " " + date_file
        file = open(FOLDER_DATA+"\\"+ file_str, "w")

        #if("GT" in barang.id_barang):
        for obj in list_obj:
            
            file.write(obj.id_barang + "\t" + obj.barang + "\t" + obj.kategori + "\t" +
                                 str(obj.harga_pokok) + "\t" + str(obj.harga_jual) + "\t" +
                                 str(obj.stock_sekarang) + "\t" + str(obj.stock_reminder) + "\n")
            
        file.close()
        # elif("PI" in barang.id_barang):
        #     file_barang_pi = open(FOLDER_DATA+"\\barang_pi.txt", "a")
        #     file_barang_pi.write(barang.id_barang + "\t" + barang.barang + "\t" + barang.kategori + "\t" +
        #                          barang.harga_pokok + "\t" + barang.harga_jual + "\t" +
        #                          barang.stock_sekarang + "\t" + barang.stock_reminder + "\n")
        #     file_barang_pi.close()   
    
    elif(nama_file == "kategori"):

        print("masuk backup kategori")

        list_obj = list_kategori_special_object

        file_str = nama_file + " " + date_file
        file = open(FOLDER_DATA+"\\"+ file_str, "w")

        #if("GT" in barang.id_barang):
        for obj in list_obj:
            
            file.write(obj.tipe + "\t" + obj.kategori + "\t" + "\n")
            
        file.close()

    elif(nama_file == "trx_toko"):
        pass

    elif(nama_file == "incoming_toko"):
        pass

    elif(nama_file == "pengeluaran"):
        pass

    elif(nama_file == "trx_pengeluaran"):
        pass
    
    elif(nama_file == "trx_incoming_pengeluaran"):
        pass

def loadfile(nama_file):

    #edit status (variable class), and also individual variable

    # if(nama_file == "all"):
    #     file_barang_gt = open(FOLDER_DATA+"\\barang_gt.txt", "r")
    #     file_barang_pi = open(FOLDER_DATA+"\\barang_pi.txt", "r")

    #     #first readline = password dummy
    #     barang_gt = file_barang_gt.readline()
    #     barang_pi = file_barang_pi.readline()

    #     while(barang_gt!=""):
    #         barang_gt = file_barang_gt.readline()
    #         print(barang_gt)

    #         if(barang_gt==""):
    #             break

    #         barang_gt = barang_gt[0:-1].split("\t")

    #         barang = Barang(barang_gt[0], barang_gt[1], barang_gt[2], barang_gt[3],
    #                         barang_gt[4], barang_gt[5], barang_gt[6])
    #         list_barang.append(barang)

    #     while(barang_pi!=""):
    #         barang_pi = file_barang_pi.readline()
    #         print(barang_pi)

    #         if(barang_pi==""):
    #             break

    #         barang_pi = barang_pi[0:-1].split("\t")

    #         barang = Barang(barang_pi[0], barang_pi[1], barang_pi[2], barang_pi[3],
    #                         barang_pi[4], barang_pi[5], barang_pi[6])
    #         list_barang.append(barang)

    #     file_barang_gt.close()
    #     file_barang_pi.close()

    if(nama_file == "all"):
        loadfile("status") #i dont think this is needed
        loadfile("barang")
        loadfile("kategori")
        loadfile("trx_toko")
        loadfile("incoming_toko")
        loadfile("pengeluaran")
        loadfile("trx_pengeluaran")
        loadfile("trx_incoming_pengeluaran")
    
    elif(nama_file == "status"):
        pass
    
    elif(nama_file == "barang"):

        global list_barang
        list_barang = []

        q = query_execute("SELECT * FROM barang","")
        if(q != None):
            return

        db_barang = db_cursor.fetchall()
        print("\nPRCHECK db_barang: ", db_barang, "\n")

        for i in range(len(db_barang)):
            if("GT" in db_barang[i][1]):
                list_barang.append(Barang(db_barang[i][1], db_barang[i][2], db_barang[i][3], db_barang[i][4], db_barang[i][5], db_barang[i][6], db_barang[i][7]))
        for i in range(len(db_barang)):
            if("PI" in db_barang[i][1]):
                list_barang.append(Barang(db_barang[i][1], db_barang[i][2], db_barang[i][3], db_barang[i][4], db_barang[i][5], db_barang[i][6], db_barang[i][7]))

    elif(nama_file == "kategori"):

        global list_kategori_gt
        global list_kategori_pi
        global list_kategori_special_object
        list_kategori_gt = []
        list_kategori_pi = []
        list_kategori_special_object = []

        q = query_execute("SELECT * FROM kategori","")
        if(q != None):
            return    

        db_barang = db_cursor.fetchall()
        print("\nPRCHECK db_barang in kategori: ", db_barang, "\n")

        for i in range(len(db_barang)):
            list_kategori_special_object.append(Kategori(db_barang[i][1], db_barang[i][2]))
            if(db_barang[i][1]=="GT"):
                list_kategori_gt.append(db_barang[i][2])
            elif(db_barang[i][1]=="PI"):
                list_kategori_pi.append(db_barang[i][2])

    elif(nama_file == "trx_toko"):
        pass

    elif(nama_file == "incoming_toko"):
        pass

    elif(nama_file == "pengeluaran"):
        pass

    elif(nama_file == "trx_pengeluaran"):
        pass
    
    elif(nama_file == "trx_incoming_pengeluaran"):
        pass

def check_last_update():
    #if
    return False

    #else
    #return True

    #or actually
    #return date2-date1





        
def scrollable_list(array, mode): #will always show at specific grid, to the most right maybe, so it can expand
    #mode indicate "selecting/searching", or "reading/not active"
    #maybe update later: reading/not active can press to have a menu for update/delete
    #actually lets do that instead! Search it, click it, pick update name/update reminder/delete/add stock
    #or actually just: update/delete (update will show Entry for every attribute)

    #show detail of every scrollable list.... and search system not only by name, but by id too and everything else. There will be detail at the bottom of whatever you search.
    pass






def transaksi_beli(tipe, nama_barang, quantity, jumlah):
    #tanggal di dalam
    #penentuan ID Format juga disini

    #savefile("trx_toko")
    pass

def transaksi_jual(tipe, nama_barang, quantity, jumlah):

    #savefile("trx_toko")
    pass

def transaksi_add_incoming(tipe, nama_barang, quantity, jumlah, tanggal_incoming):
    #ID incoming here
    #dari parameter dibuat jadi incoming TRX_Toko..incoming_toko()... dimana trx_toko adalah kelas

    #savefile("incoming_toko")
    pass


def add_barang(barang):

    id_barang_number = -1
    
    for i in reversed(range(len(list_barang))):
        if(barang.id_barang in list_barang[i].id_barang):
            id_barang_number = int(list_barang[i].id_barang[2:]) + 1
            break

    if(id_barang_number==-1):
        barang.id_barang += "001"
    else:
        barang.id_barang += convert_id(id_barang_number, 3)

    sql = "INSERT INTO barang (id_barang, barang, kategori, harga_pokok, harga_jual, stock_sekarang, stock_reminder) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (barang.id_barang, barang.barang, barang.kategori, barang.harga_pokok, barang.harga_jual, barang.stock_sekarang, barang.stock_reminder)
    query_execute(sql, val)

    kategori_exist = False

    if("GT" in barang.id_barang):
        list_kategori_target = list_kategori_gt
    elif("PI" in barang.id_barang):
        list_kategori_target = list_kategori_pi
    
    for i in range(len(list_kategori_target)):
        if(list_kategori_target[i]==barang.kategori):
            kategori_exist = True
            break

    if(not kategori_exist):
        sql = "INSERT INTO kategori (tipe, kategori) VALUES (%s, %s)"
        val = (barang.id_barang[0:2], barang.kategori)
        query_execute(sql, val)
        print("QUERY ALSO EXECUTED FOR KATEGORI! FROM add_barang()")
        
        loadfile("kategori")
        backupfile("kategori")
        

    db.commit()
    
    print("success add barang!")

    loadfile("barang")
    backupfile("barang")
    #status.update()

    create_window.success_toplevel("Add Barang")
    

def update_barang(barang_target, barang):

    print("barang_target, barang: ", barang_target.id_barang, barang.id_barang)
    
    if(barang_target.id_barang != barang.id_barang):
        id_barang_number = -1
        
        for i in reversed(range(len(list_barang))):
            if(barang.id_barang in list_barang[i].id_barang):
                id_barang_number = int(list_barang[i].id_barang[2:]) + 1
                break

        if(id_barang_number==-1):
            barang.id_barang += "001"
        else:
            barang.id_barang += convert_id(id_barang_number, 3)

    sql = "UPDATE barang SET id_barang = %s, barang = %s, kategori = %s, harga_pokok = %s, harga_jual = %s, stock_sekarang = %s, stock_reminder = %s WHERE id_barang = %s"
    val = (barang.id_barang, barang.barang, barang.kategori, barang.harga_pokok, barang.harga_jual, barang.stock_sekarang, barang.stock_reminder, barang_target.id_barang)
    query_execute(sql, val)
    db.commit()

    
    #status.update()

    kategori_old_exist = False
    kategori_new_exist = False

    for i in range(len(list_barang)):

        if(list_barang[i].kategori == barang.kategori):
            kategori_new_exist = True
            break 

    loadfile("barang")  
    backupfile("barang")

    for i in range(len(list_barang)):

        if(list_barang[i].kategori == barang_target.kategori):
            kategori_old_exist = True
            break

    if(not kategori_new_exist):
        sql = "INSERT INTO kategori (tipe, kategori) VALUES (%s, %s)"
        val = (barang.id_barang[0:2], barang.kategori)
        query_execute(sql, val)

        db.commit()
        print("QUERY ALSO EXECUTED FOR KATEGORI! FROM add_barang()")
        backupfile("kategori") 

    if(not kategori_old_exist):
        sql = "DELETE FROM kategori WHERE kategori = %s"
        val = (barang_target.kategori,)
        query_execute(sql, val)

        db.commit()
        print("ALSO DELETED KATEGORI_OLD BECAUSE NONE EXIST")
        backupfile("kategori") 

    print("kategori_old, kategori_new, ",kategori_old_exist, kategori_new_exist)    
    print("barang.id", barang.id_barang)

    create_window.success_toplevel("Update Barang")

    # index_update = -1

    # for i in range(len(list_barang)):
    #     if(barang_target.id_barang == list_barang[i].id_barang and barang_target.barang == list_barang[i].barang):
    #         index_update = i
    #         break

    # #!!!actually update in Database okay!
    # print("Update index: ", index_update)

def delete_barang(barang):

    sql = "DELETE FROM barang WHERE id_barang = %s"
    val = (barang.id_barang,)
    query_execute(sql, val)
    
    db.commit()

    
    #status.update()
    loadfile("barang")
    backupfile("barang")

    kategori_exist = False

    for i in range(len(list_barang)):
        if(list_barang[i].kategori == barang.kategori):
            kategori_exist = True
            break

    if(not kategori_exist):
        sql = "DELETE FROM kategori WHERE kategori = %s"
        val = (barang.kategori,)
        query_execute(sql, val)

        db.commit()
        print("ALSO DELETED KATEGORI BECAUSE NONE EXIST")
        backupfile("kategori")


    print("success delete barang!")
    create_window.success_toplevel("Delete Barang")

    # index_delete = -1

    # for i in range(len(list_barang)):
    #     if(barang.id_barang == list_barang[i].id_barang and barang.barang == list_barang[i].barang):
    #         index_delete = i
    #         break

    # print("Deleted index: ", index_delete)

    # if("GT" in barang.id_barang):
    #     pass
    #     print("masuk GT")
    #     # file_barang_gt = open(FOLDER_DATA+"\\barang_gt.txt", "a")
    #     # file_barang_gt.write(barang.id_barang + "\t" + barang.barang + "\t" +
    #     #                      barang.harga_pokok + "\t" + barang.harga_jual + "\t" +
    #     #                      barang.stock_sekarang + "\t" + barang.stock_reminder + "\n")
    #     # file_barang_gt.close()

    # elif("PI" in barang.id_barang):
    #     pass
    #     # file_barang_pi = open(FOLDER_DATA+"\\barang_pi.txt", "a")
    #     # file_barang_pi.write(barang.id_barang + "\t" + barang.barang + "\t" +
    #     #                      barang.harga_pokok + "\t" + barang.harga_jual + "\t" +
    #     #                      barang.stock_sekarang + "\t" + barang.stock_reminder + "\n")
    #     # file_barang_pi.close()       

    # #!!!actually delete the barang from database
    # #!!!update total capital

    # list_barang.pop(index_delete)

def update_incoming_barang(target_id_incoming_toko, id_incoming_toko, trx_toko, tanggal_incoming):
    #update tujuan with new parameter
    
    #savefile("incoming_toko")
    pass

def delete_incoming_barang(id_incoming_toko):
    #savefile("incoming_toko")
    pass






def pembayaran_pengeluaran(nama_pengeluaran, jumlah):
    #ID dan tanggal here

    #savefile("trx_pengeluaran")
    pass

def pembayaran_add_incoming(nama_pengeluaran, jumlah, tanggal_incoming):
    #ID incoming here
    #dari parameter dibuat jadi TRX_Pengeluaran

    #savefile("incoming_pengeluaran")
    pass

def update_pengeluaran(target_nama_pengeluaran, id_pengeluaran, pengeluaran):
    #update tujuan with new parameter

    #savefile("pengeluaran")
    pass

def delete_pengeluaran(nama_pengeluaran):
    #savefile("pengeluaran")
    pass

#id_incoming_toko, trx_toko, tanggal_incoming):
def update_incoming_pengeluaran(target_id_incoming_pengeluaran, id_incoming_pengeluaran, trx_pengeluaran, tanggal_incoming):
    #update tujuan with new parameter
    
    #savefile("incoming_pengeluaran")
    pass

def delete_incoming_pengeluaran(id_incoming_pengeluaran):
    #savefile("incoming_pengeluaran")
    pass


 ######################################################
 ######################################################
 ######################################################
 ######################################################

'''
def g_cf(var_grid, ):
    for i in var_grid:
'''

class create_window:

    def __init__(self, window_name):
        self.window_name = window_name

    def hide_content():
        f_content.grid_remove()
        f_content_toko.grid_remove()

    def hide_main_menu():
        f_main_menu.grid_remove()
        f_toko_main_menu.grid_remove()
        f_pengeluaran_main_menu.grid_remove() 

    def hide_toko_sub_menu():
        f_toko_barang.grid_remove()
        f_toko_barang_add.grid_remove()
        f_toko_barang_update.grid_remove()
        f_toko_transaksi.grid_remove()
        f_toko_beli.grid_remove()
        f_toko_beli_barang.grid_remove()
        f_toko_beli_operational.grid_remove()
        f_toko_jual.grid_remove()

    def hide_pengeluaran_sub_menu():
        pass

    def show_main_menu():
        f_content.grid(row=0, column=0, sticky=(N, S, E, W))
        f_content.rowconfigure(0, weight=1)
        f_content.columnconfigure(0, weight=1)
        #f_content.columnconfigure(1, weight=1)
        f_main_menu.grid()
        print("showminamenu")

    def show_toko_main_menu():
        f_content_toko.grid(row=0, column=0, sticky=(N, S, E, W))
        #f_content_toko.rowconfigure(0, weight=1)
        #f_content_toko.columnconfigure(0, weight=1)
        f_toko_main_menu.grid()

    def show_toko_barang():
        f_toko_barang.grid(row=0, column=COLUMN_SUB_MENU, sticky=(N,S,W,E))
        #f_toko_main_menu.grid(sticky=(N,S,E,W))
        f_toko_barang.columnconfigure((0,1,2), weight=1)
        #f_content_toko.columnconfigure(1, weight=1)

    def show_toko_barang_add():
        f_toko_barang_add.grid(row=0, column=COLUMN_SUB_MENU, sticky=(N,S,W,E))
        #f_toko_main_menu.grid(sticky=(N,S,E,W))
        f_toko_barang.columnconfigure((0,1,2), weight=1)
        #f_content_toko.columnconfigure(1, weight=1)

    def show_toko_barang_update():
        f_toko_barang_update.grid(row=0, column=COLUMN_SUB_MENU, sticky=(N,S,W,E))
        f_toko_barang.columnconfigure((0,1,2), weight=1)

    @classmethod
    def success_toplevel(cls, msg):
        top_success = Toplevel()
        top_success.grab_set()
        top_success.focus_set()

        top_success.geometry("+600+340")
        top_success.config(bg="green")
        top_success.overrideredirect(1)

        l_msg = Label(top_success, text=msg+" Success!", borderwidth=5, relief="raised")
        #l_msg.config(bg="green")
        l_msg.grid(row=0, column=0, sticky=NSEW, pady=50, padx=100)

        var = IntVar()
        top_success.after(1000, var.set, 1)
        top_success.wait_variable(var)
        top_success.destroy()

    @classmethod
    def exit_menu(cls):
        root.destroy()

    @classmethod
    def main_menu(cls):

        status.update()

        cls.hide_content()
        cls.hide_main_menu()
        cls.hide_toko_sub_menu()
        cls.hide_pengeluaran_sub_menu()
        cls.show_main_menu()
        f_main_menu.focus_set()

        root.geometry('400x600+540+100')

        font_main_menu = tkFont.Font(family="Times New Roman", size=20)
        style_toko = Style(root)
        style_toko.configure("TButton", font=font_main_menu)       
        
        l_title = Label(f_main_menu, text = "Enyi_App_Desu!", font=tkFont.Font(family="Times New Roman", size=32, weight="bold"))
        

        btn_toko = Button(f_main_menu, width=19,text="Toko", command=create_window.toko_main_menu)
        btn_pengeluaran = Button(f_main_menu, width=19, text="Pengeluaran Pribadi", state="disabled")
        btn_exit = Button(f_main_menu, width=19, text="Exit~", command=create_window.exit_menu)

        f_temp_capital_barang = Frame(f_main_menu)
        l_temp_capital_barang = Label(f_temp_capital_barang, text="Capital Barang: ")
        l_temp_capital_barang_int = Label(f_temp_capital_barang, text="Rp. " + locale.format_string("%d", int(status.capital_barang), grouping=True))

        l_title.grid(row=0, column=0, columnspan=3, pady=20, padx=20)

        btn_toko.grid(row=1, column=1,pady=(0,5))
        btn_pengeluaran.grid(row=2, column=1)
        btn_exit.grid(row=3, column=1, pady=20)
        f_temp_capital_barang.grid(row=4, column=1)

        l_temp_capital_barang.grid(row=0, column=0)
        l_temp_capital_barang_int.grid(row=0, column=1)
        

        #g_cf()
        #g_rf()
        #show grid main_menu
    
    @classmethod
    def toko_main_menu(cls):

        cls.hide_content
        cls.hide_toko_sub_menu()
        cls.hide_main_menu()
        cls.show_toko_main_menu()
        f_toko_main_menu.focus_set()

        root.geometry('1920x1080+0+0')
        root.geometry("281x502+195+149")

        font_toko = tkFont.Font(family="Comic Sans MS", size=20)
        style_toko = Style(root)
        style_toko.configure("TButton", font=font_toko)

        l_title = Label(f_toko_main_menu, text = "Toko", font=tkFont.Font(family="Comic Sans MS", size=32, weight="bold"))
        
        btn_barang = Button(f_toko_main_menu, text="Barang", command=create_window.toko_barang)
        btn_transaksi = Button(f_toko_main_menu, text="Transaksi", state="disabled")
        btn_beli = Button(f_toko_main_menu, text="Beli", state="disabled")
        btn_jual = Button(f_toko_main_menu, text="Jual", command=lambda:print(root.geometry()), state="disabled")
        btn_go_back = Button(f_toko_main_menu, text="Main Menu", command=create_window.main_menu)
        btn_exit = Button(f_toko_main_menu, text="Exit", command=create_window.exit_menu)
        #btn_barang['font']=font_toko
        #jual... you can actually pick from multiple option or something
        #waktu pilih operasional ... other entry will be blocked

        #btn_barang.configure(font=font_toko)
        l_title.grid(row=0, column=0, columnspan=3, pady=20, padx=80)
        btn_barang.grid(row=1, column=1)
        btn_transaksi.grid(row=2, column=1)
        btn_beli.grid(row=3, column=1, pady=(20,0))
        btn_jual.grid(row=4, column=1)
        btn_go_back.grid(row=5, column=1, pady=20)
        btn_exit.grid(row=6, column=1, pady=(0,30))
        print("im at the toko_main_menu!")

    @classmethod
    def toko_barang(cls): #disini bisa macam macam, langsung delete disini. kalau pilih update baru ke barang_update
        
        #def yview_all(x,y):
        #    lb_barang.yview(x,y)
        #    lb_barang.yview

        # def scroll_sync(x1,x2):
        #     event=(x1,x2)
        #     #print(event)
        #     scrollbar.set(x1,x2)
        #     lb_id_barang.yview_scroll(int(-4*(event.delta/120)), "units")

        cls.hide_toko_sub_menu()
        cls.show_toko_barang()
        f_toko_barang.focus_set()
        root.geometry("1275x498")#+195+149")

        loadfile("barang")
        loadfile("kategori")

        def scroll_sync(event, lb_trigger):
            if(lb_trigger!=lb_id_barang):
                lb_id_barang.yview_scroll(int(-4*(event.delta/120)), "units")
            if(lb_trigger!=lb_barang):
                lb_barang.yview_scroll(int(-4*(event.delta/120)), "units")
            if(lb_trigger!=lb_kategori):
                lb_kategori.yview_scroll(int(-4*(event.delta/120)), "units")
            if(lb_trigger!=lb_harga_pokok):
                lb_harga_pokok.yview_scroll(int(-4*(event.delta/120)), "units")
            if(lb_trigger!=lb_harga_jual):
                lb_harga_jual.yview_scroll(int(-4*(event.delta/120)), "units")
            if(lb_trigger!=lb_stock_sekarang):
                lb_stock_sekarang.yview_scroll(int(-4*(event.delta/120)), "units")
            if(lb_trigger!=lb_stock_reminder):
                lb_stock_reminder.yview_scroll(int(-4*(event.delta/120)), "units")
            print(event)

        l_title = Label(f_toko_barang, text = "Daftar Barang", font=tkFont.Font(family="Comic Sans MS", size=28, weight="bold"))
    
        f_lb = Frame(f_toko_barang)
        scrollbar = Scrollbar(f_lb, orient=VERTICAL)
        l_id_barang = Label(f_lb, text="ID", font=(14))
        l_barang = Label(f_lb, text="Nama Barang", font=(14))
        l_kategori = Label(f_lb, text="Kategori", font=(14))
        l_harga_pokok = Label(f_lb, text="Harga Pokok", font=(14))
        l_harga_jual = Label(f_lb, text="Harga Jual", font=(14))
        l_stock_sekarang = Label(f_lb, text="Stock Sekarang", font=(14))
        l_stock_reminder = Label(f_lb, text="Stock Reminder", font=(14))
        lb_id_barang = Listbox(f_lb, selectbackground=SELECT_BACKGROUND_COLOR, yscrollcommand=scrollbar.set, exportselection=0, selectmode=BROWSE, height=12, cursor="tcross", font=(18), width=6)
        lb_barang = Listbox(f_lb, selectbackground=SELECT_BACKGROUND_COLOR, yscrollcommand=scrollbar.set, exportselection=0, selectmode=BROWSE, height=12, cursor="tcross", font=(18), width=40)
        lb_kategori = Listbox(f_lb, selectbackground=SELECT_BACKGROUND_COLOR, yscrollcommand=scrollbar.set, exportselection=0, selectmode=BROWSE, height=12, cursor="tcross", font=(18), width=12)
        lb_harga_pokok = Listbox(f_lb, selectbackground=SELECT_BACKGROUND_COLOR, yscrollcommand=scrollbar.set, exportselection=0, selectmode=BROWSE, height=12, cursor="tcross", font=(18), width=12)
        lb_harga_jual = Listbox(f_lb, selectbackground=SELECT_BACKGROUND_COLOR, yscrollcommand=scrollbar.set, exportselection=0, selectmode=BROWSE, height=12, cursor="tcross", font=(18), width=12)
        lb_stock_sekarang = Listbox(f_lb, selectbackground=SELECT_BACKGROUND_COLOR, yscrollcommand=scrollbar.set, exportselection=0, selectmode=BROWSE, height=12, cursor="tcross", font=(18), width=14)
        lb_stock_reminder = Listbox(f_lb, selectbackground=SELECT_BACKGROUND_COLOR, yscrollcommand=scrollbar.set, exportselection=0, selectmode=BROWSE, height=12, cursor="tcross", font=(18), width=14)
        #scrollbar.config(command=yview_all)

        for i in range(len(list_barang)):
            lb_id_barang.insert(END, list_barang[i].id_barang)
            lb_barang.insert(END, list_barang[i].barang)
            lb_kategori.insert(END, list_barang[i].kategori)
            lb_harga_pokok.insert(END, "Rp. " + locale.format_string("%d", int(list_barang[i].harga_pokok), grouping=True))
            lb_harga_jual.insert(END, "Rp. " + locale.format_string("%d", int(list_barang[i].harga_jual), grouping=True))
            lb_stock_sekarang.insert(END, list_barang[i].stock_sekarang)
            lb_stock_reminder.insert(END, list_barang[i].stock_reminder)

        #l_search = Label(f_toko_barang, text="") #????
        
        def callback_select(event):
            selection = event.widget.curselection()
            print(selection)
            if selection:

                lb_id_barang.selection_clear(0, END)
                lb_id_barang.selection_set(selection)
                lb_barang.selection_clear(0, END)
                lb_barang.selection_set(selection)
                lb_kategori.selection_clear(0, END)
                lb_kategori.selection_set(selection)
                lb_harga_pokok.selection_clear(0, END)
                lb_harga_pokok.selection_set(selection)
                lb_harga_jual.selection_clear(0, END)
                lb_harga_jual.selection_set(selection)
                lb_stock_sekarang.selection_clear(0, END)
                lb_stock_sekarang.selection_set(selection)
                lb_stock_reminder.selection_clear(0, END)
                lb_stock_reminder.selection_set(selection)

                select = lb_barang.curselection()
                print(lb_id_barang.get(select))
                print(select)
                print(lb_barang.get(select))
                if(lb_barang.get(select) == ""):
                    return
                btn_update['state']="enable"
                btn_delete['state']="enable"
                #entry_search.focus_set()
                print(root.focus_get())
                #sv.set(lb_barang.get(select))
                #lb_barang.delete(0, END) #DELETE ALL THE LIST
                
                #Lb1.grid_remove()
            else:
                pass
                #label.configure(text="")
        
        lb_id_barang.bind("<MouseWheel>", lambda event: scroll_sync(event, lb_id_barang))
        lb_barang.bind("<MouseWheel>", lambda event: scroll_sync(event, lb_barang))
        lb_kategori.bind("<MouseWheel>", lambda event: scroll_sync(event, lb_kategori))
        lb_harga_pokok.bind("<MouseWheel>", lambda event: scroll_sync(event, lb_harga_pokok))
        lb_harga_jual.bind("<MouseWheel>", lambda event: scroll_sync(event, lb_harga_jual))
        lb_stock_sekarang.bind("<MouseWheel>", lambda event: scroll_sync(event, lb_stock_sekarang))
        lb_stock_reminder.bind("<MouseWheel>", lambda event: scroll_sync(event, lb_stock_reminder))
        lb_id_barang.bind("<<ListboxSelect>>", callback_select)
        lb_barang.bind("<<ListboxSelect>>", callback_select)
        lb_kategori.bind("<<ListboxSelect>>", callback_select)
        lb_harga_pokok.bind("<<ListboxSelect>>", callback_select)
        lb_harga_jual.bind("<<ListboxSelect>>", callback_select)
        lb_stock_sekarang.bind("<<ListboxSelect>>", callback_select)
        lb_stock_reminder.bind("<<ListboxSelect>>", callback_select)
        lb_id_barang.bind("<FocusIn>", lambda Event: entry_search.focus_set())
        lb_barang.bind("<FocusIn>", lambda Event: entry_search.focus_set())
        lb_kategori.bind("<FocusIn>", lambda Event: entry_search.focus_set())
        lb_harga_pokok.bind("<FocusIn>", lambda Event: entry_search.focus_set())
        lb_harga_jual.bind("<FocusIn>", lambda Event: entry_search.focus_set())
        lb_stock_sekarang.bind("<FocusIn>", lambda Event: entry_search.focus_set())
        lb_stock_reminder.bind("<FocusIn>", lambda Event: entry_search.focus_set())
        #lb_barang.bind('<Button-1>', lambda Event: entry_search.focus_set())

        def callback_keystroke(sv_entry_search):
            #if(Lb1.winfo_ismapped()==False):
            #    Lb1.grid()
            #    print("restored!")
            lb_id_barang.delete(0, END)
            lb_barang.delete(0, END)
            lb_kategori.delete(0, END)
            lb_harga_pokok.delete(0, END)
            lb_harga_jual.delete(0, END)
            lb_stock_sekarang.delete(0, END)
            lb_stock_reminder.delete(0, END)

            btn_update['state']="disabled"
            btn_delete['state']="disabled"
            search_query = sv_entry_search.get()

            #!!!make the search system for certain part (By name, By category, by harga, by stock, by stock reminder)... actually just by name, and you can sort by any other
            #!!!list_search = list_barang[i]

            for i in range(len(list_barang)): #range barang
                if search_query.lower() in list_barang[i].barang.lower():
                    lb_id_barang.insert(END, list_barang[i].id_barang)
                    lb_barang.insert(END, list_barang[i].barang)
                    lb_kategori.insert(END, list_barang[i].kategori)
                    lb_harga_pokok.insert(END, "Rp. " + str(list_barang[i].harga_pokok))
                    lb_harga_jual.insert(END, "Rp. " + str(list_barang[i].harga_jual))
                    lb_stock_sekarang.insert(END, list_barang[i].stock_sekarang)
                    lb_stock_reminder.insert(END, list_barang[i].stock_reminder)
            #print (sv.get())

        sv_entry_search = StringVar()
        sv_entry_search.trace("w", lambda name, index, mode, sv=sv_entry_search: callback_keystroke(sv))

        f_entry = Frame(f_toko_barang)
        l_entry = Label(f_entry, text="Search: ")
        entry_search = Entry(f_entry, textvariable=sv_entry_search, width=24)

        def bridge_toko_barang_update_toplevel():

            curselection = lb_id_barang.curselection()

            int_harga_pokok = lb_harga_pokok.get(curselection).replace("Rp.", "")
            int_harga_pokok = int_harga_pokok.replace(",", "")
            int_harga_pokok = int(int_harga_pokok.replace(" ", ""))

            print("INT HARGA POKOK: ", int_harga_pokok)

            int_harga_jual = lb_harga_jual.get(curselection).replace("Rp.", "")
            int_harga_jual = int_harga_jual.replace(",", "")
            int_harga_jual = int(int_harga_jual.replace(" ", ""))

            barang = Barang(lb_id_barang.get(curselection), lb_barang.get(curselection),lb_kategori.get(curselection), int_harga_pokok, int_harga_jual,
                            lb_stock_sekarang.get(curselection), lb_stock_reminder.get(curselection))
            
            create_window.toko_barang_update(barang)

            
        def bridge_toko_barang_delete_toplevel():
            curselection = lb_id_barang.curselection()

            int_harga_pokok = lb_harga_pokok.get(curselection).replace("Rp.", "")
            int_harga_pokok = int_harga_pokok.replace(",", "")
            int_harga_pokok = int(int_harga_pokok.replace(" ", ""))

            print("INT HARGA POKOK: ", int_harga_pokok)

            int_harga_jual = lb_harga_jual.get(curselection).replace("Rp.", "")
            int_harga_jual = int_harga_jual.replace(",", "")
            int_harga_jual = int(int_harga_jual.replace(" ", ""))

            barang = Barang(lb_id_barang.get(curselection), lb_barang.get(curselection), lb_kategori.get(curselection), int_harga_pokok, int_harga_jual,
                            lb_stock_sekarang.get(curselection), lb_stock_reminder.get(curselection))
            
            create_window.toko_barang_delete_toplevel(barang)

        f_btn = Frame(f_toko_barang)
        btn_add = Button(f_btn, text="Add", command=create_window.toko_barang_add)
        btn_update = Button(f_btn, state="disabled", text="Update", command=bridge_toko_barang_update_toplevel)
        btn_delete = Button(f_btn, state="disabled", text="Delete", command=bridge_toko_barang_delete_toplevel)
        #command=lambda:print(lb_barang.get(lb_barang.curselection()))

        l_title.grid(row=0, column=1, pady=(10,0))

        f_lb.grid(row=1, column=0, pady=10, padx=30, columnspan=3)
        l_id_barang.grid(row=0, column=0, sticky=W)
        l_barang.grid(row=0, column=1, sticky=W)
        l_kategori.grid(row=0, column=2, sticky=W)
        l_harga_pokok.grid(row=0, column=3, sticky=W)
        l_harga_jual.grid(row=0, column=4, sticky=W)
        l_stock_sekarang.grid(row=0, column=5, sticky=W)
        l_stock_reminder.grid(row=0, column=6, sticky=W)
        lb_id_barang.grid(row=1, column=0)
        lb_barang.grid(row=1, column=1)
        lb_kategori.grid(row=1, column=2)
        lb_harga_pokok.grid(row=1, column=3)
        lb_harga_jual.grid(row=1, column=4)
        lb_stock_sekarang.grid(row=1, column=5)
        lb_stock_reminder.grid(row=1, column=6)
        scrollbar.grid(row=1, column=7, sticky=(N,S))

        f_entry.grid(row=2, column=1)
        l_entry.grid(row=0, column=0)
        entry_search.grid(row=0, column=1)

        f_btn.grid(row=3, column=1, padx=10)
        btn_add.grid(row=0, column=0, padx=(0,80))
        btn_update.grid(row=0, column=1, pady=20)   #f_btn
        btn_delete.grid(row=0, column=2)            #f_btn

    @classmethod
    def toko_barang_add(cls):

        def bridge_toko_barang_add_toplevel():
            barang = Barang(sv_tipe_barang.get(), sv_barang.get(), sv_kategori.get(), sv_harga_pokok.get(), sv_harga_jual.get(), sv_stock_sekarang.get(), sv_stock_reminder.get())
            create_window.toko_barang_add_toplevel(barang)

        cls.hide_toko_sub_menu()
        cls.show_toko_barang_add()
        f_toko_barang_add.focus_set()
        root.geometry("833x498")#+261+151")

        font_radio_button = tkFont.Font(family="Times New Roman", size=100)
        style_toko_barang_add = Style(root)
        style_toko_barang_add.configure("TRadioButton", font=font_radio_button)

        bool_condition_add_barang = False

        l_title = Label(f_toko_barang_add, text = "Add Barang", font=tkFont.Font(family="Comic Sans MS", size=28, weight="bold"))

        sv_tipe_barang = StringVar()
        sv_barang = StringVar()
        sv_kategori = StringVar()
        sv_harga_pokok = StringVar()
        sv_harga_jual = StringVar()
        sv_stock_sekarang = StringVar()
        sv_stock_reminder = StringVar()

        sv_tipe_barang.set("GT")

        list_kategori = list_kategori_gt
        if(list_kategori):
            sv_kategori.set(list_kategori[0])
        else:
            sv_kategori.set("")

        #DUMMY RECORD
        # sv_tipe_barang.set("GT")
        # sv_barang.set("ASUS")
        # sv_kategori.set("Elektronik")
        # sv_harga_pokok.set("230000")
        # sv_harga_jual.set("275000")
        # sv_stock_sekarang.set("5")
        # sv_stock_reminder.set("2")

        f_add_barang = Frame(f_toko_barang_add)
        f_tipe_barang = Frame(f_add_barang)
        l_tipe_barang = Label(f_tipe_barang, text="Tipe Barang:", font=(14)) #GT PI
        rb_tipe_barang_gt = Radiobutton(f_tipe_barang, text="Great Tech", variable=sv_tipe_barang, value="GT")
        rb_tipe_barang_pi = Radiobutton(f_tipe_barang, text="Permata Indah", variable=sv_tipe_barang, value="PI")
        l_barang = Label(f_add_barang, text="Nama Barang:", font=(14))
        l_kategori = Label(f_add_barang, text="Kategori:", font=(14))
        l_harga_pokok = Label(f_add_barang, text="Harga Pokok:", font=(14))
        l_rp_pokok = Label(f_add_barang, text="Rp.", width=3, font=(14), borderwidth=3)
        l_harga_jual = Label(f_add_barang, text="Harga Jual:", font=(14))
        l_rp_jual = Label(f_add_barang, text="Rp.", width=3, font=(14), borderwidth=3)
        l_stock_sekarang = Label(f_add_barang, text="Stock Sekarang:", font=(14))
        l_stock_reminder = Label(f_add_barang, text="Stock Reminder:", font=(14))
        entry_barang = Entry(f_add_barang, textvariable=sv_barang, width=40) #40
        entry_barang.focus_set()
        #entry_kategori = Entry(f_add_barang, textvariable=sv_kategori, width=40) #12
        entry_kategori = Combobox(f_add_barang, textvariable=sv_kategori, width=37, values=list_kategori)
        #dropdown_kategori / or toplevel kategori
        entry_harga_pokok = Entry(f_add_barang, textvariable=sv_harga_pokok, width=40) #12
        entry_harga_jual = Entry(f_add_barang, textvariable=sv_harga_jual, width=40) #12
        entry_stock_sekarang = Entry(f_add_barang, textvariable=sv_stock_sekarang, width=40) #3
        entry_stock_reminder = Entry(f_add_barang, textvariable=sv_stock_reminder, width=40) #3
                              
        l_warning = Label(f_toko_barang_add, text="", font=(14))

        f_btn = Frame(f_toko_barang_add)
        btn_add = Button(f_btn, text="Add to Inventory", command=bridge_toko_barang_add_toplevel)
        btn_back = Button(f_btn, text="Back", command=create_window.toko_barang)

        btn_add['state'] = "disabled"
        #btn_add['state'] = "enable"

        def check_condition_add_barang(event):
            if(bool_condition_add_barang is True):
                bridge_toko_barang_add_toplevel()
            else:
                print("the condition is not sastified")

        def dropdown_event_generate(event):
            entry_kategori.event_generate('<Button-1>')

        f_toko_barang_add.bind("<Return>", check_condition_add_barang)
        rb_tipe_barang_gt.bind("<Return>", check_condition_add_barang)
        rb_tipe_barang_pi.bind("<Return>", check_condition_add_barang)
        entry_barang.bind("<Return>", check_condition_add_barang)
        entry_kategori.bind("<Return>", check_condition_add_barang)
        entry_kategori.bind("<Control_L>", dropdown_event_generate)
        entry_kategori.bind("<Control_R>", dropdown_event_generate)
        entry_harga_pokok.bind("<Return>", check_condition_add_barang)
        entry_harga_jual.bind("<Return>", check_condition_add_barang)
        entry_stock_sekarang.bind("<Return>", check_condition_add_barang)
        entry_stock_reminder.bind("<Return>", check_condition_add_barang)

        def bridge_toko_barang(event):
            create_window.toko_barang()

        # f_toko_barang_add.bind("<Escape>", bridge_toko_barang)
        # rb_tipe_barang_gt.bind("<Escape>", bridge_toko_barang)
        # rb_tipe_barang_pi.bind("<Escape>", bridge_toko_barang)
        # entry_barang.bind("<Escape>", bridge_toko_barang)
        # entry_kategori.bind("<Escape>", bridge_toko_barang)
        # entry_harga_pokok.bind("<Escape>", bridge_toko_barang)
        # entry_harga_jual.bind("<Escape>", bridge_toko_barang)
        # entry_stock_sekarang.bind("<Escape>", bridge_toko_barang)
        # entry_stock_reminder.bind("<Escape>", bridge_toko_barang)
        


        # def callback_keystroke_harga_pokok(sv):
        #     sv_value = sv.get().replace(".","")
        #     harga_pokok = sv_value
        #     print("harga_pokok: ", harga_pokok)
            
        #     sv_harga_pokok.set(locale.format_string("%d", int(sv_value), grouping=True).replace(",","."))
        #     str_harga_pokok = sv.get().replace(".","")
        #     #sv_harga_pokok.set()
        #     entry_harga_pokok.icursor(END)

        def callback_keystroke_check_condition():

            btn_add['state'] = "disabled"

            nonlocal bool_condition_add_barang
            bool_condition_add_barang = False

            if(sv_tipe_barang.get()=="" or sv_barang.get()=="" or sv_kategori.get()=="" or sv_harga_pokok.get()==""
               or sv_harga_jual.get()=="" or sv_stock_sekarang.get()=="" or sv_stock_reminder.get()==""):
                return
            
            bool_duplicate_barang = False

            for i in range(len(list_barang)):
                if(list_barang[i].barang.lower() == sv_barang.get().lower()):
                    bool_duplicate_barang = True
                    break
            
            if(bool_duplicate_barang is False):
                bool_condition_add_barang=True
                btn_add['state']="enable"
            else:
                bool_condition_add_barang=False
                btn_add['state']="disabled"

            if(int(sv_stock_sekarang.get()) >= 32000 or int(sv_stock_reminder.get()) >=32000):
                bool_condition_add_barang = False
                btn_add['state']="disabled"
                

        def callback_keystroke_check_tipe():

            nonlocal list_kategori

            if(sv_tipe_barang.get()=="GT"):
                list_kategori = list_kategori_gt
            elif(sv_tipe_barang.get()=="PI"):
                list_kategori = list_kategori_pi

            entry_kategori['values'] = list_kategori

            if(list_kategori):
                sv_kategori.set(list_kategori[0])
            else:
                sv_kategori.set("")

            callback_keystroke_check_condition()

        def callback_keystroke_check_number(sv):
            str_sv = sv.get()

            for i in str_sv:
                print("i: ",i)
                if(i.isdigit()==FALSE):
                    print("masuk IF")
                    str_sv = str_sv.replace(i,"")
                    break

            sv.set(str_sv)

            print(str_sv)

            callback_keystroke_check_condition()


        sv_tipe_barang.trace("w", lambda name, index, mode, sv=sv_tipe_barang: callback_keystroke_check_tipe())
        sv_barang.trace("w", lambda name, index, mode, sv=sv_barang: callback_keystroke_check_condition())
        sv_kategori.trace("w", lambda name, index, mode, sv=sv_kategori: callback_keystroke_check_condition())
        sv_harga_pokok.trace("w", lambda name, index, mode, sv=sv_harga_pokok: callback_keystroke_check_number(sv))
        sv_harga_jual.trace("w", lambda name, index, mode, sv=sv_harga_jual: callback_keystroke_check_number(sv))
        sv_stock_sekarang.trace("w", lambda name, index, mode, sv=sv_stock_sekarang: callback_keystroke_check_number(sv))
        sv_stock_reminder.trace("w", lambda name, index, mode, sv=sv_stock_reminder: callback_keystroke_check_number(sv))

        #rb_tipe_barang_gt.config(font=)

        l_title.grid(row=0, column=1, pady=20)

        f_add_barang.grid(row=1, column=0, pady=10, padx=30, columnspan=3)
        f_tipe_barang.grid(row=0, column=0, pady=(0,20)) #inside f_add_barang
        #f_tipe_barang
        l_tipe_barang.grid(row=0, column=0)
        rb_tipe_barang_gt.grid(row=0, column=1, sticky=(W), padx=(5,0))
        rb_tipe_barang_pi.grid(row=1, column=1, sticky=(W), padx=(5,0))

        #f_add_barang continue
        l_barang.grid(row=1, column=0, sticky=(W,E))
        l_kategori.grid(row=2, column=0, sticky=(W,E))
        l_harga_pokok.grid(row=3, column=0, sticky=(W,E))
        l_harga_jual.grid(row=4, column=0, sticky=(W,E))  
        l_stock_sekarang.grid(row=5, column=0, sticky=(W,E))
        l_stock_reminder.grid(row=6, column=0, sticky=(W,E))
        l_rp_pokok.grid(row=3, column=1, sticky=(W,E))
        l_rp_jual.grid(row=4, column=1, sticky=(W,E))

        entry_barang.grid(row=1, column=1, sticky=W)
        entry_kategori.grid(row=2, column=1, sticky=W)
        entry_harga_pokok.grid(row=3, column=1, sticky=W)
        entry_harga_jual.grid(row=4, column=1, sticky=W)
        entry_stock_sekarang.grid(row=5, column=1, sticky=W)
        entry_stock_reminder.grid(row=6, column=1, sticky=W)

        f_btn.grid(row=2, column=1, pady=20)
        btn_add.grid(row=0, column=0, padx=(0,10))
        btn_back.grid(row=0, column=1, padx=(10,0))

    @classmethod
    def toko_barang_add_toplevel(cls, barang):
        #confirm toplevel menu

        top_confirm = Toplevel()
        top_confirm.grab_set()
        top_confirm.focus_set()
        top_confirm.geometry("+346+286")
        top_confirm.title("Confirmation - Add Barang")

        def confirm_add(event):
            print(event)
            top_confirm.destroy()
            add_barang(barang)
            create_window.toko_barang()

        def bridge_toplevel_destroy(event):
            top_confirm.destroy()
            f_toko_barang_add.focus_set()
        
        top_confirm.bind("<Return>", confirm_add)
        top_confirm.bind("<Escape>", bridge_toplevel_destroy)

        f_top_detail = Frame(top_confirm, borderwidth=5)
        l_top_dialog = Label(top_confirm, relief="flat", borderwidth=0, text="Are you sure you want to add this item?")
        
        l_top_text = []
        top_text = ["ID Barang", "Nama Barang", "Kategori", "Harga Pokok", "Harga Jual", 
                    "Stock Sekarang", "Stock Reminder"]
        
        for i in range(len(top_text)):
            l_top_text.append(Label(f_top_detail, relief="solid", borderwidth=2, text=top_text[i]))

        l_top_id_barang = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.id_barang) #THIS MUST CHANGE (FOLLOW LAST ID)
        l_top_barang = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.barang)
        l_top_kategori = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.kategori)
        l_top_harga_pokok = Label(f_top_detail, width=12, relief="solid", borderwidth=2, text="Rp. "+locale.format_string("%d", int(barang.harga_pokok), grouping=True))
        l_top_harga_jual = Label(f_top_detail, width=12, relief="solid", borderwidth=2, text="Rp. "+locale.format_string("%d", int(barang.harga_jual), grouping=True))
        l_top_stock_sekarang = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.stock_sekarang)
        l_top_stock_reminder = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.stock_reminder)

        f_btn_toplevel = Frame(top_confirm)

        btn_add_to_inventory = Button(f_btn_toplevel, text="Add", command=lambda:confirm_add(None))
        btn_cancel = Button(f_btn_toplevel, text="Cancel", command=lambda:bridge_toplevel_destroy(None))
        #btn_cancel = Button(f_top_detail, text="Cancel", command=lambda:print(top_confirm.geometry()))


        l_top_dialog.grid(row=0, column=0, padx=80, pady=20)
        f_top_detail.grid(row=1, column=0)
        f_btn_toplevel.grid(row=2, column=0)
        
        for i in range(len(top_text)):
            l_top_text[i].grid(row=0, column=i, sticky=(W,E))

        l_top_id_barang.grid(row=1, column=0, sticky=(W,E))
        l_top_barang.grid(row=1, column=1, sticky=(W,E))
        l_top_kategori.grid(row=1, column=2, sticky=(W,E))
        l_top_harga_pokok.grid(row=1, column=3, sticky=(W,E))
        l_top_harga_jual.grid(row=1, column=4, sticky=(W,E))
        l_top_stock_sekarang.grid(row=1, column=5, sticky=(W,E))
        l_top_stock_reminder.grid(row=1, column=6, sticky=(W,E))

        btn_add_to_inventory.grid(row=0, column=0, sticky=(W,E))
        btn_cancel.grid(row=0, column=1, sticky=(W,E), pady=20, padx=(20,0))

    @classmethod
    def toko_barang_update(cls, barang_target):

        cls.hide_toko_sub_menu()
        cls.show_toko_barang_update()
        f_toko_barang_update.focus_set()
        root.geometry("985x498")#+195+149")

        list_kategori = []

        def bridge_toko_barang_update_toplevel():
            if(sv_tipe_barang.get() in barang_target.id_barang):
                barang = Barang(barang_target.id_barang, sv_barang.get(), sv_kategori.get(), sv_harga_pokok.get(), sv_harga_jual.get(), sv_stock_sekarang.get(), sv_stock_reminder.get())
            else:
                barang = Barang(sv_tipe_barang.get(), sv_barang.get(), sv_kategori.get(), sv_harga_pokok.get(), sv_harga_jual.get(), sv_stock_sekarang.get(), sv_stock_reminder.get())
            create_window.toko_barang_update_toplevel(barang_target, barang)

        font_radio_button = tkFont.Font(family="Times New Roman", size=100)
        style_toko_barang_add = Style(root)
        style_toko_barang_add.configure("TRadioButton", font=font_radio_button)

        #bool_condition_add_barang = False
        bool_condition_update_barang = False

        l_title = Label(f_toko_barang_update, text = "Update Barang", font=tkFont.Font(family="Comic Sans MS", size=28, weight="bold")) #0,0

        sv_tipe_barang = StringVar()
        sv_barang = StringVar()
        sv_kategori = StringVar()
        sv_harga_pokok = StringVar()
        sv_harga_jual = StringVar()
        sv_stock_sekarang = StringVar()
        sv_stock_reminder = StringVar()

        sv_target_tipe_barang = StringVar()
        sv_target_barang = StringVar()
        sv_target_kategori = StringVar()
        sv_target_harga_pokok = StringVar()
        sv_target_harga_jual = StringVar()
        sv_target_stock_sekarang = StringVar()
        sv_target_stock_reminder = StringVar()

        #DUMMY RECORD

        if("GT" in barang_target.id_barang):
            target_tipe_barang = "GT"
            list_kategori = list_kategori_gt
        elif("PI" in barang_target.id_barang):
            target_tipe_barang = "PI"
            list_kategori = list_kategori_pi

        sv_tipe_barang.set(target_tipe_barang)
        sv_barang.set(barang_target.barang)
        sv_kategori.set(barang_target.kategori)
        sv_harga_pokok.set(barang_target.harga_pokok)
        sv_harga_jual.set(barang_target.harga_jual)
        sv_stock_sekarang.set(barang_target.stock_sekarang)
        sv_stock_reminder.set(barang_target.stock_reminder)

        barang_target.print()

        sv_target_tipe_barang.set(target_tipe_barang)
        sv_target_barang.set(barang_target.barang)
        sv_target_kategori.set(barang_target.kategori)
        sv_target_harga_pokok.set(barang_target.harga_pokok)
        sv_target_harga_jual.set(barang_target.harga_jual)
        sv_target_stock_sekarang.set(barang_target.stock_sekarang)
        sv_target_stock_reminder.set(barang_target.stock_reminder)

        f_update_barang = Frame(f_toko_barang_update)
        f_tipe_barang = Frame(f_update_barang)
        rb_tipe_barang_gt = Radiobutton(f_update_barang, text="Great Tech", variable=sv_tipe_barang, value="GT", state="disabled")
        rb_tipe_barang_pi = Radiobutton(f_update_barang, text="Permata Indah", variable=sv_tipe_barang, value="PI", state="disabled")
        l_barang = Label(f_update_barang, text="Nama Barang:", font=(14))
        l_kategori = Label(f_update_barang, text="Kategori:", font=(14))
        l_harga_pokok = Label(f_update_barang, text="Harga Pokok:", font=(14))
        l_rp_pokok = Label(f_update_barang, text="   ", width=3, font=(14), borderwidth=3)
        l_harga_jual = Label(f_update_barang, text="Harga Jual:", font=(14))
        l_rp_jual = Label(f_update_barang, text="   ", width=3, font=(14), borderwidth=3)
        l_stock_sekarang = Label(f_update_barang, text="Stock Sekarang:", font=(14))
        l_stock_reminder = Label(f_update_barang, text="Stock Reminder:", font=(14))
        entry_barang = Entry(f_update_barang, textvariable=sv_barang, width=40) #40
        entry_barang.focus_set()
        entry_kategori = Combobox(f_update_barang, textvariable=sv_kategori, width=37, values=list_kategori)
        entry_harga_pokok = Entry(f_update_barang, textvariable=sv_harga_pokok, width=40) #12
        entry_harga_jual = Entry(f_update_barang, textvariable=sv_harga_jual, width=40) #12
        entry_stock_sekarang = Entry(f_update_barang, textvariable=sv_stock_sekarang, width=40) #3
        entry_stock_reminder = Entry(f_update_barang, textvariable=sv_stock_reminder, width=40) #3

        f_target_tipe_barang = Frame(f_update_barang)
        l_tipe_barang = Label(f_update_barang, text="Tipe Barang:", font=(14)) #GT PI
        rb_target_tipe_barang_gt = Radiobutton(f_update_barang, text="Great Tech", variable=sv_target_tipe_barang, value="GT", state="disabled")
        rb_target_tipe_barang_pi = Radiobutton(f_update_barang, text="Permata Indah", variable=sv_target_tipe_barang, value="PI", state="disabled")
        entry_target_barang = Entry(f_update_barang, textvariable=sv_target_barang, width=40, state="disabled") #40
        entry_target_kategori = Entry(f_update_barang, textvariable=sv_target_kategori, width=40, state="disabled") #12
        entry_target_harga_pokok = Entry(f_update_barang, textvariable=sv_target_harga_pokok, width=40, state="disabled") #12
        entry_target_harga_jual = Entry(f_update_barang, textvariable=sv_target_harga_jual, width=40, state="disabled") #12
        entry_target_stock_sekarang = Entry(f_update_barang, textvariable=sv_target_stock_sekarang, width=40, state="disabled") #3
        entry_target_stock_reminder = Entry(f_update_barang, textvariable=sv_target_stock_reminder, width=40, state="disabled") #3
                              
        l_warning = Label(f_toko_barang_update, text="", font=(14))

        f_btn = Frame(f_toko_barang_update)
        btn_update = Button(f_btn, text="Update Barang", command=bridge_toko_barang_update_toplevel)
        btn_back = Button(f_btn, text="Back", command=create_window.toko_barang)

        btn_update['state'] = "disabled"
        #btn_add['state'] = "enable"

        def check_condition_add_barang(event):
            if(bool_condition_update_barang is True):
                bridge_toko_barang_update_toplevel()
            else:
                print("the condition is not sastified")

        def dropdown_event_generate(event):
            entry_kategori.event_generate('<Button-1>')

        f_toko_barang_add.bind("<Return>", check_condition_add_barang)
        rb_tipe_barang_gt.bind("<Return>", check_condition_add_barang)
        rb_tipe_barang_pi.bind("<Return>", check_condition_add_barang)
        entry_barang.bind("<Return>", check_condition_add_barang)
        entry_kategori.bind("<Return>", check_condition_add_barang)
        entry_kategori.bind("<Control_L>", dropdown_event_generate)
        entry_kategori.bind("<Control_R>", dropdown_event_generate)
        entry_harga_pokok.bind("<Return>", check_condition_add_barang)
        entry_harga_jual.bind("<Return>", check_condition_add_barang)
        entry_stock_sekarang.bind("<Return>", check_condition_add_barang)
        entry_stock_reminder.bind("<Return>", check_condition_add_barang)

        def bridge_toko_barang(event):
            create_window.toko_barang()

        # f_toko_barang_add.bind("<Escape>", bridge_toko_barang)
        # rb_tipe_barang_gt.bind("<Escape>", bridge_toko_barang)
        # rb_tipe_barang_pi.bind("<Escape>", bridge_toko_barang)
        # entry_barang.bind("<Escape>", bridge_toko_barang)
        # entry_harga_pokok.bind("<Escape>", bridge_toko_barang)
        # entry_harga_jual.bind("<Escape>", bridge_toko_barang)
        # entry_stock_sekarang.bind("<Escape>", bridge_toko_barang)
        # entry_stock_reminder.bind("<Escape>", bridge_toko_barang)

        def callback_keystroke_check_condition():

            btn_update['state'] = "disabled"

            nonlocal bool_condition_update_barang
            bool_condition_update_barang = False

            if(sv_tipe_barang.get()=="" or sv_barang.get()=="" or sv_kategori.get()=="" or sv_harga_pokok.get()==""
               or sv_harga_jual.get()=="" or sv_stock_sekarang.get()=="" or sv_stock_reminder.get()==""):
                return
            
            if(sv_tipe_barang.get()==sv_target_tipe_barang.get() and sv_barang.get()==sv_target_barang.get() and sv_kategori.get()==sv_target_kategori.get() 
               and sv_harga_pokok.get()==sv_target_harga_pokok.get() and sv_harga_jual.get()==sv_target_harga_jual.get() 
               and sv_stock_sekarang.get()==sv_target_stock_sekarang.get() and sv_stock_reminder.get()==sv_target_stock_reminder.get()):
                return
            
            bool_duplicate_barang = False

            for i in range(len(list_barang)):
                if(list_barang[i].barang.lower() == sv_barang.get().lower()):
                    if(list_barang[i].barang.lower()==sv_target_barang.get().lower()):
                        break
                    bool_duplicate_barang = True
                    break
                
            if(bool_duplicate_barang is False):
                bool_condition_update_barang=True
                btn_update['state']="enable"
            else:
                bool_condition_update_barang=False
                btn_update['state']="disabled"

            if(int(sv_stock_sekarang.get()) >= 32000 or int(sv_stock_reminder.get()) >=32000):
                bool_condition_update_barang = False
                btn_update['state']="disabled"

        def callback_keystroke_check_tipe():

            nonlocal list_kategori

            if(sv_tipe_barang.get()=="GT"):
                list_kategori = list_kategori_gt
            elif(sv_tipe_barang.get()=="PI"):
                list_kategori = list_kategori_pi

            entry_kategori['values'] = list_kategori

            if(list_kategori):
                sv_kategori.set(list_kategori[0])

            callback_keystroke_check_condition()

        def callback_keystroke_check_number(sv):
            str_sv = sv.get()

            for i in str_sv:
                print("i: ",i)
                if(i.isdigit()==FALSE):
                    print("masuk IF")
                    str_sv = str_sv.replace(i,"")
                    break

            sv.set(str_sv)

            print(str_sv)

            callback_keystroke_check_condition()


        sv_tipe_barang.trace("w", lambda name, index, mode, sv=sv_tipe_barang: callback_keystroke_check_tipe())
        sv_barang.trace("w", lambda name, index, mode, sv=sv_barang: callback_keystroke_check_condition())
        sv_kategori.trace("w", lambda name, index, mode, sv=sv_kategori: callback_keystroke_check_condition())
        sv_harga_pokok.trace("w", lambda name, index, mode, sv=sv_harga_pokok: callback_keystroke_check_number(sv))
        sv_harga_jual.trace("w", lambda name, index, mode, sv=sv_harga_jual: callback_keystroke_check_number(sv))
        sv_stock_sekarang.trace("w", lambda name, index, mode, sv=sv_stock_sekarang: callback_keystroke_check_number(sv))
        sv_stock_reminder.trace("w", lambda name, index, mode, sv=sv_stock_reminder: callback_keystroke_check_number(sv))

        #rb_tipe_barang_gt.config(font=)

        l_title.grid(row=0, column=1, pady=20)

        f_update_barang.grid(row=1, column=0, pady=10, padx=30, columnspan=3)
        #f_tipe_barang.grid(row=0, column=1, pady=(0,20)) #inside f_update_barang
        #f_target_tipe_barang.grid(row=0, column=0, pady=(0,20))
        #f_tipe_barang
        
        #!!!!rb_tipe_barang_gt.grid(row=1, column=3, sticky=(W), padx=(5,0))
        #!!!!rb_tipe_barang_pi.grid(row=2, column=3, sticky=(W), padx=(5,0), pady=(0,10))

        l_tipe_barang.grid(row=1, column=0)
        rb_target_tipe_barang_gt.grid(row=1, column=2, sticky=(W), padx=(5,0))
        rb_target_tipe_barang_pi.grid(row=2, column=2, sticky=(W), padx=(5,0), pady=(0,10))

        #f_update_barang continue
        l_barang.grid(row=3, column=0, sticky=(W,E))
        l_kategori.grid(row=4, column=0, sticky=(W,E))
        l_harga_pokok.grid(row=5, column=0, sticky=(W,E))
        l_harga_jual.grid(row=6, column=0, sticky=(W,E))  
        l_stock_sekarang.grid(row=7, column=0, sticky=(W,E))
        l_stock_reminder.grid(row=8, column=0, sticky=(W,E))
        l_rp_pokok.grid(row=5, column=1, sticky=(W,E))
        l_rp_jual.grid(row=6, column=1, sticky=(W,E))

        entry_barang.grid(row=3, column=3, sticky=(W,E))
        entry_kategori.grid(row=4, column=3, sticky=(W,E))
        entry_harga_pokok.grid(row=5, column=3, sticky=(W,E))
        entry_harga_jual.grid(row=6, column=3, sticky=(W,E))
        entry_stock_sekarang.grid(row=7, column=3, sticky=(W,E))
        entry_stock_reminder.grid(row=8, column=3, sticky=(W,E))

        entry_target_barang.grid(row=3, column=2, sticky=W)
        entry_target_kategori.grid(row=4, column=2, sticky=W)
        entry_target_harga_pokok.grid(row=5, column=2, sticky=W)
        entry_target_harga_jual.grid(row=6, column=2, sticky=W)
        entry_target_stock_sekarang.grid(row=7, column=2, sticky=W)
        entry_target_stock_reminder.grid(row=8, column=2, sticky=W)

        f_btn.grid(row=2, column=1, pady=20)
        btn_update.grid(row=0, column=0, padx=(0,10))
        btn_back.grid(row=0, column=1, padx=(10,0))

    @classmethod
    def toko_barang_update_toplevel(cls, barang_target, barang):

        top_confirm = Toplevel()
        top_confirm.grab_set()
        top_confirm.focus_set()
        top_confirm.geometry("+346+286")
        top_confirm.title("Confirmation - Update Barang")

        def confirm_update(event):
            print(event)
            top_confirm.destroy()
            update_barang(barang_target, barang)
            create_window.toko_barang()

        def bridge_toplevel_destroy(event):
            top_confirm.destroy()
            f_toko_barang_update.focus_set()
        
        top_confirm.bind("<Return>", confirm_update)
        top_confirm.bind("<Escape>", bridge_toplevel_destroy)

        f_top_detail = Frame(top_confirm, borderwidth=5)
        f_top_target_detail = Frame(top_confirm, borderwidth=5)
        l_top_dialog = Label(top_confirm, relief="flat", borderwidth=0, text="Update this item?")
        
        l_top_text = []
        l_to = Label(top_confirm, relief="flat", borderwidth=0, text="V", font=(40))
        l_top_target_text = []
        top_text = ["ID Barang", "Nama Barang", "Kategori", "Harga Pokok", "Harga Jual", 
                    "Stock Sekarang", "Stock Reminder"]
        
        for i in range(len(top_text)):
            l_top_text.append(Label(f_top_detail, relief="solid", borderwidth=2, text=top_text[i]))

        l_top_id_barang = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.id_barang) #THIS MUST CHANGE (FOLLOW LAST ID)
        l_top_barang = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.barang)
        l_top_kategori = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.kategori)
        l_top_harga_pokok = Label(f_top_detail, width=12, relief="solid", borderwidth=2, text="Rp. "+locale.format_string("%d", int(barang.harga_pokok), grouping=True))
        l_top_harga_jual = Label(f_top_detail, width=12, relief="solid", borderwidth=2, text="Rp. "+locale.format_string("%d", int(barang.harga_jual), grouping=True))
        l_top_stock_sekarang = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.stock_sekarang)
        l_top_stock_reminder = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.stock_reminder)

        for i in range(len(top_text)):
            l_top_target_text.append(Label(f_top_target_detail, relief="solid", borderwidth=2, text=top_text[i]))

        l_top_target_id_barang = Label(f_top_target_detail, relief="solid", borderwidth=2, text=barang_target.id_barang) #THIS MUST CHANGE (FOLLOW LAST ID)
        l_top_target_barang = Label(f_top_target_detail, relief="solid", borderwidth=2, text=barang_target.barang)
        l_top_target_kategori = Label(f_top_target_detail, relief="solid", borderwidth=2, text=barang_target.kategori)
        l_top_target_harga_pokok = Label(f_top_target_detail, width=12, relief="solid", borderwidth=2, text="Rp. "+locale.format_string("%d", int(barang_target.harga_pokok), grouping=True))
        l_top_target_harga_jual = Label(f_top_target_detail, width=12, relief="solid", borderwidth=2, text="Rp. "+locale.format_string("%d", int(barang_target.harga_jual), grouping=True))
        l_top_target_stock_sekarang = Label(f_top_target_detail, relief="solid", borderwidth=2, text=barang_target.stock_sekarang)
        l_top_target_stock_reminder = Label(f_top_target_detail, relief="solid", borderwidth=2, text=barang_target.stock_reminder)

        f_btn_toplevel = Frame(top_confirm)

        btn_update = Button(f_btn_toplevel, text="Update", command=lambda:confirm_update(None))
        btn_cancel = Button(f_btn_toplevel, text="Cancel", command=lambda:bridge_toplevel_destroy(None))
        #btn_cancel = Button(f_top_detail, text="Cancel", command=lambda:print(top_confirm.geometry()))


        l_top_dialog.grid(row=0, column=0, padx=80, pady=20)
        f_top_target_detail.grid(row=1, column=0)
        l_to.grid(row=2, column=0, pady=10)
        f_top_detail.grid(row=3, column=0)
        f_btn_toplevel.grid(row=4, column=0)
        
        for i in range(len(top_text)):
            l_top_target_text[i].grid(row=0, column=i, sticky=(W,E))

        l_top_target_id_barang.grid(row=1, column=0, sticky=(W,E))
        l_top_target_barang.grid(row=1, column=1, sticky=(W,E))
        l_top_target_kategori.grid(row=1, column=2, sticky=(W,E))
        l_top_target_harga_pokok.grid(row=1, column=3, sticky=(W,E))
        l_top_target_harga_jual.grid(row=1, column=4, sticky=(W,E))
        l_top_target_stock_sekarang.grid(row=1, column=5, sticky=(W,E))
        l_top_target_stock_reminder.grid(row=1, column=6, sticky=(W,E))

        for i in range(len(top_text)):
            l_top_text[i].grid(row=0, column=i, sticky=(W,E))

        l_top_id_barang.grid(row=1, column=0, sticky=(W,E))
        l_top_barang.grid(row=1, column=1, sticky=(W,E))
        l_top_kategori.grid(row=1, column=2, sticky=(W,E))
        l_top_harga_pokok.grid(row=1, column=3, sticky=(W,E))
        l_top_harga_jual.grid(row=1, column=4, sticky=(W,E))
        l_top_stock_sekarang.grid(row=1, column=5, sticky=(W,E))
        l_top_stock_reminder.grid(row=1, column=6, sticky=(W,E))

        btn_update.grid(row=0, column=0, sticky=(W,E))
        btn_cancel.grid(row=0, column=1, sticky=(W,E), pady=20, padx=(20,0))

    @classmethod
    def toko_barang_delete_toplevel(cls, barang):

        top_confirm = Toplevel()
        top_confirm.grab_set()
        top_confirm.focus_set()
        top_confirm.geometry("+346+286")
        top_confirm.title("Confirmation - Delete")

        def confirm_delete(event):
            print(event)
            top_confirm.destroy()
            delete_barang(barang)
            create_window.toko_barang()

        def bridge_toplevel_destroy(event):
            top_confirm.destroy()
            f_toko_barang.focus_set()
        
        #top_confirm.bind("<Return>", confirm_delete)
        top_confirm.bind("<Escape>", bridge_toplevel_destroy)

        f_top_detail = Frame(top_confirm, borderwidth=5)
        l_top_dialog = Label(top_confirm, relief="flat", borderwidth=0, text="DELETE this item?")
        
        l_top_text = []
        top_text = ["ID Barang", "Nama Barang", "Kategori", "Harga Pokok", "Harga Jual", 
                    "Stock Sekarang", "Stock Reminder"]
        
        for i in range(len(top_text)):
            l_top_text.append(Label(f_top_detail, relief="solid", borderwidth=2, text=top_text[i]))

        l_top_id_barang = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.id_barang) #THIS MUST CHANGE (FOLLOW LAST ID)
        l_top_barang = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.barang)
        l_top_kategori = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.kategori)
        l_top_harga_pokok = Label(f_top_detail, width=12, relief="solid", borderwidth=2, text="Rp. "+locale.format_string("%d", int(barang.harga_pokok), grouping=True))
        l_top_harga_jual = Label(f_top_detail, width=12, relief="solid", borderwidth=2, text="Rp. "+locale.format_string("%d", int(barang.harga_jual), grouping=True))
        l_top_stock_sekarang = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.stock_sekarang)
        l_top_stock_reminder = Label(f_top_detail, relief="solid", borderwidth=2, text=barang.stock_reminder)

        f_btn_toplevel = Frame(top_confirm)

        btn_delete = Button(f_btn_toplevel, text="Delete", command=lambda:confirm_delete(None))
        btn_cancel = Button(f_btn_toplevel, text="Cancel", command=lambda:bridge_toplevel_destroy(None))
        #btn_cancel = Button(f_top_detail, text="Cancel", command=lambda:print(top_confirm.geometry()))


        l_top_dialog.grid(row=0, column=0, padx=80, pady=20)
        f_top_detail.grid(row=1, column=0)
        f_btn_toplevel.grid(row=2, column=0)
        
        for i in range(len(top_text)):
            l_top_text[i].grid(row=0, column=i, sticky=(W,E))

        l_top_id_barang.grid(row=1, column=0, sticky=(W,E))
        l_top_barang.grid(row=1, column=1, sticky=(W,E))
        l_top_kategori.grid(row=1, column=2, sticky=(W,E))
        l_top_harga_pokok.grid(row=1, column=3, sticky=(W,E))
        l_top_harga_jual.grid(row=1, column=4, sticky=(W,E))
        l_top_stock_sekarang.grid(row=1, column=5, sticky=(W,E))
        l_top_stock_reminder.grid(row=1, column=6, sticky=(W,E))

        btn_delete.grid(row=0, column=0, sticky=(W,E))
        btn_cancel.grid(row=0, column=1, sticky=(W,E), pady=20, padx=(20,0))

    @classmethod
    def toko_transaksi(cls):

        cls.hide_toko_sub_menu()
        f_toko_transaksi.grid()

        pass

    @classmethod
    def toko_beli_barang(cls):
                
        cls.hide_toko_sub_menu()
        f_toko_beli_barang.grid()
        
        pass
    
    @classmethod
    def toko_beli_operational(cls):
                
        cls.hide_toko_sub_menu()
        f_toko_beli_operational.grid()
        
        pass
    
    @classmethod
    def toko_jual(cls):
                
        cls.hide_toko_sub_menu()
        f_toko_jual.grid()
        
        pass
    

    
    @classmethod
    def pengeluaran_main_menu(cls):
        pass

    @classmethod
    def pengeluaran_bayar(cls):
        pass       

    @classmethod
    def pengeluaran_update(cls):
        pass

    @classmethod
    def pengeluaran_incoming(cls):
        pass
 ######################################################
 ######################################################

def configure_initial_window(root):
    root.title("Enyi App Desu")
    root.geometry('400x600')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    #root.resizable(False, False)
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=14)
    
 ######################################################
 ######################################################

#CONSTANT    
COLUMN_MAIN_MENU = 0    #f_content
COLUMN_SUB_MENU = 1     #f_content

SELECT_BACKGROUND_COLOR = "grey"

NAMA_FILE = []
FOLDER_DATA="data_enyi_app"
PASSWORD=["boncis", "wow", "kawaii", "mi_estas", "panda_busu", "really"," nani!?", "masa leh", "nntau", "unyu desu", "kion"]

ID_BARANG=["GT", "PI"]
ID_TRX_TOKO=["J_OFF", "J_ON", "B", "OP"]
ID_INCOMING_TOKO=["INC_T"]
ID_PENGELUARAN=["P"]
ID_TRX_PENGELUARAN=["TRX_P"]
ID_INCOMING_PENGELUARAN=["INC_P"]
ID_prive = ["PV"]

#Global List
list_barang = []
list_kategori_special_object = [] #Kategori class
list_kategori_gt = [] #only kategori (string)
list_kategori_pi = [] #only katgeori (string)
list_trx_toko = []
list_incoming_toko = []
list_pengeluaran = []
list_trx_pengeluaran = []
list_incoming_pengeluaran= []
list_prive = []

#Global Variabel

status = Status(0, 0, 0, #capital_barang, capital_uang, uang_pribadi,
                0, 0, 0, #perputaran_toko_harian, perputaran_toko_bulanan, gross_profit,
                0, 0, #pengeluaran_harian, pengeluaran_bulanan
                0) #jumlah_prive

root = Tk()
configure_initial_window(root)

toplevel_password = None #Toplevel(root)

f_content = Frame(root, padding=(3,6,6,12)) #The content, every main_menu will go here
f_content_toko = Frame(root, padding=(3,3,12,12))
f_content_toko.grid(row=0, column=0, sticky=(W,N,S,E))
f_content_toko.columnconfigure((2), weight=1)

f_main_menu = Frame(f_content, borderwidth=5, relief="ridge") #main_menu attaches to the f_content
f_main_menu.grid(row=0, column=COLUMN_MAIN_MENU, sticky=(W, E, N, S))
f_main_menu.columnconfigure((0,1,2,3), weight=1)
#f_main_menu.rowconfigure(0, weight=1)
#f_main_menu.rowconfigure(1, weight=1)




f_toko_main_menu = Frame(f_content_toko, borderwidth=5, relief="ridge") #column 0
f_toko_main_menu.grid(row=0, column=COLUMN_MAIN_MENU, sticky=(W,N,S,E))
f_toko_main_menu.columnconfigure((0,1,2,3), weight=1)
f_toko_main_menu.grid_remove()
#f_toko_sub_menu = Frame(f_content, borderwidth=5, relief="ridge") #column 1

f_toko_barang = Frame(f_content_toko, borderwidth=5, relief="ridge")            #sub_menu
f_toko_barang_update = Frame(f_content_toko)     #sub_menu 1
f_toko_transaksi = Frame(f_content_toko)         #sub_menu 1
f_toko_beli = Frame(f_content_toko)              #sub_menu 1
f_toko_beli_barang = Frame(f_content_toko)       #sub_menu 1
f_toko_beli_operational = Frame(f_content_toko)  #sub_menu 1
f_toko_jual = Frame(f_content_toko)              #sub_menu 1

f_toko_barang_add = Frame(f_content_toko, borderwidth=5, relief="ridge")
f_toko_barang_update = Frame(f_content_toko, borderwidth=5, relief="ridge")

#f_toko_sub_menu.grid(row=0, column=1, sticky=(W,N,S))
#f_toko_sub_menu.columnconfigure((0,1,2,3), weight=1)
#f_toko_sub_menu.grid_remove()


#f_toko_barang.columnconfigure((), weight=1)
#f_toko_barang.grid_remove()

f_pengeluaran_main_menu = Frame(f_content)  #column 0
f_pengeluaran_sub_menu = Frame(f_content)   #column 1

f_pengeluaran_bayar = Frame(f_pengeluaran_sub_menu)      #sub_menu
f_pengeluaran_update = Frame(f_pengeluaran_sub_menu)     #sub_menu
f_pengeluaran_incoming = Frame(f_pengeluaran_sub_menu)   #sub_menu

loadfile("all")
status.update()

create_window.main_menu()
root.mainloop()

#varBarang = Barang("ID001", "Kabel", 20000, 27000, 4, 2)
