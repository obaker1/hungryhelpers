# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView, TemplateView
from mealPlan.forms import mealPlanForm
from mealPlan.models import Post


class mealPlanView(TemplateView):
    template_name = 'mealPlan/index.html'

    def get(self, request):
        form = mealPlanForm()
        posts = Post.objects.all()

        args = {'form': form, 'posts': posts}

        return render(request, self.template_name, args)

    def post(self, request):
        form = mealPlanForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            text = form.cleaned_data['post']
            form = mealPlanForm()

            #return redirect('mealPlan:index')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)