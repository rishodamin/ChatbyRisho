from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(req):
    return render(req, 'index.html')

def home(req, act):
    cont = {'join':True}
    if act=='create':
        cont = {'join':False}
    return render(req, 'home.html', cont)

def login(req):
    if req.method=="POST":
        username = req.POST["username"]
        password = req.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(req, user)
            return redirect("/")
        messages.info(req, "Credentials Invalid")
        return redirect("login")
    return render(req, "login.html")

def logout(req):
    auth.logout(req)
    return redirect("/")

def register(req):
    if req.method=="POST":
        username = req.POST["username"]
        email = req.POST["email"]
        password = req.POST["password"]
        password2 = req.POST["password2"]
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(req, "Email already used")
                return redirect('register')
            if User.objects.filter(username=username).exists():
                messages.info(req, "Username already used")
                return redirect("register")
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect("login")
        messages.info(req, "Passwords not match")
        return redirect("register")
            
    return render(req, 'register.html')

def room(request, room):
    if not request.user.is_authenticated:
        return redirect('/login')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.GET['room_name']
    join = request.GET.get('join')

    if join=="True":
        if Room.objects.filter(name=room).exists():
            return redirect('room/'+room)
        messages.info(request, "There is no room named "+room)
        return redirect('/home/join')
    else:
        if Room.objects.filter(name=room).exists():
            messages.info(request, room+" already exists")
            return redirect('/home/create')
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('room/'+room)
    
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    messData = list(messages.values())
    for m in messData:
        m["date"] = str(m['date'])[:-13]+" UTC"
    return JsonResponse({"messages":messData})

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')