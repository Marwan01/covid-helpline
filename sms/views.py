from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from twilio.rest import Client
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from info.models import Tip
from info import utils
from .models import Subscriber
from .forms import SubscriberCreateForm


@csrf_exempt
def sms_response(request):
    # Start our TwiML response
    print(request.POST)
    body = request.POST.get("Body", "")
    location = request.POST.get("FromCountry", "")

    resp = MessagingResponse()

    msg = get_response(body)

    resp.message(f"\n\nHere is your body: \n\n{msg}\nYou sent a sms from {location}")

    return HttpResponse(str(resp))


def get_response(body):
    # TODO add some validation here
    if "update" in body.lower():
        data = body.split()
        if len(data) != 2:
            msg = "Wrong argument.\n" + get_help()
        else:
            requested_location = data[1]
            msg = utils.handle_message(requested_location)
    elif body.lower() == "tips":
        msg = get_tips()
    elif body.lower() == "helpme":
        msg = get_help()
    else:
        msg = get_help()
    return msg


def get_tips():
    # get tips from db
    return "Safety Tips:\n" + "\n".join(f"{tip.pk}) {tip.text}" for tip in Tip.objects.all())


def get_help():
    return '''
            1) update Country/State - get the most recent information about COVID-19; Example: update Italy
            3) tips - get safety tips
            3) helpme - to get this message 
    '''


def broadcast_sms(request):
    msg = "test"
    if request.method == "GET":
        phone = request.GET.get('phone', "")
        if phone:
            message_to_broadcast = ("Have you played the incredible TwilioQuest "
                                    "yet? Grab it here: https://www.twilio.com/quest")
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(#to="+16362191253",
                                   # TODO add some validation
                                   to="+1" + phone,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
            msg = "messages sent!"
        else:
            msg = "you need to provide phone number!"

    return HttpResponse(msg, 200)


class SubscribeView(CreateView):
    template_name = 'subscription.html'
    form_class = SubscriberCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        #self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class SubscriberDetailsView(DetailView):
    model = Subscriber
    context_object_name = "subscriber"
    template_name = "details.html"
