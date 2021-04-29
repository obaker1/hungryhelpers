from django.shortcuts import render
from accounts.models import Student


def staffPage(request):
    theMeal= ["Chicken, Rice, and Vegetables", "No", "Yes", "Yes" , "Yes", "Yes", "No", "No", "No", "Yes"]
    students = Student.objects.all()
    conflicts = []
    for i in students:
        newConflict = [i.first_name]
        if i.allergic_celiac == "Yes" and theMeal[1] == "No":
            newConflict.append("Celiac allergy Conflict")
        if i.allergic_shellfish == "Yes" and theMeal[2] == "No":
            newConflict.append("Shellfish allergy Conflict")
        if i.allergic_lactose == "Yes" and theMeal[3] == "No":
            newConflict.append("Lactose allergy Conflict")
        if i.preference_halal == "Yes" and theMeal[5] == "No":
            newConflict.append("Halal Conflict")
        if i.preference_kosher== "Yes" and theMeal[5] == "No":
            newConflict.append("Kosher Conflict")
        if i.preference_vegetarian == "Yes" and theMeal[6] == "No":
            newConflict.append("Vegetarian Conflict")
        if len(newConflict) > 1:
            conflicts.append(newConflict)
    print(conflicts)
    context={'theMeal': theMeal,
             'students': conflicts}
    return render(request, 'mealPlan/choosemeal.html', context)

