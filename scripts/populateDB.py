def run():
    from findLocation.models import GoogleMapsResponse, Origin
    from accounts.models import Profile
    from django.contrib.auth.models import User
    import os
    from openpyxl import load_workbook
    LOCATION = 1; DISTANCE = 2; TIME = 3; BUS = 4; SCHOOL = 5; ADDRESS = 6; TIMEFRAME = 7; LATITUDE = 8; LONGITUDE = 9;
    username = "admin"; email = "myemail@test.com"; password = "admin";

    print("Flushing all tables in db.sqlite3")
    os.system("python manage.py flush --noinput")
    print("Running makemigrations...")
    os.system("python manage.py makemigrations")
    print("Running migrate...")
    os.system("python manage.py migrate")

    my_admin = User.objects.create_superuser(username, email, password)
    profile = Profile(user=my_admin, address='', city='', state='', zip='', district='')
    profile.save()
    print("Created superuser account (username: " + username + ", password: " + password + ")")

    newOrigin = Origin(origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213, longitude=-76.7143524)
    newOrigin.save()
    print("Set origin for findLocation")

    file = "Locations.xlsx"
    workbook = load_workbook(filename=file)
    sheet = workbook.active

    for data in sheet.iter_rows(values_only=True):
        newDest = GoogleMapsResponse(location=data[LOCATION], distance=data[DISTANCE],
                                        time=data[TIME], bus=data[BUS], school=data[SCHOOL],
                                        address=data[ADDRESS], timeframe=data[TIMEFRAME],
                                        latitude=data[LATITUDE], longitude=data[LONGITUDE])
        newDest.save()

    print("Added all locations for findLocation")