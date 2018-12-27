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
                response['Content-Disposition'] = "attachment; filename='Report_%s.xls'" % event
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet(event.event_name)

                # Sheet header, first row
                row_num = 0
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                columns = ['S. No.', 'Receipt No.', 'Student Name', 'Admission No.', 'Amount', 'Balance', 'Date',
                           'Remark']
                for col_num in range(8):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()
                for student in student_list:
                    row_num += 1
                    ws.write(row_num, 0, row_num, font_style)
                    ws.write(row_num, 1, student.registration_id, font_style)
                    ws.write(row_num, 2, student.student.user.first_name + ' ' + student.student.user.last_name, font_style)
                    ws.write(row_num, 3, student.student.roll_no, font_style)
                    ws.write(row_num, 4, student.amount, font_style)
                    ws.write(row_num, 5, student.balance, font_style)
                    ws.write(row_num, 6, student.timestamp.strftime('%Y-%m-%d'), font_style)
                    ws.write(row_num, 7, '', font_style)
                wb.save(response)
                return response
            raise PermissionDenied
        except PermissionDenied:
            messages.error(request, 'You Does not Permission')
            return redirect('home')
        # except Exception:
        #     messages.error(request, 'Something went wrong')
        #     return redirect('home')


# noinspection PyBroadException
class TransactionReport(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                student_list = RegistrationRecord.objects.filter(event=event)
                context = {'event': event, 'student_list': student_list}
                # return render(request, self.template_name, context)
                template = get_template('report.html')
                html = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
                if not pdf.err:
                    response = HttpResponse(result.getvalue(), content_type='application/pdf')
                    filename = "Report.pdf"
                    # content = "inline; filename='%s'" % filename
                    content = "attachment; filename='%s'" % filename
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


# noinspection PyBroadException
class EnrollmentReport(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                student_list = RegistrationRecord.objects.filter(event=event)
                context = {'event': event, 'student_list': student_list}
                # return render(request, self.template_name, context)
                template = get_template('report.html')
                html = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
                if not pdf.err:
                    response = HttpResponse(result.getvalue(), content_type='application/pdf')
                    filename = "Report.pdf"
                    # content = "inline; filename='%s'" % filename
                    content = "attachment; filename='%s'" % filename
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
