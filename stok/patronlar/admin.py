from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, portrait
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors


def export_to_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="firmalar.pdf"'

    # PDF dosyasını oluştur (portrait fonksiyonunu kullandık)
    doc = SimpleDocTemplate(response, pagesize=portrait(letter), rightMargin=1, leftMargin=1, topMargin=100, bottomMargin=10)
    # PDF dosyasını oluştur (portrait fonksiyonunu kullandık)
    doc = SimpleDocTemplate(response, pagesize=(2 * letter[0], letter[1]), topMargin=100, bottomMargin=10)


    # CSV verilerini al
    csv_data = []
    fields = [field.name for field in queryset.model._meta.fields if field.name not in ['id']]  # ID ve not_bilgisi sütunlarını dışarıda bırak
    csv_data.append(fields)

    for obj in queryset:
        row = [str(getattr(obj, field)) for field in fields]
        csv_data.append(row)

    # Tabloyu oluştur
    table = Table(csv_data)

    # Tablonun genişlik ayarlarını belirle
    table.setStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle([('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])  # Yazı tipini belirle

    # Tablonun içerisindeki metinlerin yazı tipini küçült
    table.setStyle([('FONTSIZE', (0, 0), (-1, -1), 8)])

    # PDF dosyasını oluştur
    doc.build([table])

    return response

export_to_pdf.short_description = "Seçilenleri PDF Olarak Dışa Aktar"

from django.contrib import admin
from .models import Firmalar

class ŞirketlerAdmin(admin.ModelAdmin):
    actions = [export_to_pdf]

admin.site.register(Firmalar, ŞirketlerAdmin)
