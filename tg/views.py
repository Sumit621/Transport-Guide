from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from jinja2.runtime import Context
from numpy import double
from tg.models import BusRoutes, PoribohonRoutes,Review
from tg.models import UserPrefHist,PlaceLocs,HubLocs,LogData,SignInOutLog
import folium

#functions

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

        half_paths=[]
        new_path=[]
        flag=True
        path=queue.pop(0)
        node=path[-1]
        if node not in visited:
            adjacent=graph[node]
            for i in adjacent:
                new_path=list(path)
                new_path.append(i)
                if i[0] == via:
                    half_paths.append(new_path)
                    flag=False
                    continue
                queue.append(new_path)
        visited.append(node)

        while queue:
            path=queue.pop(0)
            node=path[-1]
            if node[0] not in visited:
                adjacent=graph[node[0]]
                for i in adjacent:
                    new_path=list(path)
                    new_path.append(i)
                    if i[0] == via:
                        half_paths.append(new_path)
                        flag=False
                        continue
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
                    queue.append(new_path)
            visited.append(node[0])
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        
        if flag==True:
            return HttpResponse("<h1>There is no required Bus Route</h1>")

        queue=[[via]]
        visited=[]

        if via == dest:
            return HttpResponse("<h1>You are already at your Destination!</h1>")

        half_paths2=[]
        new_path2=[]
        flag=True
        path=queue.pop(0)
        node=path[-1]
        if node not in visited:
            adjacent=graph[node]
            for i in adjacent:
                new_path2=list(path)
                new_path2.append(i)
                if i[0] == dest:
                    new_path2.pop(0)
                    half_paths2.append(new_path2)
                    flag=False
                    continue
                queue.append(new_path2)
        visited.append(node)

        while queue:
            path=queue.pop(0)
            node=path[-1]
            if node[0] not in visited:
                adjacent=graph[node[0]]
                for i in adjacent:
                    new_path2=list(path)
                    new_path2.append(i)
                    if i[0] == dest:
                        new_path2.pop(0)
                        half_paths2.append(new_path2)
                        flag=False
                        continue
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
                    queue.append(new_path2)
            visited.append(node[0])
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        if flag==True:
            return "There is no required Bus Routes"
        txtList=[]
        pathNo=1
        for i in half_paths:
            for j in half_paths2:
                final_path=i+j
                txt=""
                for it in range(1,len(final_path)-1):
                    if final_path[it][1]!=final_path[it+1][1]:
                            txt=txt+"Go upto "+final_path[it][0]+" in "+final_path[it][1]+" ➔ "
                txt=txt+"Go upto "+final_path[-1][0]+" in "+final_path[-1][1]+"."
                txtList.append(txt)
                pathNo+=1
                print(txt)
                print(final_path)
        return txtList


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
            for i in adjacent:
                new_path=list(path)
                new_path.append(i)
                queue.append(new_path)
                if i == via:
                    flag=False
                    break
        visited.append(node)

        while queue and flag==True:
            path=queue.pop(0)
            node=path[-1]
            if node not in visited and flag==True:
                adjacent=graph[node]
                for i in adjacent:
                    new_path=list(path)
                    new_path.append(i)
                    queue.append(new_path)
                    if i == via:
                        flag=False
                        break
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
            for i in adjacent:
                new_path2=list(path)
                new_path2.append(i)
                queue.append(new_path2)
                if i == dest:
                    new_path2.pop(0)
                    flag=False
                    break
        visited.append(node)

        while queue and flag==True:
            path=queue.pop(0)
            node=path[-1]
            if node[0] not in visited and flag==True:
                adjacent=graph[node]
                for i in adjacent:
                    new_path2=list(path)
                    new_path2.append(i)
                    queue.append(new_path2)
                    if i == dest:
                        new_path2.pop(0)
                        flag=False
                        break
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
            visited.append(node[0])
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        if flag==True:
            return "There is no required Road Route"
        final_path=new_path+new_path2
        dist=len(final_path)
        fare=FareCalc(dist)
        msg='You will have to pay around '+fare
        return msg


def showMap(request):
    if request.method=="POST":
        startText=request.POST.get("start")
        destText=request.POST.get("dest")
        start=BusRoutes.objects.get(place=startText)
        dest=BusRoutes.objects.get(place=destText)
        A_lat=start.geoLocLat
        A_lon=start.geoLocLon
        pointA=(A_lat,A_lon)
        B_lat=dest.geoLocLat
        B_lon=dest.geoLocLon
        pointB=(B_lat,B_lon)
        m=folium.Map(width='100%',height='100%',location=getCenter(A_lat,A_lon,B_lat,B_lon),zoom_start=12.4)
        folium.Marker([A_lat,A_lon],tooltip='Click for details',popup=start.place,
                    icon=folium.Icon(color='blue')).add_to(m)
        
        folium.Marker([B_lat,B_lon],tooltip='Click for details',popup=dest.place,
                    icon=folium.Icon(color='red', icon='cloud')).add_to(m)
        m=m._repr_html_()
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
            return "Starting Point not Identified!"
        queue=[[start]]
        visited=[]

        if start == dest:
            return "You are already at your Destination!"

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
                    msg='You will have to pay around '+fare
                    return msg
        visited.append(node)

        while queue:
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
                        msg='You will have to pay around '+fare
                        return msg
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
            visited.append(node)
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        return "There is no required Road Route"

def addHistory(uName,start,dest):
    user=UserPrefHist.objects.get(UserName=uName)
    newRec=start+' to '+dest
    histList=user.history.split(",")

    if len(histList)==5:
        histList.pop()
        histList.insert(0,newRec)
    else:
        histList.insert(0,newRec)
    data=","
    data=data.join(histList)
    user.history=data
    user.save()

def addHistory3(uName,start,via,dest):
    user=UserPrefHist.objects.get(UserName=uName)
    newRec=start+' to '+dest+' via '+via
    histList=user.history.split(",")

    if len(histList)==5:
        histList.pop()
        histList.insert(0,newRec)
    else:
        histList.insert(0,newRec)
    data=","
    data=data.join(histList)
    user.history=data
    user.save()

def addPref(uName,start,dest,bus):
    user=UserPrefHist.objects.get(UserName=uName)
    newRec=start+' to '+dest+' in '+bus
    if user.preferredRoutes=="":
        user.preferredRoutes=newRec
    else:
        user.preferredRoutes=user.preferredRoutes+','+newRec
    user.save()

def delPref(uName,start,dest,bus):
    user=UserPrefHist.objects.get(UserName=uName)
    delRec=start+' to '+dest+' in '+bus
    prefList=user.preferredRoutes.split(",")
    i=0
    flag=False
    for rec in prefList:
        if rec==delRec:
            flag=True
            prefList.pop(i)
            break
        i+=1
    # if flag==False:
    #     print('Preferred Route does not exist')
    data=","
    data=data.join(prefList)
    user.preferredRoutes=data
    user.save()



# Create your views here. The End of User Defined Ultility Functions and Start of Functions to handle page requests.

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method=="POST":
        start=request.POST.get("start")
        dest=request.POST.get("dest")
        addHistory(request.user.username,start,dest)
        uNm=request.user.username
        det=uNm+' searched routes for '+start+' to '+dest
        logEntry=LogData(uName=request.user,logType="searched-route",details=det)
        logEntry.save()
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

        if start == dest:
            return HttpResponse("<h1>You are already at your Destination!</h1>")

        startObj=BusRoutes.objects.get(place=start)
        destObj=BusRoutes.objects.get(place=dest)
        A_lat=startObj.geoLocLat
        A_lon=startObj.geoLocLon
        pointA=(A_lat,A_lon)
        B_lat=destObj.geoLocLat
        B_lon=destObj.geoLocLon
        pointB=(B_lat,B_lon)
        m=folium.Map(width='100%',height='100%',location=getCenter(A_lat,A_lon,B_lat,B_lon),zoom_start=12.4)
        folium.Marker([A_lat,A_lon],tooltip='Click for details',popup=startObj.place,
                    icon=folium.Icon(color='blue')).add_to(m)
        
        folium.Marker([B_lat,B_lon],tooltip='Click for details',popup=destObj.place,
                    icon=folium.Icon(color='red', icon='cloud')).add_to(m)
        
        m=m._repr_html_()

        txtList=[]
        pathNo=1
        busFound=False
        cngFound=False
        path=queue.pop(0)
        node=path[-1]
        if node not in visited:
            adjacent=graph[node]
            for i in adjacent:
                new_path=list(path)
                new_path.append(i)
                if i[0] == dest:
                    busFound=True
                    txt=""
                    txt=txt+") Go upto "+new_path[-1][0]+" in "+new_path[-1][1]+"."
                    txtList.append(txt)
                    if cngFound==False:
                        cngFound=True
                        msgCNG=getCNGfare(request)
                    pathNo+=1
                    continue
                    
                queue.append(new_path)
        visited.append(node)

        while queue:
            path=queue.pop(0)
            node=path[-1]
            # print('-----nodes-----')
            # print(node)
            if node[0] not in visited:
                adjacent=graph[node[0]]
                for i in adjacent:
                    new_path=list(path)
                    new_path.append(i)
                    if i[0] == dest:
                        busFound=True
                        txt=""
                        for it in range(1,len(new_path)-1):
                            # print('-----Tuples-------')
                            # print(new_path[it])
                            if new_path[it][1]!=new_path[it+1][1]:
                                    txt=txt+"Go upto "+new_path[it][0]+" in "+new_path[it][1]+" ➔ "
                        txt=txt+"Go upto "+new_path[-1][0]+" in "+new_path[-1][1]+"."
                        txtList.append(txt)
                        print(txt)
                        if cngFound==False:
                            cngFound=True
                            msgCNG=getCNGfare(request)
                        pathNo+=1
                        continue
    
                    queue.append(new_path)
                        # return HttpResponse("<h1>{}</h1>".format(new_path))
            visited.append(node[0])
            # if node == dest:
            #      return HttpResponse("<h1>new_path</h1>")
        if busFound==True:
            context={
                    'msg':txtList,
                    'msg2':msgCNG,
                    'map':m,
                    }
            return viewRoute2(request,context)
            
        return HttpResponse("<h1>There is no required Bus Route</h1>")
    if request.user.is_staff:
        context={
            'Staff':"yes",
        }
        return render(request,"index.html",context)
    return render(request,"index.html")

def viaPlace(request):
    if request.method=="POST":
        msgBus=Djik3node(request)
        msgCNG=getCNGviaFare(request)
        m=showMap(request)
        start=request.POST.get("start")
        via=request.POST.get("via")
        dest=request.POST.get("dest")
        addHistory3(request.user.username,start,via,dest)
        uNm=request.user.username
        det=uNm+' searched routes for '+start+' to '+dest+' via '+via
        logEntry=LogData(uName=request.user,logType="searched-via-route",details=det)
        logEntry.save()
        context={
                'msg':msgBus,
                'msg2':msgCNG,
                'map':m,
            }
        return render(request,'viewRoute.html',context)
    return render(request,'viaPlace.html')

def loginUser(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                det=request.user.username+' logged in as Staff'
                signLogEntry=SignInOutLog(uName=request.user,details=det)
                signLogEntry.save()
                return redirect("/adminIndex")
            det=request.user.username+' logged in'
            signLogEntry=SignInOutLog(uName=request.user,details=det)
            signLogEntry.save()
            return redirect("/index")
        # A backend authenticated the credentials
        else:
         # No backend authenticated the credentials
            messages.error(request,'username or password not correct')
            return render(request,"login.html")

    return render(request,"login.html")

def logoutUser(request):
    det=request.user.username+' logged out'
    signLogEntry=SignInOutLog(uName=request.user,details=det)
    signLogEntry.save()
    logout(request)
    return redirect("/login")

def signupUser(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        eMail=request.POST.get("email")
        Fname=request.POST.get("firstname")
        Lname=request.POST.get("lastname")
        user = User.objects.create_user(username, eMail, password)
        user.first_name=Fname
        user.last_name=Lname
        userPrfs=UserPrefHist(UserName=username,preferredRoutes="",history="")
        user.save()
        userPrfs.save()
        login(request, user)
        det=user.username+' signed up'
        signLogEntry=SignInOutLog(uName=user,details=det)
        signLogEntry.save()
        return redirect("/")
    return render(request,"signup.html")

def viewRoute2(request,context):
    return render(request,'viewRoute.html',context)

def viewRoute(request):
    return render(request,'viewRoute.html')

class histElem:
    start="-"
    end="-"
    via="-"

def viewHistory(request):
    uNm=request.user.username
    userData=UserPrefHist.objects.get(UserName=uNm)
    hist=userData.history
    histElemList=[]
    histList=hist.split(',')
    try:
        for i in histList:
            temp=histElem()
            startDest=i.split(' to ')
            destVia=startDest[1].split(' via ')
            temp.start=startDest[0]
            temp.end=destVia[0]
            if len(destVia)==2:
                temp.via=destVia[1]
            histElemList.append(temp)

        context={
            'name':uNm,
            'msg':histElemList,
        }
        
    except:
        temp=histElem()
        histElemList.append(temp)
        context={
            'name':uNm,
            'msg':histElemList,
        }
    det=uNm+' viewed History'
    logEntry=LogData(uName=request.user,logType="viewed-History",details=det)
    logEntry.save()
        
    return render(request,'viewHistory.html',context)

def viewPoribohon(request):
    if request.method=="POST":
        busName=request.POST.get("busname")
        uNm=request.user.username
        det=uNm+' viewed poribohon route for '+busName
        logEntry=LogData(uName=request.user,logType="viewed-Poribohon",details=det)
        logEntry.save()
        if PoribohonRoutes.objects.filter(poribohonName=busName).exists():
            poribohon=PoribohonRoutes.objects.get(poribohonName=busName)
            route=poribohon.fullRoute
            routeList=route.split(',')
            context={
                'name':busName,
                'route':routeList,
            }
        else:
            context={
                'name':"Unknown",
                'route':0,
            }
        return render(request,'viewPoribohon.html',context)
    return render(request,'viewPoribohon.html')

class prefObj:
    start=None
    end=None
    bus=None

def modPrefs(request):
    if request.method=="POST" and 'addBtn' in request.POST:
        start=request.POST.get("start")
        dest=request.POST.get("dest")
        bus=request.POST.get("bus")
        uNm=request.user.username
        addPref(uNm,start,dest,bus)
        det=uNm+' added Preference '+start+' to '+dest+' in '+bus
        logEntry=LogData(uName=request.user,logType="added-pref",details=det)
        logEntry.save()
        uRow=UserPrefHist.objects.get(UserName=uNm)
        prefRoutes=uRow.preferredRoutes
        prefObjList=[]
        prefList=prefRoutes.split(',')
        for i in prefList:
            tp=prefObj()
            startDest=i.split(' to ')
            tp.start=startDest[0]
            destBus=startDest[1].split(' in ')
            tp.end=destBus[0]
            if len(destBus)<2:
                tp.bus='-'
            else:
                tp.bus=destBus[1]
            prefObjList.append(tp)
        context={
            'name':uNm,
            'route':prefObjList,
        }
        return render(request,'modPrefs.html',context)
    elif request.method=="POST" and 'delBtn' in request.POST:
        start=request.POST.get("start")
        dest=request.POST.get("dest")
        bus=request.POST.get("bus")
        uNm=request.user.username
        delPref(uNm,start,dest,bus)
        det=uNm+' deleted Preference '+start+' to '+dest+' in '+bus
        logEntry=LogData(uName=request.user,logType="deleted-pref",details=det)
        logEntry.save()
        uRow=UserPrefHist.objects.get(UserName=uNm)
        prefRoutes=uRow.preferredRoutes
        if prefRoutes!="":
            prefObjList=[]
            prefList=prefRoutes.split(',')
            for i in prefList:
                tp=prefObj()
                startDest=i.split(' to ')
                tp.start=startDest[0]
                destBus=startDest[1].split(' in ')
                tp.end=destBus[0]
                if len(destBus)<2:
                    tp.bus='-'
                else:
                    tp.bus=destBus[1]
                prefObjList.append(tp)
            context={
                'name':uNm,
                'route':prefObjList,
            }
        else:
            context={
                'name':uNm,
                'route':0,
            }
        return render(request,'modPrefs.html',context)
    uNm=request.user.username
    det=uNm+' viewed Preference'
    logEntry=LogData(uName=request.user,logType="viewed-pref",details=det)
    logEntry.save()
    uRow=UserPrefHist.objects.get(UserName=uNm)
    prefRoutes=uRow.preferredRoutes
    if prefRoutes!="":
        prefObjList=[]
        prefList=prefRoutes.split(',')
        for i in prefList:
            tp=prefObj()
            startDest=i.split(' to ')
            tp.start=startDest[0]
            destBus=startDest[1].split(' in ')
            tp.end=destBus[0]
            if len(destBus)<2:
                tp.bus='-'
            else:
                tp.bus=destBus[1]
            prefObjList.append(tp)
        context={
            'name':uNm,
            'route':prefObjList,
        }
    else:
        context={
            'name':uNm,
            'route':0,
        }
    return render(request,'modPrefs.html',context)

def showMapSingle(lat,lon):
    point=(lat,lon)
    m=folium.Map(width='100%',height='100%',location=[lat,lon],zoom_start=16)
    folium.Marker([lat,lon],tooltip='Click for details',popup="Hub",
                icon=folium.Icon(color='blue')).add_to(m)
    
    m=m._repr_html_()
    return m

def nearestHub(request):
    m=folium.Map(width='100%',height='100%',location=[23.779533,90.398828],zoom_start=16)
    m=m._repr_html_()
    placeTxt=""
    if request.method=="POST":
        locat=request.POST.get("locat")
        uNm=request.user.username
        det=uNm+' viewed Nearest Hub to '+locat
        logEntry=LogData(uName=request.user,logType="viewed-hub",details=det)
        logEntry.save()
        nrst=""
        place=""
        place=PlaceLocs.objects.get(placeName=locat)
        if place!="" or place!=None:
            placeLat=place.geoLocLat
            placeLon=place.geoLocLon
            minDist=9999
            hubs=HubLocs.objects.all()
            for i in hubs:
                hubLat=i.geoLocLat
                hubLon=i.geoLocLon
                dist=((hubLat-placeLat)*(hubLat-placeLat))+((hubLon-placeLon)*(hubLon-placeLon))
                if dist<minDist:
                    minDist=dist
                    nrst=i
            m=showMapSingle(nrst.geoLocLat,nrst.geoLocLon)
            placeTxt="Nearest hub is "+nrst.hubName
            
        else:
            m=folium.Map(width='100%',height='100%',location=[23.779533,90.398828],zoom_start=15)
            m=m._repr_html_()
    context={'place':placeTxt,
             'map':m,
             }
    return render(request,'nearestHub.html',context)

def busReview(request):
    isStaff=request.user.is_staff
    context={
             'pName':"none",
              'usrName':"none",
              'route':"none",
              'link':"none",
              'reviews':"none",
              'Staff':isStaff,
            }
    if request.method=="POST" and 'slctBus' in request.POST:
        uNm=request.user.username

        prb=request.POST.get("busInput")
        det=uNm+' viewed Bus Review page of '+prb
        logEntry=LogData(uName=request.user,logType="viewed-busrev",details=det)
        logEntry.save()
        prbGet=PoribohonRoutes.objects.get(poribohonName=prb)
        prbRoute=prbGet.fullRoute
        imLn=prbGet.imgLink
        try:
            rvws=list(prbGet.pReviews.all())
            context={
                'pName':prb,
                'usrName':uNm,
                'route':prbRoute,
                'link':imLn,
                'reviews':rvws,
                'Staff':isStaff,
                }
        except:
            context={
                'pName':prb,
                'usrName':uNm,
                'route':prbRoute,
                'link':imLn,
                'reviews':0,
                'Staff':isStaff,
                }
    elif request.method=="POST" and 'addCmnt' in request.POST:
        uNm=request.user.username
        
        cmnt=request.POST.get("cmnt")
        prb=request.POST.get("busInput")
        det=uNm+' added Review to '+prb
        logEntry=LogData(uName=request.user,logType="added-busrev",details=det)
        logEntry.save()
        prbGet=PoribohonRoutes.objects.get(poribohonName=prb)
        rev=Review(uName=request.user,poribohon=prbGet,comment=cmnt)
        rev.save()
        rvws=list(Review.objects.filter(poribohon=prbGet))
        prbRoute=prbGet.fullRoute
        imLn=prbGet.imgLink
        context={
            'pName':prb,
            'usrName':uNm,
            'route':prbRoute,
            'link':imLn,
            'reviews':rvws,
            'Staff':isStaff,
            }
    elif request.method=="POST" and 'delCmnt' in request.POST:
        uNm=request.user.username
        
        delId=request.POST.get("delCmnt")
        rev=Review.objects.get(id=delId)
        rev.delete()
        prb=request.POST.get("busInput")
        det=uNm+' deleted Review on '+prb
        logEntry=LogData(uName=request.user,logType="deleted-busrev",details=det)
        logEntry.save()
        prbGet=PoribohonRoutes.objects.get(poribohonName=prb)
        prbRoute=prbGet.fullRoute
        imLn=prbGet.imgLink
        try:
            rvws=list(prbGet.pReviews.all())
            context={
                'pName':prb,
                'usrName':uNm,
                'route':prbRoute,
                'link':imLn,
                'reviews':rvws,
                'Staff':isStaff,
                }
        except:
            context={
                'pName':prb,
                'usrName':uNm,
                'route':prbRoute,
                'link':imLn,
                'reviews':0,
                'Staff':isStaff,
                }


    return render(request,'busReview.html',context)


def adminIndex(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    return render(request,"adminIndex.html")

def statisticsPage(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    totalLogs=len(LogData.objects.all())
    if totalLogs==0:
        totalLogs=1
    nRLogs=len(LogData.objects.filter(logType="searched-route"))
    nRRatio=nRLogs/totalLogs
    vRLogs=len(LogData.objects.filter(logType="searched-via-route"))
    vRRatio=vRLogs/totalLogs
    nHLogs=len(LogData.objects.filter(logType="viewed-hub"))
    nHRatio=nHLogs/totalLogs
    histLogs=len(LogData.objects.filter(logType="viewed-History"))
    histRatio=histLogs/totalLogs
    poriLogs=len(LogData.objects.filter(logType="viewed-Poribohon"))
    poriRatio=poriLogs/totalLogs
    prefLogs=len(LogData.objects.filter(logType="viewed-pref"))
    prefRatio=prefLogs/totalLogs
    addPrefLogs=len(LogData.objects.filter(logType="added-pref"))
    addPrefRatio=addPrefLogs/totalLogs
    delPrefLogs=len(LogData.objects.filter(logType="deleted-pref"))
    delPrefRatio=delPrefLogs/totalLogs
    revLogs=len(LogData.objects.filter(logType="viewed-busrev"))
    revRatio=revLogs/totalLogs
    addRevLogs=len(LogData.objects.filter(logType="added-busrev"))
    addRevRatio=addRevLogs/totalLogs
    delRevLogs=len(LogData.objects.filter(logType="deleted-busrev"))
    delRevRatio=delRevLogs/totalLogs
    context={
        'nRLogs':nRLogs,
        'nRRatio':nRRatio,
        'vRLogs':vRLogs,
        'vRRatio':vRRatio,
        'nHLogs':nHLogs,
        'nHRatio':nHRatio,
        'histLogs':histLogs,
        'histRatio':histRatio,
        'poriLogs':poriLogs,
        'poriRatio':poriRatio,
        'prefLogs':prefLogs,
        'prefRatio':prefRatio,
        'addPrefLogs':addPrefLogs,
        'addPrefRatio':addPrefRatio,
        'delPrefLogs':delPrefLogs,
        'delPrefRatio':delPrefRatio,
        'revLogs':revLogs,
        'revRatio':revRatio,
        'addRevLogs':addRevLogs,
        'addRevRatio':addRevRatio,
        'delRevLogs':delRevLogs,
        'delRevRatio':delRevRatio,
    }
    return render(request,"statisticsPage.html",context)

def viewLogs(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    logList=LogData.objects.all()
    if len(logList)==0:
        context={
            'logs':"none",
        }
    else:
        logList=logList.reverse()
        context={
            'logs':logList,
        }
    if request.method=="POST":
        LogData.objects.all().delete()
        return redirect("/viewLogs")
    return render(request,"viewLogs.html",context)

def viewSignInOut(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    logList=SignInOutLog.objects.all()
    if len(logList)==0:
        context={
            'logs':"none",
        }
    else:
        logList=logList.reverse()
        context={
            'logs':logList,
        }
    if request.method=="POST":
        SignInOutLog.objects.all().delete()
        return redirect("/viewSignInOut")
    return render(request,"viewSignInOut.html",context)

def DataBusRoutes(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    bRoutes=BusRoutes.objects.all()
    if len(bRoutes)==0:
        context={
            'datList':"none",
        }
    else:
        context={
            'datList':bRoutes,
        }
    if request.method=="POST" and 'addDat' in request.POST:
        context2={
            'datRoute':"none",
        }
        return render(request,'AddBusRoutes.html',context2)
    elif request.method=="POST" and 'editDat' in request.POST:
        editID=request.POST.get("editDat")
        selDat=BusRoutes.objects.get(id=editID)
        context2={
            'datRoute':selDat,
        }
        return render(request,'AddBusRoutes.html',context2)
    elif request.method=="POST" and 'delDat' in request.POST:
        delID=request.POST.get("delDat")
        delDat=BusRoutes.objects.get(id=delID)
        delDat.delete()
        return redirect("/DataBusRoutes")

    return render(request,'DataBusRoutes.html',context)

def AddBusRoutes(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    if request.method=="POST":
        _place=request.POST.get("place")
        _values=request.POST.get("values")
        _roads=request.POST.get("roads")
        _lat=float(request.POST.get("lat"))
        _lon=float(request.POST.get("lon"))
        try:
            datObj=BusRoutes.objects.get(place=_place)
            datObj.place=_place
            datObj.values=_values
            datObj.roads=_roads
            datObj.geoLocLat=_lat
            datObj.geoLocLon=_lon
            datObj.save()
            return redirect("/DataBusRoutes")
        except:
            newObj=BusRoutes(place=_place,values=_values,roads=_roads,geoLocLat=_lat,geoLocLon=_lon)
            newObj.save()
            return redirect("/DataBusRoutes")
    
    return render(request,"AddBusRoutes.html")

def DataPoribohonRoutes(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    pRoutes=PoribohonRoutes.objects.all()
    if len(pRoutes)==0:
        context={
            'datList':"none",
        }
    else:
        context={
            'datList':pRoutes,
        }
    if request.method=="POST" and 'addDat' in request.POST:
        context2={
            'datRoute':"none",
        }
        return render(request,'AddPoribohonRoutes.html',context2)
    elif request.method=="POST" and 'editDat' in request.POST:
        editID=request.POST.get("editDat")
        selDat=PoribohonRoutes.objects.get(id=editID)
        context2={
            'datRoute':selDat,
        }
        return render(request,'AddPoribohonRoutes.html',context2)
    elif request.method=="POST" and 'delDat' in request.POST:
        delID=request.POST.get("delDat")
        delDat=PoribohonRoutes.objects.get(id=delID)
        delDat.delete()
        return redirect("/DataPoribohonRoutes")

    return render(request,'DataPoribohonRoutes.html',context)

def AddPoribohonRoutes(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    if request.method=="POST":
        _pname=request.POST.get("pname")
        _fRoute=request.POST.get("fRoute")
        _imLn=request.POST.get("imLn")
        try:
            datObj=PoribohonRoutes.objects.get(poribohonName=_pname)
            datObj.poribohonName=_pname
            datObj.fullRoute=_fRoute
            datObj.imgLink=_imLn
            datObj.save()
            return redirect("/DataPoribohonRoutes")
        except:
            newObj=PoribohonRoutes(poribohonName=_pname,fullRoute=_fRoute,imgLink=_imLn)
            newObj.save()
            return redirect("/DataPoribohonRoutes")
    
    return render(request,"AddPoribohonRoutes.html")

def DataUserPrefs(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    uList=UserPrefHist.objects.all()
    if len(uList)==0:
        context={
            'datList':"none",
        }
    else:
        context={
            'datList':uList,
        }
    if request.method=="POST" and 'addDat' in request.POST:
        context2={
            'datRoute':"none",
        }
        return render(request,'AddUserPrefs.html',context2)
    elif request.method=="POST" and 'editDat' in request.POST:
        editID=request.POST.get("editDat")
        selDat=UserPrefHist.objects.get(id=editID)
        context2={
            'datRoute':selDat,
        }
        return render(request,'AddUserPrefs.html',context2)
    elif request.method=="POST" and 'delDat' in request.POST:
        delID=request.POST.get("delDat")
        delDat=UserPrefHist.objects.get(id=delID)
        delDat.delete()
        return redirect("/DataUserPrefs")

    return render(request,'DataUserPrefs.html',context)

def AddUserPrefs(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    if request.method=="POST":
        _uname=request.POST.get("uname")
        _pRoutes=request.POST.get("pRoutes")
        _hist=request.POST.get("hist")
        try:
            datObj=UserPrefHist.objects.get(UserName=_uname)
            datObj.UserName=_uname
            datObj.preferredRoutes=_pRoutes
            datObj.history=_hist
            datObj.save()
            return redirect("/DataUserPrefs")
        except:
            newObj=UserPrefHist(UserName=_uname,preferredRoutes=_pRoutes,history=_hist)
            newObj.save()
            return redirect("/DataUserPrefs")
    
    return render(request,"AddUserPrefs.html")

def DataPlaceLocs(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    pList=PlaceLocs.objects.all()
    if len(pList)==0:
        context={
            'datList':"none",
        }
    else:
        context={
            'datList':pList,
        }
    if request.method=="POST" and 'addDat' in request.POST:
        context2={
            'datRoute':"none",
        }
        return render(request,'AddPlaceLocs.html',context2)
    elif request.method=="POST" and 'editDat' in request.POST:
        editID=request.POST.get("editDat")
        selDat=PlaceLocs.objects.get(id=editID)
        context2={
            'datRoute':selDat,
        }
        return render(request,'AddPlaceLocs.html',context2)
    elif request.method=="POST" and 'delDat' in request.POST:
        delID=request.POST.get("delDat")
        delDat=PlaceLocs.objects.get(id=delID)
        delDat.delete()
        return redirect("/DataPlaceLocs")

    return render(request,'DataPlaceLocs.html',context)

def AddPlaceLocs(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    if request.method=="POST":
        _pname=request.POST.get("pname")
        _lat=float(request.POST.get("lat"))
        _lon=float(request.POST.get("lon"))
        try:
            datObj=PlaceLocs.objects.get(placeName=_pname)
            datObj.placeName=_pname
            datObj.geoLocLat=_lat
            datObj.geoLocLon=_lon
            datObj.save()
            return redirect("/DataPlaceLocs")
        except:
            newObj=PlaceLocs(placeName=_pname,geoLocLat=_lat,geoLocLon=_lon)
            newObj.save()
            return redirect("/DataPlaceLocs")
    
    return render(request,"AddPlaceLocs.html")

def DataHubLocs(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    hList=HubLocs.objects.all()
    if len(hList)==0:
        context={
            'datList':"none",
        }
    else:
        context={
            'datList':hList,
        }
    if request.method=="POST" and 'addDat' in request.POST:
        context2={
            'datRoute':"none",
        }
        return render(request,'AddHubLocs.html',context2)
    elif request.method=="POST" and 'editDat' in request.POST:
        editID=request.POST.get("editDat")
        selDat=HubLocs.objects.get(id=editID)
        context2={
            'datRoute':selDat,
        }
        return render(request,'AddHubLocs.html',context2)
    elif request.method=="POST" and 'delDat' in request.POST:
        delID=request.POST.get("delDat")
        delDat=HubLocs.objects.get(id=delID)
        delDat.delete()
        return redirect("/DataHubLocs")

    return render(request,'DataHubLocs.html',context)

def AddHubLocs(request):
    if request.user.is_anonymous or request.user.is_staff==False:
        return redirect("/login")
    if request.method=="POST":
        _hname=request.POST.get("hname")
        _lat=float(request.POST.get("lat"))
        _lon=float(request.POST.get("lon"))
        try:
            datObj=HubLocs.objects.get(hubName=_hname)
            datObj.hubName=_hname
            datObj.geoLocLat=_lat
            datObj.geoLocLon=_lon
            datObj.save()
            return redirect("/DataHubLocs")
        except:
            newObj=HubLocs(hubName=_hname,geoLocLat=_lat,geoLocLon=_lon)
            newObj.save()
            return redirect("/DataHubLocs")
    
    return render(request,"AddHubLocs.html")









        
    





    
