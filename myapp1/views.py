from django.shortcuts import render, HttpResponse
from .models import *
from employee.models import Salaries
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect

# TODO 
    # Put Ajax
    # Pay Fees
    # Resolve Date Null
    # put check if student with rollno. exist 

def home(request):
    if request.user.is_authenticated :
        student_transaction = PaidFees.objects.all()
        employee_transaction = Salaries.objects.all()
        return render(request, 'index.html', {'s_transaction':student_transaction, 'e_transaction':employee_transaction})
    else :
        return HttpResponse('please login')

def form(request):
    name = request.POST.get('name1')
    rollno = request.POST.get('pswd')
    obj = Student(name=name , rollno=rollno)
    obj.save()
    return HttpResponse('ye walla function hit hua hai')

# CRUD [Create ,Retrive, Update, Delete]--------------

# Create/Data Add karna
def add_student(request):
    if request.method == 'POST':

        stu_name = request.POST.get('name')
        stu_roll = request.POST.get('rollnumber')

        obj = Student(name = stu_name, rollno = stu_roll)
        obj.save()

        return HttpResponse(f'stu_roll:{stu_roll}')

    return render(request, 'basic-form.html')
   

# RETRIVE
def student_detail(request, slug):
    obj = Student.objects.filter(rollno = slug)
    tam = obj[0]

    return HttpResponse(f'rollno:{tam.rollno}, name:{tam.name}this is slug -{slug}')

def delete_student(request):
    if request.method == 'POST':

        stu_rollno = request.POST.get('rollnumber')
        obj = Student.objects.filter(rollno = stu_rollno)
        obj.delete()
        return HttpResponse('User Deleted Successfully sayad')
    return render(request, 'delete-student.html')

def update_student(request, slug):
    if request.method == "POST":
        stu_name = request.POST.get('name')
        print(stu_name)
        rollno = request.POST.get('rollnumber')
        obj = Student.objects.get(rollno = slug)
        obj.name = stu_name
        obj.rollno = rollno
        obj.save()
        # filter = [list of objects]
        # get = single object
        return HttpResponse("updated successfully")
    obj = Student.objects.filter(rollno = slug)
    return render(request, 'update-form.html', {"data":obj})



def emp_details(request):
    if request.method=='POST':
        name=request.POST.get('name')
        emp_id=request.POST.get('e_Id')
        age=request.POST.get('e_age')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        address=request.POST.get('address')
        email=request.POST.get('email')
        salary=request.POST.get('salary')
        obj=Employee(name=name,e_id=emp_id,age=age,gender=gender,address=address, salary=salary)
        obj.save()
        return HttpResponse('added successfully')
    return render(request,'emp-details.html')


def add_detail(request):
    if request.method=='POST':
        # TODO 
            # Add Roll Number Check
        name=request.POST.get('name')
        rollno=request.POST.get('rollno')
        email=request.POST.get('email')
        fname=request.POST.get('f_name')
        mname=request.POST.get('m_name')
        address=request.POST.get('address')
        dob=request.POST.get('dob')
        branch_id = request.POST.get('Branch')
        branch = Branch.objects.filter(id=branch_id).first()
        print('...........', branch)
        obj=Student(name=name,rollno=rollno,email=email,f_name=fname,m_name=mname,address=address,dateOfBirth=dob,stu_class='1', branch=branch )
        obj.save()
        return HttpResponse('added successfully')

    courses = Course.objects.all()
    
    return render(request,'basic-form.html', {'courses':courses, 'branches':''})


def update_stu(request):
    if request.method=='POST':
        roll_no=request.POST.get('search')
        obj=Student.objects.filter(rollno=roll_no).first()
        if obj == None :
            print('......chala')
            messages.error(request, 'Student Not Found')
            return render(request, 'index.html')
        courses = Course.objects.all()
        
        return render(request,'update-student-form.html',{'tam':obj, 
                                                        'courses':courses,
                                                        'selected_branch':obj.branch,
                                                        'selected_course':obj.branch.course_name, 
                                                         'url':"/update3"})
    return render(request,'index.html')


def update3(request):
    if request.method=='POST':
        name=request.POST.get('name')
        rollno=request.POST.get('rollno')
        email=request.POST.get('email')
        fname=request.POST.get('f_name')
        mname=request.POST.get('m_name')
        address=request.POST.get('address')
        dob=request.POST.get('dob')
        branch_id = request.POST.get('Branch')
        branch = Branch.objects.filter(id=branch_id).first()

        obj=Student.objects.filter(rollno=rollno).first()
        obj.name=name
        obj.rollno=rollno
        obj.email=email
        obj.f_name=fname
        obj.m_name=mname
        obj.address=address
        obj.dob=dob
        obj.branch=branch
        obj.save()
        return HttpResponse('data is updated successfully')


def loginuser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user==None:
            return HttpResponse('please enter correct details')
        else:
            login(request, user)
            return HttpResponse('login successfully')
    return render(request,'user-login.html')


def logoutuser(request):
    logout(request)
    return HttpResponse('logout successfully')


def fees_form(request):
    try:
        if request.method =='POST':
            roll_no = request.POST.get('rollno')
            branch = request.POST.get('Branch')
            print('.....id', branch)
            course = request.POST.get('Course')
            obj1 = BranchFees.objects.filter(branch__id = branch).first()
            total = obj1.fees + obj1.tution_fees + obj1.exam_fees + obj1.library_charges
            obj2 = Student.objects.filter(rollno = roll_no).filter(branch = obj1.branch).first()
            if obj2 == None:
                print('dfdfd')
                courses = Course.objects.all()
                branches = Branch.objects.all()
                messages.error(request,'Student Not Found')
                return render(request, 'student-fess-search.html', {'courses':courses, 'branches':branches})
            return render(request, 'fees-form.html', {'fees_detail':obj1, 'student_detail':obj2, 'total':total})
        courses = Course.objects.all()
        branches = Branch.objects.all()
        return render(request, 'student-fess-search.html', {'courses':courses, 'branches':branches})
    except:
        return HttpResponse('Wrong Input Passed')
def pay_fees(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rollno = request.POST.get('rollno')
        f_name = request.POST.get('f_name')
        dob = request.POST.get('dob')
        fees = request.POST.get('fees')
        tution_fees = request.POST.get('tution_fees')
        exam_fees = request.POST.get('exam_fees')
        library_charges = request.POST.get('library_charges')
        late_charges = request.POST.get('late_charges')
        total = request.POST.get('total')

        print('.........',name, rollno, f_name, dob, fees, tution_fees, exam_fees, library_charges, late_charges, total)

        student = Student.objects.filter(rollno= rollno).first()
        fees_paid = PaidFees()
        fees_paid.student = student
        fees_paid.course_fee = fees
        fees_paid.tution_fee=tution_fees
        fees_paid.branch = student.branch
        fees_paid.exam_fee = exam_fees
        fees_paid.library_charges = library_charges
        fees_paid.total_fee = total
        fees_paid.save()
        return HttpResponse('Fees Successfully Paid')
    return HttpResponse('Bad Request')

    
# Basic
def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        Course(course_name = name, duration = duration).save()
        messages.success(request, 'Course Added Successfully')
        return render(request, 'test.html')
    return render(request, 'test.html')

def add_branch(request):
    if request.method == 'POST':
        branch_name = request.POST.get('branch_name')
        fees = request.POST.get('fees')
        tution_fees = request.POST.get('tution_fees')
        exam_fees = request.POST.get('exam_fees')
        library_charges = request.POST.get('library_charges')
        course_id = request.POST.get('Course')
        course = Course.objects.filter(id = course_id).first()
        b = Branch(branch_name = branch_name, course_name = course)
        b.save()
        BranchFees(fees = fees, tution_fees = tution_fees, exam_fees = exam_fees, library_charges = library_charges, branch=b).save()
        messages.success(request, 'Added Successfully')
        return render(request, 'new-branch-form.html')
    course = Course.objects.all()
    return render(request, 'new-branch-form.html', {'courses':course})

def add_course_detail(request):
    if request.method =='POST':
        course_name = request.POST.get('name')
        course_duration = request.POST.get('duration')
        Course(course_name = course_name, duration = course_duration).save()
        return HttpResponse('added successfully')
    branch = Branch.objects.all()
    return render(request, 'course-form.html', {'branches':branch})

def render_update_branch(request):
    if request.method == 'POST': 
        id = request.POST.get('Branch')
        obj = BranchFees.objects.filter(branch__id = id).first()
        return render(request, 'branch-detail-form.html', {'course_detail':obj,'type':'update'})
    obj = Course.objects.all()
    obj2 = Branch.objects.all()
    return render(request, 'branch-search.html', {'courses':obj, 'branches':obj2, 'type':'update'})

def update_course(request):
    if request.method == 'POST':
        fees = request.POST.get('fees')
        t_fees = request.POST.get('tution_fees')
        e_fees = request.POST.get('exam_fees')
        l_charges = request.POST.get('library_charges')
        b_id = request.POST.get('branch_id')
        print('///////', b_id)
        # BranchFees(fees = fees, tution_fees = t_fees, exam_fees=e_fees, library_charges = l_charges, branch__id=b_id).save()
        obj = BranchFees.objects.filter(branch__id = b_id).first()
        obj.fees = fees
        obj.tution_fees = t_fees
        obj.exam_fees = e_fees
        obj.library_charges = l_charges
        obj.save()
        return HttpResponse('Updated Successfully')

# def add_branch(request):
#     return render(request, 'branch-form.html')

def update_branch(request):
    return render(request, 'branch-form.html')

def branch_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        branches = Branch.objects.filter(course_name__id = query)
        branch_list = []
        for i in branches :
            branch_list.append({'name':i.branch_name, 'id':i.id})
        print('.....list', branch_list)
        return JsonResponse({'branches':branch_list})
    return JsonResponse({'error':True})
