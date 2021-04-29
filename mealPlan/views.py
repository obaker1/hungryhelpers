# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import DetailView, TemplateView
from mealPlan.forms import mealPlanForm
from mealPlan.models import Post


def meal_plan(request):
    form = mealPlanForm()
    # get all content from Post objects
    posts = Post.objects.all()
    # filter to only content for user that is currently logged in
    cur_posts = Post.objects.filter(user=request.user)

    args = {'form': form, 'posts': posts, 'cur_posts': cur_posts}

    return render(request, 'mealPlan/index.html', args)


def ticket_add(request):
    # create post object using content from form and save
    post_text = request.POST['post']
    post = Post(post=post_text, user=request.user)
    post.save()
    return HttpResponseRedirect(reverse('meal_plan'))
    #return HttpResponseRedirect(reverse(mealPlanView.template_name))

'''
class mealPlanView(TemplateView):
    template_name = 'mealPlan/index.html'

    def get(self, request):
        form = mealPlanForm()
        # display all content from Post objects
        posts = Post.objects.all()

        args = {'form': form, 'posts': posts}

        return render(request, self.template_name, args)

    def post(self, request):
        form = mealPlanForm(request.POST)
        if form.is_valid():
            # clean up the form data
            # save the info to be rendered
            post = form.save(commit=False)
            post.user = request.user
            text = form.cleaned_data['post']
            form = mealPlanForm()

            #return redirect('mealPlan/index.html')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)
'''