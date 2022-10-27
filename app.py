from flask import Flask, jsonify, render_template, request, session, redirect, url_for, abort, make_response, g
from flask_cors import CORS, cross_origin
from controller.user import *
from controller.payroll import *
from flask_apscheduler import APScheduler
import threading
import time
import json
import requests
import datetime
from datetime import datetime
app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.secret_key = "redsecretkey"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


scheduler = APScheduler()


@app.before_request
def before_request():
    now = datetime.now()
    datenowww = now.strftime("%Y-%m")
    g.countemployee = 0
    if 'user_id' in session:
        insertemployee = requests.get(
            'https://acumatica-firebase.firebaseio.com/Employee/'+session['user_id']+'.json')
        employeedir = json.dumps(insertemployee.json())
        employeeloads = json.loads(employeedir)
        g.user = employeeloads

        gettimein = requests.get(
            'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+datenowww+'/'+session['user_id']+'.json')
        gettimeindir = json.dumps(gettimein.json())
        gettimeinloads = json.loads(gettimeindir)
        g.usertimein = gettimeinloads

        getpayslip = requests.get(
            'https://acumatica-firebase.firebaseio.com/payslip/'+session['user_id']+'.json')
        getpayslipdir = json.dumps(getpayslip.json())
        getpaysliploads = json.loads(getpayslipdir)
        g.userpayslip = getpaysliploads

        getannouncements = requests.get(
            'https://acumatica-firebase.firebaseio.com/announcements/.json')
        getannouncementsdir = json.dumps(getannouncements.json())
        getannouncementsloads = json.loads(getannouncementsdir)
        g.announcements = getannouncementsloads

        getnotification = requests.get(
            'https://acumatica-firebase.firebaseio.com/notification/'+session['user_id']+'.json')
        getnotificationdir = json.dumps(getnotification.json())
        getnotificationloads = json.loads(getnotificationdir)
        g.getnotification = getnotificationloads

        checkifhasleave = requests.get(
            'https://acumatica-firebase.firebaseio.com/leave/'+datenowww+'/'+session['user_id']+'.json')
        checkifhasleavedir = json.dumps(checkifhasleave.json())
        checkifhasleaveloads = json.loads(checkifhasleavedir)
        g.leavedata = checkifhasleaveloads

    else:
        g.user = None


@app.template_filter('ctime')
def timectime(s):
    if s == 0000000000:
        return "no timeout"
    return time.ctime(s)


@app.route('/payrollcalculate')
def payroll():
    return jsonify(PayRolls.payrollcalculate())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        logindata = {
            'email': username,
            'password': password,
        }
        User.jsonglobal = logindata
        insertemployee = requests.get(
            'https://acumatica-firebase.firebaseio.com/Employee/'+username+'.json')
        employeedir = json.dumps(insertemployee.json())
        employeeloads = json.loads(employeedir)
        password2 = employeeloads['Password']
        role = employeeloads['Role']

        if password == password2:
            if role == '1':
                session['user_id'] = username
                return redirect(url_for('index'))
            elif role == '2':
                session['user_id'] = username
                return redirect(url_for('timein', value=username))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')


@ app.route('/timein/<value>', methods=['GET', 'POST'])
def timein(value):
    if g.user is None:
        return redirect(url_for('login'))
    return render_template('timein.html', value=value)


@ app.route('/timein2', methods=['GET', 'POST'])
def timein2():
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form.get("timein"):

            username = request.form['Username']
            print(username)
            now = datetime.now()
            d1 = now.strftime("%Y-%m-%d")
            d2 = now.strftime("%Y-%m")
            timestamp = datetime.timestamp(now)
            timestampstr = int(timestamp)

            data = {
                "TimeIn": timestampstr,
                "TimeOut": 0
            }
            inserttimelog = requests.patch(
                'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+d2+'/'+username+'/'+d1+'.json', json=data)
            print(inserttimelog)
        elif request.form.get("timeout"):
            username = request.form['Username']
            now = datetime.now()
            d1 = now.strftime("%Y-%m-%d")
            d2 = now.strftime("%Y-%m")
            timestamp = datetime.timestamp(now)
            timestampstr = int(timestamp)

            data = {
                "TimeOut": timestampstr
            }
            inserttimelog = requests.patch(
                'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+d2+'/'+username+'/'+d1+'.json', json=data)
            print(inserttimelog)
        elif request.form.get("leavebtn"):
            username = request.form['Username']
            leavenote = request.form['Leave']
            leaveDate = request.form['LeaveDate']
            leaveenddate = request.form['LeaveendDate']
            NumberofDays = request.form['NumberofDays']
            LeaveType = request.form['LeaveType']
            now = datetime.now()
            d1 = now.strftime("%Y-%m-%d")
            timestamp = datetime.timestamp(now)
            timestampstr = int(timestamp)

            data = {
                "LeaveNote": leavenote,
                "Applydate": d1,
                "LeaveDate": leaveDate,
                "Username": username,
                "LeaveendDate": leaveenddate,
                "NumberofDays": NumberofDays,
                "LeaveType": LeaveType,
            }
            inserttimelog = requests.patch(
                'https://acumatica-firebase.firebaseio.com/LeaveRequest/'+username+'/.json', json=data)
        elif request.form.get("save"):
            name = request.form['name']
            BirthDate = request.form['BirthDate']
            Age = request.form['Age']
            CivilStatus = request.form['CivilStatus']
            NameOfSpouse = request.form['NameOfSpouse']
            Gender = request.form['Gender']
            Address = request.form['Address']
            Number = request.form['Number']
            email = request.form['E-mail']
            EmergencyContact = request.form['EmergencyContact']
            Username = request.form['Username']
            Tin = request.form['Tin']
            SSS = request.form['SSS']
            PHIC = request.form['PHIC']
            HDMF = request.form['HDMF']

            Bank = request.form['Bank']
            AccountNo = request.form['AccountNo']
            AccountName = request.form['AccountName']
            PayOutOption = request.form['PayOutOption']
            employeedata = {
                'name': name,
                'BirthDate': BirthDate,
                'Age': Age,
                'CivilStatus': CivilStatus,
                'NameOfSpouse': NameOfSpouse,
                'Gender': Gender,
                'Address': Address,
                'Number': Number,
                'email': email,
                'EmergencyContact': EmergencyContact,
                'Tin': Tin,
                'SSS': SSS,
                'PHIC': PHIC,
                'HDMF': HDMF,

                'Bank': Bank,
                'AccountNo': AccountNo,
                'AccountName': AccountName,
                'PayOutOption': PayOutOption,

            }
            User.jsonglobal = employeedata
            return redirect(url_for('UserDynamo'))
    return redirect(url_for('timein', value=g.user['Username']))


@ app.route('/getcode', methods=['GET'])
def getcode():
    return 'OK'

# API ROUTES


@ app.route('/index')
def index():
    if g.user is None:
        return redirect(url_for('login'))
    now = datetime.now()
    datenowww = now.strftime("%Y-%m")
    gettimein = requests.get(
        'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+datenowww+'.json')
    gettimeindir = json.dumps(gettimein.json())
    gettimeinloads = json.loads(gettimeindir)

    for employees in gettimeinloads:
        g.countemployee = g.countemployee + 1
        print(employees)
    return render_template('index.html', timein=gettimeinloads)
    # return redirect(url_for('index'))


@ app.route('/profile')
def profile():
    if g.user is None:
        return redirect(url_for('login'))
    return render_template('profile.html')


@ app.route('/blank22', methods=['GET', 'POST'])
def blank22():
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form.get("accept"):
            employeeid = request.form['Username']
            numberofdays = request.form['NumberofDays']
            print(employeeid, numberofdays)
        if request.form.get("deny"):
            employeeid = request.form['leavedata']
            return redirect(url_for('elements', value=employeeid))


@ app.route('/leaveform', methods=['GET', 'POST'])
def leaveform():
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = g.user['Username']
        leavenote = request.form['Leave']
        leavestartdate = request.form['LeavestartDate']
        leaveenddate = request.form['LeaveendDate']
        NumberofDays = request.form['NumberofDays']
        LeaveType = request.form['LeaveType']
        now = datetime.now()
        d1 = now.strftime("%Y-%m")
        timestamp = datetime.timestamp(now)
        timestampstr = int(timestamp)
        data = {
            "LeaveNote": leavenote,
            "Applydate": d1,
            "LeaveDate": leavestartdate,
            "Username": username,
            "LeaveendDate": leaveenddate,
            "NumberofDays": NumberofDays,
            "LeaveType": LeaveType,
        }
        inserttimelog = requests.patch(
            'https://acumatica-firebase.firebaseio.com/leave/'+d1+'/'+username+'/.json', json=data)
        print(inserttimelog)
    return render_template('leaveform.html')


@ app.route('/employee-alt')
def employeealt():
    if g.user is None:
        return redirect(url_for('login'))
    return render_template('employee-alt.html')


@ app.route('/announcements', methods=['GET', 'POST'])
def announcements():
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        header = request.form['header']
        text = request.form['textarea']
        date = request.form['date']
        employeedata = {
            'header': header,
            'textarea': text,
            'date': date
        }
        insertannouncements = requests.patch(
            'https://acumatica-firebase.firebaseio.com/announcements/'+date+'/'+header+'.json', json=employeedata)

    return render_template('announcements.html')

    # return redirect(url_for('index'))


@ app.route('/announcements-alt')
def announcementsalt():
    if g.user is None:
        return redirect(url_for('login'))
    return render_template('announcements-alt.html')
    # return redirect(url_for('index'))


@ app.route('/employee-details-view')
def employeedetailsview():
    if g.user is None:
        return redirect(url_for('login'))

    return render_template('employee-details-view.html')
    # return redirect(url_for('index'))


@ app.route('/payslip')
def payslip():
    if g.user is None:
        return redirect(url_for('login'))
    return render_template('payslip.html')
    # return redirect(url_for('index'))


@ app.route('/timein')
def timein3():
    if g.user is None:
        return redirect(url_for('login'))
    return render_template('timein.html')
    # return redirect(url_for('index'))


@ app.route('/panels', methods=['GET', 'POST'])
def panels():
    if g.user is None:
        return redirect(url_for('login'))
    now = datetime.now()
    datenowww = now.strftime("%Y-%m")
    getemployee = requests.get(
        'https://acumatica-firebase.firebaseio.com/Employee.json')
    getemployeedir = json.dumps(getemployee.json())
    getemployeeloads = json.loads(getemployeedir)
    getleavereq = requests.get(
        'https://acumatica-firebase.firebaseio.com/leave/'+datenowww+'.json')
    getleavereqdir = json.dumps(getleavereq.json())
    getleavereqloads = json.loads(getleavereqdir)

    gettimein = requests.get(
        'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+datenowww+'.json')
    gettimeindir = json.dumps(gettimein.json())
    gettimeinloads = json.loads(gettimeindir)
    if request.method == 'POST':
        if request.form.get("edit"):
            employeeid = request.form['employeedata']
            return redirect(url_for('employeeview', value=employeeid))
        if request.form.get("View"):
            employeeid = request.form['leavedata']
            return redirect(url_for('elements', value=employeeid))
    return render_template('panels.html', value=getemployeeloads, leavereq=getleavereqloads, timein=gettimeinloads)


@ app.route('/leave-requests/<value>', methods=['GET', 'POST'])
def elements(value):
    if g.user is None:
        return redirect(url_for('login'))
    now = datetime.now()
    datenowww = now.strftime("%Y-%m")
    getleave = requests.get(
        'https://acumatica-firebase.firebaseio.com/leave/'+datenowww+'/'+value+'.json')
    getleavedir = json.dumps(getleave.json())
    getleaveloads = json.loads(getleavedir)
    print(getleaveloads)
    name = getleaveloads['Username']
    getemployeename = requests.get(
        'https://acumatica-firebase.firebaseio.com/Employee/'+name+'.json')
    getemployeenamedir = json.dumps(getemployeename.json())
    getemployeenameloads = json.loads(getemployeenamedir)
    if request.method == 'POST':
        username = request.form['Username']
        applydate = requests.form['ApplyDate']
        leavenote = request.form['Leave']

        leavedata = {
            "Leave": 1
        }
        leavepatch = requests.patch(
            'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+datenowww+'/'+username+'/'+applydate+'.json', json=leavedata)
        print(leavepatch)
        leavedeletepatch = requests.delete(
            'https://acumatica-firebase.firebaseio.com/leave/'+datenowww+'/'+username+'.json')
        print(leavedeletepatch)
    return render_template('blank2.html', value=getleaveloads, value1=getemployeenameloads)


@ app.route('/blank2', methods=['GET', 'POST'])
def blank2():
    if g.user is None:
        return redirect(url_for('login'))
    now = datetime.now()
    datenowww = now.strftime("%Y-%m")
    if request.method == 'POST':
        if request.form.get("accept"):
            employeeid = request.form['Username']
            numberofdays = request.form['NumberofDays']
            now = datetime.now()
            d1 = now.strftime("%Y-%m-%d")
            d2 = now.strftime("%Y-%m")
            getleave = requests.get(
                'https://acumatica-firebase.firebaseio.com/leave/'+datenowww+'/'+employeeid+'.json')
            getleavedir = json.dumps(getleave.json())
            getleaveloads = json.loads(getleavedir)

            name = getleaveloads['Username']
            getemployeename = requests.get(
                'https://acumatica-firebase.firebaseio.com/Employee/'+employeeid+'.json')
            getemployeenamedir = json.dumps(getemployeename.json())
            getemployeenameloads = json.loads(getemployeenamedir)
            leavecreditnow = getemployeenameloads['leaveCredit']
            if int(leavecreditnow) < int(numberofdays):
                return redirect(url_for('panels'))
            leavedata = {
                "Leave": int(numberofdays),
                "username": str(employeeid)
            }

            inserttimelog = requests.patch(
                'https://acumatica-firebase.firebaseio.com/leave/'+d2+'/'+employeeid+'.json', json=leavedata)

            leavedeletepatch = requests.delete(
                'https://acumatica-firebase.firebaseio.com/LeaveRequest/'+employeeid+'.json')
            dataforpatchh = {
                "leaveCredit": int(leavecreditnow) - int(numberofdays)
            }
            patchemployee = requests.patch(
                'https://acumatica-firebase.firebaseio.com/Employee/'+employeeid+'.json')
            return redirect(url_for('panels'))
        if request.form.get("deny"):
            employeeid = request.form['leavedata']
            return redirect(url_for('elements', value=employeeid))
    return render_template('blank2.html', value=getleaveloads, value1=getemployeenameloads)


@ app.route('/elements2', methods=['GET', 'POST'])
def elements2():
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['Username']
        applydate = request.form['ApplyDate']
        leavenote = request.form['Leave']

        leavedata = {
            "Leave": 1
        }
        leavepatch = requests.patch(
            'https://acumatica-firebase.firebaseio.com/TimeLogEntry/Aug1stCutoff/TimeLog/'+username+'/'+applydate+'.json', json=leavedata)
        print(leavepatch)
        leavedeletepatch = requests.delete(
            'https://acumatica-firebase.firebaseio.com/LeaveRequest/'+username+'.json')
        print(leavedeletepatch)
    return render_template('elements.html')


@ app.route('/employee-view/<value>', methods=['GET', 'POST'])
def employeeview(value):
    if g.user is None:
        return redirect(url_for('login'))
    getemployeee = requests.get(
        'https://acumatica-firebase.firebaseio.com/Employee/'+value+'.json')
    getemployeeedir = json.dumps(getemployeee.json())
    getemployeeeloads = json.loads(getemployeeedir)
    if request.method == 'POST':
        name = request.form['name']
        BirthDate = request.form['BirthDate']
        Age = request.form['Age']
        CivilStatus = request.form['CivilStatus']
        NameOfSpouse = request.form['NameOfSpouse']
        Gender = request.form['Gender']
        Address = request.form['Address']
        Number = request.form['Number']
        email = request.form['E-mail']
        EmergencyContact = request.form['EmergencyContact']
        Username = request.form['Username']
        Password = request.form['Password']

        Position = request.form['Position']
        Department = request.form['Department']
        Branch = request.form['Branch']
        Section = request.form['Section']
        EmployeeType = request.form['EmployeeType']
        Role = request.form['Role']
        JoinDate = request.form['JoinDate']
        RegularDate = request.form['RegularDate']
        BasicSalary = request.form['BasicSalary']
        Cola = request.form['Cola']
        Allowances = request.form['Allowances']
        ServiceCharge = request.form['ServiceCharge']
        HMO = request.form['HMO']
        Benefits = request.form['Benefits']
        Bio = request.form['Bio']

        Tin = request.form['Tin']
        SSS = request.form['SSS']
        PHIC = request.form['PHIC']
        HDMF = request.form['HDMF']

        Bank = request.form['Bank']
        AccountNo = request.form['AccountNo']
        AccountName = request.form['AccountName']
        PayOutOption = request.form['PayOutOption']
        employeedata = {
            'name': name,
            'BirthDate': BirthDate,
            'Age': Age,
            'CivilStatus': CivilStatus,
            'NameOfSpouse': NameOfSpouse,
            'Gender': Gender,
            'Address': Address,
            'Number': Number,
            'email': email,
            'EmergencyContact': EmergencyContact,
            'Username': Username,
            'Password': Password,

            'Position': Position,
            'Department': Department,
            'Branch': Branch,
            'Section': Section,
            'EmployeeType': EmployeeType,
            'Role': Role,
            'JoinDate': JoinDate,
            'RegularDate': RegularDate,
            'BasicSalary': BasicSalary,
            'Cola': Cola,
            'Allowances': Allowances,
            'ServiceCharge': ServiceCharge,
            'HMO': HMO,
            'Benefits': Benefits,
            'Bio': Bio,

            'Tin': Tin,
            'SSS': SSS,
            'PHIC': PHIC,
            'HDMF': HDMF,

            'Bank': Bank,
            'AccountNo': AccountNo,
            'AccountName': AccountName,
            'PayOutOption': PayOutOption,

        }
        User.jsonglobal = employeedata
        return redirect(url_for('UserDynamo'))

    # return render_template('employee-view.html', value=getemployeeeloads)
    return render_template('employee-view.html', value=getemployeeeloads)


@ app.route('/employee', methods=['GET', 'POST'])
def widgets():
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        BirthDate = request.form['BirthDate']
        Age = request.form['Age']
        CivilStatus = request.form['CivilStatus']
        NameOfSpouse = request.form['NameOfSpouse']
        Gender = request.form['Gender']
        Address = request.form['Address']
        Number = request.form['Number']
        email = request.form['E-mail']
        EmergencyContact = request.form['EmergencyContact']
        Username = request.form['Username']
        Password = request.form['Password']

        Position = request.form['Position']
        Department = request.form['Department']
        Branch = request.form['Branch']
        Section = request.form['Section']
        EmployeeType = request.form['EmployeeType']
        Role = request.form['Role']
        JoinDate = request.form['JoinDate']
        RegularDate = request.form['RegularDate']
        BasicSalary = request.form['BasicSalary']
        Cola = request.form['Cola']
        Allowances = request.form['Allowances']
        ServiceCharge = request.form['ServiceCharge']
        HMO = request.form['HMO']
        Benefits = request.form['Benefits']
        Bio = request.form['Bio']

        Tin = request.form['Tin']
        SSS = request.form['SSS']
        PHIC = request.form['PHIC']
        HDMF = request.form['HDMF']

        Bank = request.form['Bank']
        AccountNo = request.form['AccountNo']
        AccountName = request.form['AccountName']
        PayOutOption = request.form['PayOutOption']

        employeedata = {
            'first_name': first_name,
            'last_name': last_name,
            'name': first_name + " " + last_name,
            'BirthDate': BirthDate,
            'Age': Age,
            'CivilStatus': CivilStatus,
            'NameOfSpouse': NameOfSpouse,
            'Gender': Gender,
            'Address': Address,
            'Number': Number,
            'email': email,
            'EmergencyContact': EmergencyContact,
            'Username': Username,
            'Password': Password,

            'Position': Position,
            'Department': Department,
            'Branch': Branch,
            'Section': Section,
            'EmployeeType': EmployeeType,
            'Role': Role,
            'JoinDate': JoinDate,
            'RegularDate': RegularDate,
            'BasicSalary': BasicSalary,
            'Cola': Cola,
            'Allowances': Allowances,
            'ServiceCharge': ServiceCharge,
            'HMO': HMO,
            'Benefits': Benefits,
            'Bio': Bio,

            'Tin': Tin,
            'SSS': SSS,
            'PHIC': PHIC,
            'HDMF': HDMF,

            'Bank': Bank,
            'AccountNo': AccountNo,
            'AccountName': AccountName,
            'PayOutOption': PayOutOption,

        }
        insertemployee = requests.patch(
            'https://acumatica-firebase.firebaseio.com/Employee/'+Username+'.json', json=employeedata)
        print(insertemployee.json())

    return render_template('employee.html')


@ app.route('/payroll-settings', methods=['GET', 'POST'])
def charts():
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        CutOffs = request.form['CutOffs']
        PaternatyLeave = request.form['PaternatyLeave']
        MaternityLeave = request.form['MaternityLeave']
        SoloParentLeave = request.form['SoloParentLeave']
        VAWC = request.form['VAWC']
        LeaveforWomen = request.form['LeaveforWomen']
        FactorDays = request.form['FactorDays']
        LeaveCredit = request.form['LeaveCredit']
        tertimonth = request.form['13thMonthPay']
        Absenses = request.form['Absenses']
        Tardiness = request.form['Tardiness']
        PremiumPay = request.form['PremiumPay']
        CutOffDays = request.form['CutOffDays']
        ModeofPayment = request.form['ModeofPayment']
        WorkHours = request.form['WorkHours']
        WorkDays = request.form['WorkDays']
        settingsdata = {
            'CutOffs': CutOffs,
            'PaternatyLeave': PaternatyLeave,
            'MaternityLeave': MaternityLeave,
            'SoloParentLeave': SoloParentLeave,
            'VAWC': VAWC,
            'LeaveforWomen': LeaveforWomen,
            'FactorDays': FactorDays,
            'LeaveCredit': LeaveCredit,
            '13thMonthPay': tertimonth,
            'Absenses': Absenses,
            'Tardiness': Tardiness,
            'PremiumPay': PremiumPay,
            'CutOffDays': CutOffDays,
            'ModeofPayment': ModeofPayment,
            'WorkHours': WorkHours,
            'WorkDays': WorkDays,
        }
        postsettings = requests.patch(
            'https://acumatica-firebase.firebaseio.com/Settings.json', json=settingsdata)
    getsettings = requests.get(
        'https://acumatica-firebase.firebaseio.com/Settings.json')
    getsettingsdir = json.dumps(getsettings.json())
    getsettingsloads = json.loads(getsettingsdir)
    print(getsettingsloads)
    return render_template('payroll-settings.html', value=getsettingsloads)


@ app.route('/api/User')
def UserDynamo():
    return jsonify(User.UserDynamoAPI())

# UserAPI


@ app.route('/UserInsert', methods=['POST', 'GET'])
def userIns():
    content = request.form.to_dict()
    contents = json.dumps(content)
    contentloads = json.loads(contents)
    dictinsert = {"Insert": contentloads}
    User.jsonglobal = dictinsert
    return redirect(url_for('UserDynamo'))


def schedulerTask():
    now = datetime.now()
    datenoww = now.strftime("%Y-%m")
    datenowww = now.strftime("%Y-%m-%d")
    timestamp = datetime.timestamp(now)
    timestampstr = int(timestamp)

    d1 = now.strftime("%H:%M")
    if d1 == "23:50":
        getalltoday = requests.get(
            'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+datenoww+'.json')
    # print(getalltoday.json())
        getalltodaydir = json.dumps(getalltoday.json())
        getalltodayloads = json.loads(getalltodaydir)
        for (k, v) in getalltodayloads.items():
            gettodayonly = requests.get(
                'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+datenoww+'/'+k+'/'+datenowww+'.json')
            gettodayonlydir = json.dumps(gettodayonly.json())
            gettodayonlyloads = json.loads(gettodayonlydir)
            if gettodayonlyloads is not None:
                if 'TimeOut' in gettodayonlyloads:
                    print("donothing")
                else:
                    print("dosomething")
                    dataforpatch = {
                        "TimeOut": timestampstr
                    }
                    patchtotimeout = requests.patch(
                        'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+datenoww+'/'+k+'/'+datenowww+'.json', json=dataforpatch)


@app.errorhandler(404)
def page_not_found(e):
    if g.user is None:
        return redirect(url_for('login'))
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__main__':
    scheduler.add_job(id='Scheduled task', func=schedulerTask,
                      trigger='interval', seconds=1)
    scheduler.start()
    app.run(host='127.0.0.1', port=5000)
