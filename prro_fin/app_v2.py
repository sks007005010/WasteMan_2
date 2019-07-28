from flask import Flask,Markup, render_template
import pymongo
import random
from datetime import datetime,timedelta  
import doctest
from itertools import permutations
import dns
import folium
from math import sin, cos, sqrt, atan2, radians
app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://sitesh:Sitesh$$#5@cluster0-9jms6.azure.mongodb.net/test?retryWrites=true&w=majority")


def get_per_waste(): 
    time = datetime.now() - timedelta(days = 3) 

    mydb = myclient["Waste_Management"]
    timestampStr = time.strftime("%d-%b-%Y")
    mycol = mydb[timestampStr]
    waste_per_wet = []
    res_name_wet = []
    waste_per_dry = []
    res_name_dry = []
    for x in mycol.find():
        if (x['_id'] % 2 == 0):
            waste_per_wet.append(x['waste_per'])
            res_name_wet.append(x['Res_name'])
        else:
            waste_per_dry.append(x['waste_per'])
            res_name_dry.append(x['Res_name'])
    
    return waste_per_wet,res_name_wet,waste_per_dry,res_name_dry
def get_corr():
    time = datetime.now() - timedelta(days = 3) 

    mydb = myclient["Waste_Management"]
    timestampStr = time.strftime("%d-%b-%Y")
    mycol = mydb[timestampStr]
    corr_dry = []
    corr_wet = []
    for x in mycol.find():
        if (x['waste_per']>=60):
        
            if (x['_id'] % 2 == 0):
                corr_wet.append(x['Res_cor'])
            else:
                
                corr_dry.append(x['Res_cor'])
    
    return corr_wet,corr_dry
waste_per_wet,name_wet,waste_per_dry,name_dry =get_per_waste()
def get_map(corr_lst,waste_per,waste_type):
    c=[]
    for i in waste_per:
        if i < 60:
            c.append("green")
           
        else:
            c.append("red")
    Starting_point = [12.97229,77.68118]
    corr_lst.append(Starting_point)
    my_map4 = folium.Map([12.97229,77.68118],zoom_start = 11.5) 
    folium.Marker([13.0708,77.65186],popup = 'Rest1',icon=folium.Icon(color=c[0])).add_to(my_map4) 
    folium.Marker([13.02248,77.55055],popup = 'Rest2',icon=folium.Icon(color=c[1])).add_to(my_map4) 
    folium.Marker([12.99196,77.58831],popup = 'Rest3',icon=folium.Icon(color=c[2])).add_to(my_map4)
    folium.Marker([12.96736,77.59559],popup = 'Rest4',icon=folium.Icon(color=c[3])).add_to(my_map4)
    folium.Marker([12.97923,77.72845],popup = 'Rest5',icon=folium.Icon(color=c[4])).add_to(my_map4)
    folium.Marker([12.82465,77.68118],popup = 'Rest6',icon=folium.Icon(color=c[5])).add_to(my_map4)
    folium.Marker([12.97229,77.68118],popup = 'Starting point',icon=folium.Icon(color='darkpurple')).add_to(my_map4)

    
    database_list=optimum_path(corr_lst) 
    folium.PolyLine(locations = database_list,line_opacity = 0.5).add_to(my_map4)
    path_str = "/home/project/WasteMan_2/prro_fin/templates/map"+ waste_type+".html"
    my_map4.save(path_str)

cor_wet,cor_dry = get_corr()
    
def dist(p1,p2):
    R = 6373.0

    lat1 = radians(p1[0])
    lon1 = radians(p1[1])
    lat2 = radians(p2[0])
    lon2 = radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def total_distance(points):
    return sum([dist(point, points[index + 1]) for index, point in enumerate(points[:-1])])
def optimum_path(points, start=[12.97229,77.68118]):
    if start is None:
        start = points[0]
    return min([perm for perm in permutations(points) if perm[0] == start], key=total_distance)
    
    
    

@app.route("/home")
def home_page():
    return render_template('home.html')
    
@app.route("/about")
def about_page():
    return render_template('about.html')
    
@app.route("/res")
def res_page():
    return render_template('restaurant.html')
    
@app.route("/driver")
def driver_page():
    return render_template('driver.html')
 
@app.route("/map")
def google_map1():
    waste_per_wet,name_wet,waste_per_dry,name_dry =get_per_waste()
    cor_wet,cor_dry = get_corr()
    get_map(cor_dry,waste_per_dry,"dry")
    return render_template('mapdry.html')
    
@app.route("/map1")
def google_map2():
    waste_per_wet,name_wet,waste_per_dry,name_dry =get_per_waste()
    cor_wet,cor_dry = get_corr()
    get_map(cor_wet,waste_per_wet,"wet")
    return render_template('mapwet.html')
 
@app.route("/wet_chart")
def chart_wet():
    waste_per_wet1,name_wet1,waste_per_dry1,name_dry1 =get_per_waste()
    return render_template('chart_v2.html',waste_per=waste_per_wet1,name=name_wet1)
    
@app.route("/dry_chart")
def chart_dry():
    waste_per_wet1,name_wet1,waste_per_dry1,name_dry1 =get_per_waste()
    return render_template('chart_v2.html',waste_per=waste_per_dry1,name=name_dry1)

@app.route("/mylink1")
def clear_bar1():
    waste_per_dry[0] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink2")
def clear_bar2():
    waste_per_dry[1] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink3")
def clear_bar3():
    waste_per_dry[2] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
 
@app.route("/mylink4")
def clear_bar4():
    waste_per_dry[3] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink5")
def clear_bar5():
    waste_per_dry[4] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink6")
def clear_bar6():
    waste_per_dry[5] = "0"
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink1")
def clear_bar7():
    waste_per_wet[0] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
    
@app.route("/mylink2")
def clear_bar8():
    waste_per_wet[1] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
   
@app.route("/mylink3")
def clear_bar9():
    waste_per_wet[2] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
 
@app.route("/mylink4")
def clear_bar10():
    waste_per_wet[3] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
    
@app.route("/mylink5")
def clear_bar11():
    waste_per_wet[4] = "0" 
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
    
@app.route("/mylink6")
def clear_bar12():
    waste_per_wet[5] = "0"
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001,debug="True")
