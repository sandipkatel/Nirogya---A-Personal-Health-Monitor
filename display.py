import graph as g
import value as v
import pressure as p
def draw(str):
    new= "dependecies\\"
    if(str=="Platelets"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+str+".txt"))
        x=[int(r) for r in month_days.get("03", [])]
        y=[float(r) for r in month_data.get("03", [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,150000,450000,"Platelets", x_label="Day", y_label="Platelets", line_color='red')
    if(str=="Haemoglobin"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+str+".txt"))
        x=[int(r) for r in month_days.get("03", [])]
        y=[float(r) for r in month_data.get("03", [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,13,17,"Haemoglobin", x_label="Day", y_label="Haemoglobin", line_color='red')
    if(str=="RBC"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+str+".txt"))
        x=[int(r) for r in month_days.get("03", [])]
        y=[float(r) for r in month_data.get("03", [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,4.5,5.5, "RBC",x_label="Day", y_label="RBC", line_color='red')

    if(str=="WBC"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+str+".txt"))
        x=[int(r) for r in month_days.get("03", [])]
        y=[float(r) for r in month_data.get("03", [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,4000,11000,"WBC", x_label="Day", y_label="WBC", line_color='red')
    
    if(str=="Weight"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+str+".txt"))
        x=[int(r) for r in month_days.get("03", [])]
        y=[float(r) for r in month_data.get("03", [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,0,52,"Weight", x_label="Day", y_label="Weight", line_color='red')

    if(str=="Screen"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+str+".txt"))
        x=[int(r) for r in month_days.get("03", [])]
        y=[float(r) for r in month_data.get("03", [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,2,4,"Screen", x_label="Day", y_label="Screen", line_color='red')

    if(str=="Water"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+str+".txt"))
        x=[int(r) for r in month_days.get("03", [])]
        y=[float(r) for r in month_data.get("03", [])]
        if(x!=[] and y!=[]):
            g.plot_lagrange_interpolation(x, y,2,4,"Water", x_label="Day", y_label="Water", line_color='red')
    
    if(str=="Pressure"):
        month_days, month_data = v.separate_by_month(v.separeatedata(new+str+".txt"))
        x=[int(r) for r in month_days.get("03", [])]
        y=[r for r in month_data.get("03", [])]
        if(x!=[] and y!=[]):
            print(x,y)
            p.pressure_bar(x,y)