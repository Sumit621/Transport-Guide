from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from tg.models import BusRoutes
from tg.models import UserPrefHist
import folium

def Djik3node(request):
    if request.method=="POST":
        start=request.POST.get("start")
        dest=request.POST.get("dest")
        via=request.POST.get("via")
        graph={}
        dataSet=BusRoutes.objects.all()
        for item in dataSet:
            rBus=item.values.split(",")
            dictVal=[]
            for j in rBus:
                tup=tuple(j.split("_"))
                dictVal.append(tup)
            graph[item.place]=dictVal

        if start not in graph.keys():
            return HttpResponse("<h1>Starting Point not Identified!</h1>")
        
        queue=[[start]]
        visited=[]

        if start == via:
            return HttpResponse("<h1>You are already at your Via!</h1>")

        new_path=[]
        flag=True
        path=queue.pop(0)
        node=path[-1]
        if node not in visited:
            adjacent=graph[node]
            for i in adjacent and flag==True:
                new_path=list(path)
                new_path.append(i)
                queue.append(new_path)
                if i[0] == via:
                    flag=False
        visited.append(node)

        while queue and flag==True:
            path=queue.pop(0)
            node=path[-1]
            if node[0] not in visited and flag==True:
                adjacent=graph[node[0]]
                for i in adjacent and flag==True:
                    new_path=list(path)
                    new_path.append(i)
                    queue.append(new_path)
                    if i[0] == via:
                        flag=False
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
            visited.append(node[0])
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        
        if flag==True:
            return HttpResponse("<h1>There is no required Bus Route</h1>")

        queue=[[via]]
        visited=[]

        if via == dest:
            return HttpResponse("<h1>You are already at your Destination!</h1>")

        new_path2=[]
        flag=True
        path=queue.pop(0)
        node=path[-1]
        if node not in visited:
            adjacent=graph[node]
            for i in adjacent and flag==True:
                new_path2=list(path)
                new_path2.append(i)
                queue.append(new_path2)
                if i[0] == dest:
                    flag=False
        visited.append(node)

        while queue and flag==True:
            path=queue.pop(0)
            node=path[-1]
            if node[0] not in visited and flag==True:
                adjacent=graph[node[0]]
                for i in adjacent and flag==True:
                    new_path2=list(path)
                    new_path2.append(i)
                    queue.append(new_path2)
                    if i[0] == dest:
                        new_path2.pop(0)
                        flag=False
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
            visited.append(node[0])
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        if flag==True:
            return HttpResponse("<h1>There is no required Bus Route</h1>")
        final_path=new_path+new_path2
        txt=""
        for it in range(1,len(final_path)-1):
            if final_path[it][1]!=final_path[it+1][1]:
                    txt=txt+"Go upto "+final_path[it][0]+" in "+final_path[it][1]+". "
        txt=txt+"Go upto "+final_path[-1][0]+" in "+final_path[-1][1]+"."
        print(txt)
        return HttpResponse("<h1>{}</h1>".format(txt))

def showMap(start,dest):
    A_lat=start.geoLocLat
    A_lon=start.geoLocLon
    pointA=(A_lat,A_lon)
    B_lat=dest.geoLocLat
    B_lon=dest.geoLocLon
    pointB=(B_lat,B_lon)
    m=folium.Map(width=800,height=500,location=getCenter(A_lat,A_lon,B_lat,B_lon))
    folium.Marker([A_lat,A_lon],tooltip='Click for details',popup=start.place,
                   icon=folium.Icon(color='blue')).add_to(m)
    
    folium.Marker([B_lat,B_lon],tooltip='Click for details',popup=dest.place,
                   icon=folium.Icon(color='red', icon='cloud')).add_to(m)
    m._repr_html_()
    return m

def getCenter(latA,lonA,latB=None,lonB=None):
    cord=(latA,lonA)
    if latB:
        cord=[(latA+latB)/2,(lonA+lonB)/2]
    return cord

def FareCalc(num):
    if num<3:
        return 'Tk.120'
    elif num>=3 and num<5:
        return 'Tk.150'
    elif num>=5 and num<7:
        return 'Tk.200'
    elif num>=8 and num<10:
        return 'Tk.250'
    elif num>=10 and num<13:
        return 'Tk.300'
    elif num>=13 and num<15:
        return 'Tk.350'
    elif num>=15 and num<17:
        return 'Tk.400'
    elif num>=17:
        return 'Tk.500'

def getCNGfare(request):
    if request.method=="POST":
        start=request.POST.get("start")
        dest=request.POST.get("dest")
        graph={}
        dataSet=BusRoutes.objects.all()
        for item in dataSet:
            rRoads=item.roads.split(",")
            graph[item.place]=rRoads
        if start not in graph.keys():
            return HttpResponse("<h1>Starting Point not Identified!</h1>")
        queue=[[start]]
        visited=[]

        if start == dest:
            return HttpResponse("<h1>You are already at your Destination!</h1>")

        path=queue.pop(0)
        node=path[-1]
        if node not in visited:
            adjacent=graph[node]
            for i in adjacent:
                new_path=list(path)
                new_path.append(i)
                queue.append(new_path)
                if i == dest:
                    dist=len(new_path)
                    fare=FareCalc(dist)
                    return HttpResponse("<h1>You will have to pay around {}</h1>".format(fare))
        visited.append(node)

        while queue:
            path=queue.pop(0)
            node=path[-1]
            if node[0] not in visited:
                adjacent=graph[node]
                for i in adjacent:
                    new_path=list(path)
                    new_path.append(i)
                    queue.append(new_path)
                    if i == dest:
                        dist=len(new_path)
                        fare=FareCalc(dist)
                        return HttpResponse("<h1>You will have to pay around {}</h1>".format(fare))
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
            visited.append(node[0])
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        return HttpResponse("<h1>There is no required Road Route</h1>")

def getCNGviaFare(request):
    if request.method=="POST":
        start=request.POST.get("start")
        dest=request.POST.get("dest")
        via=request.POST.get("via")
        graph={}
        dataSet=BusRoutes.objects.all()
        for item in dataSet:
            rRoads=item.roads.split(",")
            graph[item.place]=rRoads

        if start not in graph.keys():
            return HttpResponse("<h1>Starting Point not Identified!</h1>")
        
        queue=[[start]]
        visited=[]

        if start == via:
            return HttpResponse("<h1>You are already at your Via!</h1>")

        new_path=[]
        flag=True
        path=queue.pop(0)
        node=path[-1]
        if node not in visited:
            adjacent=graph[node]
            for i in adjacent and flag==True:
                new_path=list(path)
                new_path.append(i)
                queue.append(new_path)
                if i == via:
                    flag=False
        visited.append(node)

        while queue and flag==True:
            path=queue.pop(0)
            node=path[-1]
            if node[0] not in visited and flag==True:
                adjacent=graph[node[0]]
                for i in adjacent and flag==True:
                    new_path=list(path)
                    new_path.append(i)
                    queue.append(new_path)
                    if i[0] == via:
                        flag=False
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
            visited.append(node[0])
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        
        if flag==True:
            return HttpResponse("<h1>There is no required Road Route</h1>")

        queue=[[via]]
        visited=[]

        if via == dest:
            return HttpResponse("<h1>You are already at your Destination!</h1>")

        new_path2=[]
        flag=True
        path=queue.pop(0)
        node=path[-1]
        if node not in visited:
            adjacent=graph[node]
            for i in adjacent and flag==True:
                new_path2=list(path)
                new_path2.append(i)
                queue.append(new_path2)
                if i == dest:
                    flag=False
        visited.append(node)

        while queue and flag==True:
            path=queue.pop(0)
            node=path[-1]
            if node[0] not in visited and flag==True:
                adjacent=graph[node]
                for i in adjacent and flag==True:
                    new_path2=list(path)
                    new_path2.append(i)
                    queue.append(new_path2)
                    if i == dest:
                        new_path2.pop(0)
                        flag=False
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
            visited.append(node[0])
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        if flag==True:
            return HttpResponse("<h1>There is no required Road Route</h1>")
        final_path=new_path+new_path2
        dist=len(final_path)
        fare=FareCalc(dist)
        return HttpResponse("<h1>You will have to pay around {}</h1>".format(fare))

def addHistory(uName,start,dest):
    user=UserPrefHist.objects.get(Username=uName)
    newRec=start+' to '+dest
    histList=user.history.split(",")

    if len(histList)==5:
        histList.pop(0)
        histList.append(newRec)
    else:
        histList.append(newRec)
    data=","
    data=data.join(histList)
    user.history=data
    user.save()

def addHistory(uName,start,via,dest):
    user=UserPrefHist.objects.get(UserName=uName)
    newRec=start+' to '+dest+' via '+via
    histList=user.history.split(",")

    if len(histList)==5:
        histList.pop(0)
        histList.append(newRec)
    else:
        histList.append(newRec)
    data=","
    data=data.join(histList)
    user.history=data
    user.save()

def addPref(uName,start,dest):
    user=UserPrefHist.objects.get(UserName=uName)
    newRec=start+' to '+dest
    user.preferredRoutes=user.preferredRoutes+','+newRec
    user.save()

def delPref(uName,start,dest):
    user=UserPrefHist.objects.get(UserName=uName)
    delRec=start+' to '+dest
    prefList=user.preferredRoutes.split(",")
    i=0
    flag=False
    for rec in prefList:
        if rec==delRec:
            flag=True
            prefList.pop(i)
            break
        i+=1
    if flag==False:
        print('Preferred Route does not exist')
    data=","
    data=data.join(prefList)
    user.preferredRoutes=data
    user.save()
