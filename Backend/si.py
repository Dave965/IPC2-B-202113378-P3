from datetime import datetime, date

print(datetime.strptime(date.today().strftime("%d/%m/%Y"), '%d/%m/%Y').date())
