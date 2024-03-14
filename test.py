import json, datetime as dt
date = str(dt.datetime.now().year) +"-" + str(dt.datetime.now().month) + "-" + str(dt.datetime.now().day)
rollno = 102206286
name ="Aditya"
bra="bece"
branch_sel = {'bece':'ECE'}
branch_name={'bece':'Electronics and Communication Engineering'}
payload = f'{{"template": {{"id":"982526"}}, "data": {{"name": "{name}", "Date": "{date}", "branch": "{branch_sel[bra]}", "title": "Mr.", "roll_no": "{rollno}", "branch_name": "{branch_name[bra]}" }}, "format": "pdf", "output": "url", "name": "Certificate Example"}}'
print(payload)