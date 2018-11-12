from django.shortcuts import render,redirect

def HomeView(request):
    return redirect('/videos/')
    #if i want to make a landing page i will use this
    #return render(request,'home.html',{})
