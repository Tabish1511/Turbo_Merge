from django.db import transaction
from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import PDFDoc
import os, PyPDF2, uuid


def clear_session(request):
    if 'upload_group_key' in request.session:
        del request.session['upload_group_key']


def index(request):
    uploads = request.FILES.getlist('uploads')
    if uploads == []:
        clear_session(request)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'upload_group_key' not in request.session:
                # Generate a new UUID key for the group
                group_key = str(uuid.uuid4())
                request.session['upload_group_key'] = group_key
            else:
                group_key = request.session['upload_group_key']
            for upload in uploads:
                PDFDoc.objects.create(upload=upload, owner=request.user, key=group_key)
                uploads = PDFDoc.objects.filter(owner=request.user, key=group_key)
        else:
            with transaction.atomic():
                if 'upload_group_key' not in request.session:
                    # Generate a new UUID key for the group
                    group_key = str(uuid.uuid4())
                    request.session['upload_group_key'] = group_key
                else:
                    group_key = request.session['upload_group_key']
                for upload in uploads:
                    PDFDoc.objects.create(upload=upload, key=group_key)
                    uploads = PDFDoc.objects.filter(key=group_key)
    else:
        clear_session(request)
    return render(request, 'merge_app/index.html', {'uploads':uploads})


def del_upload(request, upload_id):
    try:
        session_keys = list(request.session.keys()) # <<== get keys list
        currentSession = request.session[session_keys[0]] # <<== get the key in session now!!!
        uploads = PDFDoc.objects.filter(key=request.session.get('upload_group_key'))
        
        upload = PDFDoc.objects.get(id=upload_id) # <<== THIS TAKES THE FILE THAT IS SUPPOSED TO BE DELETED ***
        if request.method == 'POST':
            upload_path = upload.upload.path
            upload.delete()
            os.remove(upload_path)
        session_keys = list(request.session.keys()) # <<== get keys list
        currentSession = request.session[session_keys[0]] # <<== get the key in session now!!!
        uploads = PDFDoc.objects.filter(key=request.session.get('upload_group_key'))
        return render(request, 'merge_app/index.html', {'uploads': uploads})
    except Exception as e:
        uploads = PDFDoc.objects.filter(key=request.session.get('upload_group_key'))
        return render(request, 'merge_app/index.html', {'uploads': uploads})


def merge_pdf(request):
    try:
        fileList = request.POST['itemNames'].split(',')
        pageList = request.POST['selectedValues'].split(',')
        if request.user.is_authenticated:
            session_keys = list(request.session.keys()) # <<== get keys list
            currentSession = request.session[session_keys[3]] # <<== get the key in session now!!!
            if fileList == ['']:
                allFiles = PDFDoc.objects.filter(owner=request.user, key=currentSession)
            else:
                allFiles = PDFDoc.objects.filter(owner=request.user, key=currentSession)
                allFiles = sorted(allFiles, key=lambda pdf_doc: fileList.index(pdf_doc.upload))
        elif 'upload_group_key' in request.session:
            session_keys = list(request.session.keys()) # <<== get keys list
            currentSession = request.session[session_keys[0]] # <<== get the key in session now!!!
            if fileList == ['']:
                allFiles = PDFDoc.objects.filter(key=currentSession)
            else:
                allFiles = PDFDoc.objects.filter(key=currentSession)
                allFiles = sorted(allFiles, key=lambda pdf_doc: fileList.index(pdf_doc.upload))
        pdfWriter = PyPDF2.PdfWriter()
        for i in range(0, len(allFiles)):
            if allFiles[i].upload.path.endswith('.pdf'):
                pdfFile = open(allFiles[i].upload.path, 'rb')
                pdfReader = PyPDF2.PdfReader(pdfFile)
                if len(pdfReader.pages) < 2:
                    for j in range(len(pdfReader.pages)):
                        pageObj = pdfReader.pages[j]
                        pdfWriter.add_page(pageObj)
                else:
                    for j in range(int(pageList[i]), len(pdfReader.pages)):
                        pageObj = pdfReader.pages[j]
                        pdfWriter.add_page(pageObj)
        # Change directory and save merged PDF
        pdf_dir = os.path.dirname(allFiles[i].upload.path)
        os.chdir(pdf_dir)
        pdf_out = open('mergefile.pdf', 'wb')
        pdfWriter.write(pdf_out)
        pdf_out.close()
        # Prepare and return the merged PDF as a response
        response = FileResponse(open('mergefile.pdf', 'rb'))
        os.remove('mergefile.pdf')
        return response
    except Exception as e:
        return redirect('merge_app:index')
