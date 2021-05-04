def run():
    import os

    print("Running findLocation tests...")
    os.system("python manage.py test findLocation")
    print("Running notifs tests...")
    os.system("python manage.py test notifs")
    print("Running accounts tests...")
    os.system("python manage.py test accounts")
    print("Running mealPlan tests...")
    os.system("python manage.py test mealPlan")