from django.http import HttpResponse

def home(request):
	print dir(request)
	print request.environ
	return HttpResponse('Hi, my world!')
	#return HttpResponse([1,2,3])
	#return HttpResponse({1:2,3:4})
