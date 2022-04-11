import json
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
import datetime
from .models import Clock
from django.utils import timezone


class clockTestCase(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/clock"
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="admin", email="example@gmail.com")
        self.user.set_password("123")
        token = get_token(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def test_query_clock_in(self):
        clockInInput = datetime.datetime.now().strftime('%Y-%m-%d') + ' 09:00:00'
        response = self.query(
            '''
            mutation clockIn($clockIn: String!) {
                clockIn(clockIn: $clockIn) {
                    clock {
                        clockIn,
                        clockOut
                        user {
                            username
                        }
                    }
                }
            }
            ''',
            op_name='clockIn',
            variables={'clockIn': clockInInput},
            headers=self.headers
       )
        self.assertResponseNoErrors(response)
    
    # required add clockIn first
    def test_mutation_clock_out_respone_error(self):
        clockOutInput = datetime.datetime.now().strftime('%Y-%m-%d') + ' 18:00:00'
        response = self.query(
            '''
            mutation clockOut($clockOut: String!) {
                clockOut(clockOut: $clockOut) {
                    clock {
                        clockIn,
                        clockOut
                        user {
                            username
                        }
                    }
                }
            }
            ''',
            op_name='clockOut',
            variables={'clockOut': clockOutInput},
            headers=self.headers
        )
        content = json.loads(response.content)
        self.assertEqual(content['errors'][0]['message'], "Please add checkIn first!")

    def test_mutation_clock_out_response_success(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d') + ' 09:00:00'
        clockInInput = timezone.make_aware(datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S"))
        clockOutInput = datetime.datetime.now().strftime('%Y-%m-%d') + ' 18:00:00'
        clock = Clock(
            clock_in=clockInInput,
            user=self.user
        )
        clock.save()
        response = self.query(
            '''
            mutation clockOut($clockOut: String!) {
                clockOut(clockOut: $clockOut) {
                    clock {
                        clockIn,
                        clockOut
                        user {
                            username
                        }
                    }
                }
            }
            ''',
            op_name='clockOut',
            variables={'clockOut': clockOutInput},
            headers=self.headers
        )
        self.assertResponseNoErrors(response)

    def test_query_current_clock(self):
        response = self.query(
            '''
            query currentClock {
                currentClock {
                    clockIn,
                    clockOut
                }
            }
            ''',
            op_name='currentClock',
            headers=self.headers
       )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['currentClock'], None)
    
    def test_query_hours_worked_today(self):
        response = self.query(
            '''
            query clockedHours {
                clockedHours(clockedHourType:"Today") {
                    today
                }
            }
            ''',
            op_name='clockedHours',
            headers=self.headers
        )
        self.assertResponseNoErrors(response)
    
    def test_query_hours_worked_current_week(self):
        response = self.query(
            '''
            query clockedHours {
                clockedHours(clockedHourType:"currentWeek") {
                    currentWeek
                }
            }
            ''',
            op_name='clockedHours',
            headers=self.headers
        )
        self.assertResponseNoErrors(response)

    def test_query_hours_worked_current_month(self):
        response = self.query(
            '''
            query clockedHours {
                clockedHours(clockedHourType:"currentMonth") {
                    currentMonth
                }
            }
            ''',
            op_name='clockedHours',
            headers=self.headers
        )
        self.assertResponseNoErrors(response)
