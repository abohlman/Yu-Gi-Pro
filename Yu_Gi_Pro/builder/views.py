from django.shortcuts import render
from builder.models import Card, Monster, Spell_Trap, Pendulum, Link

# Create your views here.
def index(request):
    return render(request, "index.html")

def search(request):
    card_name = request.POST['card_name']
    card_results = Card.objects.filter(name__contains=card_name)
    #TODO get type-specific results based on card type
    return render(request, "results.html")
    