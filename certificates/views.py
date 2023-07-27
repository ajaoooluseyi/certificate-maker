import os
import uuid
from io import BytesIO

from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from fpdf import FPDF

from .models import Certificate


def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    return render(
        request, "certificates/certificate_detail.html", {"certificate": certificate}
    )


def create_certificate(request):
    if request.method == "POST":
        name = request.POST["name"]
        date = request.POST["date"]
        signature = request.POST["signature"]
        details = request.POST["details"]

        certificate = Certificate.objects.create(
            name=name, date=date, signature=signature, details=details
        )

        # Generate the PDF certificate using fpdf
        pdf = FPDF(format="A4", orientation="L", unit="mm")
        pdf.add_page()

        # Set certificate background image (adjust the path according to your image)
        pdf.image("C:/Users/USER/Desktop/Backend/core/cert.jpg", x=0, y=0, w=297, h=210)

        # Add the custom font
        pdf.add_font(
            "WCL",
            "",
            "C:/Users/USER/Desktop/Backend/core/certificates/fonts/Wolf in the City Light.ttf",
            uni=True,
        )

        # Set font and text color
        pdf.set_font("WCL", size=100)
        pdf.set_text_color(0, 0, 0)

        # Customize the certificate content and layout
        pdf.cell(0, 50, txt="Certificate of Achievement", ln=True, align="C")

        # Add the custom font
        pdf.add_font(
            "TTM",
            "",
            "C:/Users/USER/Desktop/Backend/core/certificates/fonts/TalkingToTheMoon.ttf",
            uni=True,
        )

        pdf.add_font(
            "VIO",
            "",
            "C:/Users/USER/Desktop/Backend/core/certificates/fonts/YanoneKaffeesatz-Regular.ttf",
            uni=True,
        )

        # Set font and text color
        pdf.set_font("TTM", size=30)
        pdf.set_text_color(0, 0, 0)

        pdf.cell(0, 20, txt="Presented to", ln=True, align="C")

        pdf.set_font("WCL", size=80)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 30, txt=certificate.name, ln=True, align="C")

        pdf.set_font("TTM", size=30)
        pdf.set_text_color(0, 0, 0)

        pdf.cell(0, 20, txt="In recognition of", ln=True, align="C")

        pdf.set_font("VIO", size=50)
        pdf.multi_cell(0, 20, txt=certificate.details, align="C")

        pdf.set_font("TTM", size=30)
        pdf.set_xy(30, 160)  # Set position for the "Date" header
        pdf.cell(0, 10, txt="Signed on:", ln=True, align="L")

        pdf.set_font("TTM", size=20)
        pdf.set_xy(30, 172)  # Set position
        pdf.cell(0, 10, txt=certificate.date, align="L")

        pdf.set_font("TTM", size=30)
        pdf.set_xy(30, 157)  # Set position for the "Date" header
        pdf.cell(0, 10, txt="Signed by:", ln=True, align="R")

        pdf.set_font("TTM", size=20)
        pdf.set_xy(30, 172)  # Set position
        pdf.cell(0, 10, txt=certificate.signature, align="R")

        # Save the PDF to a BytesIO object
        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        pdf_bytes_io = BytesIO(pdf_bytes)

        # Save the PDF to a file
        file_path = f"certificates/certificates/{certificate.name}.pdf"
        with open(file_path, "wb") as pdf_file:
            pdf_file.write(pdf_bytes_io.getvalue())

        # Save the file path to the certificate model
        certificate.pdf_file.name = file_path
        certificate.save()

        certificate_id = certificate.pk
        return redirect("certificate_detail", certificate_id=certificate_id)

    return render(request, "certificates/create_certificate.html")


def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except (TypeError, ValueError):
        return False


def verify_certificate(request):
    if request.method == "POST":
        certificate_id = request.POST["certificate_id"]

        if not is_valid_uuid(certificate_id):
            # Handle the UUID validation error here (e.g., display an error message)
            error_message = f"{certificate_id} is not a valid ID format. Try again."
            return HttpResponse(error_message, status=404)

        try:
            Certificate.objects.get(pk=certificate_id)

            return HttpResponse("Certificate is valid!")
        except Certificate.DoesNotExist:
            return HttpResponse("Certificate not valid!")
    return render(request, "certificates/verify_certificate.html")


def download_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(pk=certificate_id)
        file_path = certificate.pdf_file.path

        if not os.path.exists(file_path):
            raise Http404("Certificate file not found.")

        with open(file_path, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    except Certificate.DoesNotExist:
        return HttpResponse("Certificate not found.", status=404)
