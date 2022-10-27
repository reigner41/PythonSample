import requests
import cgi
import cgitb
import os
import ssl
import sys
import json
import datetime
from datetime import datetime


class PayRolls:

    def payrollcalculate():
        now = datetime.now()
        d1 = now.strftime("%Y-%m-%d")
        d2 = now.strftime("%Y-%m")
        getperson = requests.get(
            'https://acumatica-firebase.firebaseio.com/Employee.json')
        getpersondir = json.dumps(getperson.json())
        getpersonloads = json.loads(getpersondir)
        for employeee in getpersonloads:
            # print(employeee)
            postdata = requests.get(
                'https://acumatica-firebase.firebaseio.com/Employee/'+employeee+'.json')
            postdatadir = json.dumps(postdata.json())
            postdataloads = json.loads(postdatadir)
            allowance = postdataloads['Allowances']
            basicSalary = postdataloads['BasicSalary']
            position = postdataloads['Position']
            Tin = postdataloads['Tin']
            email = postdataloads['email']
            name = postdataloads['name']
            employeetype = postdataloads['EmployeeType']
            username = postdataloads['Username']
            gettimeentry = requests.get(
                'https://acumatica-firebase.firebaseio.com/TimeLogEntry/'+d2+'/'+employeee+'.json')
            # gettimeentry = requests.get(
            #     'https://acumatica-firebase.firebaseio.com/TimeLogEntry/2020-10/'+employeee+'.json')
            gettimeentrydir = json.dumps(gettimeentry.json())
            gettimeentryloads = json.loads(gettimeentrydir)
            print(gettimeentryloads)
            if gettimeentryloads is None:
                print("nonde")
            else:
                hasleave = True
                hourselapsed = 0
                numberoddays = 0
                totalnumberoftime = 0

                getsettings = requests.get(
                    'https://acumatica-firebase.firebaseio.com/Settings.json')
                getsettingsdir = json.dumps(getsettings.json())
                getsettingsloads = json.loads(getsettingsdir)
                Cutoffs = getsettingsloads['CutOffs']
                FactorDays = getsettingsloads['FactorDays']
                Tardiness = getsettingsloads['Tardiness']
                basicSalary2 = int(basicSalary) / int(Cutoffs)
                allowance2 = int(allowance) / int(Cutoffs)
                dailyrate = (int(basicSalary) * 12) / int(FactorDays)
                hourlyrate = dailyrate / int(Tardiness)

                # sss
                sss = 0
                if int(basicSalary) > 10000:
                    sss = 420
                elif int(basicSalary) > 11000:
                    sss = 480
                elif int(basicSalary) > 12750:
                    sss = 520
                elif int(basicSalary) > 13750:
                    sss = 560
                elif int(basicSalary) > 16750:
                    sss = 680
                elif int(basicSalary) > 19250:
                    sss = 780
                elif int(basicSalary) > 19750:
                    sss = 800

                sss2 = int(sss) / int(Cutoffs)

                philhealth = 0
                # philhealth
                if int(basicSalary) > 10000:
                    philhealth = 137
                elif int(basicSalary) < 10001:
                    philhealth = int(basicSalary) * 0.03
                elif int(basicSalary) < 40000:
                    philhealth = 550

                philhealth2 = philhealth / int(Cutoffs)

                pagibig = 100
                pagibig2 = pagibig / int(Cutoffs)

                taxpercent = 0.00
                taxpercent1 = 0.00
                taxammount = 0
                if int(basicSalary) < 20000:
                    taxpercent = 0.00
                elif int(basicSalary) > 20000:
                    taxpercent = int(basicSalary) - sss - \
                        philhealth - pagibig - 20833
                    taxpercent1 = taxpercent * .20 / 2
                elif int(basicSalary) > 33333:
                    taxpercent = int(basicSalary) - sss - \
                        philhealth - pagibig - 33333 - 2500
                    taxpercent1 = taxpercent * .25 / 2
                elif int(basicSalary) > 66666:
                    taxpercent = int(basicSalary) - sss - \
                        philhealth - pagibig - 20833
                    taxpercent1 = taxpercent * .20 / 2
                elif int(basicSalary) > 166667:
                    taxpercent = int(basicSalary) - sss - \
                        philhealth - pagibig - 20833
                    taxpercent1 = taxpercent * .20 / 2
                johnformula1 = 0.00
                hasleave = False

                for (k, v) in gettimeentryloads.items():
                    if k == 'Leave':
                        leave = gettimeentryloads['Leave']
                        count = leave['Count']
                    timein = (v['TimeIn'])
                    timeout = (v['TimeOut'])
                    result = int(timeout) - int(timein)
                    sec_value = result % (24 * 3600)
                    hourvalue = sec_value // 3600
                    hourvalue = hourvalue - 1
                    totalnumberoftime = totalnumberoftime + hourvalue
                    if hourvalue > 8:
                        hourvalue = 8
                        numberoddays = numberoddays + 1
                    hourselapsed = hourselapsed + hourvalue
                    johnformula = (hourlyrate * hourvalue) - dailyrate
                    johnformula1 = johnformula1 + johnformula
                #salary = totalnumberoftime * hourlyrate + allowance2
                if hasleave == True:
                    if employeetype == 'Regular':
                        print('employeeisregular')
                    elif employeetype == 'Probitionary':
                        totalnumberofleave = dailyrate * float(count)
                        basicSalary2 = basicSalary2 - totalnumberofleave
                        print(totalnumberofleave)
                salary = basicSalary2 + allowance2 + johnformula1
                tax = basicSalary2 * taxpercent
                totalwithdeduction = salary - sss2 - philhealth2 - pagibig2 - taxpercent1
                TOTALDEDUC = sss2 + philhealth2 + pagibig2 + taxpercent1
                data = {
                    "Name": name,
                    "Position": position,
                    "Deminis Benefit": allowance2,
                    "Withholding Tax on Compensation": taxpercent1,
                    "SSS": sss2,
                    "Philhealth": philhealth2,
                    "Pag-Ibig": pagibig2,
                    "Total": salary,
                    "Total Deduction": TOTALDEDUC,
                    "NetPay": totalwithdeduction,
                    "email": email

                }
                requests.patch(
                    'https://acumatica-firebase.firebaseio.com/payslip/'+username+'.json', json=data)
                datafornotification = {
                    "Message": "payslip available for " + d1,
                    "data": d1
                }
                requests.patch('https://acumatica-firebase.firebaseio.com/notification/' +
                               username+'/' + d1 + '.json', json=datafornotification)
            # requests.post(
            #    'https://hooks.zapier.com/hooks/catch/6596733/oaxsxee/', json=data)
        return 'Success sending Payslip'
