import src.graph as g
import src.value as v
import src.pressure as p
from datetime import datetime
from datetime import datetime

def is_single_digit(number):
    return isinstance(number, int) and 0 <= number <= 9

def draw(new_st,month_name):
    day_integer = datetime.strptime(month_name, '%B').month
    if is_single_digit(day_integer):
        day=str(day_integer)
        day="0"+day
    else:
        day=str(day_integer)
    new= "dependencies//txt_files//"
    print(day)
    if(new_st=="Platelets"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+new_st+".txt"))
        x=[int(r) for r in month_days.get(day, [])]
        y=[float(r) for r in month_data.get(day, [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,150000,450000,month_name, x_label="Day", y_label="Platelets", line_color='red')
    if(new_st=="Haemoglobin"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+new_st+".txt"))
        x=[int(r) for r in month_days.get(day, [])]
        y=[float(r) for r in month_data.get(day, [])]
        print(x,y)
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,13,17,month_name, x_label="Day", y_label="Haemoglobin", line_color='red')
    if(new_st=="RBC"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+new_st+".txt"))
        x=[int(r) for r in month_days.get(day, [])]
        y=[float(r) for r in month_data.get(day, [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,4.5,5.5, month_name,x_label="Day", y_label="RBC", line_color='red')

    if(new_st=="WBC"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+new_st+".txt"))
        x=[int(r) for r in month_days.get(day, [])]
        y=[float(r) for r in month_data.get(day, [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,4000,11000,month_name, x_label="Day", y_label="WBC", line_color='red')
    
    if(new_st=="Weight"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+new_st+".txt"))
        x=[int(r) for r in month_days.get(day, [])]
        y=[float(r) for r in month_data.get(day, [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,0,52,month_name, x_label="Day", y_label="Weight", line_color='red')

    if(new_st=="Screen"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+new_st+".txt"))
        x=[int(r) for r in month_days.get(day, [])]
        y=[float(r) for r in month_data.get(day, [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,2,4,month_name, x_label="Day", y_label="Screen", line_color='red')

    if(new_st=="Water"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+new_st+".txt"))
        x=[int(r) for r in month_days.get(day, [])]
        y=[float(r) for r in month_data.get(day, [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,2,4,month_name, x_label="Day", y_label="Water", line_color='red')
    
    if(new_st=="Pressure"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+new_st+".txt"))
        x=[int(r) for r in month_days.get(day, [])]
        y=[r for r in month_data.get(day, [])]
        if(x!=[] and y!=[]):
            print(x,y)
            p.pressure_bar(x,y)