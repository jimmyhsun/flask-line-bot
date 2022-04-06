from flask import Flask, render_template, request , redirect
import sqlite3 as sql
import sqlite3


app = Flask(__name__)

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(num, alphabet=ALPHABET):
    """
    10进制转62进制
    :param num:
    :param alphabet:
    :return:
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    cool = len(num)
    base = len(alphabet)
    while cool:
        rem = cool % base
        cool = cool // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

@app.route('/', methods=['POST', 'GET'])
def index():
    try :
        conn = sqlite3.connect('database.db') #建立資料庫
        conn.cursor()
        conn.execute('CREATE TABLE shorturl (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, shorturl TEXT, longurl TEXT)')
        conn.close()
        return render_template("index.html")
    except :
        return render_template("index.html")

@app.route('/short', methods=['POST', 'GET'])
def short():

    if request.method == 'POST':
        global url
        url = request.form.get('url')
        index = str(url)
        token = base62_encode(index)

        short_url = str(f"https://urlchange.herokuapp.com/{token}".format(token=token))
        conn = sql.connect('database.db')
        cur = conn.cursor()
        cur.execute('insert into shorturl (shorturl,longurl) values (?,?)',(token,index))
        conn.commit()
        return render_template('index.html',short_url=short_url)



@app.route('/<token>')
def long_url(token):

    con = sql.connect("database.db")


    cur = con.cursor()
    cur.execute("select longurl from shorturl where shorturl=(?)", (token,))
    con.commit()
    rows = cur.fetchall()
    change = str(rows[0][0])


    return redirect(change)

if __name__ == "__main__":
    app.debug = True
    app.run()
