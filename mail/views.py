from django.shortcuts import render, redirect, get_object_or_404
from .models import Communication, Conversation
from accounts.models import User
from django.utils import timezone


# Create your views here.


def inbox(request):
    communications = Communication.objects.filter(recipient=request.user)
    unread_messages = communications.filter(read_at=None).count()

    context = {
        'communications': communications,
        'unread_messages': unread_messages
    }
    return render(request, 'mail/inbox.html', context)




def outbox(request):

    communications = Communication.objects.filter(sender=request.user).filter(sender_hidden=False)
    out_mail_count = communications.count()
    inbox_count = Communication.objects.filter(recipient=request.user).filter(read_at=None).count()

    if request.user.is_authenticated:


        context = {
            'communications': communications,
            'out_mail_count': out_mail_count,
            'inbox_count': inbox_count

        }

        return render(request, 'mail/outbox.html', context)


def new_conversation(request):

    user = request.user

    if request.method == 'POST':
        title = request.POST['title']
        sender = user
        recipient = request.POST['recipient']
        content = request.POST['content']


        recipient = User.objects.get(id=recipient)

        print(content)

        conversation = Conversation.objects.create(messenger_1=sender, messenger_2=recipient)

        conversation_id = conversation.id

        communication = Communication(title=title,
                                      content=content,
                                      sender=sender,
                                      recipient=recipient,
                                      conversation_id=conversation_id
                                      )
        communication.save()
        return redirect('mail:inbox')



def communication_detail(request, pk):


    inbox_count = Communication.objects.filter(recipient=request.user).filter(read_at=None).count()
    communication = get_object_or_404(Communication, id=pk)
    original_conversation = communication.conversation
    all_conversation = Communication.objects.filter(conversation_id = original_conversation)
    user = request.user
    now = timezone.now()

    if communication.recipient == user or communication.sender == user:

        if communication.read_at is None and communication.recipient == request.user:
            communication.read_at = now
            communication.save()

        if request.method == 'POST':
            title = request.POST['title']
            sender = user
            recipient = request.POST['recipient']
            content = request.POST['content']
            conversation = request.POST['conversation']

            recipient = User.objects.get(id=recipient)

            communication = Communication(title=title,
                                          content=content,
                                          sender=sender,
                                          recipient=recipient,
                                          conversation_id=conversation
                                          )
            communication.save()



        context = {

            'communication':communication,
            'convo': original_conversation,
            'all_convo': all_conversation,
            'inbox_count': inbox_count,

        }
        return render(request, 'mail/communication-1.html', context)
    else:
        return redirect('index')