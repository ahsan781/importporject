# Basic Django Imports
import re
from os import waitpid
from django.contrib.admin.sites import all_sites
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render, HttpResponse
# Imports for csv File
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from website.models import Vendor_profile
import pandas as pd
import csv
# imports for PAth
from Dummy.settings import TEMPLATE_DIR
import os
# import for handling file stream
import io
# import for iterating over the loop
from itertools import zip_longest
# FILE UPLOAD form FROM PROJECT
from Dummy.form import FileUpload
# DJANGO MODELS
from website.models import CsvSavedData

TEMP_CSV_DIR = os.path.join(TEMPLATE_DIR, "temporaryCsvFiles")
CSV_FILE_DIR = os.path.join(TEMPLATE_DIR, "CVSFiles")


def randomFileName(fname):
    counter = 0
    pre, suf = fname.split('.')
    while os.path.exists(os.path.join(TEMP_CSV_DIR, fname)):
        counter = counter + 1
        fname = pre + str(counter) + "." + suf
    return fname

def index(request):
    return redirect("/")
def readCsvFile(fname):
    f = open(os.path.join(TEMP_CSV_DIR, fname), 'r')
    csv_r = csv.reader(f)
    headers = next(csv_r, None)
    all_rows_csv = []
    for row in csv_r:
        all_rows_csv.append(row)
    f.close()
    return all_rows_csv, headers


def handle_uploaded_file(file):
    data_set = file.read().decode("UTF-8")
    io_stream = io.StringIO(data_set)
    all_rows = []
    for row in csv.reader(io_stream):
        all_rows.append(row)
    with open(os.path.join(TEMP_CSV_DIR, file.name), "w", newline="") as b:
        writer = csv.writer(b)
        for row in all_rows:
            writer.writerow(row)


@login_required(login_url='login/')
def csvDisplay(request):
    request.session['EditFile'] = False
    if request.method == "POST":
        fileForm = FileUpload(request.POST, request.FILES)
        if fileForm.is_valid():
            file = request.FILES['file']
            filename = randomFileName(file.name)
            file.name = filename
            handle_uploaded_file(file)
            request.session['FILENAME'] = filename
        data = pd.read_csv(os.path.join(TEMP_CSV_DIR, filename))
        headers = pd.read_csv(os.path.join(TEMP_CSV_DIR, filename), nrows=1).columns

        data_html = data.to_html()
        context = {'loaded_data': data_html, "form": fileForm, "fname": filename,"header":headers}
        return render(request, "index.html", context=context)
    else:
        fileForm = FileUpload()
        context = {"form": fileForm}
        return render(request, "index.html", context=context)


@login_required(login_url='login/')
def editCsv(request):
    fname = request.session.get("FILENAME")
    all_rows_csv, headers = readCsvFile(fname)
    return render(request, "Tables.html", context={"headers": headers, "all_rows_csv": all_rows_csv,
                                                   "editFile": request.session.get("EditFile")})


@login_required(login_url='login/')
def changeRow(request, rowNum):
    fname = request.session.get("FILENAME")
    all_rows_csv, headers = readCsvFile(fname)
    if request.method == "POST":
        row_data = []
        for key, val in request.POST.items():
            if key == "csrfmiddlewaretoken":
                continue
            else:
                row_data.append(val)
        line_to_override = {rowNum: row_data}
        with open(os.path.join(TEMP_CSV_DIR, fname), 'w', newline='') as b:
            writer = csv.writer(b)
            writer.writerow(headers)
            for line, row in enumerate(all_rows_csv, 1):
                data = row
                if line == rowNum:
                    data = line_to_override.get(line, row)
                    writer.writerow(data)
                    continue
                writer.writerow(row)
        return redirect(editCsv)
    else:
        for line, row in enumerate(all_rows_csv, 1):
            if line == rowNum:
                content_data = zip_longest(headers, row)
                context = {"header_values": content_data, "rowNum": rowNum}
                return render(request, "editForm.html", context=context)


def deleteRow(request, rowNum):
    fname = request.session.get("FILENAME")
    all_rows_csv, headers = readCsvFile(fname)
    with open(os.path.join(TEMP_CSV_DIR, fname), 'w', newline='') as b:
        writer = csv.writer(b)
        writer.writerow(headers)
        for line, row in enumerate(all_rows_csv, 1):
            if line == rowNum:
                continue
            else:
                writer.writerow(row)
    return redirect(editCsv)


def discardFile(request):
    fname = request.session.get("FILENAME")
    os.remove(os.path.join(TEMP_CSV_DIR, fname))
    return redirect(csvDisplay)


@login_required(login_url='login/')
def displayUserCSV(request):
    # csv_data = CsvSavedData.objects.filter(user=request.user)
    csv_data = CsvSavedData.objects.all()
    context = {
        "csv_data": csv_data
    }
    return render(request, "csvFiles.html", context=context)


from import_export import resources
from .models import CsvSavedData


def saveCsvFile(request):
    dataFrame  = pd.read_csv(os.path.join(TEMP_CSV_DIR, request.session.get("FILENAME")))
    for items in dataFrame.values.tolist():
        CsvSavedData.objects.create(
            first_name = items[0],
            last_name = items[1],
            email = items[2],
            mobile = items[3],
            address = items[4],
            suburb = items[5],
            state = items[6],
            postal = items[7],
            gender = items[8],
            DOB = items[9]
        )
    try:
        os.remove(os.path.join(TEMP_CSV_DIR, request.session.get("FILENAME")))
        print("[+] File removed Suceesfull")
    except:
        print("[+] Error While removing file ")
    return redirect(displayUserCSV)


def updateCSVFile(request, fname):
    f = open(os.path.join(TEMP_CSV_DIR, fname), 'r')
    request.session['FILENAME'] = fname
    request.session['EditFile'] = True
    return redirect(editCsv)


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            vendor = Vendor_profile(user=user, name=str(request.POST["first_name"] + request.POST["last_name"]))
            vendor.save()
            # else:
            #     customer = Customer_profile(user=user, first_name=str(request.POST["first_name"]),
            #                                 last_name=str(request.POST["last_name"]))
            #     customer.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def csvdata(request):
    # csv_data = CsvSavedData.objects.filter(user=request.user)
    csv_data = CsvSavedData.objects.all()
    context = {
        "csv_data": csv_data
    }
    return render(request, "csvdata.html", context=context)
    # members_list = CsvSavedData.objects.all()
    # paginator = Paginator(members_list, 5)
    # page = request.GET.get('page')
    # try:
    #     members = paginator.page(page)
    # except PageNotAnInteger:
    #     members = paginator.page(1)
    # except EmptyPage:
    #     members = paginator.page(paginator.num_pages)
    # return render(request, 'csvdata.html', {'members': members})
