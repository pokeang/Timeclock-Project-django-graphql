from graphene_django import DjangoObjectType
import graphene
from .models import Clock
from user.schema import UserType
from datetime import datetime
from django.utils import timezone


# Make models available to graphene.Field
class ClockType(DjangoObjectType):
    class Meta:
        model = Clock


class ClockedHours(graphene.ObjectType):
    today = graphene.Int()
    currentWeek = graphene.Int()
    currentMonth = graphene.Int()

## Mutation: Create Clock In
# We want to return:
# - The new `clock` entry
class ClockIn(graphene.Mutation):
    clock = graphene.Field(ClockType)

    class Arguments:
        clockIn = graphene.String(required=True)
        id = graphene.ID()

    def mutate(self, info, clockIn):
        user = info.context.user
        clockInDateInput = timezone.make_aware(datetime.strptime(clockIn, "%Y-%m-%d %H:%M:%S"))
        clocked = Clock.objects.filter(user=user, clock_in__date=clockInDateInput)
        
        if clocked:
            raise Exception('This clock-in already added !')

        clock = Clock(
            clock_in=clockInDateInput,
            user=user
        )

        clock.save()
        return ClockIn(clock=clock)

## Mutation: Create Clock Out
# We want to return:
# - The update clock_out to exited clock_in (one user can add only one click_in per day) return `clock` entry
class ClockOut(graphene.Mutation):
    clock = graphene.Field(ClockType)

    class Arguments:
        clockOut = graphene.String(required=True)

    def mutate(self, info, clockOut):
        user = info.context.user
        clockOutDateInput = timezone.make_aware(datetime.strptime(clockOut, "%Y-%m-%d %H:%M:%S"))
        clocked = Clock.objects.filter(user=user, clock_in__date=clockOutDateInput).first()
        if clocked is None:
            raise Exception('Please add checkIn first!')
        else:
            clockedIn = (clocked.clock_in).strftime("%Y-%m-%d %H:%M:%S")
            if (clockOutDateInput.timestamp() <= clocked.clock_in.timestamp()):
                raise Exception('Please add checkout bigger than checkIn: ' + timezone.make_aware(datetime.strptime(clockedIn, "%Y-%m-%d %H:%M:%S")))
            clocked.clock_out=clockOutDateInput
            clocked.save()
            return ClockOut(clock=clocked)

# Finalize creating mutation for schema
class Mutation(graphene.ObjectType):
    clock_in = ClockIn.Field()
    clock_out = ClockOut.Field()


## Query
class Query(graphene.ObjectType):
    currentClock = graphene.Field(ClockType)
    clockedHours = graphene.Field(ClockedHours, clockedHourType=graphene.String())

    def resolve_currentClock(self, info):
        user = info.context.user
        # Check to to ensure you're signed-in to see yourself
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        today = timezone.now()
        clock = Clock.objects.filter(user=user, clock_in__date=today).first()
        if clock:
            return clock
        else:
            return None

    def resolve_clockedHours(self, info, clockedHourType):
        user_id = info.context.user.id
        user = info.context.user
        # Check to to ensure you're signed-in to see yourself
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        workedInToday = 0
        workedInCurrentWeek = 0
        workedInCurrentMonth = 0
        if clockedHourType == 'Today':
            sqlToday = '''SELECT id, ((julianday(clock_out) - julianday(clock_in)) * 24) as today
            FROM timetable where user_id=%s AND strftime('%%Y-%%m-%%d', clock_in) = strftime('%%Y-%%m-%%d', date('now'))'''
            clockedToday = Clock.objects.raw(sqlToday, [user_id])
            if clockedToday:
                workedInToday = int(clockedToday[0].today)

        if clockedHourType == 'currentWeek':
            sqlCurrentWeek = '''SELECT id, sum((julianday(clock_out) - julianday(clock_in)) * 24) as currentWeek
            FROM timetable where user_id=%s
            AND DATE(clock_in) >= DATE('now', 'weekday 0', '-7 days')'''
            clockedCurrentWeek = Clock.objects.raw(sqlCurrentWeek, [user_id])
            if (clockedCurrentWeek[0].currentWeek is not None):
                workedInCurrentWeek = int(clockedCurrentWeek[0].currentWeek)

        if clockedHourType == 'currentMonth':
            sqlCurrentMonth = '''SELECT id, sum((julianday(clock_out) - julianday(clock_in)) * 24) as currentMonth
            FROM timetable where user_id=%s
            AND strftime('%%Y', clock_in) = strftime('%%Y',date('now'))
            AND strftime('%%m', clock_in) = strftime('%%m', date('now'))'''
            clockedCurrentMonth = Clock.objects.raw(sqlCurrentMonth, [user_id])
            if clockedCurrentMonth[0].currentMonth is not None:
                workedInCurrentMonth = int(clockedCurrentMonth[0].currentMonth)

        clock = ClockedHours(today=workedInToday, currentWeek=workedInCurrentWeek, currentMonth=workedInCurrentMonth)
        return clock
# Create schema
schema = graphene.Schema(query=Query, mutation=Mutation)
