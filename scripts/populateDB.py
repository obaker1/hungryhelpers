def run():
    from findLocation.models import GoogleMapsResponse, Origin
    from accounts.models import Profile
    from django.contrib.auth.models import User
    import xlrd, os
    LOCATION = 0; DISTANCE = 1; TIME = 2; BUS = 3; SCHOOL = 4; ADDRESS = 5; TIMEFRAME = 6; LATITUDE = 7; LONGITUDE = 8;
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
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_index(0)

    for row in range(worksheet.nrows):
        data = []
        for col in range(1, worksheet.ncols):
           data.append(worksheet.cell_value(row, col))
        #print(data)
        newDest = GoogleMapsResponse(location=data[LOCATION], distance=data[DISTANCE],
                                     time=data[TIME], bus=data[BUS], school=data[SCHOOL],
                                     address=data[ADDRESS], timeframe=data[TIMEFRAME],
                                     latitude=data[LATITUDE], longitude=data[LONGITUDE])
        newDest.save()
    print("Added all locations for findLocation")