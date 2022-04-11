# Timeclock-Project-django-graphql
### The project using library:
```
● Python version 3.9
● Django version 4.0.3
● Graphene version 2.1.9
● Graphene-Django version 2.15.0
● Django-GraphQL-JWT version 0.3.4
```

### Create own enviroment & run project
Go to path project, run command:
```
python3 -m venv enviroment_name (giving name)
source enviroment_name/bin/active
cd timeclock
pip install -r requirements.txt
python manage.py runserver
```
#### In case error lib of graphene_django
env/lib/python3.9/site-packages/graphene_django/utils/utils.py", line 6, in <module>from django.utils.encoding import force_text
```
Go to enviroment_folder/graphene_django/utils/utils.py
replace force_text to force_str
```

#### I also uploaded env folder, so pip install (optional) , enable env and runserver
```
python manage.py runserver
```
### Run ClockTestCase (test only clock module)
stand on project folder, then go to test path:
```
cd timeclock
python manage.py test timetable.tests.clockTestCase
```
### It can test with postman
In post-man folder, it has two files enviroment file & endpoint file


### API that was implemented mutations
#### Create User, please change your data in (username, password and email)
+ url: http://localhost:8000/graphql/user
```
mutation createUser {
  createUser(username: "<username>", password: "<password>", email: "<email>") {
    token
    user {
      username,
      email
    }
  }
}
```

#### An obtain, please change your data in (username and password)
+ url: http://localhost:8000/graphql/user
```
mutation loginUser {
  tokenAuth(username: "<username>", password: "<password>") {
    token
    payload
  }
}
```

#### clockIn, please change clockIn value, ex: 2022-04-08 09:30:00
+ url: http://localhost:8000/graphql/clock
```
mutation clockIn {
  clockIn(clockIn: "<clockIn>") {
    clock {
      clockIn,
      user {
        username
      }
    }
  }
}
```

#### clockOut, please change clockOut value, ex: 2022-04-08 18:30:00, need add clockOut bigger than clockIn
+ url: http://localhost:8000/graphql/clock
```
mutation clockOut {
  clockOut(clockOut: <clockOut>) {
    clock {
      clockIn,
      clockOut
      user {
        username
      }
    }
  }
}
```

## For API queries, need add header Authorization: Bearer {{TOKEN}}

### An authenticated, query me
+ url: http://localhost:8000/graphql/user
```
query {
  me {
    username,
    email
  }
}
```

### An authenticated, query currentClock
+ url: http://localhost:8000/graphql/clock
```
query {
  currentClock {
    clock_in,
    clock_out
  }
}
```

### An authenticated, query today is representing numbers of hours worked today
+ url: http://localhost:8000/graphql/clock
```
query {
    clockedHours(clockedHourType:"Today"){
      today
    }
}
```

### An authenticated, query currentWeek is representing numbers of hours worked this week
+ url: http://localhost:8000/graphql/clock
```
query {
    clockedHours(clockedHourType:"currentWeek"){
      currentWeek
    }
}
```

### An authenticated, query currentMonth is representing numbers of hours worked this month
+ url: http://localhost:8000/graphql/clock
```
query {
    clockedHours(clockedHourType:"currentMonth"){
      currentMonth
    }
}
```
