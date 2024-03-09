

from collections import defaultdict
# from graph import plot_lagrange_interpolation
# from graph import lagrange_interpolation
def separeatedata(abc):
    x_values = []
    with open(abc) as f:
        contents = f.readlines()
    for i in contents:
        x_values.append((i[:-1]))
    return x_values

def separate_by_month(data_list):
    month_days = defaultdict(list)
    month_data = defaultdict(list)

    for entry in data_list:
        date, value = entry.split(':')
        _, month, day = date.split('/')
        month_key = f"{month}"
        month_days[month_key].append(day)
        month_data[month_key].append(value.strip())

    return month_days, month_data

