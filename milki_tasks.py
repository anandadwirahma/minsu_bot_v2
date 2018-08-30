import json
import traceback
import urlparse
import MySQLdb
import random
import string
import requests
#import template_flex_message
import requests

from datetime import datetime, timedelta
from celery import Celery
from email_validator import validate_email, EmailNotValidError
#from template_flex_message import flextemplateReceipt

from bot import Bot
from nlp.nlp_rivescript import Nlp

# app = Celery('rogu_tasks', backend = 'amqp', broker = 'amqp://')
app = Celery('milki_tasks', backend='amqp', broker='redis://localhost:6379/9')

LINE_TOKEN = ""
DEBUG_MODE = "D"  # I=Info, D=Debug, V=Verbose, E=Error
first_name = ""

#--OPEN CONFIGURATION (For Linux) --#
# with open('RGCONFIG.txt') as f:
#     content = f.read().splitlines()
# f.close
# LINE_TOKEN=content[0].split('=')[1]

##########OPEN CONFIGURATION#######################
#--Mysql Prod--#
MYSQL_HOST="us-cdbr-iron-east-04.cleardb.net"
MYSQL_USER="b8891eaa7d84f1"
MYSQL_PWD="f5c5dbef"
MYSQL_DB="heroku_a23c62e0062b156"

#--Mysql Dev--#
# MYSQL_HOST = "127.0.0.1"
# MYSQL_USER = "root"
# MYSQL_PWD = ""
# MYSQL_DB = "milki"

#--LINE TOKEN PROD--#
LINE_TOKEN = "sajVouljE8GHl8BAFPcsJfy/Zy0GTPtubgsYQlkB+YQCT4pHawfMnIWUthlf00OfWlqo21sKbtQa2okJ3UCkYMqsm+zSV9HOVnMRDNVnREEcxoD/7BJQdjm/1ppdjhBrkfEAZwOg+/cj0ebV6ErjdQdB04t89/1O/w1cDnyilFU="

#--LINE TOKEN DEV--#
# LINE_TOKEN = "yqGbUixBtC4Bpo1RYw9VKYg/qfZgqYKyTcKg9Af/8PfICEkhGlv60SKVN2/H4szM+CnqldcXTgZUL8JgZsBB8X9Hv1XAFjjzGInO2xlTPVCRw0oa+3z00kaZn6zqJv2QNYXM/Qj+IMJr0goSI//bVwdB04t89/1O/w1cDnyilFU="

linebot = Bot(LINE_TOKEN)
lineNlp = Nlp()

#=============================================== Function Addon ===============================================#


def request(sql):
    try:
        db_connect = MySQLdb.connect(
            host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PWD, db=MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        sqlout = cursor.fetchall()

        return sqlout
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)
                  ).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])


def insert(sql):
    try:
        db_connect = MySQLdb.connect(
            host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PWD, db=MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        db_connect.commit()
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)
                  ).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])


def update(sql):
    try:
        db_connect = MySQLdb.connect(
            host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PWD, db=MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        db_connect.commit()
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)
                  ).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])


def delete(sql):
    try:
        db_connect = MySQLdb.connect(
            host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PWD, db=MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        db_connect.commit()
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)
                  ).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])


def parseJson(data):
    result = json.dumps(data)

    return result

##** Konfirmasi Chart Shop **#


def confirm_chartshop(msisdn):
    getChartshop = lineNlp.redisconn.get("milkibot/%s/chartshop" % (msisdn))
    jsonStr = getChartshop.decode("utf-8")
    parse_chartshop = json.loads(jsonStr)

    hitung_harga = 0
    for shopItems in parse_chartshop:
        qty = int(shopItems["qty"])
        harga = int(shopItems["harga"])
        hitung_harga = hitung_harga + (harga * qty)

    total_harga = str(formatrupiah(int(hitung_harga)))
    linebot.send_composed_confirm(
        msisdn, 'Konfirmasi Pembayaran', 'Total belanja yang harus dibayar : ' +
            total_harga + '\nTekan beli untuk melanjutkan pembayaran',
        {'label': 'Beli', 'type': 'postback', 'data': 'evt=confirmorder'},
        {'label': 'Batal', 'type': 'postback', 'data': 'evt=cancelorder'}
    )

##** Carrousel Pilih Category **#


def create_category(msisdn):

    sql = "SELECT id_cat,category,url_img FROM category"
    sqlout = request(sql)

    columns = []
    for row in sqlout:
        id_cat = row[0]
        category = row[1]
        url_img = row[2]

        column = {}
        column['thumbnail_image_url'] = url_img
        column['title'] = category.upper()
        column['text'] = 'Menu Kategori'
        column['actions'] = [
            {'type': 'postback', 'label': 'Pilih Kategori',
                'data': 'evt=selecttaste&id_cat=' + str(id_cat)}
        ]
        columns.append(column)

    return columns

##** Carrousel Pilih Rasa **#


def create_taste(msisdn, sqlout):
    columns = []
    for row in sqlout:
        id_brg = row[0]
        rasa = row[1]
        img = row[2]
        description = row[3]

        column = {}
        column['thumbnail_image_url'] = img
        column['title'] = rasa.upper()
        column['text'] = 'Menu Rasa'
        column['actions'] = [
            {'type': 'postback', 'label': 'Pilih Rasa',
                'data': 'evt=select_type&id_brg=' + str(id_brg)},
            {'type': 'postback', 'label': 'Detail Product',
                'data': 'evt=detail_product&id_brg=' + str(id_brg)}
        ]
        columns.append(column)

    return columns

##** Carrousel Pilih Size **#


def create_taste_size(msisdn, id_brg):
    sql = "select b.id_detail_brg as id_detail_brg,a.id_brg as id_brg, a.rasa as rasa, a.url_img as url_img, b.type as size, b.stock as stock, b.harga as harga from barang a INNER JOIN detail_barang b on a.id_brg = b.id_brg WHERE b.id_brg = '" + id_brg + "'"
    sqlout = request(sql)

    columns = []
    for row in sqlout:
        id_detail_brg = row[0]
        id_brg = row[1]
        rasa = row[2]
        url_img = row[3]
        size = row[4]
        if row[5] == '0':
            stock = 'Kosong'
        else:
            stock = row[5]
        harga = row[6]

        column = {}
        column['thumbnail_image_url'] = url_img
        column['title'] = rasa.upper()
        column['text'] = 'Harga : ' + \
            str(formatrupiah(int(harga))) + \
                "\nSize : " + size + "\nStock : " + stock
        column['actions'] = [
            {'type': 'postback', 'label': 'Beli', 'data': 'evt=beli&id_brg=' +
                str(id_brg) + '&id_detailbrg=' + str(id_detail_brg)}
        ]
        columns.append(column)

    return columns

##** Carrousel Shopping Chart **#


def create_chartshop(msisdn):
    getChartshop = lineNlp.redisconn.get("milkibot/%s/chartshop" % (msisdn))
    jsonStr = getChartshop.decode("utf-8")
    parse_chartshop = json.loads(jsonStr)

    columns = []
    for shopItems in parse_chartshop:
        chartid = shopItems["chartid"]
        url_img = shopItems["url_img"]
        rasa = shopItems["rasa"]
        qty = shopItems["qty"]
        harga = shopItems["harga"]
        type_size = shopItems["type_size"]
        id_brg = shopItems["id_brg"]
        id_detail_brg = shopItems["id_detail_brg"]

        column = {}
        column['thumbnail_image_url'] = url_img
        column['title'] = rasa.upper()
        column['text'] = 'Harga : ' + str(formatrupiah(int(harga))) + "\nSize : " + str(
            type_size) + "\nJumlah Order : " + str(qty)
        column['actions'] = [
            {'type': 'postback', 'label': 'Hapus Dari Keranjang', 'data': 'evt=deleteitem&id_brg=' +
                str(id_brg) + '&id_detailbrg=' + str(id_detail_brg) + '&chartid=' + str(chartid)}
        ]
        columns.append(column)

    return columns

# def chartshop(msisdn):
#     sql = "SELECT a.msisdn as msisdn,b.rasa as rasa,COUNT(b.id_brg) as total_brg,SUM(b.harga) as total_harga,a.id_brg as id_brg from chart_shop a INNER JOIN barang b on a.id_brg = b.id_brg where msisdn = '" + msisdn + "' group by msisdn,rasa,id_brg"
#     sqlout = request(sql)

#     sum_price = 0
#     checkout_msg = "Keranjang Belanja Kamu :\n"
#     checkout_msg += "=====================\n"
#     for row in sqlout:
#         item_name = row[1]
#         count_item = row[2]
#         price = row[3]
#         sum_price = sum_price + price

#         checkout_msg += item_name + " = " + str(count_item) + "\n"

#     checkout_msg += "\nTotal Harga = " + str(formatrupiah(int(sum_price)))

#     linebot.send_composed_confirm(
#         msisdn, 'confirm_checkout', checkout_msg,
#         {'label': 'Beli', 'type': 'postback', 'data': 'evt=beli'},
#         {'label': 'Batal', 'type': 'postback', 'data': 'evt=cancelorder'}
#     )


def cancelorder(msisdn):
    lineNlp.redisconn.delete("milkibot/%s/chartshop" % (msisdn))
    lineNlp.redisconn.delete("milkibot/%s/inputorder" % (msisdn))
    lineNlp.redisconn.delete("milkibot/%s/status" % (msisdn))


def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3:
        return 'Rp ' + y
    else:
        p = y[-3:]
        q = y[:-3]
        return formatrupiah(q) + '.' + p
        print 'Rp ' + formatrupiah(q) + '.' + p

#=============================================== Function Worker ===============================================#


def onMessage(msisdn, ask, param):
    logDtm = (datetime.now() + timedelta(hours=0)
              ).strftime('%Y-%m-%d %H:%M:%S')
    print "--- Send asking to rivescript and get answer --->", logDtm, msisdn, ask

    status = lineNlp.redisconn.get("milkibot/%s/status" % (msisdn))

    if status is not None:
        jsonStr = status.decode("utf-8")
        parse_status = json.loads(jsonStr)
        statement = parse_status["state"]
        action = parse_status["action"]

        print '--- Parameter Action --->', action
        print '--- Parameter Statement --->', statement
    
        #-- Add CharShop --#
        if statement == 'stateOrder' and action == 'input order':
            if ask.lower() == "cancel":
                cancelorder(msisdn)
                linebot.send_text_message(msisdn, "Baik kak kita cancel ya, \n Kalau pengen pesan minsu jangan malu-malu hubungin milki ya.")
            else:
                try:
                    qtyOrder = int(ask)
                    getInputorder = lineNlp.redisconn.get(
                        "milkibot/%s/inputorder" % (msisdn))
                    jsonStr = getInputorder.decode("utf-8")
                    parse_chartshop = json.loads(jsonStr)
                    userid = parse_chartshop["userid"]
                    item = parse_chartshop["item"]

                    sql = "select b.id_brg as id_brg,a.id_detail_brg as id_detail_brg, a.type as type_size, a.stock as stock, a.harga as harga,b.rasa as rasa, b.url_img as url_img,c.category as category,a.id_cat as id_cat from detail_barang a INNER JOIN barang b ON a.id_brg = b.id_brg INNER JOIN category c ON a.id_cat = c.id_cat where a.id_detail_brg = '" + item + "'"
                    sqlout = request(sql)

                    columns = []
                    for row in sqlout:
                        id_brg = row[0]
                        id_detail_brg = row[1]
                        type_size = row[2]
                        stock = row[3]
                        harga = row[4]
                        rasa = row[5]
                        url_img = row[6]
                        category = row[7]
                        id_cat = row[8]

                    chartshop = []  # -- Variable to collect temp chartshop

                    # -- Get data chartshop existing in redis (for append with new chartshop)
                    getChartshopexist = lineNlp.redisconn.get(
                        "milkibot/%s/chartshop" % (msisdn))
                    if getChartshopexist is not None:
                        jsonStr = getChartshopexist.decode("utf-8")
                        parse_chartshopexist = json.loads(jsonStr)

                        for shopExist in parse_chartshopexist:
                            chartid_exist = shopExist["chartid"]
                            id_brg_exist = shopExist["id_brg"]
                            id_detail_brg_exist = shopExist["id_detail_brg"]
                            type_size_exist = shopExist["type_size"]
                            qty_exist = shopExist["qty"]
                            harga_exist = shopExist["harga"]
                            rasa_exist = shopExist["rasa"]
                            url_img_exist = shopExist["url_img"]
                            category_exist = shopExist["category"]

                            chartshop.append({'chartid': chartid_exist, 'id_brg': id_brg_exist, 'id_detail_brg': id_detail_brg_exist, 'type_size': type_size_exist,
                                            'qty': qty_exist, 'harga': harga_exist, 'rasa': rasa_exist, 'url_img': url_img_exist, 'category': category_exist})

                    #** Checking stock barang **#
                    if int(stock) >= int(qtyOrder):
                        chartid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

                        # -- Append new chartshop with chartshop existing and save to redis
                        chartshop.append({'chartid': chartid, 'id_brg': id_brg, 'id_detail_brg': id_detail_brg, 'type_size': type_size,
                                        'qty': qtyOrder, 'harga': harga, 'rasa': rasa, 'url_img': url_img, 'category': category})
                        v_chartshop = parseJson(chartshop)
                        lineNlp.redisconn.set(
                            "milkibot/%s/chartshop" % (msisdn), v_chartshop)
                        # -- delete temporary input order
                        lineNlp.redisconn.delete("milkibot/%s/inputorder" % (msisdn))

                        # -- Kurangi stock sesuai jumlah order
                        update_stock = "UPDATE detail_barang SET stock=stock-" + \
                            str(qtyOrder) + " where id_detail_brg = '" + \
                                str(id_detail_brg) + "'"
                        update(update_stock)

                        linebot.send_text_message(
                            msisdn, "Barang kamu berhasil ditambahkan ke keranjang belanja nih")
                        linebot.send_composed_img_buttons(msisdn,
                            "Konfirmasi Shoping Chart",
                            'https://milki.herokuapp.com/assets/img/cat_prodserv.png',
                            'Konfirmasi Shoping Chart',
                            "Ada lagi yang bisa dibantu siis ?",
                            [
                                {'type': 'postback', 'label': 'Kembali ke Kategori',
                                    'data': 'evt=category'},
                                {'type': 'postback', 'label': 'Kembali ke Product',
                                    'data': '&evt=selecttaste&id_cat=' + str(id_cat)},
                                {'type': 'postback', 'label': 'Lihat Keranjang',
                                    'data': 'evt=showchartshop'}
                            ]
                        )
                    else:
                        linebot.send_text_message(
                            msisdn, "Maaf kakak , stock tidak cukup")
                except ValueError:
                    linebot.send_text_message(
                        msisdn, "maaf masukan angka ya siiis")

        # -- Save pic order into redis
        elif statement == 'stateOrder' and action == 'mnPicorder':
            lineNlp.redisconn.set("milkibot/%s/picorder" % (msisdn), ask)
            # -- Next process is asking location
            v_state = parseJson({"state": "stateOrder", "action": "locationorder"})
            lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

            message = "Untuk pemesanannya mau dikirim kemana ?\nShare loc aja ya kak.."
            linebot.send_text_message(msisdn, message)

        # -- Save location order into redis
        elif statement == 'stateOrder' and action == 'phoneorder':
            try:
                phone = int(ask)
                lineNlp.redisconn.set(
                    "milkibot/%s/phoneorder" % (msisdn), phone)
                answer = lineNlp.doNlp('phone', msisdn, param)
            except ValueError:
                answer = lineNlp.doNlp(ask, msisdn, param)

        # -- Save email order into redis
        elif statement == 'stateOrder' and action == 'mailorder':
            email = ask
            try:
                v = validate_email(email)
                email = v["email"]
                lineNlp.redisconn.set(
                    "milkibot/%s/mailorder" % (msisdn), email)
                answer = lineNlp.doNlp('email', msisdn, param)
            except EmailNotValidError as e:
                answer = lineNlp.doNlp(ask, msisdn, param)
        else:
            answer = lineNlp.doNlp(ask, msisdn, param)
    else:
        answer = lineNlp.doNlp(ask, msisdn, param)

    #==== Statement Menu Milki ====#
    if answer[:7] == "mnMilki":
        v_state = parseJson({"state" : "stateOrder", "action" : "menu utama"})
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

        linebot.send_text_message(msisdn, answer[7:])
        linebot.send_text_message(msisdn, "Nih milki kasih berbagai macam varian susu, ada susu sapi murni dan ada juga susu milkshake yang cocok banget buat kamu.\npenasaran kan ? cobain langsung yuk :)")
        linebot.send_composed_img_buttons(msisdn,
            "Menu Utama",
            'https://milki.herokuapp.com/assets/img/cat_prodserv.png',
            'Menu Product & Layanan',
            "Produk & Layanan",
            [
                {'type': 'postback', 'label': 'Pilih Kategory', 'data': 'evt=category'},
                {'type': 'uri', 'label': 'Complain', 'uri': 'line://ti/p/@zim0097b'}
                # {'type': 'postback', 'label': 'History Pemesanan', 'data': 'evt=historyorder'}
            ]
        )
        print "-- answer reply send -->", answer, answer[:7]

    #==== Statement Asking Total Order ====#
    elif answer[:13] == "anwTotalorder":
        v_state = parseJson({"state" : "stateOrder", "action" : "input order"})
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

        linebot.send_text_message(msisdn, answer[13:])
        print "-- answer reply send -->", answer, answer[:13]

    #==== Statement History Order ====#
    elif answer[:14] == "mnHistoryOrder":
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), 'stateOrder')

        linebot.send_text_message(msisdn, "Ini history.")
        print "-- answer reply send -->", answer, answer[:7]

    #==== Statement Complain ====#
    elif answer[:10] == "mnComplain":
        v_state = parseJson({"state" : "stateOrder", "action" : "complain"})
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

        linebot.send_text_message(msisdn, "Ini complain.")
        print "-- answer reply send -->", answer, answer[:7]

    #==== Statement Pic Order ====#
    elif answer[:10] == "mnPicorder":
        v_state = parseJson({"state" : "stateOrder", "action" : answer[:10]})
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

        message = "Untuk pemesanannya atas nama siapa ya kak ?"
        linebot.send_text_message(msisdn, message)

    #==== Statement Asking Phone Number ====#
    elif answer[:4] == 'uLoc':
        lineNlp.redisconn.set("milkibot/%s/locationorder" % (msisdn), str(param))
        v_state = parseJson({"state" : "stateOrder", "action" : 'phoneorder'})
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

        message = "Nomer telfonnya berapa ya kak ?"
        linebot.send_text_message(msisdn, message)
    
    #==== Statement Asking Email====#
    elif answer[:6] == 'uPhone':
        v_state = parseJson({"state" : "stateOrder", "action" : 'mailorder'})
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

        message = "Emailnya apa ya kak ?"
        linebot.send_text_message(msisdn, message)

    #==== Statement Show Detail Order ====#
    elif answer[:5] == 'uMail':
        v_state = parseJson({"state" : "stateOrder", "action" : 'detailorder'})
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

        picorder = lineNlp.redisconn.get("milkibot/%s/picorder" % (msisdn))
        locationorder = lineNlp.redisconn.get("milkibot/%s/locationorder" % (msisdn))
        mailorder = lineNlp.redisconn.get("milkibot/%s/mailorder" % (msisdn))
        phoneorder = lineNlp.redisconn.get("milkibot/%s/phoneorder" % (msisdn))

        checkout_msg = "Untuk pesanan minsunya mohon dicek kembali ya kak..\n"
        checkout_msg += "- Nama Pemesan : " + picorder + "\n"
        checkout_msg += "- Email : " + mailorder + "\n"
        checkout_msg += "- Phone Number : " + phoneorder + "\n"
        checkout_msg += "- Detail Order :\n"    

        getChartshop = lineNlp.redisconn.get("milkibot/%s/chartshop" % (msisdn))
        jsonStr = getChartshop.decode("utf-8")
        parse_chartshop = json.loads(jsonStr)  

        chartshop = []
        hitung_harga = 0
        for shopItems in parse_chartshop:
            chartid = shopItems["chartid"]
            id_brg = shopItems["id_brg"]
            id_detail_brg = shopItems["id_detail_brg"]
            type_size = shopItems["type_size"]
            qty = int(shopItems["qty"])
            harga = int(shopItems["harga"])
            rasa = shopItems["rasa"]
            url_img = shopItems["url_img"]
            category = shopItems["category"]
            hitung_harga = hitung_harga + (harga * qty)
         
            checkout_msg += "   - " + rasa + " ("+ type_size +") = " + str(qty) + "\n"
            
        total_harga = int(hitung_harga)
        lineNlp.redisconn.set("milkibot/%s/totalharga" % (msisdn), total_harga)

        checkout_msg += "- Alamat Pengiriman : " + locationorder
        checkout_msg += "\n======================="
        checkout_msg += "\nTotal Harga = " + str(formatrupiah(int(total_harga)))
        
        linebot.send_text_message(msisdn, checkout_msg)
        linebot.send_composed_confirm(
            msisdn, 'confirm_checkout', 'Tekan "beli" untuk konfirmasi pemesanan. Tekan "cancel" untuk membatalkan pesanan.',
            {'label': 'Beli', 'type': 'postback', 'data': 'evt=finalorder'},
            {'label': 'Cancel', 'type': 'postback', 'data': 'evt=cancelorder'}
        )

    #==== Statement CancelOrder ====#
    elif answer[:9] == 'ordCancel':
        cancelorder(msisdn)
        linebot.send_text_message(msisdn, answer[9:])
    
    #==== Statement Show Detail Order ====#
    # elif answer[:7] == 'chatnow':
    #     linebot.send_text_message(msisdn, "Ini chatnow")

    elif answer[:8] == 'complain':
        linebot.send_text_message(msisdn, "Ini Complain")
    
    elif answer[:7] == 'history':
        linebot.send_text_message(msisdn, "Ini History")
    
    elif answer[:9] == 'keranjang':
        v_state = parseJson({"state" : "stateOrder", "action" : "showchartshop"})
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)
        getChartshop = lineNlp.redisconn.get("milkibot/%s/chartshop" % (msisdn))
        
        if getChartshop is None:
            linebot.send_text_message(msisdn, "Maaf kaak , keranjang belanjanya kosong.")
        else:
            linebot.send_text_message(msisdn, "Berikut detail pesanan kamu yaa , cek dulu ya siis")
            linebot.send_composed_carousel(msisdn, "keranjang belanja", create_chartshop(msisdn))
            confirm_chartshop(msisdn) #-- Display confirmasi chartshop
    else:
        linebot.send_text_message(msisdn, answer)

@app.task(ignore_result=True)
def doworker(req):
    content = json.dumps(req)
    content = json.loads(content)
    print ""
    print "================================ INCOMING LINE MESSAGE REQUEST ============================================="
    print content

    if not content.has_key('events'):
        return

    for event in content["events"] :
        msisdn = ""
        ask = ""
        longitude = ""
        latitude = ""
        contentType = 0
        first_name = ""
        replyToken = ""

        try:
            if event["type"] == "message":
                contentType = event["message"]["type"]
                msisdn = str(event["source"]["userId"])
                replyToken = str(event["replyToken"])

                if contentType == "text":
                    ask = str(event["message"]["text"])
                    print "--- Message Type : Text ---", ask
                elif contentType == "location":
                    longitude = event["message"]["longitude"]
                    latitude = event["message"]["latitude"]
                    address = event["message"]["address"]
                    print "--- Message Type : Location ---", longitude, latitude, address
                elif contentType == "sticker":
                    sticker = event["message"]["packageId"]
                    stickerid = event["message"]["stickerId"]
                    print "--- Message Type : Sticker ---", sticker, stickerid
                elif contentType == "image":
                    print "--- Message Type : Image ---"
                else:
                    print "--->"+contentType.capitalize()
            else:
                opType = event["type"]
                if event["source"].has_key('userId'):
                    msisdn = str(event["source"]["userId"])
                elif event["source"].has_key('groupId'):
                    msisdn = str(event["source"]["groupId"])
                print "-->", opType, msisdn

        except:
            opType = content["result"][0]["content"]["opType"]
            msisdn = str(content["result"][0]["content"]["params"][0])
            print "-->", opType, msisdn

        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')

        if event["type"] == "message":
            if contentType == "text" or contentType == "location":  # request text location
                print "<<-- Incoming Message -->>", logDtm, msisdn, ask, replyToken, longitude, latitude,
                incomingClient = lineNlp.redisconn.get("status/%s" % (msisdn))

                # print incomingClient

                if ask.lower() == "cancel":
                    lineNlp.doNlp(ask.lower(), msisdn, '')

                if incomingClient is None:
                    lineNlp.redisconn.set("status/%s" % (msisdn), 0)
                    incomingClient = "0"
                if longitude != "":
                    ask = "[LOC]" + str(latitude) + ";" + str(longitude)
                    print "<<-- Incoming Message -->>", longitude, ask
                try:
                    if contentType == 'location':
                        onMessage(str(msisdn), contentType, address)
                    else:
                        onMessage(str(msisdn), ask,first_name)
                except Exception as e:
                    # print e
                    traceback.print_exc()
                    print "ERROR HAPPEN!!!"
                    lineNlp.redisconn.set("milki-status/%s" % (msisdn), 0)
                    lineNlp.redisconn.delete("milki-users/%s" % (msisdn))
        elif event["type"] == "postback":
            msisdn = str(event["source"]["userId"])
            parsed = urlparse.urlparse('?' + event["postback"]["data"])
            postback_event = urlparse.parse_qs(parsed.query)['evt'][0]

            status = lineNlp.redisconn.get("milkibot/%s/status" % (msisdn))
            jsonStr = status.decode("utf-8")
            parse_status = json.loads(jsonStr)
            statement = parse_status["state"]
            action = parse_status["action"]

            print status

            print '--- Parameter Action --->', action
            print '--- Parameter Statement --->', statement

            # if (statement == 'stateOrder') and (action == 'mnPicorder' or action == 'locationorder' or action == 'mailorder' or action == 'phoneorder'):
            #     if action != 'mnPicorder' or action != 'locationorder' or action != 'mailorder' or action != 'phoneorder':
            #         linebot.send_text_message(msisdn, "Maaf kak harap selesaikan proses order terlebih dahulu, atau ketik 'cancel' untuk keluar dari proses order.")
            #     else:
            #         continue
            # else:
            #     continue
            
            #-- Postback Category Product --#
            if (postback_event == 'category'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                linebot.send_composed_carousel(msisdn, "pilih kategori", create_category(msisdn))

            #-- Postback Detail Product --#
            elif (postback_event == 'detail_product'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                id_brg = urlparse.parse_qs(parsed.query)['id_brg'][0]
                sql = "SELECT * FROM barang WHERE id_brg = '"+ id_brg +"'"
                sqlout = request(sql)

                columns = []
                for row in sqlout:
                    description = row[2]

                linebot.send_text_message(msisdn, description)

            #-- Postback Complain Product --#
            elif (postback_event == 'complain'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                onMessage(str(msisdn), 'complain', first_name)

            #-- Postback History Order --#
            elif (postback_event == 'historyorder'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                onMessage(str(msisdn), 'historyorder', first_name)

            #-- Postback Cancel Order --#
            elif (postback_event == 'cancelorder'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                cancelorder(msisdn)
                linebot.send_text_message(msisdn, "Baik kak kita cancel ya, \n Kalau pengen pesan minsu jangan malu-malu hubungin milki ya.")
                
            #-- Postback Select Rasa Product --#
            elif (postback_event == 'selecttaste'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                id_cat = urlparse.parse_qs(parsed.query)['id_cat'][0]
                sql = "SELECT distinct a.id_brg as id_brg, a.rasa as rasa,a.url_img as url_img,a.description as description FROM barang a INNER JOIN detail_barang b ON a.id_brg = b.id_brg WHERE b.id_cat = '"+ id_cat +"'"
                sqlout = request(sql)

                if len(sqlout) == 0:
                    linebot.send_text_message(msisdn, "Maaf barang untuk kategori ini belum tersedia")
                else:
                    linebot.send_composed_carousel(msisdn, "pilih rasa", create_taste(msisdn,sqlout))
            
            #-- Postback Select Size Product --#
            elif (postback_event == 'select_type'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                id_brg = urlparse.parse_qs(parsed.query)['id_brg'][0]
                
                linebot.send_composed_carousel(msisdn, "pilih tipe", create_taste_size(msisdn,id_brg))

            #-- Postback Input Jumlah Beli --#
            elif (postback_event == 'beli'):
                id_detailbrg = urlparse.parse_qs(parsed.query)['id_detailbrg'][0]
                v_state = parseJson({"state" : "stateOrder", "action" : "input jumlah order", "idDetailbrg" :  str(id_detailbrg)})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)
                
                # -- Set item selected
                v_chartshop = parseJson({"userid": str(msisdn), "item" : str(id_detailbrg)})
                lineNlp.redisconn.set("milkibot/%s/inputorder" % (msisdn), v_chartshop)

                onMessage(str(msisdn), 'ask total order', first_name)

            #-- Postback Display Shoping Chart --#
            elif (postback_event == 'showchartshop'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                linebot.send_text_message(msisdn, "Berikut detail pesanan kamu yaa , cek dulu ya siis")
                linebot.send_composed_carousel(msisdn, "keranjang belanja", create_chartshop(msisdn))
                confirm_chartshop(msisdn) #-- Display confirmasi chartshop

            #-- Postback Delete Item --#
            elif (postback_event == 'deleteitem'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                postback_iddetailbrg = urlparse.parse_qs(parsed.query)['id_detailbrg'][0]
                postback_chartid = urlparse.parse_qs(parsed.query)['chartid'][0]

                getChartshop = lineNlp.redisconn.get("milkibot/%s/chartshop" % (msisdn))
                jsonStr = getChartshop.decode("utf-8")
                parse_chartshop = json.loads(jsonStr)

                chartshop = []
                total_harga = 0
                for shopItems in parse_chartshop:
                    chartid = shopItems["chartid"]
                    id_brg = shopItems["id_brg"]
                    id_detail_brg = shopItems["id_detail_brg"]
                    type_size = shopItems["type_size"]
                    qty = shopItems["qty"]
                    harga = shopItems["harga"]
                    rasa = shopItems["rasa"]
                    url_img = shopItems["url_img"]
                    category = shopItems["category"]
                    
                    if str(shopItems["chartid"]) == str(postback_chartid):
                        # --Rollback stock
                        update_stock = "UPDATE detail_barang SET stock=stock+"+ str(qty) +" where id_detail_brg = '" + str(id_detail_brg) +"'"
                        update(update_stock)
                    else:
                        # -- Update data redis after delete item
                        chartshop.append({'chartid' : chartid, 'id_brg' : id_brg, 'id_detail_brg' : id_detail_brg, 'type_size' : type_size, 'qty' : qty, 'harga' : harga, 'rasa' : rasa, 'url_img' : url_img, 'category' : category})

                v_chartshop = parseJson(chartshop)
                lineNlp.redisconn.set("milkibot/%s/chartshop" % (msisdn), v_chartshop)

                linebot.send_text_message(msisdn, "Berikut detail pesanan kamu yaa , cek dulu ya siis")
                linebot.send_composed_carousel(msisdn, "keranjang belanja", create_chartshop(msisdn))
                confirm_chartshop(msisdn) #-- Display confirmasi chartshop

            elif (postback_event == 'confirmorder'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                onMessage(str(msisdn), 'confirmorder', first_name)

            elif (postback_event == 'finalorder'):
                v_state = parseJson({"state" : "stateOrder", "action" : postback_event})
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), v_state)

                orderid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                picorder = lineNlp.redisconn.get("milkibot/%s/picorder" % (msisdn))
                locationorder = lineNlp.redisconn.get("milkibot/%s/locationorder" % (msisdn))
                mailorder = lineNlp.redisconn.get("milkibot/%s/mailorder" % (msisdn))
                phoneorder = lineNlp.redisconn.get("milkibot/%s/phoneorder" % (msisdn))
                totalharga = lineNlp.redisconn.get("milkibot/%s/totalharga" % (msisdn))

                #-- Insert to table order
                insert_order = "insert into `order` (id_order,nama,tgl,lokasi,status_payment,harga,email,phone,lineid) values('"+ orderid +"','"+ picorder +"',CONVERT_TZ(NOW(),'+00:00','+07:00'),'"+ locationorder +"',1,'"+totalharga+"','"+ mailorder +"','"+ phoneorder + "','" + msisdn + "')"
                insert(insert_order)
                insert_tracker = "insert into `tracker` (id_order,datetime,status,description) values('" + orderid + "',CONVERT_TZ(NOW(),'+00:00','+07:00'),'waiting payment','')"
                insert(insert_tracker)
                
                #-- Insert to table detail order
                getChartshop = lineNlp.redisconn.get("milkibot/%s/chartshop" % (msisdn))
                jsonStr = getChartshop.decode("utf-8")
                parse_chartshop = json.loads(jsonStr)  

                chartshop = []
                flexitem = []
                detailorder = []
                hitung_harga = 0
                hitung_item = 0
                for shopItems in parse_chartshop:
                    chartid = shopItems["chartid"]
                    id_brg = shopItems["id_brg"]
                    id_detail_brg = shopItems["id_detail_brg"]
                    type_size = shopItems["type_size"]
                    qty = int(shopItems["qty"])
                    harga = int(shopItems["harga"])
                    rasa = shopItems["rasa"]
                    url_img = shopItems["url_img"]
                    category = shopItems["category"]
                    hitung_harga = hitung_harga + (harga * qty)
                    hitung_item = hitung_item + qty
                    
                    insert_detorder = "insert into `detail_order` (id_order,id_brg,qty) values('" + orderid + "','" + str(id_detail_brg) + "','" + str(qty) + "')"
                    insert(insert_detorder)

                    flexitem.append({
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": category + ' ' + rasa + ' ('+ type_size +') X ' + str(qty),
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(formatrupiah(int(harga))),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            }
                        ]
                    })
                
                cleansing_flexitem = ",".join(str(x) for x in flexitem)

                detailorder = [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "xxl",
                        "contents": [
                            {
                                "type": "text",
                                "text": "TOTAL BARANG",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": hitung_item,
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "xxl",
                        "contents": [
                            {
                                "type": "text",
                                "text": "TOTAL HARGA",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(formatrupiah(int(harga))),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "xxl",
                        "contents": [
                            {
                                "type": "text",
                                "text": "PAYMENT METHOD",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": '-',
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            }
                        ]
                    }
                ]
                cleansing_detailorder = ",".join(str(x) for x in detailorder)
                
                footer = [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "PAYMENT ID",
                                "size": "xs",
                                "color": "#aaaaaa",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "#" + str(orderid),
                                "color": "#aaaaaa",
                                "size": "xs",
                                "align": "end"
                            }
                        ]
                    }
                ]
                cleansing_footer = ",".join(str(x) for x in footer)

                #-- Cleansing temp history order
                lineNlp.redisconn.delete("milkibot/%s/picorder" % (msisdn))
                lineNlp.redisconn.delete("milkibot/%s/locationorder" % (msisdn))
                lineNlp.redisconn.delete("milkibot/%s/mailorder" % (msisdn))
                lineNlp.redisconn.delete("milkibot/%s/phoneorder" % (msisdn))
                lineNlp.redisconn.delete("milkibot/%s/totalharga" % (msisdn))
                lineNlp.redisconn.delete("milkibot/%s/chartshop" % (msisdn))
                lineNlp.redisconn.delete("milkibot/%s/inputorder" % (msisdn))
                lineNlp.redisconn.delete("milkibot/%s/status" % (msisdn))

                linktracker = "https://milki.herokuapp.com/tracker/status/" + str(orderid)

                message = "Terima kasih pesanannya segera kita proses. Untuk melakukan pembayaran dan memantau pesanan anda, klik aja link berikkut ya kak.\n" + linktracker
                linebot.send_text_message(msisdn, message)
                #linebot.send_text_message(msisdn, "Berikut order receiptnya ya kak..")
            

                # headers = {
                #     'Content-Type': 'application/json',
                #     'Authorization': 'Bearer {'+ LINE_TOKEN +'}',
                # }
                # data = flextemplateReceipt(msisdn,cleansing_flexitem,cleansing_detailorder,cleansing_footer)
                # print data

                # response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(data))

                # print response

            
@app.task(ignore_result=True)
def doworker_postmsg(req):
    content = json.dumps(req)
    content = json.loads(content)
    print ""
    print "================================ INCOMING MESSAGE FROM CMS ============================================="
    print content

    orderid = content["orderid"]
    status = content["status"]
    messages = content["messages"]
    description = content["description"]

    getStatusorder = lineNlp.redisconn.get("milkibot/%s/statusorder/%s" % (orderid,status))

    if getStatusorder is None:
        sql = "SELECT * FROM `order` WHERE id_order = '"+ orderid +"'"
        sqlout = request(sql)

        for row in sqlout:
            lineid = row[8]
        
        if status == '1':
            linebot.send_text_message(lineid, messages)
        elif status == '2' or status == '3':
            regexDesc = description.split(",")
            transaction_time = regexDesc[0]
            transaction_status = regexDesc[1]
            payment_type = regexDesc[2]
            linebot.send_text_message(lineid, messages + '\nPayment Method : ' + str(payment_type) + '\nTransaction Time : ' + str(transaction_time) + '\nStatus : ' + str(transaction_status))
            linebot.send_text_message("U6097f19983034aa9f02806f83ef8b29e", "MINSU STORE - Pesanan baru dengan id #" + str(orderid) + " telah menunggumu loh.")
        elif status == '4':
            regexDesc = description.split(",")
            shippingid = regexDesc[0]
            name = regexDesc[1]
            phone = regexDesc[2]
            linebot.send_text_message(lineid, messages + '\nShipingID : ' + str(shippingid) + '\nNama Kurir : ' + str(name) + '\nPhone : ' + str(phone))
        if status == '5':
            linktracker = "https://milki.herokuapp.com/tracker/status/" + str(orderid)

            linebot.send_text_message(lineid, messages)
            linebot.send_text_message(lineid, 'Untuk menyelesaikan proses order , silahkan confirm order pada link berikut\n' + linktracker)

        lineNlp.redisconn.set("milkibot/%s/statusorder/%s" % (orderid,status), content)