import plotly.express as px
from django.shortcuts import render, redirect


def test(request):

    return render(request, 'graph/graph.html')
