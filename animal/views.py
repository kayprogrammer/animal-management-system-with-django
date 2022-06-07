from django.utils import timezone
import json
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
#from django.utils.formats import get_format
from django.utils.dateformat import DateFormat
from product.decorators import authenticated_user
from . decorators import *
import xlwt
import sweetify
from animal.models import Animal, Breeding, ClientData, Employee, Finance, HealthReport
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

User = get_user_model()

# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@authenticated_user
@employees_only
def animalrecords(request):
    animals = Animal.objects.all()
    count = animals.count()
    
    if is_ajax(request=request):
        data_response = dict()
        data = json.loads(request.body)
        type = data.get('type')
        animalname = data.get('animalname')
        animal_id = data.get('animal_id')
        if animal_id:
            animal = Animal.objects.get(id=animal_id)
            print(animal)
            data_response['animal'] = render_to_string('animal/animalprofile.html', {'animal':animal}, request=request)
            return JsonResponse(data_response)
        if animalname:
            print(animalname)
            filtered_animals = Animal.objects.filter(name__contains = animalname)
            data_response['results'] = render_to_string('animal/animal_list.html', {'animals':filtered_animals}, request=request)
            data_response['count'] = filtered_animals.count()
            return JsonResponse(data_response)

        if type != 'Animal Type' or type != None or type != "":
            filtered_animals = Animal.objects.filter(animal_type = type)
            data_response['results'] = render_to_string('animal/animal_list.html', {'animals':filtered_animals}, request=request)
            data_response['count'] = filtered_animals.count()
            return JsonResponse(data_response)
    elif request.method == 'POST':
        if Animal.objects.filter(idt=request.POST.get('idt')).exists():
            sweetify.error(request, title='Error', text='Animal with that id already exists', icon='error', button='Ok', timer=3000)
            return redirect('/animalrecords/')
        else:
            Animal.objects.create(idt = request.POST.get('idt'), name = request.POST.get('animalname'), ear_tag = request.POST.get('eartag'), sire_id = request.POST.get('sireid'), dam_id = request.POST.get('damid'), animal_type = request.POST.get('animaltype'), breed = request.POST.get('breed'), color = request.POST.get('color'), pasture = request.POST.get('pasture'), birth_date = request.POST.get('birthdate'), current_age = request.POST.get('currentage'), weight = request.POST.get('watbirth'), first_age = request.POST.get('firstage'))
            sweetify.success(request, title='Success', text='Animal has been added', icon='success', button='Ok', timer=3000)
            return redirect('/animalrecords/')

    context = {'animals':animals, 'count':count}
    return render(request, 'animal/animalrecords.html', context)

@authenticated_user
@employees_only
def updaterecord(request):
    if request.method == 'POST':
        idt = request.POST.get('animalid')
        print(idt)
        if 'update' in request.POST:
            Animal.objects.filter(idt = idt).update(name = request.POST.get('animalname'), ear_tag = request.POST.get('eartag'), sire_id = request.POST.get('sireid'), dam_id = request.POST.get('damid'), animal_type = request.POST.get('animaltype'), breed = request.POST.get('breed'), color = request.POST.get('color'), pasture = request.POST.get('pasture'), birth_rate = request.POST.get('birthrate'), current_age = request.POST.get('currentage'), weight = request.POST.get('watbirth'), first_age = request.POST.get('firstage'))
        elif 'delete' in request.POST:
            Animal.objects.get(idt = idt).delete()
    return redirect('/animalrecords/')

@authenticated_user
@employees_only
def animalhealth(request):
    animals = Animal.objects.all()
    count = animals.count()
    
    if is_ajax(request=request):
        data_response = dict()
        data = json.loads(request.body)
        type = data.get('type')
        animalname = data.get('animalname')
        animal_id = data.get('animal_id')
        if animal_id:
            animal = Animal.objects.get(id=animal_id)
            try:
                report = HealthReport.objects.get(animal=animal)
            except:
                report = ""
            print(report)
            data_response['animal'] = render_to_string('animal/healthreports.html', {'animal':animal, 'report':report}, request=request)
            return JsonResponse(data_response)
        
    elif request.method == 'POST':
        animal = Animal.objects.get(idt=request.POST.get('idt'))
        report = HealthReport.objects.filter(animal=animal) 
        if report.exists():
            report.update(type = request.POST.get('healtheventtype'), diagnosis = request.POST.get('diagnosis'), treatment = request.POST.get('treatment'), cost = request.POST.get('treatmentcost'), vet = request.POST.get('vetname'), date_created = request.POST.get('date'))
            sweetify.success(request, title='Success', text='Health report updated', icon='success', button='Ok', timer=3000)
            return redirect('/animalhealth/')
        else:
            HealthReport.objects.create(animal = animal, type = request.POST.get('healtheventtype'), diagnosis = request.POST.get('diagnosis'), treatment = request.POST.get('treatment'), cost = request.POST.get('treatmentcost'), vet = request.POST.get('vetname'), date_created = request.POST.get('date'))
            sweetify.success(request, title='Success', text='Health report created', icon='success', button='Ok', timer=3000)
            return redirect('/animalhealth/')

    context = {'animals':animals, 'count':count}
    return render(request, 'animal/animalhealth.html', context)

@authenticated_user
@employees_only
def breeding(request):
    breedings = Breeding.objects.all()
    animals = Animal.objects.filter(animal_type='Cow')

    if is_ajax(request=request):
        data_response = dict()
        data = json.loads(request.body)
        breeding_data = data.get('breeding_data')
        animal_id = data.get('animal_id')
        breed_id = data.get('breed_id')
        print(breed_id)
        print(animal_id)
        if breed_id:
            breed = Breeding.objects.get(id=breed_id)
            data_response['breed'] = render_to_string('animal/breedprofile.html', {'breed':breed}, request=request)
            return JsonResponse(data_response)
        if animal_id:
            animal = Animal.objects.get(id=animal_id)
            calves = list(Animal.objects.filter(animal_type="Cow").exclude(id=animal_id))
            calf = random.choice(calves)
            print(calf)
            data_response['bullid'] = animal.idt
            data_response['bullname'] = animal.name
            data_response['ccalv'] = animal.current_age
            data_response['calfname'] = calf.name
            data_response['calfid'] = calf.idt
            return JsonResponse(data_response)
        if breeding_data:
            print(breeding_data)
            filtered_data = Breeding.objects.filter(bull__name__contains = breeding_data)
            data_response['results'] = render_to_string('animal/breedinglist.html', {'breedings':filtered_data}, request=request)
            return JsonResponse(data_response)
    elif request.method == 'POST':
        if "save" in request.POST:
            bull = Animal.objects.get(idt=request.POST.get('bullid'))
            calf = Animal.objects.get(idt=request.POST.get('calf_id'))
            Breeding.objects.create(bull = bull, calf=calf, breeding_date = request.POST.get('breeding_date'), pregnancy_diagnosis_date = request.POST.get('pdd'), calve_due_date = request.POST.get('date_due_to_calve'), calved_date = request.POST.get('date_calved'), calf_notes = request.POST.get('calf_notes'))
            sweetify.success(request, title='Success', text='Breed Data created', icon='success', button='Ok', timer=3000)
            return redirect('/breeding/')
        elif "update" in request.POST:
            Breeding.objects.filter(id=request.POST.get('breed_id')).update(pregnancy_diagnosis_date = request.POST.get('pdd'), calve_due_date = request.POST.get('date_due_to_calve'), calved_date = request.POST.get('date_calved'), calf_notes = request.POST.get('calf_notes'))
            sweetify.success(request, title='Success', text='Breed Data updated', icon='success', button='Ok', timer=3000)
            return redirect('/breeding/')
    context = {'breedings':breedings, 'animals':animals}
    return render(request, 'animal/breeding.html', context)

@authenticated_user
@employees_only
def export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="breeding.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Bull', 'Calf', 'Pregnancy Diagnosis Date', 'Breeding Date', 'Date Due To Calve', 'Date Calved', 'Calf Notes']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    font_style.num_format_str = 'D-MMM-YY'

    rows = Breeding.objects.all().values_list('bull__name', 'calf__name', 'pregnancy_diagnosis_date', 'breeding_date', 'calve_due_date', 'calved_date', 'calf_notes')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

@authenticated_user
@employees_only
def producesale(request):
    cd = timezone.now()
    df = DateFormat(cd)
    cd = df.format('Y-m-d')
    distribution = ClientData.objects.filter(date_bought=cd).order_by('-date_bought')
    # for i in range(10):
    #     ClientData.objects.create(name=f'My-name-{i+10}', contact=f'38729929287{i+1}', amount=f'{i+200}')
    if request.method=='POST':
        ClientData.objects.create(name=request.POST.get('client_name'), contact=request.POST.get('client_contact'), amount=request.POST.get('amount_bought'))
        sweetify.success(request, title='Success', text='Data added', icon='success', button='Ok', timer=3000)
        return redirect('/producesale/')

    context = {'distribution':distribution}
    return render(request, 'animal/producesale.html', context)

@authenticated_user
@employees_only
def farmfinance(request):
    cd = timezone.now()
    df = DateFormat(cd)
    cd = df.format('Y-m-d')
    finance = Finance.objects.all()
    incfinance = finance.filter(type2='income', date_incurred=cd)
    expfinance = finance.filter(type2='expense', date_incurred=cd)
    inctotal = sum([i.amount for i in incfinance])
    exptotal = sum([i.amount for i in expfinance])

    if request.method == 'POST':
        if 'save1' in request.POST:
            Finance.objects.create(type2="expense", amount=request.POST.get('expensesamount'), type=request.POST.get('expensestype'))
            sweetify.success(request, title='Success', text='Expenses data added', icon='success', button='Ok', timer=3000)
            return redirect('/farmfinance/')
        elif 'save2' in request.POST:
            Finance.objects.create(type2="income", amount=request.POST.get('expensesamount2'), type=request.POST.get('expensestype2'))
            sweetify.success(request, title='Success', text='Income data added', icon='success', button='Ok', timer=3000)
            return redirect('/farmfinance/')

    inctotal2 = inctotal if incfinance else 50
    exptotal2 = exptotal if expfinance else 50
    total = inctotal2 + exptotal2

    incp = inctotal2 * 100/total 
    expp = exptotal2 * 100/total 

    labels = 'Income', 'Expenses'
    sizes = [incp, expp]
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('static/images/inc_exp_chart.png',dpi=100)

    inctype = incfinance.order_by('-amount').first().type if incfinance else 'null'
    exptype = expfinance.order_by('-amount').first().type if expfinance else 'null'
    cash_profit = (inctotal-exptotal) if incfinance and expfinance else 'null'
    
    percent_profit = cash_profit * 100/exptotal if incfinance and expfinance else 'null'
    context = {'incfinance':incfinance, 'expfinance':expfinance, 'exptotal':exptotal, 'inctotal':inctotal, 'exptype':exptype, 'inctype':inctype, 'cash_profit':cash_profit, 'percent_profit':percent_profit}
    return render(request, 'animal/farmfinance.html', context)

@authenticated_user
@admin_only
def employees(request):
    employees = Employee.objects.all()
    if is_ajax(request=request):
        data_response = dict()
        data = json.loads(request.body)
        emp_id = data.get('empid')
        emp_name = data.get('employeename')
        if emp_id:
            employee = employees.get(id=emp_id)
            data_response['emp'] = render_to_string('animal/emp_profile.html', {'emp':employee}, request=request)
            return JsonResponse(data_response)
        if emp_name:
            filtered_data = Employee.objects.filter(emp_name__contains = emp_name)
            data_response['results'] = render_to_string('animal/emplist.html', {'employees':filtered_data}, request=request)
            return JsonResponse(data_response)
    elif request.method == 'POST':
        if 'addemp' in request.POST:
            print(request.POST.get('gender'))
            if employees.filter(emp_id=request.POST.get('employeeid')).exists():
                sweetify.error(request, title='Error', text='Employee with that id already exists', icon='error', button='Ok', timer=3000)
                return redirect('/employees/')
            elif User.objects.filter(username = request.POST.get('username')).exists():
                sweetify.error(request, title='Error', text='User with that username already exists', icon='error', button='Ok', timer=3000)
                return redirect('/employees/')
            elif len(request.POST.get('password')) < 8:
                sweetify.error(request, title='Error', text='Password must be 8 characters or more', icon='error', button='Ok', timer=3000)
                return redirect('/employees/')
            else:
                emp = Employee.objects.create(emp_id=request.POST.get('employeeid'), emp_name=request.POST.get('employeename'), dob=request.POST.get('dob'), date_hired=request.POST.get('datehired'), gender=request.POST.get('gender'), contact=request.POST.get('contact'), address=request.POST.get('address'), designation=request.POST.get('permission'), salary=request.POST.get('basicsalary'), job_title=request.POST.get('jobtitle'))
                user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
                emp.user = user
                emp.save()
                sweetify.success(request, title='Success', text='Employee created', icon='success', button='Ok', timer=3000)
                return redirect('/employees/')
        elif 'updatesalary' in request.POST:
            percent = int(request.POST.get('salary-upd'))
            empl = employees.get(id=request.POST.get('emp_id'))
            salary = empl.salary
            new_salary = salary + (salary * percent/100)
            empl.salary = new_salary
            empl.save()
            sweetify.success(request, title='Success', text=f'{empl.emp_name} salary updated', icon='success', button='Ok', timer=3000)
            return redirect('/employees/')
        elif 'deleterecord' in request.POST:
            empl = employees.get(id=request.POST.get('emp_id'))
            empl.user.delete()
            empl.delete()
            sweetify.success(request, title='Success', text='Employee Deleted', icon='success', button='Ok', timer=3000)
            return redirect('/employees/')
    context = {'employees':employees}
    return render(request, 'animal/employees.html', context)