from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import View
from notes.forms import TaskForm,RegistrationForm,SignInForm
from django.contrib import messages
from notes.models import Task
from django import forms
from django.db.models import Q

from notes.decorators import signin_required
from django.utils.decorators import method_decorator


@method_decorator(signin_required,name="dispatch")
class TaskCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TaskForm()
        
        return render(request,"task_create.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user=request.user
            # data=form_instance.cleaned_data
            # Task.objects.create

            form_instance.save()

            messages.success(request,"task added successfully")

            return redirect("task-list")
        else:

            messages.error(request,"failed")
            
            return render(request,"task_create.html",{"form":form_instance})
        
@method_decorator(signin_required,name="dispatch")
class TaskListView(View):
    def get(self,request,*args,**kwargs):

        print(request.GET.get("search_text"))
        # qs=Task.objects.all()



        # if "category" in request.GET:
        #     category_value=request.GET.get("category")
        #     qs=qs.filter(category=category_value)

            # if category_value=="all":
            #     qs=Task.objects.all()

        selected_category=request.GET.get("category","all")
        search_text=request.GET.get("search_text")

        if selected_category=="all":
            # qs=Task.objects.all()    for that particular user--change into-->
            qs=Task.objects.filter(user=request.user)
        else:
            qs=Task.objects.filter(category=selected_category,user=request.user)


# for search text:
        if search_text !=None:
            qs=Task.objects.filter(user=request.user)
            qs=qs.filter(Q(title__icontains=search_text)|Q(description__icontains=search_text))


        return render(request,"task_list.html",{"tasks":qs,"selected":selected_category})







        # return render(request,"task_list.html",{"tasks":qs,"selected":request.GET.get("category","all")})
    

@method_decorator(signin_required,name="dispatch")

class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        return render(request,"task_detail.html",{"task":qs})
    

@method_decorator(signin_required,name="dispatch")
class TaskUpdateView(View):
    def get(self,request,*args,**kwargs):

        #extract pk from kwargs
        id=kwargs.get("pk")

        #fetchtask object with id=id
        task_obj=Task.objects.get(id=id)

        #initialize taskform with task_obj
        form_instance=TaskForm(instance=task_obj)

        #add status field to form_instance
        form_instance.fields["status"]=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select
                                                         (attrs={"class":"form-control form-select"}),
                                                         initial=task_obj.status)

        return render(request,"task_edit.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):
        # id=extract id from kwargs
        id=kwargs.get("pk")


        task_obj=Task.objects.get(id=id)

        form_instance=TaskForm(request.POST,instance=task_obj)

        if form_instance.is_valid():
            form_instance.instance.status=request.POST.get("status")

            form_instance.save()

            return redirect("task-list")
        else:
            return render(request,"task_edit.html",{"form":form_instance})
        

@method_decorator(signin_required,name="dispatch")

class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):

        #extract id and delete task objects with id 

        Task.objects.get(id=kwargs.get("pk")).delete()

        return redirect("task-list")
    

    

from django.db.models import Count
@method_decorator(signin_required,name="dispatch")

class TaskSummaryView(View):
    def get(self,request,*args,**kwargs):

        qs=Task.objects.all()

        total_task_count=qs.count()

        category_summary=Task.objects.all().values("category").annotate(cat_count=Count("category"))
        print(category_summary)

        status_summary=Task.objects.all().values("status").annotate(sts_summary=Count("status"))
        print(status_summary)

        
        context={
               "total_task_count":total_task_count,
               "category_summary":category_summary,
               "status_summary":status_summary,
        }
        return render(request,"task_summary.html",context)
    




    

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout
    

class SignUpView(View):
    template_name="register.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)#for hidden password in database

            return redirect("signin")
        
        else:

            return render(request,self.template_name,{"form":form_instance})
        
class SignInView(View):

    template_name="login.html"

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        #initialize form with request.post

        form_instance=SignInForm(request.POST)

        # check form_instance is valid?

        if form_instance.is_valid():

            #extract userneame and password

            uname=form_instance.cleaned_data.get("username")
            pword=form_instance.cleaned_data.get("password")

            #authenticate :is usernsme and password correct??

            user_object=authenticate(request,username=uname,password=pword)

            if user_object:

                login(request,user_object)

                return redirect("task-list")
        return render(request,self.template_name,{"form":form_instance})
    
    
    
@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    
    


    
    
        

    
    



