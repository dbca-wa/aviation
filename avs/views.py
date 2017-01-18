# before changing tasks, task, activity_type to task

from django.views.generic.list import ListView

from django.views.generic.edit import CreateView, UpdateView

from django.views.generic import TemplateView

from django import forms

from avs.models import *

from avs.forms import *

from django.shortcuts import redirect

from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response

from django.forms.models import inlineformset_factory

from django.db.models import Sum, Max, Min, Q

import datetime

from datetime import timedelta

import time

import re

from datetime import datetime as from_datetime

from django.template import RequestContext

from django.views.decorators.csrf import csrf_protect


# Summary - Fire

@login_required
def firesummary(request, str_date_to=None, str_date_from=None):

    state = ''
    state_type = ''
    table = ''
    header = ''

    if request.method == 'POST':  # If the form has been submitted...

        drForm = DateRangeForm(request.POST)  # A form bound to the POST data

        if drForm.is_valid():  # All validation rules pass

            str_date_from = request.POST['date_from']

            str_date_to = request.POST['date_to']

    # Get Filtered Aircraft Flight Logs

    if str_date_to is None:

        date_to = from_datetime.strptime(
            "30/06/" + str(datetime.date.today().year), "%d/%m/%Y")

    else:

        date_to = from_datetime.strptime(str_date_to, "%d/%m/%Y")

    if str_date_from is None:

        date_from = from_datetime.strptime(
            "01/07/" + str(datetime.date.today().year - 1), "%d/%m/%Y")

    else:

        date_from = from_datetime.strptime(str_date_from, "%d/%m/%Y")

    str_date_to = date_to.strftime("%d/%m/%Y")

    str_date_from = date_from.strftime("%d/%m/%Y")

    data = {'date_to': str_date_to, 'date_from': str_date_from}

    drForm = DateRangeForm(data)

    if date_from > date_to:

        state = 'Date From must be less than Date To'

        state_type = 'Warning'

    else:

        fire_flightlogs = AircraftFlightLogDetail.objects.exclude(
            fire_number='').exclude(
            fire_number=None).filter(
            aircraft_flight_log__date__gte=date_from).filter(
                aircraft_flight_log__date__lte=date_to)

        logs_2000 = AircraftFlightLogDetail.objects

        header = '<th>Flight Log Number</th><th>Date</th><th>Task</th><th>Fire Number</th><th>Job Number</th><th>Datcon</th>'

        table = ''

        for fl in fire_flightlogs:

            table = table + '<tr>'

            table = table + '<td>' + '<a href="' + str(fl.aircraft_flight_log.get_absolute_url(
            )) + '">' + str(fl.aircraft_flight_log.flight_log_number) + '</a>' + '</td>'

            #table = table + '<td>' + str(fl.aircraft_flight_log.flight_log_number) + '</td>'

            table = table + '<td>' + \
                str(fl.aircraft_flight_log.date.strftime("%d/%m/%Y")) + '</td>'

            if fl.task is None:

                table = table + '<td></td>'

            else:

                table = table + '<td>' + fl.task.name + '</td>'

            table = table + '<td>' + fl.fire_number + '</td>'

            table = table + '<td>' + fl.job_number + '</td>'

            table = table + '<td>' + str(fl.datcon) + '</td>'

            table = table + '</tr>'

    return render_to_response("summaryfire.html",
                              {'table': table,
                               'header': header,
                               'drForm': drForm,
                               'state': state,
                               'state_type': state_type,
                               'pagetitle': 'Datcon Fire Summary'},
                              context_instance=RequestContext(request))


def createSummaryFlightHTML(aircraft_post, task_post, pilot_post):

    task = task_post.order_by("name")

    # ----- Create Header Row --------

    header = "<th>Year</th>"

    footer = '<th></th>'

    header_size = 0

    for a in task:

        header = header + "<th>" + a.name + "</th>"

        footer = footer + '<th></th>'

        header_size = header_size + 1

    header = header + "<th>Total</th>"

    header_size = header_size + 2

    footer = footer + '<th></th>'

    table = ''

    # -------------

    '''

     logs_2000 = AircraftFlightLogDetail.objects.filter(aircraft_flight_log__date__gte=date_from).filter(aircraft_flight_log__date__lte=date_to) \

    .filter(Q(pilot_in_command__in = pilot_ids) | Q(pilot_in_command_under_supervision__in = pilot_ids))

    '''

    flightlogs = AircraftFlightLogDetail.objects.filter(
        aircraft_flight_log__aircraft__in=aircraft_post)

    flightlogs = flightlogs.filter(Q(pilot_in_command__in=pilot_post) | Q(
        pilot_in_command_under_supervision__in=pilot_post))

    #flightlogs = AircraftFlightLogDetail.objects.extra(where=["1=0"])

    # if (flightlogs) = 0:

    # if len(aircraft) != 0 and len(flightlogs) != 0:

    if flightlogs:

        # Determine start and finish date for years

        maxYear = flightlogs.aggregate(Max('aircraft_flight_log__date'))[
            'aircraft_flight_log__date__max'].year

        minYear = flightlogs.aggregate(Min('aircraft_flight_log__date'))[
            'aircraft_flight_log__date__min'].year

        # Create Table with Sum of months

        table = ''

        year = minYear - 1

        while year <= maxYear:

            table = table + '<tr>'

            table += '<td>' + str(year) + '/' + str(year + 1) + '</td>'

            date_from = from_datetime.strptime(
                "01/07/" + str(year), "%d/%m/%Y")

            date_to = from_datetime.strptime(
                "30/06/" + str(year + 1), "%d/%m/%Y")

            fl_year = flightlogs.filter(
                aircraft_flight_log__date__gte=date_from).filter(
                aircraft_flight_log__date__lte=date_to)

            total = 0

            for a in task:

                sum_datcon = 0

                fl_year_task = fl_year.filter(task=a)

                sum_datcon = fl_year_task.aggregate(Sum('datcon'))[
                    'datcon__sum']

                if sum_datcon is None:

                    sum_datcon = 0

                total += sum_datcon

                table = table + '<td>' + str(sum_datcon) + '</td>'

            table = table + '<td>' + str(total) + '</td>'

            table = table + '</tr>'

            year += 1

        #header_size = header_size + 1

    return (header, table, footer, header_size)


# Summary - Flight Task

@login_required
def flightsummary(request):

    aircraft_post = []

    task_post = []

    pilot_post = []

    if request.method == 'POST':  # If the form has been submitted...

        drForm = FieldFilterForm(request.POST)  # A form bound to the POST data

        if drForm.is_valid():  # All validation rules pass

            aircraft_post = drForm.cleaned_data['aircraft']

            task_post = drForm.cleaned_data['task']

            pilot_post = drForm.cleaned_data['pilot']

    aircraft_ids = []

    for x in aircraft_post:

        aircraft_ids.append(x.id)

    task_ids = []

    for x in task_post:

        task_ids.append(x.id)

    pilot_ids = []

    for x in pilot_post:

        pilot_ids.append(x.id)

    if len(aircraft_ids) == 0 or len(pilot_ids) == 0 or len(task_ids) == 0:

        header = ''

        table = ''

        footer = ''

        header_size = 0

        state = 'Please select a minimum of 1 item from each select list.'

        state_type = 'Warning'

    else:

        #header, table, footer, header_size = createSummaryPilotHTML(pilot_post, task_post, logs_2000, 'command')

        #header, table, footer, header_size = createSummaryAircraftHTML(logs_2000, aircraft_post, task_post, )

        header, table, footer, header_size = createSummaryFlightHTML(
            aircraft_post, task_post, pilot_post)

        state = ''

        state_type = ''

    default_data = {
        'aircraft': aircraft_ids,
        'pilot': pilot_ids,
        'task': task_ids}

    drForm = FieldFilterForm(default_data)

    #header, table, footer, header_size = createSummaryFlightHTML(aircraft_post)

    return render_to_response("summaryflight.html",
                              {'pagetitle': 'Datcon Flight Summary',
                               'table': table,
                               'header': header,
                               'footer': footer,
                               'header_size': header_size,
                               'drForm': drForm,
                               'state': state,
                               'state_type': state_type},
                              context_instance=RequestContext(request))


def createSummaryPilotHTML(pilots, tasks, flightlogs, pilot_type):

    time_start = time.time()

    #tasks = Task.objects.all().order_by("name")

    # ----- Create Header Row --------

    header = "<th>Pilot</th>"

    footer = '<th></th>'

    header_size = 0

    for a in tasks:

        header = header + "<th>" + a.name + "</th>"

        footer = footer + '<th></th>'

        header_size = header_size + 1

    # Add 2 more onto header size. 1 because javascript counts from 0 and
    # another for the total on the end.

    header_size = header_size + 2

    header = header + "<th>Total</th>"

    footer = footer + '<th></th>'

    # -------------

    table = ''

    time_middle = time.time()

    time_total = time_middle - time_start

    # print 'Create Header: ' +str(time_total)

    for p in pilots:

        time_section = time.time()

        # Start New Row

        temp_table = table

        table = table + '<tr>'

        if pilot_type == 'command':

            logs_2000_pilot = flightlogs.filter(pilot_in_command=p)

        elif pilot_type == 'training':

            logs_2000_pilot = flightlogs.filter(
                pilot_in_command_under_supervision=p)

        table = table + '<td>' + p.first_name + " " + p.last_name + '</td>'

        total = 0

        for a in tasks:

            sum_datcon = 0

            logs_2000_task = logs_2000_pilot.filter(task=a)

            #total += logs_2000_task.count()

            sum_datcon = logs_2000_task.aggregate(Sum('datcon'))['datcon__sum']

            # print sum_datcon

            if sum_datcon is None:

                sum_datcon = 0

            total += sum_datcon

            # print a.name + ": " + str(logs_2000_task.count())

            table = table + '<td>' + str(sum_datcon) + '</td>'

        if total == 0:

            table = temp_table

        else:

            table = table + '<td>' + str(total) + '</td>'

        # End Row

        table = table + '</tr>'

        time_middle = time.time()

        time_total = time_middle - time_section

        # print 'Create Row: ' + p.first_name + ' - ' +str(time_total)

        time_total = time_middle - time_start

        # print 'Create Row: ' + p.first_name + ' - ' +str(time_total)

    time_end = time.time()

    time_total = time_end - time_start

    # print 'Total: ' +str(time_total)

    return (header, table, footer, header_size)


# Summary - Training Pilot Task

@login_required
def trainingpilotsummary(request, str_date_to=None, str_date_from=None,
                         aircraft_post=None, pilot_post=None, task_post=None):

    # print '+++++++++++++++'

    #time_start = time.time()
    state = ''

    state_type = ''

    if request.method == 'POST':  # If the form has been submitted...

        # A form bound to the POST data
        drForm = FieldFilterDRForm(request.POST)

        if drForm.is_valid():  # All validation rules pass

            str_date_from = request.POST['date_from']

            str_date_to = request.POST['date_to']

            aircraft_post = drForm.cleaned_data['aircraft']

            pilot_post = drForm.cleaned_data['pilot']

            task_post = drForm.cleaned_data['task']

    # Get Filtered Aircraft Flight Logs

    if str_date_to is None:

        date_to = from_datetime.strptime(
            "30/06/" + str(datetime.date.today().year), "%d/%m/%Y")

    else:

        date_to = from_datetime.strptime(str_date_to, "%d/%m/%Y")

    if str_date_from is None:

        date_from = from_datetime.strptime(
            "01/07/" + str(datetime.date.today().year - 1), "%d/%m/%Y")

    else:

        date_from = from_datetime.strptime(str_date_from, "%d/%m/%Y")

    str_date_to = date_to.strftime("%d/%m/%Y")

    str_date_from = date_from.strftime("%d/%m/%Y")

    table = ''

    logs_2000 = AircraftFlightLogDetail.objects.extra(where=["1=0"])

    aircraft_ids = []
    if aircraft_post is not None:

        logs_2000 = AircraftFlightLogDetail.objects.filter(
            aircraft_flight_log__date__gte=date_from).filter(
            aircraft_flight_log__date__lte=date_to) .filter(
            aircraft_flight_log__aircraft__in=aircraft_post)

        for x in aircraft_post:
            aircraft_ids.append(x.id)

    pilot_ids = []
    if pilot_post is not None:

        for p in pilot_post:

            pilot_ids.append(p.id)

    task_ids = []
    if task_post is not None:

        for a in task_post:

            task_ids.append(a.id)

    data = {
        'date_to': str_date_to,
        'date_from': str_date_from,
        'aircraft': aircraft_ids,
        'pilot': pilot_ids,
        'task': task_ids}

    drForm = FieldFilterDRForm(data)

    if date_from < date_to:

        if len(aircraft_ids) == 0 or len(pilot_ids) == 0 or len(task_ids) == 0:

            header = ''

            table = ''

            footer = ''

            header_size = 0

            state = 'Please select a minimum of 1 item from each select list.'

            state_type = 'Warning'

        else:

            header, table, footer, header_size = createSummaryPilotHTML(
                pilot_post, task_post, logs_2000, 'training')

    else:
        header = ''

        table = ''

        footer = ''

        header_size = 0

        state = 'Date From must be less than Date To'

        state_type = 'Warning'

    #time_end = time.time()

    #time_total = time_end - time_start

    # print 'Total Time: ' +str(time_total)

    return render_to_response(
        "summarytrainingpilot.html",
        {
            'pagetitle': 'Datcon Pilot in Command Under Supervision Summary',
            'table': table,
            'drForm': drForm,
            'header': header,
            'footer': footer,
            'header_size': header_size,
            "state": state,
            "state_type": state_type},
        context_instance=RequestContext(request))


# Summary - Time

@login_required
def timesummary(request):

    state = ''
    state_type = ''

    aircraft_post = []

    task_post = []

    pilot_post = []

    if request.method == 'POST':  # If the form has been submitted...

        drForm = FieldFilterForm(request.POST)  # A form bound to the POST data

        if drForm.is_valid():  # All validation rules pass

            aircraft_post = drForm.cleaned_data['aircraft']

            task_post = drForm.cleaned_data['task']

            pilot_post = drForm.cleaned_data['pilot']

    aircraft_ids = []

    task_ids = []

    pilot_ids = []

    for x in aircraft_post:

        aircraft_ids.append(int(x.id))

    for x in task_post:

        task_ids.append(int(x.id))

    for x in pilot_post:

        pilot_ids.append(int(x.id))

    flightlogs = AircraftFlightLogDetail.objects.extra(where=["1=0"])

    if len(aircraft_ids) == 0 or len(pilot_ids) == 0 or len(task_ids) == 0:

        header = ''

        table = ''

        footer = ''

        header_size = 0

        state = 'Please select a minimum of 1 item from each select list.'

        state_type = 'Warning'

    else:

        flightlogs = AircraftFlightLogDetail.objects.filter(
            aircraft_flight_log__aircraft__in=aircraft_ids)
        flightlogs = flightlogs.filter(task__in=task_ids)
        flightlogs = flightlogs.filter(Q(pilot_in_command__in=pilot_ids) | Q(
            pilot_in_command_under_supervision__in=pilot_ids))
        go = 1

        # Create Month Array [(1,'Jan')

        month_choices = []

        for i in range(7, 13):

            month_choices.append((i, datetime.date(2008, i, 1).strftime('%b')))

        for i in range(1, 7):

            month_choices.append((i, datetime.date(2008, i, 1).strftime('%b')))

        footer = '<th></th>'

        # Create Table Header with Months

        header = ''

        header += '<th>Year</th>'

        for month in month_choices:

            header += '<th>' + month[1] + '</th>'

            footer = footer + '<th></th>'

        header += '<th>Total</th>'

        footer = footer + '<th></th>'

        table = ''

        if flightlogs:

            # print len(flightlogs)

            # Determine start and finish date for years

            maxYear = flightlogs.aggregate(Max('aircraft_flight_log__date'))[
                'aircraft_flight_log__date__max'].year

            minYear = flightlogs.aggregate(Min('aircraft_flight_log__date'))[
                'aircraft_flight_log__date__min'].year

            # print maxYear

            # print minYear

            # Create Table with Sum of months

            year = minYear - 1

            while year <= maxYear:

                # print 'Row: ' + str(year)

                table = table + '<tr>'

                total = 0

                table += '<td>' + str(year) + '/' + str(year + 1) + '</td>'

                # July to Dec

                fl_year = flightlogs.filter(
                    aircraft_flight_log__date__year=year)

                # print len(fl_year)

                counter = 0

                while counter < 6:

                    fl_month = fl_year.filter(
                        aircraft_flight_log__date__month=month_choices[counter][0])

                    sum_datcon = fl_month.aggregate(
                        Sum('datcon'))['datcon__sum']

                    # print str(year) + " : " + str(month_choices[counter][0])
                    # + " : " + str(sum_datcon)

                    if sum_datcon is None:

                        sum_datcon = 0

                    table = table + '<td>' + str(sum_datcon) + '</td>'

                    total += sum_datcon

                    counter += 1

                # Jan to June

                fl_year = flightlogs.filter(
                    aircraft_flight_log__date__year=year + 1)

                # print len(fl_year)

                while counter < 12:

                    fl_month = fl_year.filter(
                        aircraft_flight_log__date__month=month_choices[counter][0])

                    sum_datcon = fl_month.aggregate(
                        Sum('datcon'))['datcon__sum']

                    # print str(year) + " : " + str(month_choices[counter][0])
                    # + " : " + str(sum_datcon)

                    if sum_datcon is None:

                        sum_datcon = 0

                    table = table + '<td>' + str(sum_datcon) + '</td>'

                    total += sum_datcon

                    counter += 1

                table = table + '<td>' + str(total) + '</td>'

                table = table + '</tr>'

                year += 1

    default_data = {
        'aircraft': aircraft_ids,
        'task': task_ids,
        'pilot': pilot_ids}

    drForm = FieldFilterForm(default_data)

    return render_to_response("summarytime.html",
                              {'pagetitle': 'Datcon Time Summary',
                               'table': table,
                               'header': header,
                               'footer': footer,
                               'drForm': drForm,
                               'state': state,
                               'state_type': state_type},
                              context_instance=RequestContext(request))


def createSummaryAircraftHTML(flightlogs, aircraft_post, task_post):

    # print flightlogs

    task = task_post.order_by("name")

    # ----- Create Header Row --------

    header = '<th style="width: 80px;">Aircraft</th>'

    footer = '<th></th>'

    header_size = 0

    for a in task:

        header = header + "<th>" + a.name + "</th>"

        footer = footer + '<th></th>'

        header_size = header_size + 1

    header = header + "<th>Total</th>"

    footer = footer + '<th></th>'

    # -------------

    table = ''

    for ac in aircraft_post:

        # Start New Row

        temp_table = table

        table = table + '<tr>'

        logs_2000_aircraft = flightlogs.filter(
            aircraft_flight_log__aircraft=ac)

        table = table + '<td>' + ac.name + '</td>'

        total = 0

        for a in task:

            sum_datcon = 0

            logs_2000_task = logs_2000_aircraft.filter(task=a)

            sum_datcon = logs_2000_task.aggregate(Sum('datcon'))['datcon__sum']

            if sum_datcon is None:

                sum_datcon = 0

            total += sum_datcon

            # print a.name + ": " + str(logs_2000_task.count())

            table = table + '<td>' + str(sum_datcon) + '</td>'

        if total == 0:

            table = temp_table

            #table = table + '<td>'+ str(total) + '</td>'

        else:

            table = table + '<td>' + str(total) + '</td>'

        # End Row

        table = table + '</tr>'

    # add 2, 1 because javascript starts at 0 and 1 for the total column

    header_size = header_size + 2

    return (header, table, footer, header_size)


# Summary - Aircraft Task

@login_required
def aircraftsummary(request, str_date_to=None, str_date_from=None):

    pilot_post = []

    task_post = []

    aircraft_post = []

    pilot_ids = []
    aircraft_ids = []
    task_ids = []

    if request.method == 'POST':  # If the form has been submitted...

        # A form bound to the POST data
        drForm = FieldFilterDRForm(request.POST)

        if drForm.is_valid():  # All validation rules pass

            str_date_from = request.POST['date_from']

            str_date_to = request.POST['date_to']

            #aircraft_post = request.POST['aircraft']

            pilot_post = drForm.cleaned_data['pilot']

            task_post = drForm.cleaned_data['task']

            aircraft_post = drForm.cleaned_data['aircraft']

    # Get Filtered Aircraft Flight Logs

    if str_date_to is None:

        date_to = from_datetime.strptime(
            "30/06/" + str(datetime.date.today().year), "%d/%m/%Y")

    else:

        date_to = from_datetime.strptime(str_date_to, "%d/%m/%Y")

    if str_date_from is None:

        date_from = from_datetime.strptime(
            "01/07/" + str(datetime.date.today().year - 1), "%d/%m/%Y")

    else:

        date_from = from_datetime.strptime(str_date_from, "%d/%m/%Y")

    str_date_to = date_to.strftime("%d/%m/%Y")

    str_date_from = date_from.strftime("%d/%m/%Y")

    if date_from > date_to:
        header = ''

        table = ''

        footer = ''

        header_size = 0

        state = 'Date From must be less than Date To'

        state_type = 'Warning'

    else:

        logs_2000 = AircraftFlightLogDetail.objects.extra(where=["1=0"])

        for x in pilot_post:

            pilot_ids.append(x.id)

        for x in aircraft_post:

            aircraft_ids.append(x.id)

        for x in task_post:

            task_ids.append(x.id)

        '''

        logs_2000 = AircraftFlightLogDetail.objects.filter(aircraft_flight_log__date__gte=date_from).filter(aircraft_flight_log__date__lte=date_to) \

        .filter(Q(pilot_in_command__in = pilot_post) | Q(pilot_in_command_under_supervision__in = pilot_post) | \

        Q(task__in = task_post) | Q(aircraft_flight_log__aircraft__in = aircraft_post) )

        '''

        logs_2000 = AircraftFlightLogDetail.objects.filter(
            aircraft_flight_log__date__gte=date_from).filter(
            aircraft_flight_log__date__lte=date_to) .filter(
            Q(
                pilot_in_command__in=pilot_ids) | Q(
                    pilot_in_command_under_supervision__in=pilot_ids))

        if len(aircraft_ids) == 0 or len(pilot_ids) == 0 or len(task_ids) == 0:

            header = ''

            table = ''

            footer = ''

            header_size = 0

            state = 'Please select a minimum of 1 item from each select list.'

            state_type = 'Warning'

        else:

            #header, table, footer, header_size = createSummaryPilotHTML(pilot_post, task_post, logs_2000, 'command')

            header, table, footer, header_size = createSummaryAircraftHTML(
                logs_2000, aircraft_post, task_post)

            state = ''

            state_type = ''

    data = {
        'date_to': str_date_to,
        'date_from': str_date_from,
        'pilot': pilot_ids,
        'aircraft': aircraft_ids,
        'task': task_ids}

    drForm = FieldFilterDRForm(data)

    #header, table, footer, header_size = createSummaryAircraftHTML(logs_2000, aircraft, task)

    return render_to_response("summaryaircraft.html",
                              {'pagetitle': 'Datcon Aircraft Summary',
                               'table': table,
                               'drForm': drForm,
                               'header': header,
                               'footer': footer,
                               'header_size': header_size,
                               "state": state,
                               "state_type": state_type},
                              context_instance=RequestContext(request))


# Summary - Command Pilot Task

@login_required
def commandpilotsummary(request, str_date_to=None, str_date_from=None,
                        aircraft_post=None, pilot_post=None, task_post=None):

    # print '+++++++++++++++'

    #time_start = time.time()

    if request.method == 'POST':  # If the form has been submitted...

        # A form bound to the POST data
        drForm = FieldFilterDRForm(request.POST)

        if drForm.is_valid():  # All validation rules pass

            str_date_from = request.POST['date_from']

            str_date_to = request.POST['date_to']

            aircraft_post = drForm.cleaned_data['aircraft']

            pilot_post = drForm.cleaned_data['pilot']

            task_post = drForm.cleaned_data['task']

    # Get Filtered Aircraft Flight Logs

    if str_date_to is None:

        date_to = from_datetime.strptime(
            "30/06/" + str(datetime.date.today().year), "%d/%m/%Y")

    else:

        date_to = from_datetime.strptime(str_date_to, "%d/%m/%Y")

    if str_date_from is None:

        date_from = from_datetime.strptime(
            "01/07/" + str(datetime.date.today().year - 1), "%d/%m/%Y")

    else:

        date_from = from_datetime.strptime(str_date_from, "%d/%m/%Y")

    str_date_to = date_to.strftime("%d/%m/%Y")

    str_date_from = date_from.strftime("%d/%m/%Y")

    table = ''

    logs_2000 = AircraftFlightLogDetail.objects.extra(where=["1=0"])

    aircraft_ids = []

    if aircraft_post is not None:

        logs_2000 = AircraftFlightLogDetail.objects.filter(
            aircraft_flight_log__date__gte=date_from).filter(
            aircraft_flight_log__date__lte=date_to) .filter(
            aircraft_flight_log__aircraft__in=aircraft_post)

        for x in aircraft_post:

            aircraft_ids.append(x.id)

    pilot_ids = []

    if pilot_post is not None:

        for p in pilot_post:

            pilot_ids.append(p.id)

    task_ids = []

    if task_post is not None:

        for a in task_post:

            task_ids.append(a.id)

    data = {
        'date_to': str_date_to,
        'date_from': str_date_from,
        'aircraft': aircraft_ids,
        'pilot': pilot_ids,
        'task': task_ids}

    drForm = FieldFilterDRForm(data)

    state = ''

    state_type = ''

    if date_from < date_to:

        if len(aircraft_ids) == 0 or len(pilot_ids) == 0 or len(task_ids) == 0:

            header = ''

            table = ''

            footer = ''

            header_size = 0

            state = 'Please select a minimum of 1 item from each select list.'

            state_type = 'Warning'

        else:

            header, table, footer, header_size = createSummaryPilotHTML(
                pilot_post, task_post, logs_2000, 'command')

    else:
        header = ''

        table = ''

        footer = ''

        header_size = 0

        state = 'Date From must be less than Date To'

        state_type = 'Warning'

    #time_end = time.time()

    #time_total = time_end - time_start

    # print 'Total Time: ' +str(time_total)

    return render_to_response("summarycommandpilot.html",
                              {'pagetitle': 'Datcon Pilot in Command Summary',
                               'table': table,
                               'drForm': drForm,
                               'header': header,
                               'footer': footer,
                               'header_size': header_size,
                               "state": state,
                               "state_type": state_type},
                              context_instance=RequestContext(request))


# Pilots

@login_required
def pilotlist(request, state='', state_type=''):

    queryset = Pilot.objects.all()

    # return object_list(request, queryset = queryset, template_name =
    # 'pilotlist.html', extra_context={'title':'Pilot List','pagetitle':'Pilot
    # List', 'state':state, 'state_type':state_type}) depracated

    view = ListView.as_view(template_name='pilotlist.html', queryset=queryset)
    return view(
        request,
        extra_context={
            'title': 'Pilot List',
            'pagetitle': 'Pilot List',
            'state': state,
            'state_type': state_type})


@login_required
def pilotadd(request):

    state = ''

    state_type = ''

    # print request.user

    if request.method == 'POST':

        form = PilotForm(data=request.POST)

        if form.is_valid():

            new_pilot = form.save(commit=False)

            new_pilot.creator = request.user

            new_pilot.modifer = request.user

            new_pilot.save()

            return redirect('pilotlist_saved')

        else:

            state = 'Warning - Pilot not valid'

            state_type = 'Warning'

    # return create_object(request, template_name = 'lookupadd.html',
    # form_class = PilotForm, extra_context={'pagetitle':'Add
    # Pilot','title':'Add Pilot','state':state, 'state_type':state_type})
    # depracated

    view = CreateView.as_view(
        template_name='lookupadd.html',
        form_class=PilotForm)
    return view(
        request,
        extra_context={
            'pagetitle': 'Add Pilot',
            'title': 'Add Pilot',
            'state': state,
            'state_type': state_type})


class PilotUpdate(UpdateView):
    # look at
    # https:/ccbv.co.uk/projects/Django/1.4/django.views.generic.edit.UpdateView/

    state = ''

    state_type = ''

    model = Pilot

    form_class = PilotForm

    template_name = 'lookupupdate.html'

    extra_context = {
        'pagetitle': 'Update Pilot',
        'title': 'Update Pilot',
        'state': state,
        'state_type': state_type}

    def get_success_url(self):
        return reverse('pilotlist_saved')

    def get_context_data(self, **kwargs):
        context = super(PilotUpdate, self).get_context_data(**kwargs)
        context.update(self.extra_context)

        return context

    def form_invalid(self, form):

        state = 'Warning - Pilot not valid'

        state_type = 'Warning'

        return self.render_to_response(self.get_context_data(form=form))


@login_required
def pilotupdate(request, id):

    state = ''

    state_type = ''

    pilot = Pilot.objects.get(id=id)

    if request.method == 'POST':

        form = PilotForm(data=request.POST, instance=pilot)

        if form.is_valid():

            new_pilot = form.save(commit=False)

            new_pilot.creator = request.user

            new_pilot.modifer = request.user

            new_pilot.save()

            return redirect('pilotlist_saved')

        else:

            state = 'Warning - Pilot not valid'

            state_type = 'Warning'

    # return update_object(request, object_id = id, model = Pilot,
    # template_name = 'lookupupdate.html', form_class = PilotForm,
    # extra_context={'pagetitle':'Update Pilot','title':'Update
    # Pilot','state':state, 'state_type':state_type}) depracated


# Aircraft

@login_required
def aircraftlist(request, state='', state_type=''):

    queryset = Aircraft.objects.all()

    # return object_list(request, queryset = queryset, template_name =
    # 'lookuplist.html', extra_context={'title':'Aircraft List',
    # 'state':state, 'state_type':state_type,'pagetitle':'Aircraft List'})
    # depracated

    view = ListView.as_view(template_name='lookuplist.html', queryset=queryset)
    return view(
        request,
        extra_context={
            'title': 'Aircraft List',
            'state': state,
            'state_type': state_type,
            'pagetitle': 'Aircraft List'})


@login_required
def aircraftadd(request):

    # print request.user

    state = ''

    state_type = ''

    if request.method == 'POST':

        form = AircraftForm(data=request.POST)

        if form.is_valid():

            new_aircraft = form.save(commit=False)

            new_aircraft.creator = request.user

            new_aircraft.modifer = request.user

            new_aircraft.save()

            return redirect('aircraftlist_saved')

        else:

            state = 'Warning - Aircraft not valid'

            state_type = 'Warning'

    # return create_object(request, template_name = 'lookupadd.html',
    # form_class = AircraftForm, extra_context={'title':'Add Aircraft',
    # 'state':state, 'state_type':state_type, 'pagetitle':'Add Aircraft'})
    # depracated

    view = CreateView.as_view(
        template_name='lookupadd.html',
        form_class=AircraftForm)
    return view(
        request,
        extra_context={
            'title': 'Add Aircraft',
            'state': state,
            'state_type': state_type,
            'pagetitle': 'Add Aircraft'})


class AircraftUpdate(UpdateView):
    # look at
    # https:/ccbv.co.uk/projects/Django/1.4/django.views.generic.edit.UpdateView/

    state = ''

    state_type = ''

    model = Aircraft

    form_class = AircraftForm

    template_name = 'lookupupdate.html'

    extra_context = {
        'pagetitle': 'Update Aircraft',
        'title': 'Update Aircraft',
        'state': state,
        'state_type': state_type}

    def get_success_url(self):
        return reverse('aircraftlist_saved')

    def get_context_data(self, **kwargs):
        context = super(AircraftUpdate, self).get_context_data(**kwargs)
        context.update(self.extra_context)

        return context

    def form_invalid(self, form):

        state = 'Warning - Aircraft not valid'

        state_type = 'Warning'

        return self.render_to_response(self.get_context_data(form=form))


@login_required
def aircraftupdate(request, id):

    state = ''

    state_type = ''

    aircraft = Aircraft.objects.get(id=id)

    if request.method == 'POST':

        form = AircraftForm(data=request.POST, instance=aircraft)

        if form.is_valid():

            new_aircraft = form.save(commit=False)

            new_aircraft.creator = request.user

            new_aircraft.modifer = request.user

            new_aircraft.save()

            return redirect('aircraftlist_saved')

        else:

            state = 'Warning - Aircraft not valid'

            state_type = 'Warning'

    # return update_object(request, object_id = id, model = Aircraft,
    # template_name = 'lookupupdate.html', form_class = AircraftForm,
    # extra_context={'pagetitle':'Update Aircraft','title':'Update Aircraft',
    # 'state':state, 'state_type':state_type}) depracated

    view = UpdateView.as_view(
        template_name='lookupupdate.html',
        form_class=AircraftForm)
    return view(
        request,
        object_id=id,
        model=Aircraft,
        extra_context={
            'pagetitle': 'Update Aircraft',
            'title': 'Update Aircraft',
            'state': state,
            'state_type': state_type})


# Task

@login_required
def tasklist(request, state='', state_type=''):

    queryset = Task.objects.all()

    # return object_list(request, queryset = queryset, template_name =
    # 'lookuplist.html', extra_context={'pagetitle':'Task List','title':'Task
    # List','pagetitle':'Task List', 'state':state, 'state_type':state_type,})
    # depracated

    view = ListView.as_view(template_name='lookuplist.html', queryset=queryset)
    return view(
        request,
        extra_context={
            'pagetitle': 'Task List',
            'title': 'Task List',
            'pagetitle': 'Task List',
            'state': state,
            'state_type': state_type,
        })


@login_required
def taskadd(request):

    # print request.user

    state = ''

    state_type = ''

    if request.method == 'POST':

        form = TaskForm(data=request.POST)

        if form.is_valid():

            new_task = form.save(commit=False)

            new_task.creator = request.user

            new_task.modifer = request.user

            new_task.save()

            return redirect('tasklist_saved')

        else:

            state = 'Warning - Task not valid'

            state_type = 'Warning'

    # return create_object(request, template_name = 'lookupadd.html',
    # form_class = TaskForm, extra_context={'pagetitle':'Add
    # Task','title':'Add Task', 'state':state, 'state_type':state_type})
    # depracated

    view = CreateView.as_view(
        template_name='lookupadd.html',
        form_class=TaskForm)
    return view(
        request,
        extra_context={
            'pagetitle': 'Add Task',
            'title': 'Add Task',
            'state': state,
            'state_type': state_type})


class TaskUpdate(UpdateView):
    # look at
    # https:/ccbv.co.uk/projects/Django/1.4/django.views.generic.edit.UpdateView/

    state = ''

    state_type = ''

    model = Task

    form_class = TaskForm

    template_name = 'lookupupdate.html'

    extra_context = {
        'pagetitle': 'Task Update',
        'title': 'Update Task',
        'state': state,
        'state_type': state_type}

    def get_success_url(self):
        return reverse('tasklist_saved')

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context.update(self.extra_context)

        return context

    def form_invalid(self, form):

        state = 'Warning - Task not valid'

        state_type = 'Warning'

        return self.render_to_response(self.get_context_data(form=form))


@login_required
def taskupdate(request, pk):

    state = ''

    state_type = ''

    task = Task.objects.get(id=pk)

    if request.method == 'POST':

        form = TaskForm(data=request.POST, instance=task)

        if form.is_valid():

            new_task = form.save(commit=False)

            new_task.creator = request.user

            new_task.modifer = request.user

            new_task.save()

            return redirect('tasklist_saved')

        else:

            state = 'Warning - Task not valid'

            state_type = 'Warning'

    # return update_object(request, object_id = id, model = Task,
    # template_name = 'lookupupdate.html', form_class = TaskForm,
    # extra_context={'pagetitle':'Task Update','title':'Update Task',
    # 'state':state, 'state_type':state_type}) depracated

# look at
# https:/ccbv.co.uk/projects/Django/1.4/django.views.generic.edit.UpdateView/


# Aircraft Flight Log Report - Detailed

@login_required
@csrf_protect
def aircraftflightloglistdetailed(
        request, str_date_to=None, str_date_from=None):
    # print '-------------------'
    time_start = time.time()
    # print 'time start: ' + str(time_start)

    aircraft = ''
    aircraft_ids = []
    task = ''
    task_ids = []
    pilot = ''
    pilot_ids = []
    flight_log_number = ''
    fire_number = ''
    job_number = ''

    if request.method == 'POST':  # If the form has been submitted...
        # drForm = DateRangeForm(request.POST) # A form bound to the POST data

        # A form bound to the POST data
        drForm = FlightLogFieldSearch(request.POST)
        # FlightLogFieldSearch
        if drForm.is_valid():  # All validation rules pass

            str_date_from = request.POST['date_from']
            str_date_to = request.POST['date_to']
            aircraft = drForm.cleaned_data['aircraft']
            task = drForm.cleaned_data['task']
            pilot = drForm.cleaned_data['pilot']
            flight_log_number = request.POST['flight_log_number']
            fire_number = request.POST['fire_number']
            job_number = request.POST['job_number']

            for a in aircraft:
                aircraft_ids.append(a.id)
            for t in task:
                task_ids.append(t.id)
            for p in pilot:
                pilot_ids.append(p.id)

    else:
        aircraft_qs = Aircraft.objects.all()
        for a in aircraft_qs:
            aircraft_ids.append(a.id)
        task_qs = Task.objects.all()
        for t in task_qs:
            task_ids.append(t.id)
        pilot_qs = Pilot.objects.all()
        for p in pilot_qs:
            pilot_ids.append(p.id)

    # Create Headers for Table

    table = ''

    # Get Filtered Aircraft Flight Logs

    if str_date_to is None:

        date_to = datetime.date.today()

    else:

        date_to = from_datetime.strptime(str_date_to, "%d/%m/%Y")

    if str_date_from is None:

        diff = datetime.timedelta(days=7)

        date_from = datetime.date.today() - diff

    else:

        date_from = from_datetime.strptime(str_date_from, "%d/%m/%Y")

    str_date_to = date_to.strftime("%d/%m/%Y")

    str_date_from = date_from.strftime("%d/%m/%Y")

    data = {
        'date_to': str_date_to,
        'date_from': str_date_from,
        'aircraft': aircraft_ids,
        'task': task_ids,
        'pilot': pilot_ids,
        'flight_log_number': flight_log_number,
        'fire_number': fire_number,
        'job_number': job_number}

    drForm = FlightLogFieldSearch(data)

    # Filter on Flight Log Fields
    queryset = AircraftFlightLog.objects.filter(
        date__gte=date_from).filter(
        date__lte=date_to)
    queryset = queryset.filter(aircraft__in=aircraft_ids)
    if len(flight_log_number) != 0:
        # print flight_log_number
        queryset = queryset.filter(
            flight_log_number__icontains=flight_log_number)

    # Fitler on Flight Log Detail Fields

    queryset_details = AircraftFlightLogDetail.objects.filter(
        aircraft_flight_log__in=queryset)
    if len(fire_number) != 0:
        queryset_details = queryset_details.filter(
            fire_number__icontains=fire_number)
    if len(job_number) != 0:
        queryset_details = queryset_details.filter(
            job_number__icontains=job_number)
    queryset_details = queryset_details.filter(task__in=task_ids)
    queryset_details = queryset_details.filter(Q(pilot_in_command__in=pilot_ids) | Q(
        pilot_in_command_under_supervision__in=pilot_ids))

    '''
    queryset_details = AircraftFlightLogDetail.objects.filter(aircraft_flight_log__in=queryset)
    kwargs = {}
    if len(fire_number) != 0:
        kwargs['fire_number__icontains'] = fire_number
    if len(job_number) != 0:
        kwargs['job_number__icontains'] = job_number
    kwargs['task__in'] = task_ids
    args = ( Q(pilot_in_command__in = pilot_ids) | Q(pilot_in_command_under_supervision__in = pilot_ids), )
    queryset_details = queryset_details.filter(*args, **kwargs)
    '''

    # Cycle Through Flight Logs

    for detail in queryset_details:

        # Start Row

        table = table + '<tr>'

        # Aircraft Flgiht Log

        table = table + '<td>' + '<a href="' + str(detail.aircraft_flight_log.get_absolute_url(
        )) + '">' + str(detail.aircraft_flight_log.flight_log_number) + '</a>' + '</td>'

        # Date

        table = table + '<td>' + \
            str(detail.aircraft_flight_log.date.strftime("%d/%m/%Y")) + '</td>'

        # Aircraft

        table = table + '<td>' + \
            str(detail.aircraft_flight_log.aircraft.name) + '</td>'

        # FDI

        fdi = detail.aircraft_flight_log.fire_danger_index

        if fdi is None:

            table = table + '<td></td>'

        else:

            table = table + '<td>' + str(fdi) + '</td>'

        # Datcon

        datcon = detail.datcon

        if datcon is None:
            datcon_sum = '0'

        table = table + '<td>' + str(datcon) + '</td>'

        # WST Out

        time_out = detail.time_out.strftime("%H:%M")

        table = table + '<td>' + time_out + '</td>'

        # Task
        table = table + '<td>' + detail.task.name + '</td>'

        # Fuel Added
        fuel_added = detail.fuel_added
        if fuel_added is None:
            fuel_added = ''
        table = table + '<td>' + str(fuel_added) + '</td>'

        # Landings
        landings = detail.landings
        if landings is None:
            landings = ''
        table = table + '<td>' + str(landings) + '</td>'

        # Fire Number
        fire_number = detail.fire_number
        if fire_number is None:
            fire_number = ''
        table = table + '<td>' + fire_number + '</td>'

        # Job Number
        job_number = detail.job_number
        if job_number is None:
            job_number = ''
        table = table + '<td>' + job_number + '</td>'

        # Pilot in Command
        pilot_in_command = detail.pilot_in_command.first_name + \
            ' ' + detail.pilot_in_command.last_name
        table = table + '<td>' + pilot_in_command + '</td>'

        # Pilot in Command Under Super
        try:
            pilot_in_command_under_supervision = detail.pilot_in_command_under_supervision.first_name + \
                ' ' + detail.pilot_in_command_under_supervision.last_name
            table = table + '<td>' + pilot_in_command_under_supervision + '</td>'
        except:
            table = table + '<td>' + '' + '</td>'

        # End Row
        table = table + '</tr>'

    state = ''
    state_type = ''

    if date_from > date_to:
        state = 'Date From must be less than Date To'
        state_type = 'Warning'

    time_finish = time.time()
    # print 'time finish: ' + str(time_finish)
    total_time = time_finish - time_start
    # print 'total time: ' + str(total_time)

    return render_to_response('aircraftflightloglistdetailed.html',
                              {'table': table,
                               'drForm': drForm,
                               'state': state,
                               'state_type': state_type,
                               'pagetitle': 'Aircraft Flight Log Report - Detailed'},
                              context_instance=RequestContext(request))


# Aircraft Flight Log Report - Summary

@login_required
@csrf_protect
def aircraftflightloglist(request, str_date_to=None, str_date_from=None):
    aircraft = ''
    aircraft_ids = []
    task = ''
    task_ids = []
    pilot = ''
    pilot_ids = []
    flight_log_number = ''
    fire_number = ''
    job_number = ''

    if request.method == 'POST':  # If the form has been submitted...
        # drForm = DateRangeForm(request.POST) # A form bound to the POST data

        # A form bound to the POST data
        drForm = FlightLogFieldSearch(request.POST)
        # FlightLogFieldSearch
        if drForm.is_valid():  # All validation rules pass

            str_date_from = request.POST['date_from']
            str_date_to = request.POST['date_to']
            aircraft = drForm.cleaned_data['aircraft']
            task = drForm.cleaned_data['task']
            pilot = drForm.cleaned_data['pilot']
            flight_log_number = request.POST['flight_log_number']
            fire_number = request.POST['fire_number']
            job_number = request.POST['job_number']

            for a in aircraft:
                aircraft_ids.append(a.id)
            for t in task:
                task_ids.append(t.id)
            for p in pilot:
                pilot_ids.append(p.id)

    else:
        aircraft_qs = Aircraft.objects.all()
        for a in aircraft_qs:
            aircraft_ids.append(a.id)
        task_qs = Task.objects.all()
        for t in task_qs:
            task_ids.append(t.id)
        pilot_qs = Pilot.objects.all()
        for p in pilot_qs:
            pilot_ids.append(p.id)

    # Create Headers for Table

    table = ''

    # Get Filtered Aircraft Flight Logs

    if str_date_to is None:

        date_to = datetime.date.today()

    else:

        date_to = from_datetime.strptime(str_date_to, "%d/%m/%Y")

    if str_date_from is None:

        diff = datetime.timedelta(days=7)

        date_from = datetime.date.today() - diff

    else:

        date_from = from_datetime.strptime(str_date_from, "%d/%m/%Y")

    str_date_to = date_to.strftime("%d/%m/%Y")

    str_date_from = date_from.strftime("%d/%m/%Y")

    # print 'ADSAA##$'

    data = {
        'date_to': str_date_to,
        'date_from': str_date_from,
        'aircraft': aircraft_ids,
        'task': task_ids,
        'pilot': pilot_ids,
        'flight_log_number': flight_log_number,
        'fire_number': fire_number,
        'job_number': job_number}

    drForm = FlightLogFieldSearch(data)

    # Filter on Flight Log Fields
    queryset = AircraftFlightLog.objects.filter(
        date__gte=date_from).filter(
        date__lte=date_to)
    queryset = queryset.filter(aircraft__in=aircraft_ids)
    if len(flight_log_number) != 0:
        # print flight_log_number
        queryset = queryset.filter(
            flight_log_number__icontains=flight_log_number)

    flight_ids_master = []
    for y in queryset:
        flight_ids_master.append(y.id)
    # Fitler on Flight Log Detail Fields
    queryset_details = AircraftFlightLogDetail.objects.filter(
        aircraft_flight_log__in=queryset)

    flight_ids_detail = []
    for y in queryset_details:
        flight_ids_detail.append(y.aircraft_flight_log_id)

    s = set(flight_ids_detail)
    # gets difference between 2 lists. flight_ids_master - flight_ids_detail.
    # Get list of flight logs without detail children
    no_detail_logs = [x for x in flight_ids_master if x not in s]
    # print 'difference'
    # print no_detail_logs

    if len(fire_number) != 0:
        queryset_details = queryset_details.filter(
            fire_number__icontains=fire_number)
        no_detail_logs = []
    if len(job_number) != 0:
        queryset_details = queryset_details.filter(
            job_number__icontains=job_number)
        no_detail_logs = []

    task_total = Task.objects.all()
    if len(task_ids) != len(task_total):
        no_detail_logs = []
    queryset_details = queryset_details.filter(task__in=task_ids)

    pilot_total = Pilot.objects.all()
    if len(pilot_ids) != len(pilot_total):
        no_detail_logs = []
    queryset_details = queryset_details.filter(Q(pilot_in_command__in=pilot_ids) | Q(
        pilot_in_command_under_supervision__in=pilot_ids))

    flight_ids = []
    for y in queryset_details:
        flight_ids.append(y.aircraft_flight_log_id)

    flight_ids.extend(no_detail_logs)

    queryset = queryset.filter(id__in=flight_ids)

    # Cycle Through Flight Logs

    for flightlog in queryset:

        # Start Row

        table = table + '<tr>'

        # Aircraft Flgiht Log

        table = table + '<td>' + '<a href="' + \
            str(flightlog.get_absolute_url()) + '">' + \
            str(flightlog.flight_log_number) + '</a>' + '</td>'

        # Date

        table = table + '<td>' + \
            str(flightlog.date.strftime("%d/%m/%Y")) + '</td>'

        # WST Out

        job_num = None

        if flightlog.aircraftflightlogdetail_set.all():

            details = flightlog.aircraftflightlogdetail_set.all().order_by('time_out')

            # print details[0].time_out.strftime("%H:%M")

            table = table + '<td>' + \
                details[0].time_out.strftime("%H:%M") + '</td>'

            job_num = details[0].job_number

            #table = table + '<td>' + str(details[0].time_out) + '</td>'

        else:
            table = table + '<td></td>'

        # Aircraft

        table = table + '<td>' + str(flightlog.aircraft.name) + '</td>'

        # VDO Time

        datcon_sum = flightlog.aircraftflightlogdetail_set.all().aggregate(Sum('datcon'))

        datcon_sum = datcon_sum['datcon__sum']

        if datcon_sum is None:
            datcon_sum = '0'

        table = table + '<td>' + str(datcon_sum) + '</td>'

        # Job Number

        if job_num is None:

            table = table + '<td></td>'

        else:

            table = table + '<td>' + job_num + '</td>'

        #Pilot in Command

        if flightlog.aircraftflightlogdetail_set.all():

            details = flightlog.aircraftflightlogdetail_set.all().order_by('time_out')

            table = table + '<td>' + \
                details[0].pilot_in_command.first_name + ' ' + \
                details[0].pilot_in_command.last_name + '</td>'

            if details[0].pilot_in_command_under_supervision:
                table = table + '<td>' + details[0].pilot_in_command_under_supervision.first_name + ' ' + details[
                    0].pilot_in_command_under_supervision.last_name + '</td>'

            else:
                table = table + '<td></td>'

            '''

            if details[0].task: table = table + '<td>' + details[0].task.name + '</td>'

            else: table = table + '<td></td>'

            '''

            if details[0].task:
                table = table + '<td>' + details[0].task.name + '</td>'

            else:
                table = table + '<td></td>'

            '''

            if details[0].activity_type: table = table + '<td>' + details[0].activity_type.name + '</td>'

            else: table = table + '<td></td>'

            '''

        else:

            table = table + '<td></td>'

            table = table + '<td></td>'

            table = table + '<td></td>'

        # End Row

        table = table + '</tr>'

    state = ''
    state_type = ''

    if date_from > date_to:
        state = 'Date From must be less than Date To'
        state_type = 'Warning'

    return render_to_response('aircraftflightloglist.html',
                              {'table': table,
                               'drForm': drForm,
                               'state': state,
                               'state_type': state_type,
                               'pagetitle': 'Aircraft Flight Log Report'},
                              context_instance=RequestContext(request))


@login_required
def aircraftflightlogadd(request):

    # print request.user

    state = ''

    state_type = ''

    if request.method == 'POST':

        form = AircraftFlightLogForm(data=request.POST)

        if form.is_valid():

            new_aircraftflightlog = form.save(commit=False)

            new_aircraftflightlog.creator = request.user

            new_aircraftflightlog.modifer = request.user

            new_aircraftflightlog.save()

            # print new_aircraftflightlog.id

            state = 'Saved'

            state_type = 'OK'

            return redirect(reverse('aircraftflightlog_saved',
                                    kwargs={'id': new_aircraftflightlog.id}))

        else:

            state = 'Warning - Flight Log is not valid.'

            state_type = 'Warning'

    # return create_object(request, template_name =
    # 'aircraftflightlogadd.html', form_class = AircraftFlightLogForm,
    # extra_context ={'state':state,'state_type':state_type,'pagetitle':'Add
    # Aircraft Flight Log'}) depracated

    view = CreateView.as_view(
        template_name='aircraftflightlogadd.html',
        form_class=AircraftFlightLogForm)
    return view(
        request,
        extra_context={
            'state': state,
            'state_type': state_type,
            'pagetitle': 'Add Aircraft Flight Log'})


@login_required
@csrf_protect
def aircraftflightlogdetailsadd(request, id, state='', state_type=''):

    # print request.user

    #state = ''

    #state_type = ''

    flightlog = AircraftFlightLog.objects.get(pk=id)
    # filter the select lists

    flightlogdetails = flightlog.aircraftflightlogdetail_set.all()

    # aircraft select list equals all active aicraft + aircraft that are
    # already selected.

    try:
        aircraft_array = []
        aircraft_array.append(flightlog.aircraft_id)
        aircraft_qs = Aircraft.objects.filter(id__in=aircraft_array)
        aircraft_qs = aircraft_qs | Aircraft.objects.filter(
            effective_to__exact=None)

    except IndexError as e:

        # Default list of no child records found
        aircraft_qs = Aircraft.objects.filter(effective_to__exact=None)

    # task select list equals all active tasks + inactive tasks that are
    # already selected.

    try:

        task_array = []

        for detail in flightlogdetails:

            task_array.append(detail.task_id)

        task_qs = Task.objects.filter(id__in=task_array)

        task_qs = task_qs | Task.objects.filter(effective_to__exact=None)

    except IndexError as e:

        # Default list of no child records found

        task_qs = Task.objects.filter(effective_to__exact=None)

    # pilot in command select list equals all active tasks + inactive tasks
    # that are already selected.

    try:

        pilot_array = []

        for detail in flightlogdetails:

            pilot_array.append(detail.pilot_in_command_id)

        pilot_qs = Pilot.objects.filter(id__in=pilot_array)

        pilot_qs = pilot_qs | Pilot.objects.filter(effective_to__exact=None)

    except IndexError as e:

        # Default list of no child records found

        pilot_qs = Pilot.objects.filter(effective_to__exact=None)

    # pilot in command select list equals all active tasks + inactive tasks
    # that are already selected.

    try:

        pilot_array = []

        for detail in flightlogdetails:

            pilot_array.append(detail.pilot_in_command_under_supervision_id)

        pilot_under_qs = Pilot.objects.filter(id__in=pilot_array)

        pilot_under_qs = pilot_under_qs | Pilot.objects.filter(
            effective_to__exact=None)

    except IndexError as e:

        # Default list of no child records found

        pilot_qs = Pilot.objects.filter(effective_to__exact=None)

    form_master = AircraftFlightLogForm(instance=flightlog)

    # Overrides Form Defaults
    form_master.fields['aircraft'].queryset = aircraft_qs

    # Make Form

    details_form = AircraftFlightLogDetailForm

    # Overrides Form Defaults

    details_form.declared_fields['task'] = forms.ModelChoiceField(
        queryset=task_qs,
        empty_label="",
        widget=forms.Select(
            attrs={
                'class': 'chzn-select-task',
                'style': 'width:200px',
            }))

    details_form.declared_fields['pilot_in_command'] = forms.ModelChoiceField(
        queryset=pilot_qs,
        empty_label="",
        widget=forms.Select(
            attrs={
                'class': 'chzn-select-command',
                'style': 'width:200px',
            }))

    details_form.declared_fields['pilot_in_command_under_supervision'] = forms.ModelChoiceField(
        queryset=pilot_under_qs,
        empty_label="",
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'chzn-select-super',
                'style': 'width:200px',
            }))

    print "-=-=-=---=-=-=-=-=-"

    FlightLogDetailInlineFormSet = inlineformset_factory(
        AircraftFlightLog, AircraftFlightLogDetail, extra=6, exclude=(
            'creator', 'modifier'), can_delete=False, form=details_form)

    if request.method == 'POST':

        form = AircraftFlightLogForm(data=request.POST, instance=flightlog)

        formset = FlightLogDetailInlineFormSet(
            request.POST, request.FILES, instance=flightlog)

        #formset = FlightLogDetailInlineFormSet(request.POST)

        if form.is_valid():

            new_aircraftflightlog = form.save(commit=False)

            new_aircraftflightlog.creator = request.user

            new_aircraftflightlog.modifer = request.user

            # print formset

            # print 'HHHHHHHHHHHH'
            if formset.is_valid():
                #instances = formset.save(commit=False)
                # for f in formset:
                # print 'Datcon' + str(f['datcon'])

                return_time_last = 0
                counter = 1
                error = 0
                for f in formset:
                    # print 'Datcon' + str(f['datcon'])
                    if error == 0:
                        datcon_html = str(f['datcon'])
                        datcon_array = datcon_html.split("\"")
                        if len(datcon_array) == 11:
                            datcon = datcon_array[7]
                            # print 'datcon: ' + datcon
                            try:
                                datcon_hour = int(datcon.split(".")[0])
                            except:
                                datcon = "0" + datcon
                                datcon_hour = int(datcon.split(".")[0])
                            datcon_24h = datcon_hour * 60
                            try:
                                datcon_minute = int(datcon.split(".")[1])
                            except:
                                datcon_minute = 0
                            datcon_min = datcon_minute * 6
                            total_datcon_minutes = datcon_24h + datcon_min

                            # print 'time Out' + str(f['time_out'])
                            timeout_html = str(f['time_out'])
                            timeout_array = timeout_html.split("\"")
                            # if len(timeout_array) == 13:
                            timeout_str = timeout_array[5]
                            if len(timeout_str) == 4:
                                timeout_hh = int(timeout_str[:2])
                                timeout_mm = int(timeout_str[2:])
                            else:
                                timeout_hh = int(timeout_str[:1])
                                timeout_mm = int(timeout_str[1:])
                            #timeout_int = int(timeout_str)

                            timeout_total_minutes = (
                                int(timeout_hh) * 60) + int(timeout_mm)

                            return_time_minutes = total_datcon_minutes + timeout_total_minutes
                            '''
                            print 'datcon: ' + str(datcon)
                            print 'datcon in minutes: ' + str(total_datcon_minutes)
                            print 'time out: ' + str(timeout_str)
                            print 'time out in minutes: ' + str(timeout_total_minutes)
                            print 'return time in minutes: ' + str(return_time_minutes)
                            print 'return time last: ' + str(return_time_last)
                            '''
                            if return_time_last > timeout_total_minutes:
                                state = 'Warning (Rows ' + str(counter - 1) + ", " + str(
                                    counter) + ') - Aircraft leaving before it has returned. See Datcon and Time Out.'

                                state_type = 'Warning'

                                error = 1

                            return_time_last = return_time_minutes
                            counter = counter + 1
                            # f.save()

                if error == 0:

                    new_aircraftflightlog.save()
                    formset.save()
                    state = 'Saved'
                    state_type = 'OK'

                    formset = FlightLogDetailInlineFormSet(instance=flightlog)
                    form = form_master
            else:
                state = 'Warning - Flight Log Details are not valid.'
                state_type = 'Warning'

        else:

            state = 'Warning - Flight Log is not valid.'

            state_type = 'Warning'

        # return
        # render_to_response('aircraftflightlogdetailsadd.html',{"formset":
        # formset,"form":form}, context_instance=RequestContext(request))

    else:

        #state = ''

        #state_type = ''

        formset = FlightLogDetailInlineFormSet(instance=flightlog)

        form = form_master
        #form = AircraftFlightLogForm(instance=flightlog)

    return render_to_response("aircraftflightlogdetailsadd.html",
                              {"formset": formset,
                               "form": form,
                               "state": state,
                               "state_type": state_type,
                               'pagetitle': 'Aircraft Flight Log Details'},
                              context_instance=RequestContext(request))


@login_required
# Duty Time
@login_required
@csrf_protect
def dutytimeadd(request):

    # print '+++++++++++++++'

    time_start = time.time()

    state = ''

    state_type = ''

    pilots = Pilot.objects.filter(
        effective_to__exact=None).order_by('last_name')

    table = ''

    # print 'pilots'

    # print pilots

    for pilot in pilots:

        # print "Pilot Name: " + pilot.first_name

        # print "Pilot ID: " + str(pilot.id)

        table += '<tr>'

        table += '<td>'

        try:

            table += '<a href="' + \
                str(pilot.dutytime_set.all()[0].get_absolute_url()) + '">'

            table += '<input type="image" src="/static/img/page_white_edit.png" name="edit" width="24" height="24" alt="Edit">'

            table += '</a>'

        except IndexError as e:

            table += '<img type="image" src="/static/img/cross.png" name="edit" width="24" height="24" alt="No Duty Time Records">'

        table += '</td>'

        table += '<td>'

        try:

            table += '<a href="../' + str(pilot.id) + '/hours">'

            table += '<input type="image" src="/static/img/page_white_edit.png" name="edit" width="24" height="24" alt="Edit">'

            table += '</a>'

        except IndexError as e:

            table += '<img type="image" src="/static/img/cross.png" name="edit" width="24" height="24" alt="No Duty Time Records">'

        table += '</td>'

        table += '<td style="text-align:center" >'

        table += '<input type="radio" name="rdio" value="' + \
            str(pilot.id) + '">'

        table += '</td>'

        table += '<td>'

        table += str(pilot.first_name)

        table += '</td>'

        table += '<td>'

        table += pilot.last_name

        table += '</td>'

        table += '<td id="date_' + str(pilot.id) + '">'

        # print '---------'

        try:

            dt_date = pilot.dutytime_set.order_by(
                '-date')[0].date.strftime("%d/%m/%Y")

            # print dt_date

        except IndexError as e:

            # print  pilot.first_name + ' ' + pilot.last_name + ' has no Last
            # Date.'

            dt_date = ''

        table += dt_date

        table += '</td>'

        table += '</tr>'

    if request.method == 'POST':

        # Validate Dates

        # print '^^^^^^^^^^^^^^^^^^^^^'

        # print request.POST['pilot_id']

        # Check if pilot id is sent back

        if request.POST['pilot_id'] != '':

            pilot = Pilot.objects.get(id=int(request.POST['pilot_id']))

            # print pilot

            # print pilot.id

            # Check if both dates have been chosen

            if request.POST['date_from'] != '' and request.POST[
                    'date_to'] != '':

                date_from = from_datetime.strptime(
                    request.POST['date_from'], "%d/%m/%Y")

                date_to = from_datetime.strptime(
                    request.POST['date_to'], "%d/%m/%Y")

                # print date_from

                # print date_to

                # Check date range is valid

                if date_to >= date_from:

                    # Make one day

                    oneday = datetime.timedelta(days=1)

                    # While date_change is less than date_to - create day
                    # records

                    date_change = date_from

                    while (date_change <= date_to):

                        # print date_change

                        dt = DutyTime(date=date_change, pilot=pilot)

                        dt.creator = request.user

                        dt.modifer = request.user

                        dt.save()

                        date_change = date_change + oneday

                        # print date_change

                    state = 'Saved'

                    state_type = 'OK'

                    return redirect(
                        reverse(
                            'dutytimeaddset_saved',
                            kwargs={
                                'id': pilot.id}))

            else:

                # No dates. Send user message.

                state = 'Warning - Enter values for both date fields'

                state_type = 'Warning'

        else:

            # No pilot id. Send user message.

            state = "Warning - No pilot selected"

            state_type = "Warning"

    drForm = DateRangeForm()

    time_end = time.time()

    time_total = time_end - time_start

    # print 'Total Time: ' +str(time_total)

    return render_to_response("dutytimeadd.html",
                              {'pagetitle': 'Duty Times',
                               "drForm": drForm,
                               'pilots': table,
                               "state": state,
                               "state_type": state_type},
                              context_instance=RequestContext(request))


@login_required
@csrf_protect
def dutytimeaddset(request, id, str_date_to=None,
                   str_date_from=None, state='', state_type=''):

    time_start = time.time()

    state = ''
    state_type = ''

    pilot = Pilot.objects.get(pk=id)

    name = pilot.first_name + ' ' + pilot.last_name

    # inlineformset

    DutyTimeInlineFormSet = inlineformset_factory(Pilot, DutyTime, exclude=(
        'creator', 'modifier'), can_delete=False, form=DutyTimeForm, extra=0)

    #dt_formset = formset_factory(DutyTimeForm, extra=2)

    # Do this if something submitted

    if request.method == "POST":

        # ^^^^^^^^^^^^^^^
        time_mid = time.time()

        time_total = time_mid - time_start

        # print "enter post: " + str(time_total)

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # if duty times are saved do this

        if request.POST['type'] == 'Save':
            # print request.POST
            formset = DutyTimeInlineFormSet(
                request.POST, request.FILES, instance=pilot)
            #formset = DutyTimeInlineFormSet(request.POST, request.FILES)
            # print formset

            # ^^^^^^^^^^^^^^^
            time_mid = time.time()

            time_total = time_mid - time_start

            # print "after formset get: " + str(time_total)

            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            if len(formset) == 0:

                date_to = pilot.dutytime_set.order_by('-date')[0].date

                # get date using last entered date - 14 days

                date_from = date_to - timedelta(days=13)

                # Create formset

                sort = 'A'

                state = 'Warning - No Records Submitted To Save'

                state_type = 'Warning'

            else:

                # ^^^^^^^^^^^^^^^
                time_mid = time.time()

                time_total = time_mid - time_start

                # print "Before Date Range: " + str(time_total)

                # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                formsetstring = str(formset)

                formsetdates = re.findall(r"\d{2}/\d{2}/\d{4}", formsetstring)

                date_from = from_datetime.strptime("01/01/2050", "%d/%m/%Y")

                date_to = from_datetime.strptime("01/01/1900", "%d/%m/%Y")

                for formdate in formsetdates:

                    thedate = from_datetime.strptime(formdate, "%d/%m/%Y")

                    if thedate > date_to:
                        date_to = thedate

                    if thedate < date_from:
                        date_from = thedate

                # ^^^^^^^^^^^^^^^
                time_mid = time.time()

                time_total = time_mid - time_start

                # print "After Date Range: " + str(time_total)

                # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                try:

                    if from_datetime.strptime(
                            formsetdates[0], "%d/%m/%Y") > from_datetime.strptime(formsetdates[1], "%d/%m/%Y"):

                        sort = 'D'

                    else:

                        sort = 'A'

                except:

                    sort = 'A'

                # ^^^^^^^^^^^^^^^
                time_mid = time.time()

                time_total = time_mid - time_start

                # print "After Order Calc: " + str(time_total)

                # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                if formset.is_valid():
                    error = 0
                    counter = 0
                    for f in formset:
                        counter = counter + 1
                        ontime = str(f['datetime_on_first'])
                        offtime = str(f['datetime_off_first'])

                        thedate = str(f['date'])

                        # print thedate

                        day = thedate.split("\"")[3]

                        ontime_arr = ontime.split("\"")
                        offtime_arr = offtime.split("\"")

                        if len(ontime_arr) == 11 and len(offtime_arr) == 11:
                            ontime = int(ontime_arr[7])
                            offtime = int(offtime_arr[7])

                            if ontime >= offtime:
                                state = 'Warning - Duty Time is not valid (' + \
                                    day + '). Time On must be less than Time Off'

                                state_type = 'Warning'

                                error = 1

                        elif len(ontime_arr) == 11 and len(offtime_arr) == 9:

                            state = 'Warning - Duty Time is not valid (' + \
                                day + '). Missing Time Off value.'

                            state_type = 'Warning'

                            error = 1

                        elif len(ontime_arr) == 9 and len(offtime_arr) == 11:

                            state = 'Warning - Duty Time is not valid (' + \
                                day + '). Missing Time On value.'

                            state_type = 'Warning'

                            error = 1

                    # print "Counter (rows): " + str(counter)
                    if error == 0:
                        formset.save()

                        state = 'Saved'

                        state_type = 'OK'

                    # ^^^^^^^^^^^^^^^
                    time_mid = time.time()

                    time_total = time_mid - time_start

                    # print "After Formset Saved: " + str(time_total)

                    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                else:

                    state = 'Warning - Duty Time is not valid.'

                    state_type = 'Warning'

        # if date filter submitted do this

        elif request.POST['type'] == 'Go':

            drForm = DateRangeForm(request.POST)

            # print 'Date Range Submitted'

            if drForm.is_valid():  # All validation rules pass

                # get date from POST

                str_date_from = request.POST['date_from']

                str_date_to = request.POST['date_to']

                # convert date from string to date object

                date_from = from_datetime.strptime(str_date_from, "%d/%m/%Y")

                date_to = from_datetime.strptime(str_date_to, "%d/%m/%Y")

                sort = request.POST['sort']

                if sort == 'A':
                    order = 'date'

                if sort == 'D':
                    order = '-date'

                #formset = DutyTimeInlineFormSet(instance=pilot, queryset=DutyTime.objects.filter(date__gte=date_from).filter(date__lte=date_to.order_by(order)))

                formset = DutyTimeInlineFormSet(
                    instance=pilot, queryset=DutyTime.objects.filter(
                        date__gte=date_from).filter(
                        date__lte=date_to).order_by(order))

                state = 'Duty Times Sorted'

                state_type = 'OK'

            else:

                state = 'Warning - Sorting Failed'

                state_type = 'Warning'

    # Do this if nothing submitted

    else:

        # do default date query here

        # get the last entered date for the pilot

        date_to = pilot.dutytime_set.order_by('-date')[0].date

        # get date using alst entered date - 14 days

        date_from = date_to - timedelta(days=13)

        # Create formset

        sort = 'A'

        #formset = DutyTimeInlineFormSet(instance=pilot, queryset=DutyTime.objects.filter(date__gte=date_from).filter(date__lte=date_to.order_by('-date')))

        formset = DutyTimeInlineFormSet(
            instance=pilot, queryset=DutyTime.objects.filter(
                date__gte=date_from).filter(
                date__lte=date_to).order_by('date'))

    # convert dates to strings

    str_date_to = date_to.strftime("%d/%m/%Y")

    str_date_from = date_from.strftime("%d/%m/%Y")

    # make dictionary to put in form

    data = {'date_to': str_date_to, 'date_from': str_date_from, 'sort': sort}

    # Create form

    drForm = DateRangeSortForm(data)

    if date_from > date_to:
        state = 'Date From must be less than Date To'
        state_type = 'Warning'

    time_end = time.time()

    time_total = time_end - time_start

    # print "total time: " + str(time_total)

    return render_to_response("dutytimeaddset.html",
                              {'pagetitle': 'Edit Duty Times / ' + name,
                               "formset": formset,
                               'state': state,
                               'state_type': state_type,
                               "name": name,
                               "drForm": drForm},
                              context_instance=RequestContext(request))


@login_required
@csrf_protect
def dutytimehours(request, id, str_date_to=None,
                  str_date_from=None, str_start_point=None):

    # print '+++++++++++++++'

    time_start = time.time()

    pilot = Pilot.objects.get(pk=id)

    name = pilot.first_name + ' ' + pilot.last_name

    # ------- Change to date filtered. Takes too long to get all

    flightlogs_command = pilot.pilot_in_command.all()

    # ------- Change to date filtered. Takes too long to get all

    flightlogs_supervised = pilot.aircraftflightlogdetail_set.all()

    if request.method == 'POST':  # If the form has been submitted...

        drForm = DateRangeForm(request.POST)  # A form bound to the POST data

        if drForm.is_valid():  # All validation rules pass

            str_date_from = request.POST['date_from']

            str_date_to = request.POST['date_to']

            str_start_point = request.POST['start_point']

    # Create Headers for Table

    table = ''

    # Get Filtered Aircraft Flight Logs

    if str_date_to is None:

        date_to = from_datetime.today()

    else:

        date_to = from_datetime.strptime(str_date_to, "%d/%m/%Y")

    if str_date_from is None:

        diff = datetime.timedelta(days=59)

        date_from = from_datetime.today() - diff

    else:

        date_from = from_datetime.strptime(str_date_from, "%d/%m/%Y")

    if str_start_point is None:

        start_point = from_datetime.strptime("15/01/2011", "%d/%m/%Y")

    else:

        start_point = from_datetime.strptime(str_start_point, "%d/%m/%Y")

    date_from = date_from.date()

    date_to = date_to.date()

    start_point = start_point.date()

    str_date_to = date_to.strftime("%d/%m/%Y")

    str_date_from = date_from.strftime("%d/%m/%Y")

    str_start_point = start_point.strftime("%d/%m/%Y")

    data = {
        'date_to': str_date_to,
        'date_from': str_date_from,
        'start_point': str_start_point}

    drForm = DutyRangeForm(data)

    dutytimes = pilot.dutytime_set.filter(
        date__gt=(
            date_from -
            datetime.timedelta(
                days=365))).filter(
        date__lte=date_to).order_by('date')

    # Look thoughs each dutytime

    counter = 0

    date_counter = date_from - datetime.timedelta(days=365)

    # print 'date_from: ' + str(date_from)

    # print 'date_to: ' + str(date_to)

    this_total = 0

    dutytime_arr = []

    datcon_arr = []

    while date_counter <= date_to:

        # print '###'

        if date_counter >= date_from:

            time_section_start = time.time()

            # print date_counter

            # Start Row

            table += '<tr>'

            # Pilot

            table += '<td>'

            table += name

            table += '</td>'

            # Date

            table += '<td>'

            table += date_counter.strftime("%d/%m/%Y")

            table += '</td>'

            date_diff = start_point - date_counter

            int_diff = int(date_diff.days)

            '''

            if int_diff % 28 == 0:

                day = date_counter.strftime("%A") + ' (7 + 14 + 28 Day Reset)'

            elif int_diff % 14 == 0:

                day = date_counter.strftime("%A") + ' (7 + 14 Day Reset)'

            elif int_diff % 7 == 0:

                day = date_counter.strftime("%A") + ' (7 Day Reset)'

            else

                day = date_counter.strftime("%A")

            '''

            if int_diff % 7 == 0:

                day = date_counter.strftime("%A") + ' (7 Day Reset)'

                if int_diff % 14 == 0:

                    day = date_counter.strftime("%A") + ' (7/14 Day Reset)'

                    if int_diff % 28 == 0:

                        day = date_counter.strftime(
                            "%A") + ' (7/14/28 Day Reset)'

            else:

                day = date_counter.strftime("%A")

            table += '<td>'

            table += day

            table += '</td>'

            time_section_2_start = time.time()

            # get a duty time record if there is one

            try:

                dtime = dutytimes.filter(date=date_counter)[0]

            except IndexError as e:

                # print 'IndexError'

                dtime = None

            if dtime:

                # Date On

                table += '<td>'

                if dtime.datetime_on_first:
                    table += dtime.datetime_on_first.strftime("%H:%M")

                table += '</td>'

                # Date Off

                table += '<td>'

                if dtime.datetime_off_first:
                    table += dtime.datetime_off_first.strftime("%H:%M")

                table += '</td>'

                #

                if dtime.datetime_on_first:

                    on_hour = dtime.datetime_on_first.hour

                    on_min = float(dtime.datetime_on_first.minute)

                    on_min = on_min / 60

                    # print on_min

                    on_time = float(on_hour) + on_min

                # print str(on_time)

                    if dtime.datetime_off_first:

                        off_hour = dtime.datetime_off_first.hour

                        off_min = float(dtime.datetime_off_first.minute)

                        off_min = off_min / 60

                        # print off_min

                        off_time = float(off_hour) + off_min

                        # print off_time

                        diff = 0.0

                        diff = off_time - on_time
                        diff = round(diff, 1)

                    else:

                        diff = 0.00

                else:

                    diff = 0.00

                dutytime_arr.append(diff)

                # Daily Total

                table += '<td>'
                table += str("%.1f" % diff)
                #table+= str(diff)

                table += '</td>'

            else:

                # Date On

                table += '<td>'

                table += ''

                table += '</td>'

                # Date Off

                table += '<td>'

                table += ''

                table += '</td>'

                # Daily

                table += '<td>'

                table += '0.00'

                table += '</td>'

                dutytime_arr.append(0)

            # 7 Days

            date_diff = start_point - date_counter

            int_diff = int(date_diff.days)

            mod_diff = int_diff % 7

            mod_changed = (7 - mod_diff)

            arr_slice = (mod_changed + 1) * -1

            if arr_slice == -8:

                arr_slice = -1

            table += '<td>'
            table += str("%.1f" % sum(dutytime_arr[arr_slice:]))
            #table+= str(sum(dutytime_arr[arr_slice:]))
            table += '</td>'

            # 14 Days

            date_diff = start_point - date_counter

            int_diff = int(date_diff.days)

            mod_diff = int_diff % 14

            mod_changed = (14 - mod_diff)

            arr_slice = (mod_changed + 1) * -1

            if arr_slice == -15:

                arr_slice = -1

            table += '<td>'

            table += str("%.1f" % sum(dutytime_arr[arr_slice:]))

            table += '</td>'

            # 28 Days

            date_diff = start_point - date_counter

            int_diff = int(date_diff.days)

            mod_diff = int_diff % 28

            mod_changed = (28 - mod_diff)

            arr_slice = (mod_changed + 1) * -1

            if arr_slice == -29:

                arr_slice = -1

            table += '<td>'

            table += str("%.1f" % sum(dutytime_arr[arr_slice:]))

            table += '</td>'

            # Travel

            dtime = dutytimes.filter(date=date_counter)

            travel = '0'

            if dtime.count() > 0:

                if dtime[0].travel_km:
                    travel = str(dtime[0].travel_km)

            table += '<td>'

            table += travel

            table += '</td>'

            # Daily

            # Command

            flightlogs_comm = flightlogs_command.filter(
                aircraft_flight_log__date=date_counter)

            time_total_comm = 0.0

            time_total_super = 0.0

            if flightlogs_comm.count() > 0:

                # print flightlogs_comm

                for f in flightlogs_comm:

                    # print 'command time: ' +  str(f.datcon)

                    time_total_comm += float(f.datcon)

                # print 'time total: ' + str(time_total)

            # Supervised

            flightlogs_super = flightlogs_supervised.filter(
                aircraft_flight_log__date=date_counter)

            if flightlogs_super.count() > 0:

                # print flightlogs_super

                for f in flightlogs_super:

                    # print 'super time: ' +  str(f.datcon)

                    time_total_super += float(f.datcon)

            time_total_both = time_total_comm + time_total_super

            datcon_arr.append(time_total_both)

            table += '<td>'

            table += str("%.1f" % time_total_both)

            table += '</td>'

            # 7 Day

            # Command

            # seven_days

            table += '<td>'

            table += str(sum(datcon_arr[-7:]))

            table += '</td>'

            # 30 Days

            table += '<td>'

            table += str(sum(datcon_arr[-30:]))

            table += '</td>'

            # 365 Day

            table += '<td>'

            table += str(sum(datcon_arr[-365:]))

            table += '</td>'

            # WST Out

            flightlogs_comm = flightlogs_command.filter(
                aircraft_flight_log__date=date_counter)

            flightlogs_super = flightlogs_supervised.filter(
                aircraft_flight_log__date=date_counter)

            wst_time = ''

            flight_time = 0.0

            if flightlogs_comm.count() > 0 and flightlogs_super.count() > 0:

                min_time = flightlogs_comm[0].time_out

                for fl in flightlogs_comm:

                    new_time = fl.time_out

                    if new_time < min_time:

                        min_time = new_time

                    flight_time += float(fl.datcon)

                for fl in flightlogs_super:

                    new_time = fl.time_out

                    if new_time < min_time:

                        min_time = new_time

                    flight_time += float(fl.datcon)

                wst_time = min_time.strftime("%H:%M")

                flight_time = str("%.1f" % flight_time)

            elif flightlogs_comm.count() > 0:

                min_time = flightlogs_comm[0].time_out

                for fl in flightlogs_comm:

                    new_time = fl.time_out

                    if new_time < min_time:

                        min_time = new_time

                    flight_time += float(fl.datcon)

                flight_time = str("%.1f" % flight_time)

                wst_time = min_time.strftime("%H:%M")

            elif flightlogs_super.count() > 0:

                min_time = flightlogs_super[0].time_out

                for fl in flightlogs_super:

                    new_time = fl.time_out

                    if new_time < min_time:

                        min_time = new_time

                    flight_time += float(fl.datcon)

                wst_time = min_time.strftime("%H:%M")

                flight_time = str("%.1f" % flight_time)

            else:

                flight_time = ''

            # WST Out

            table += '<td>'

            table += wst_time

            table += '</td>'

            # Time - Day Total

            table += '<td>'

            table += flight_time

            table += '</td>'

            # Fuel - Day Total

            table += '<td>'

            table += '0'

            table += '</td>'

            # End Row

            table += '</tr>'

        else:

            # Calc Duty Day Total

            try:

                dtime = dutytimes.filter(date=date_counter)[0]

            except IndexError as e:

                # print 'IndexError'

                dtime = None

            if dtime:

                if dtime.datetime_on_first:

                    on_hour = dtime.datetime_on_first.hour

                    on_min = float(dtime.datetime_on_first.minute)

                    on_min = on_min / 60

                    # print on_min

                    on_time = float(on_hour) + on_min

                # print str(on_time)

                    if dtime.datetime_off_first:

                        off_hour = dtime.datetime_off_first.hour

                        off_min = float(dtime.datetime_off_first.minute)

                        off_min = off_min / 60

                        # print off_min

                        off_time = float(off_hour) + off_min

                        # print off_time

                        diff = 0.00

                        diff = off_time - on_time

                    else:

                        diff = 0.00

                else:

                    diff = 0.00

                x = diff

            else:

                x = 0

            dutytime_arr.append(x)

            # Calc Datcon Daily Total

            flightlogs_comm = flightlogs_command.filter(
                aircraft_flight_log__date=date_counter)

            time_total_comm = 0.0

            time_total_super = 0.0

            if flightlogs_comm.count() > 0:

                # print flightlogs_comm

                for f in flightlogs_comm:

                    # print 'command time: ' +  str(f.datcon)

                    time_total_comm += float(f.datcon)

                # print 'time total: ' + str(time_total)

            # Supervised

            flightlogs_super = flightlogs_supervised.filter(
                aircraft_flight_log__date=date_counter)

            if flightlogs_super.count() > 0:

                # print flightlogs_super

                for f in flightlogs_super:

                    # print 'super time: ' +  str(f.datcon)

                    time_total_super += float(f.datcon)

            time_total_both = time_total_comm + time_total_super

            y = time_total_both

            datcon_arr.append(y)

        date_counter += datetime.timedelta(days=1)

    state = ''
    state_type = ''

    if date_from > date_to:
        state = 'Date From must be less than Date To'
        state_type = 'Warning'

    return render_to_response("dutytimehours.html",
                              {'pagetitle': 'Duty Times + Flights - Report / ' + name,
                               'name': name,
                               'table': table,
                               'drForm': drForm,
                               'state': state,
                               'state_type': state_type},
                              context_instance=RequestContext(request))


# This is required in order for the extra context can be added to the view.

class ExtraContextTemplateView(TemplateView):
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        context = super(
            ExtraContextTemplateView,
            self).get_context_data(
            *args,
            **kwargs)

        if self.extra_context:
            context.update(self.extra_context)
        return context
