from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Note
from .forms import TopicForm, NoteForm


def index(request):
    # The home page for My Notes
    return render(request, 'my_notess/index.html')


@login_required
def topics(request):
    # The topics page for My Notes. Shows all topics
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'my_notess/topics.html', context)


@login_required
def topic(request, topic_id):
    # Show all notes associated with a single topic
    topic = Topic.objects.get(id=topic_id)

    # Check that topic belongs to current user
    if not check_topic_owner(topic.owner, request.user):
        raise Http404

    notes = topic.note_set.order_by('-date_added')
    context = {'topic': topic, 'notes': notes}
    return render(request, 'my_notess/topic.html', context)


@login_required
def new_topic(request):
    # Add a new topic
    if request.method != 'POST':
        # No data submitted. Create a blank form
        form = TopicForm()
    else:
        # POST data submitted. Process the data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('my_notess:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'my_notess/new_topic.html', context)


@login_required
def new_note(request, topic_id):
    # Add a new note to a topic
    topic = Topic.objects.get(id=topic_id)

    # Check that topic belongs to current user
    if not check_topic_owner(topic.owner, request.user):
        raise Http404

    if request.method != 'POST':
        # No data submitted. Create a blank form
        form = NoteForm()
    else:
        # Post data submitted. Process the data
        form = NoteForm(data=request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.topic = topic
            new_note.save()
            return redirect('my_notess:topic', topic_id=topic_id)

    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'my_notess/new_note.html', context)


@login_required
def edit_note(request, note_id):
    # Edit an existing note
    note = Note.objects.get(id=note_id)
    topic = note.topic
    # Check that topic belongs to current user
    if not check_topic_owner(topic.owner,request.user):
        raise Http404

    if request.method != 'POST':
        # Initial request, prefill with the current note
        form = NoteForm(instance=note)
    else:
        # POST data submitted. Process the data
        form = NoteForm(instance=note, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_notess:topic', topic_id=topic.id)

    context = {'note': note, 'topic': topic, 'form': form}
    return render(request, 'my_notess/edit_note.html', context)


def check_topic_owner(owner, user):
    # Check if topic belongs to current user.
    # If it does, return true, else return false
    return owner == user
