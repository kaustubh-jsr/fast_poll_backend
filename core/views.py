from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
# Create your views here.

def index(request):
    return JsonResponse({
        'status':'ok'
    },status=200)

@csrf_exempt
def create_poll(request):
    if request.method == "POST":
        try:
            question_text = request.POST["question"]
            choices = json.loads(request.POST['choices'])
            print(question_text)
            print(choices)
            question = Question.objects.create(question_text=question_text)
            for new_choice in choices:
                choice = Choice.objects.create(choice_text=new_choice['title'],question=question,question_choice_id=new_choice['id'])
            return JsonResponse({'status':'ok','message':'Poll created succesfully','pollId':question.id},status=201)
        except:
            return JsonResponse({'status':'failed','message':"Something went wrong."},status=400)
    return JsonResponse({'status':'failed','message':"Bad Request"},status=405)

def get_poll(request):
    if request.method == "GET":
        poll_id = request.GET['pollId']
        # try:
        question = Question.objects.get(pk=poll_id)
        poll = {}
        poll['question'] = question.question_text
        poll['options'] = []
        choices = question.choice_set.all()
        for choice in choices:
            option = {}
            option['opt_id'] = choice.question_choice_id
            option['title'] = choice.choice_text
            option['votes'] = choice.votes
            poll['options'].append(option)
        poll['totalVotes'] = question.total_votes
        return JsonResponse({'status':'ok','message':'Poll retrived succesfully','pollId':question.id,'poll':poll,'isPollExists':True},status=200)
        # except:
        #     return JsonResponse({'status':'failed','message':"Poll does not exist.",'isPollExists':False},status=400)
    return JsonResponse({'status':'failed','message':"Bad Request"},status=405)

@csrf_exempt
def caste_vote(request):
    if request.method == "POST":
        # try:
        question_id = request.POST["pollId"]
        question_choice_id = request.POST["optId"]
        question = Question.objects.get(pk=question_id)
        question.total_votes+=1
        choice = question.choice_set.get(question_choice_id=question_choice_id)
        choice.votes += 1
        choice.save()
        question.save()
        return JsonResponse({'status':'ok','message':'Vote casted successfully','pollId':question.id},status=201)
        # except:
        #     return JsonResponse({'status':'failed','message':"Poll not found"},status=400)
    return JsonResponse({'status':'failed','message':"Bad Request"},status=405)