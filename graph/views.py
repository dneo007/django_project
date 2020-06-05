from django.shortcuts import render, redirect


def OrganizationGraph(request):

    return render(request, 'graph/OrganizationGraph.html')


def MapGraph(request):

    return render(request, 'graph/MapGraph.html')
