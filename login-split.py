from flask import Flask, render_template, redirect, url_for, request
import pymysql
import pymysql.cursors

conn= pymysql.connect(host='localhost', user='root', password='Rainbow.86', db='ProjectTestDBA')
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello,World!'
    return redirect(url_for('Login'))


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/AdminWelcome', methods = ['GET', 'POST'])
def AdminWelcome():
    a = conn.cursor()
    error = None
    if request.method =='POST':
        name = request.form['UserName']
        print(name)
        password = request.form['Password']
        role = request.form['UserRole']
        addsql = 'INSERT INTO UserTable VALUES (%s, %s, %s)'
        a.execute(addsql, (name, password, role))
        conn.commit()
        return redirect(url_for('AdminWelcome'))
    return render_template('adminadd.html', error = error)

@app.route('/search', methods =['GET', 'POST'])
def ManagerHome():
    a = conn.cursor()
    error = None
    if request.method == 'POST':
        item = request.form['search']
        sql = 'SELECT * FROM ItemTable WHERE ItemName = %s'
        a.execute(sql, (item))
        results = a.fetchone()
        N1 = results[0]
        N2 = results[1]
        N3 = results[2]
        sql2 = 'INSERT INTO MatIndentTable VALUES (%s, %s, %s)'
        a.execute(sql2, (str(N1), str(N2), N3))
        conn.commit()
        print(results)
        #return(str(results))
        return redirect(url_for('PurchaseOrderCreate'))
    return render_template('search.html', error = error)

@app.route('/orderconfirm')
def PurchaseOrderCreate():
    a = conn.cursor()
    sql = 'INSERT INTO PurchaseOrder SELECT * FROM MatIndentTable'
    a.execute(sql)
    conn.commit()
    return redirect(url_for('CreateGoodsReceipt'))

@app.route('/goodsreceiptinfo')
def CreateGoodsReceipt():
    a = conn.cursor()
    sql = 'SELECT * FROM PurchaseOrder'
    a.execute(sql)
    results = a.fetchall()
    print(results)
    return redirect(url_for('ManagerHome'))

@app.route('/VendorHome')
def CustomerHome():
    return 'You are a vendor!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usern = request.form['username']
        passw = request.form['password']
        a = conn.cursor()
        sql = 'SELECT * FROM UserTable WHERE UserName = %s AND PasswordInf = %s'
        data = a.execute(sql, (usern, passw))
        data2 = a.fetchone()
        if data2[2] == "Admin":
            return redirect(url_for('AdminWelcome'))
        elif data2[2] == "Manager":
            return redirect(url_for('ManagerHome'))
        elif data2[2] == "Vendor":
            return redirect(url_for('VendorHome'))
        #....
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('fancylogin.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)


