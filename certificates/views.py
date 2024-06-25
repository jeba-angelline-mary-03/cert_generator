import csv
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import UploadedFile, Certificate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import uuid
from datetime import datetime
from django.templatetags.static import static 
from reportlab.lib.colors import HexColor

@login_required  # Ensuring user is logged in before uploading files
def upload_file(request):
    form = UploadFileForm()  # Initialize the form
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            if request.user.is_authenticated:
                uploaded_file.user = request.user
            else:
                uploaded_file.user = None
            uploaded_file.save()
            process_csv(uploaded_file.file.path)
            return redirect('certificate_list')
    return render(request, 'certificates/upload_file.html', {'form': form})


def home(request):
    return render(request, 'certificates/home.html')
    
def process_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[0]
            generate_certificate(name, f'{settings.MEDIA_ROOT}/certificates/{name}.pdf')

def generate_certificate(name, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    certificate_id = uuid.uuid4().hex[:8]  
    current_date = datetime.now().strftime("%B %d, %Y") 
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFillColor(HexColor("#F6F6F6"))  # Light gray background
    c.rect(0, 0, 612, 792, fill=1)
    
    # Title
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(HexColor("#B71C1C"))  # Red color
    c.drawCentredString(306, 680, "Certificate of Appreciation")
    
    # Presented to
    c.setFont("Helvetica", 24)
    c.setFillColor(HexColor("#004D40"))  # Dark green color
    c.drawString(100, 600, "Presented to")
    c.setFont("Helvetica-Bold", 28)
    c.drawString(100, 560, f"{name}")
    
    # Additional details
    c.setFont("Helvetica", 18)
    c.setFillColor(HexColor("#1A237E"))  # Blue color
    c.drawString(100, 500, "This is to certify that")
    c.drawString(100, 470, f"{name} has actively participated in an online quiz")
    c.drawString(100, 440, "on International Yoga E-Quiz conducted by")
    c.drawString(100, 410, "Department of Electrical and Electronics Engineering,")
    c.drawString(100, 380, "SNS College of Technology, Coimbatore.")
    
    # Footer
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(HexColor("#FF6F00"))  # Orange color
    c.drawCentredString(306, 300, "Yoga for Harmony and Peace")
    
    # Date and Certificate ID
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#424242"))  # Dark gray color
    c.drawString(100, 250,  f"Date: {current_date}")
    c.drawString(400, 250, f"Certificate ID: {certificate_id}")
    
    # Draw decorative lines
    c.setStrokeColor(HexColor("#757575"))  # Light gray lines
    c.line(100, 700, 512, 700)  # Horizontal line below title
    c.line(100, 540, 512, 540)  # Horizontal line below name
    c.line(100, 360, 512, 360)  # Horizontal line above footer
    c.save()

def certificate_list(request):
    certificates = Certificate.objects.filter(user=request.user)
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})