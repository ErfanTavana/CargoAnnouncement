
from persiantools.jdatetime import JalaliDate

def convert_to_jalali(gregorian_date):
    # gregorian_date باید به شکل 'YYYY-MM-DD' باشد
    parts = gregorian_date.split('-')
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])

    jalali_date = JalaliDate.to_jalali(year, month, day)
    return f"{jalali_date.year}-{jalali_date.month:02d}-{jalali_date.day:02d}"


jalali_date = convert_to_jalali('2024-01-09')
print(jalali_date)



def convert_to_gregorian(jalali_date):
    # jalali_date باید به شکل 'YYYY-MM-DD' باشد
    parts = jalali_date.split('-')
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])

    jalali_obj = JalaliDate(year, month, day)
    gregorian_date = jalali_obj.to_gregorian()
    return f"{gregorian_date.year}-{gregorian_date.month:02d}-{gregorian_date.day:02d}"
gregorian_date = convert_to_gregorian('1402-10-19')
print(gregorian_date)

