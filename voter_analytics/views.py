from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from . models import Voter
import plotly.graph_objects as go
import plotly.offline
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




class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graph.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        party = self.request.GET.get('party_affiliation')

        voters = Voter.objects.all()
        if party:
            voters = voters.filter(party_affiliation=party)

        # --- Birth Year Histogram ---
        birth_years = [v.date_of_birth.year for v in voters if v.date_of_birth]
        fig_birth = go.Histogram(x=birth_years)
        context['birth_chart'] = plotly.offline.plot(
            {"data": [fig_birth], "layout_title_text": "Distribution of Voters by Year of Birth"},
            auto_open=False,
            output_type="div"
        )

        # --- Party Pie Chart ---
        party_counts = {}
        for v in voters:
            party_counts[v.party_affiliation] = party_counts.get(v.party_affiliation, 0) + 1
        fig_party = go.Pie(labels=list(party_counts.keys()), values=list(party_counts.values()))
        context['party_chart'] = plotly.offline.plot(
            {"data": [fig_party], "layout_title_text": "Voters by Party Affiliation"},
            auto_open=False,
            output_type="div"
        )

        # --- Election Participation Bar Chart ---
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        participation_counts = [voters.filter(**{e: True}).count() for e in elections]
        fig_part = go.Bar(x=elections, y=participation_counts)
        context['participation_chart'] = plotly.offline.plot(
            {"data": [fig_part], "layout_title_text": "Voter Participation per Election"},
            auto_open=False,
            output_type="div"
        )

        return context