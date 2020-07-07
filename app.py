from flask import Flask, render_template, request, url_for, Response, redirect
import sqlite3
import getpass

app = Flask(__name__, template_folder="templates", static_folder="assets")

user=getpass.getuser()
DB = "/Users/" + user + "/Documents/Development/Frontline/frontline.db"



@app.route('/',methods=['GET','POST'])
def index():
    """ This function renders the index template."""
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT [id], [Starttime], [Platform], [Client],[Instance], [Alert], [Case], [Comments] "
            "FROM Alert_Logs "
                "ORDER BY Starttime DESC LIMIT 15;")

    cur1 = con.cursor()
    cur1.execute('''SELECT [client], [startdate], [message], [enddate] FROM Shift_Change_Messages ORDER BY startdate DESC''')
    notes=cur1.fetchall();
    
    rows=cur.fetchall();
    return render_template("index.html", rows=rows,notes=notes)  




@app.route('/enter_new_alert',  methods=['POST','GET'])
def enter_new_alert():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    if request.method == 'POST':
        try:
            Starttime = request.form.get('Starttime')
            Platform = request.form.get('Platform')
            client = request.form.get('client')
            instance = request.form.get('instance')
            alert = request.form.get('alert')
            case = request.form.get('case')
            Comments = request.form.get('Comments')
            cur = con.cursor()
            cur.execute('''INSERT INTO Alert_Logs([Starttime], [Platform], [Client],[Instance], [Alert], [Case], [Comments]) VALUES(?,?,?,?,?,?,?)''',
                (Starttime, Platform, client, instance, alert, case, Comments))
            con.commit()
            msg="Record Successfully added"
        except:
            con.rollback()
            msg ="Error in insert operation"
        finally:
            return redirect('/')
            #return render_template('index.html',msg=msg)
            con.close()


@app.route('/enter_new_shift_change_note',methods=['POST','GET'])
def enter_new_shift_change_note():
    con=sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    if request.method == 'POST':
        try:
            client1 = request.form.get('client1')
            starttime1 = request.form.get('starttime1')
            message1 = request.form.get('message1')
            endtime1 =request.form.get('endtime1')
            cur = con.cursor()
            cur.execute('''INSERT INTO Shift_Change_Messages([client],[startdate],[message],[enddate]) VALUES(?, ?, ?, ?) ''',(client1,starttime1,message1,endtime1))
            con.commit()
        except:
            con.rollback()
        finally:
            msg="Successfully added shift change note"
            return redirect('/')



@app.route('/graphs',methods=['GET',])
def graphs():
	""" This function renders the index template."""
	return render_template("graphs.html")

app.run(host='0.0.0.0', port=8050, debug=True)