import email
from flask import Flask, render_template,request,session,redirect,url_for,make_response
from werkzeug.wrappers import response
from DBConnection import Db
from flask_mail import Mail, Message
from random import randint
import pdfkit
from user_test import test1
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders

app = Flask(__name__)
mail = Mail(app)
 

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sicklecellanemiasca@gmail.com'
app.config['MAIL_PASSWORD'] = 'ihpxfpfkwjtwyotx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 
otp=randint(000000,999999)

static_path="home\\afzal\\Desktop\\LDwebapp\\static\\"
app.secret_key="LDAPP900"

@app.route('/')
def hello_world():
    return render_template('webapp.html')

@app.route('/login')
def login_page1():
    return render_template('user_login_page.html')

@app.route('/loginverify',methods=['post'])
def loginpost234():
    username=request.form['username']
    db=Db()
    re=db.selectOne(" SELECT* FROM login WHERE username='"+username+"'")
    if re is not None:
        re77=re['Verified']
        lid=re['login_id']
        session['lid']=lid
        if re77=="Not_Verified":
            msg = Message('OTP',sender ='sicklecellanemiasca@gmail.com',recipients = [username])
            msg.body="Hello,\r\n Your OTP is  "+str(otp)+"."
            mail.send(msg)
            return render_template('otpverification.html')
        elif re77=="Verified":
                msg = Message('Login Info',sender ='sicklecellanemiasca@gmail.com',recipients = [username])
                msg.body="Hello,\r\n You are logged in CCA-Webapp Successfully.\r\n"
                mail.send(msg)
                return redirect(url_for('login_page1'))
    else:
        return render_template('message11.html')

@app.route('/loginpost',methods=['post'])
def loginpost():
    username=request.form['username']
    password=request.form['password']
    db=Db()
    re=db.selectOne(" SELECT* FROM login WHERE username='"+username+"' AND  PASSWORD='"+password+"'")
    if re is not None:
        type=re['usertype']
        re77=re['Verified']
        lid=re['login_id']
        session['lid']=lid
        if type=="admin":
            return redirect(url_for('admin'))
        elif type=="user":
            if re77=="Not_Verified":
                msg = Message('OTP',sender ='sicklecellanemiasca@gmail.com',recipients = [username])
                msg.body="Hello, Your OTP is  "+str(otp)+"."
                mail.send(msg)
                return render_template('otpverification.html')
            else:
                return redirect(url_for('user_account2'))
    else:
        return render_template('message1.html')

@app.route('/signup')
def register_user():
    return render_template('user_signup.html')

@app.route('/verifyemailid')
def register_user56():
    return render_template('verifyemail.html')

@app.route('/otpverification')
def register_user5623():
    return render_template('otpverification.html')
  
@app.route('/otpverificationpost',methods=['POST'])
def otpverificationpost():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        db=Db()
        lid=session['lid']
        res98=db.selectOne("select* from login where login_id='"+str(lid)+"'")
        db1=Db()
        re390=db1.update("UPDATE login SET Verified='Verified' WHERE login_id='"+str(lid)+"'")
        re394=db1.update("UPDATE user_table SET Verified='Verified' WHERE login_id='"+str(lid)+"'")
        return render_template('message10.html')
    else:
        return render_template('message9.html')

@app.route('/registerpost',methods=['post'])
def registerpost():
    firstname=request.form['fname']
    lastname=request.form['lname']
    gender=request.form['gender']
    dateofbirth=request.form['dob']
    mobilenumber=request.form['mob']
    emailid=request.form['email']
    password=request.form['password']
    db=Db()
    res5558=db.selectOne(" SELECT* FROM login WHERE username='"+emailid+"'")
    if res5558 is not None:
        return render_template('message2.html')
    else:
        re2312=db.insert("INSERT INTO login VALUES(NULL ,'"+emailid+"','"+password+"','user',CURDATE(),CURTIME(),'Not_Verified')")
        re345=db.selectOne(" SELECT* FROM login WHERE username='"+emailid+"' AND  PASSWORD='"+password+"'")
        lid=re345['login_id']
        session['lid']=lid
        re42=db.insert("INSERT INTO user_table VALUES(NULL ,'"+firstname+"','"+lastname+"','"+gender+"','"+dateofbirth+"','"+emailid+"','"+mobilenumber+"','"+str(lid)+"','Not_Verified')")
        msg = Message('Login Info',sender ='sicklecellanemiasca@gmail.com',recipients = [emailid])
        msg.body="Hello,\r\n\r\nYour Login Informations\r\n\r\n" "Username= "+emailid+".\r\nPassword= "+password
        mail.send(msg)
        return render_template('message8.html')
               
@app.route('/useraccount')
def user_account2():
    db=Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    lid = session['lid']
    res98=db.selectOne("select* from user_table where login_id='"+str(lid)+"'")
    return render_template('user_account.html',data=res98)

@app.route('/viewprofile')
def user_profile():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    lid=session['lid']
    res5=db.selectOne("select* from user_table where login_id='"+str(lid)+"'")
    return render_template('userprofile.html',data=res5)


@app.route('/back')
def user_account3():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return redirect(url_for('user_account2'))

@app.route('/leukemiainfo')
def leukemia_info():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return render_template('Leukemia_info.html')

@app.route('/back')
def user_account4():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return render_template('user_account.html')

@app.route('/taketest')
def take_test():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return render_template('clientdetails.html')
@app.route('/taketest1')
def take_test1():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return render_template('clientdetails1.html')

@app.route('/taketesthistory',methods=['POST'])
def take_testpost():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    firstname=request.form['fname']
    lastname=request.form['lname']
    gender=request.form['gender']
    Age=request.form['age']
    bloodgroup=request.form['bloodroup']
    email=request.form['email']
    mobilenumber=request.form['mob']
    lid = session['lid']
    re42=db.insert("INSERT INTO client_table VALUES(NULL ,'"+firstname+"','"+lastname+"','"+gender+"','"+Age+"','"+bloodgroup+"','"+mobilenumber+"',CURDATE(),CURTIME(),'" + str(lid) + "',NULL,'"+email+"')")
    session['cl_id']=re42
    return render_template('taketest.html')

@app.route('/taketesthistory1',methods=['POST'])
def take_testpost1():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    firstname=request.form['fname']
    lastname=request.form['lname']
    gender=request.form['gender']
    Age=request.form['age']
    bloodgroup=request.form['bloodroup']
    email=request.form['email']
    mobilenumber=request.form['mob']
    lid = session['lid']
    re42=db.insert("INSERT INTO client_table VALUES(NULL ,'"+firstname+"','"+lastname+"','"+gender+"','"+Age+"','"+bloodgroup+"','"+mobilenumber+"',CURDATE(),CURTIME(),'" + str(lid) + "',NULL,'"+email+"')")
    session['cl_id']=re42
    return render_template('taketest1.html')

@app.route("/taketest_post",methods=['post'])
def taketest_post():
    file=request.files['myfile']
    import time
    timestr=time.strftime("%Y%m%d_%H%M%S")
    filename=timestr+".jpg"
    file.save(static_path+"uploads\\"+filename)
    t1=test1()
    res=t1.find_result(filename)
    cl_id=str(session['cl_id'])
    db=Db()
    db.update("update client_table set test_result='"+res+"' where client_id='"+cl_id+"'")
    return render_template("testresult.html",data=res)

@app.route("/taketest_postadmin",methods=['post'])
def taketest_post1():
    file=request.files['myfile']
    import time
    timestr=time.strftime("%Y%m%d_%H%M%S")
    filename=timestr+".jpg"
    file.save(static_path+"uploads\\"+filename)
    t1=test1()
    res=t1.find_result(filename)
    cl_id=str(session['cl_id'])
    db=Db()
    db.update("update client_table set test_result='"+res+"' where client_id='"+cl_id+"'")
    return render_template("testresultadmin.html",data=res)


@app.route('/download',methods=['GET'])
def download():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    cl_id = str(session['cl_id'])
    res98 = db.selectOne("select * from client_table where client_id='" + str(cl_id) + "'")
    html = render_template('pdf.html',data=res98)
    pdf = pdfkit.from_string(html,static_path+"TestResult.pdf")
    mail_content = "Hello,\r\n\r\nYour Test Result is here,\r\n\r\n" 
    sender_address = 'sicklecellanemiasca@gmail.com'
    sender_pass = 'ihpxfpfkwjtwyotx'
    receiver_address = res98['email']
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Test_Result'
    message.attach(MIMEText(mail_content, 'plain'))
    with open(static_path+"TestResult.pdf","rb") as f:
        attach=MIMEApplication(f.read(),_subtype="pdf")
    attach.add_header("Content-Disposition","attachment",filename="TestResult.pdf")
    message.attach(attach)
    sess = smtplib.SMTP('smtp.gmail.com', 587)
    sess.starttls() 
    sess.login(sender_address, sender_pass)
    text = message.as_string()
    sess.sendmail(sender_address, receiver_address, text)
    sess.quit()
    pdf = pdfkit.from_string(html,False)
    response = make_response(pdf)
    response.headers["Content-Type"]="application/pdf"
    response.headers["Content-Disposition"]="inline; filename=TestResult.pdf"
    return response

@app.route('/changepassword')
def change_password():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return render_template('changepassword.html')

@app.route('/changepasswordpost',methods=['post'])
def changepasswordpost():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    currpassword=request.form['currpass']
    newpassword=request.form['newpass']
    conpassword=request.form['conpass']
    lid=session['lid']
    db=Db()
    re4=db.selectOne("select* from login where login_id='"+str(lid)+"' AND password='"+currpassword+"'")
    if re4 !=None:
        if currpassword==newpassword:
            return render_template('message6.html')
        elif newpassword==conpassword:
                db1=Db()
                re390=db1.update("UPDATE login SET PASSWORD='"+newpassword+"' WHERE login_id='"+str(lid)+"'")
                re42=db1.selectOne("select* from login where login_id='"+str(lid)+"' AND password='"+newpassword+"'")
                email=re42['username']
                msg = Message('Password Changed',sender ='sicklecellanemiasca@gmail.com',recipients = [email])
                msg.body = 'Hello! \r\n\r\n Your are successfully Changed Your Password.\r\n\r\n Your New password is  '+newpassword
                mail.send(msg)
                return render_template('message3.html')
        elif newpassword!=conpassword:
                return render_template('message4.html')
        else:
            return render_template('message5.html')

@app.route('/addfeedback')
def add_feedback():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return render_template('addfeedback.html')

@app.route('/addfeedbackpost',methods=['post'])
def addfeedbackpost():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    lid=session['lid']
    feedback=request.form['subject']
    db=Db()
    re3=db.insert("INSERT INTO feedback VALUES(NULL ,'"+str(lid)+"','"+feedback+"',CURDATE(),CURTIME())")
    return render_template('message7.html')

@app.route('/contactus')
def contact_us():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return render_template('contactus.html')

@app.route('/submit')
def login_page2():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return render_template('user_login_page.html')


@app.route('/adminhome')
def admin():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    lid = session['lid']
    res98 = db.selectOne("select* from login where login_id='" + str(lid) + "'")
    return render_template('adminhomepage.html',data=res98)



@app.route('/testresult')
def admin3():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    return render_template("testresult.html")


@app.route('/viewuser')
def admin4():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    re1=db.select("SELECT* FROM user_table")
    if  len(re1)>0:
        return render_template('viewuser.html',data=re1)
    else:
        return '<script>alert("No Dta");window.location="/adminhome";</script>'

@app.route('/viewtesthistory')
def admin5():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    re1=db.select("SELECT* FROM client_table")
    if  len(re1)>0:
        return render_template('viewhistory.html',data=re1)
    else:
        return '<script>alert("No Dta");window.location="/adminhome";</script>'

@app.route('/viewfeedbacks')
def admin6():
    db = Db()
    if session.get('lid') is None:
        return render_template('message12.html')
    re2 = db.select("SELECT feedback.*,user_table.* FROM feedback,USER_table WHERE user_table.login_id=feedback.login_id")
    if len(re2) > 0:
        return render_template('viewfeedback.html', data=re2)
    else:
        return '<script>alert("No Dta");window.location="/adminhome";</script>'

@app.route('/logout')
def admin8():
    db = Db()
    session.clear()
    return redirect(url_for('hello_world'))

if __name__ == '__main__':
    app.run(debug=True)

 
