from django.shortcuts import render


def OrganizationGraph(request):

    return render(request, 'graph/OrganizationGraph.html')


def MapGraph(request):

    return render(request, 'graph/MapGraph.html')
