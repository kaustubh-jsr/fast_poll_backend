from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    total_votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.question_text
    
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question_choice_id = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.choice_text
    

@receiver(post_save,sender=Choice)
def vote_add_handler(instance,created,**kwargs):
    if not created:
        choice = instance
        # try:
        question = choice.question
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
        channel_layer = get_channel_layer()
        data = {
            'pollId':question.id,'poll':poll,'isPollExists':True
        }
        print('prepared data, now performing the async to sync operation to broadcast data')
        try:
            async_to_sync(channel_layer.group_send)(f'poll_results_{question.id}',{
                'type':'poll_results_update',
                'value':data,
            })
        except Exception as e:
            print('Error occured')
            print(e)
        print('broadcast complete, should have called consumers or printed error')