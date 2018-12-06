from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa

from event.models import *


def some_view(request):
    # return render(request, 'report.html')
    list = User.objects.all()
    template = get_template('report.html')
    context = {
        'event': 'Workshop',
        'student_list': list,
    }
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = "Report.pdf"
        content = "inline; filename='%s'" % (filename)
        # content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def home(request):
    event_list = EventRecord.objects.all().order_by('-pk')
    return render(request, 'index.html',
                  {'event_list': event_list})


def excellence_center(request):
    return render(request, 'excellence_center.html')


def structural_design(request):
    return render(request, 'static1.html')


def cisco_networking_academy(request):
    return render(request, 'static2.html')


def texas(request):
    return render(request, 'static3.html')


def smc_india(request):
    return render(request, 'static4.html')


def automation_research(request):
    return render(request, 'static5.html')


def vlsi_design(request):
    return render(request, 'static6.html')


def big_data(request):
    return render(request, 'static7.html')


def innovation_centre(request):
    return render(request, 'static8.html')


def mobile_application(request):
    return render(request, 'static9.html')


def software_development(request):
    return render(request, 'static10.html')
