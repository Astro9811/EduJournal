from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
	'''The home page for EduJournal'''
	return render(request, 'edujournals/index.html')

@login_required
def topics(request):
	'''Show all topics'''
	topics = Topic.objects.filter(owner = request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'edujournals/topics.html', context)

@login_required	
def topic(request, topic_id):
	'''Show a single topic and all its entries.'''
	topic = Topic.objects.get(id = topic_id)
	check_topic_owner(topic, request)
	
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'edujournals/topic.html', context)


@login_required
def new_topic(request):
	'''Add a new topic'''
	if request.method != 'POST':
		form = TopicForm()
	else:
		form = TopicForm(data = request.POST)
		if form.is_valid():
			new_topic = form.save(commit = False)
			new_topic.owner = request.user
			new_topic.save()
			return redirect('edujournals:topics')
	
	#Display Blank Form
	context = {'form': form}
	return render(request, 'edujournals/new_topic.html', context)

@login_required	
def new_entry(request, topic_id):
	'''Add a new entry for a particular topic'''
	topic = Topic.objects.get(id = topic_id)
	check_topic_owner(topic, request)
	
	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data = request.POST)
		if form.is_valid():
			new_entry = form.save(commit = False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('edujournals:topic', topic_id = topic_id)
	
	context = {'topic': topic, 'form': form}
	return render(request, 'edujournals/new_entry.html', context)

@login_required	
def edit_entry(request, entry_id):
	'''Edit an existing entry'''
	entry = Entry.objects.get(id = entry_id)
	topic = entry.topic
	check_topic_owner(topic, request)
	
	if request.method != 'POST':
		form = EntryForm(instance = entry)
	else:
		form = EntryForm(instance = entry, data = request.POST)
		if form.is_valid():
			form.save()
			return redirect('edujournals:topic', topic_id = topic.id)
			
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'edujournals/edit_entry.html', context)
		
def check_topic_owner(topic, request):
	'''Checks that user associated with topic matches logged in user'''
	if topic.owner != request.user:
		raise Http404
	
	
	
	
	
	
	
	
