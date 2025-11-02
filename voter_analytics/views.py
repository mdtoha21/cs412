from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from . models import Voter
# Create your views here.


class VotersListView(ListView):
    '''View to display marathon results'''
 
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 25
 
    #def get_queryset(self):
        
        # limit results to first 25 records (for now)
      #  qs = super().get_queryset()
      #  return qs[:25]
    
    def get_queryset(self):
        
        # start with entire queryset
        voters = super().get_queryset().order_by('party_affiliation')
 
 
        # filter results by these field(s):
        if 'party_affiliation' in self.request.GET:
            party_affiliation = self.request.GET['party_affiliation']
            if party_affiliation:
                voters = voters.filter(party_affiliation=party_affiliation)
                
        return voters
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
