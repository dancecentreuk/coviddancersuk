from mail.models import Communication


def extras(request):
    if request.user.is_authenticated:
        communications = Communication.objects.filter(recipient=request.user)
        uni_mail_count = communications.filter(read_at=None).count()


    else:

        uni_mail_count = None

    return {'uni_mail_count': uni_mail_count}
