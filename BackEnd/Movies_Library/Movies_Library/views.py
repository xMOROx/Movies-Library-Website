from django.shortcuts import render
from . import firebase_config

CONFIG = firebase_config.get_config()
database = CONFIG["database"]


def home(request):
    day = database.child("Data").child("Day").get().val()
    id = database.child("Data").child("id").get().val()
    projectname = database.child("Data").child("SampleName").get().val()
    return render(
        request, "home.html", {"day": day, "id": id, "projectname": projectname}
    )
