from datetime import date
from io import BytesIO

import xlwt
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.views.generic import TemplateView
from xhtml2pdf import pisa

from event.models import EventRecord
from student.models import StudentRecord
from .forms import TransactionForm
from .models import RegistrationRecord


# Create your views here.
# noinspection PyBroadException
class RegisterEvent(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            if not request.user.is_staff and not request.user.is_superuser:
                obj = EventRecord.objects.get(slug=kwargs['slug'])
                t = date.today()
                if obj.registration_open and (obj.registration_start <= t) and (t <= obj.registration_end):
                    try:
                        student = StudentRecord.objects.get(user=request.user)
                    except ObjectDoesNotExist:
                        messages.info(request, 'Fill your personal information before registration')
                        return redirect('home')
                    try:
                        RegistrationRecord.objects.get(student=student, event=obj)
                        msg = str('Already Register in ' + obj.event_name)
                        messages.warning(request, msg)
                    except ObjectDoesNotExist:
                        obj.registered_student += 1
                        RegistrationRecord.objects.create(student=student, user=request.user, event=obj,
                                                          c_o_e=obj.c_o_e, type=obj.type, balance=obj.fees)
                        obj.save(update_fields=['registered_student'])
                        msg = str('Successfully Register for ' + obj.event_name)
                        messages.success(request, msg)
                        current_site = get_current_site(request)
                        mail_subject = 'Welcome to CBSE Course: ' + obj.event_name
                        message = render_to_string('registration_email.txt', {
                            'user': request.user,
                            'domain': current_site.domain,
                            'event': obj,
                            'email': settings.EMAIL_HOST_USER,
                        })
                        email = EmailMessage(mail_subject, message, to=[request.user.email])
                        email.send()
                        return redirect("account:consolidated_view_all")
                else:
                    messages.info(request, 'Registration Closed/Does not Start')
            else:
                raise PermissionDenied
            return redirect('event:event_detail', kwargs['slug'])
        except ObjectDoesNotExist:
            messages.error(request, 'Record Not Found')
            return redirect('home')
        except PermissionDenied:
            messages.warning(request, 'You have not Permission to Register')
        except Exception:
            messages.error(request, 'Try After Some Time')
            return redirect('home')


# noinspection PyBroadException
class RegistrationDetail(TemplateView):
    template_name = 'registration_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            obj = RegistrationRecord.objects.get(registration_id=kwargs['registration_id'])
            if request.user.is_superuser or request.user == obj.event.user:
                form = TransactionForm()
                return render(request, self.template_name, {'obj': obj, 'form': form, 'staff': True})
            student = StudentRecord.objects.get(user=request.user)
            if student == obj.student:
                return render(request, self.template_name, {'obj': obj, 'staff': False})
            raise PermissionDenied
        except Exception:
            messages.error(request, 'You Does not Permission')
            return redirect('home')

    def post(self, request, **kwargs):
        try:
            obj = RegistrationRecord.objects.get(registration_id=kwargs['registration_id'])
            if request.user.is_superuser or request.user == obj.event.user:
                form = TransactionForm(request.POST)
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.registration_id = obj.registration_id
                    temp.user = request.user
                    obj.amount += temp.amount
                    obj.balance -= temp.amount
                    temp.save()
                    obj.save(update_fields=['amount', 'balance'])
                    obj.transaction_id.add(temp)
                    messages.success(request, 'Successfully Update')
                    return redirect('registration:registration_detail', kwargs['registration_id'])
                else:
                    messages.error(request, 'Invalid Inputs')
                    return render(request, self.template_name, {'obj': obj, 'form': form, 'staff': True})
            else:
                raise PermissionDenied
        except PermissionDenied:
            messages.error(request, 'You Does not Permission')
            return redirect('home')
        except Exception:
            messages.error(request, 'Error, Contact to US')
            return redirect('home')


# noinspection PyBroadException
class RegisterStudentList(TemplateView):
    template_name = 'register_student_list.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                obj = RegistrationRecord.objects.filter(event=event)
                return render(request, self.template_name, {'obj': obj})
            raise PermissionDenied
        except Exception:
            messages.error(request, 'You Does not Permission')
            return redirect('home')


# noinspection PyBroadException
class RegistrationReport(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                student_list = RegistrationRecord.objects.filter(event=event)
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = "attachment; filename='Registration Report %s.xls'" % event
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet(event.event_name)

                # Sheet header, first row
                font_style_bold = xlwt.XFStyle()
                font_style_bold.font.bold = True

                ws.write_merge(0, 0, 2, 4, 'ABES Engineering College, Ghaziabad', font_style_bold)
                ws.write_merge(1, 1, 1, 5, '19th Km Stone NH-24, Near Crossing Republic, Ghaziabad - 201009(UP), INDIA')

                ws.write(3, 0, 'Event Code')
                ws.write(3, 1, event.slug, font_style_bold)
                ws.write(3, 2, 'Event Name')
                ws.write_merge(3, 3, 3, 4, event.event_name, font_style_bold)
                ws.write(3, 5, 'Event Date')
                ws.write(3, 6, event.event_date.strftime('%b %d, %Y'), font_style_bold)

                ws.write(4, 0, 'COE')
                ws.write(4, 1, event.c_o_e, font_style_bold)
                ws.write(4, 2, 'Instructor Name')
                ws.write_merge(4, 4, 3, 4, event.resource_person, font_style_bold)
                ws.write(4, 5, 'Event Fees')
                ws.write(4, 6, event.fees, font_style_bold)

                row_num = 6
                columns = ['S. No.', 'Registration Id', 'Student Name', 'Admission No.', 'Amount', 'Balance', 'Date']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num])

                # Sheet body, remaining rows
                for student in student_list:
                    row_num += 1
                    ws.write(row_num, 0, row_num - 6)
                    ws.write(row_num, 1, student.registration_id)
                    ws.write(row_num, 2, student.student.user.first_name + ' ' + student.student.user.last_name)
                    ws.write(row_num, 3, student.student.roll_no)
                    ws.write(row_num, 4, student.amount)
                    ws.write(row_num, 5, student.balance)
                    ws.write(row_num, 6, student.timestamp.strftime('%b %d, %Y'))

                ws.write_merge(row_num + 2, row_num + 2, 0, 3, 'Printed on ' + str(timezone.now()) + ' (UTC)')
                wb.save(response)
                return response
            raise PermissionDenied
        except PermissionDenied:
            messages.error(request, 'You Does not Permission')
            return redirect('home')
        except Exception:
            messages.error(request, 'Something went wrong')
            return redirect('home')


# noinspection PyBroadException
class TransactionReport(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                student_list = RegistrationRecord.objects.filter(event=event)
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = "attachment; filename='Transaction Report_%s.xls'" % event
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet(event.event_name)

                # Sheet header, first row
                font_style_bold = xlwt.XFStyle()
                font_style_bold.font.bold = True

                ws.write_merge(0, 0, 2, 4, 'ABES Engineering College, Ghaziabad', font_style_bold)
                ws.write_merge(1, 1, 1, 5, '19th Km Stone NH-24, Near Crossing Republic, Ghaziabad - 201009(UP), INDIA')

                ws.write(3, 0, 'Event Code')
                ws.write(3, 1, event.slug, font_style_bold)
                ws.write(3, 2, 'Event Name')
                ws.write_merge(3, 3, 3, 4, event.event_name, font_style_bold)
                ws.write(3, 5, 'Event Date')
                ws.write(3, 6, event.event_date.strftime('%b %d, %Y'), font_style_bold)

                ws.write(4, 0, 'COE')
                ws.write(4, 1, event.c_o_e, font_style_bold)
                ws.write(4, 2, 'Instructor Name')
                ws.write_merge(4, 4, 3, 4, event.resource_person, font_style_bold)
                ws.write(4, 5, 'Event Fees')
                ws.write(4, 6, event.fees, font_style_bold)

                row_num = 6
                columns = ['S. No.', 'Receipt No.', 'Student Name', 'Admission No.', 'Amount', 'Date', 'User']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style_bold)

                # Sheet body, remaining rows
                for student in student_list:
                    for s in student.transaction_id.all():
                        row_num += 1
                        ws.write(row_num, 0, row_num - 6)
                        ws.write(row_num, 1, student.registration_id)
                        ws.write(row_num, 2, student.student.user.first_name + ' ' + student.student.user.last_name)
                        ws.write(row_num, 3, student.student.roll_no)
                        ws.write(row_num, 4, s.amount)
                        ws.write(row_num, 5, s.timestamp.strftime('%b %d, %Y'))
                        ws.write(row_num, 6, s.user.username)

                ws.write_merge(row_num + 2, row_num + 2, 0, 3, 'Printed on ' + str(timezone.now()) + ' (UTC)')
                wb.save(response)
                return response
            raise PermissionDenied
        except PermissionDenied:
            messages.error(request, 'You Does not Permission')
            return redirect('home')
        except Exception:
            messages.error(request, 'Something went wrong')
            return redirect('home')


# noinspection PyBroadException
class EnrollmentReport(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                if event.fees == 0:
                    student_list = RegistrationRecord.objects.filter(event=event)
                else:
                    student_list = RegistrationRecord.objects.filter(event=event, balance__lt=event.fees)

                template = get_template('report.html')
                html = template.render({'event': event, 'student_list': student_list, 'now': timezone.now()})

                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

                if not pdf.err:
                    response = HttpResponse(result.getvalue(), content_type='application/pdf')
                    # content = "inline; filename='Enrollment Report %s.pdf'" % event
                    content = "attachment; filename='Enrollment Report %s.pdf'" % event
                    response['Content-Disposition'] = content
                    return response

                return HttpResponse("Not found")
            raise PermissionDenied
        except PermissionDenied:
            messages.error(request, 'You Does not Permission')
            return redirect('home')
        except Exception:
            messages.error(request, 'Something went wrong')
            return redirect('home')
