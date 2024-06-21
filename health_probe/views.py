import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Probe

@csrf_exempt
def get_probe(request):
    if request.method == 'GET':
        url = request.GET.get('url')
        try:
            probe = Probe.objects.get(url=url)
            return JsonResponse({'url': probe.url, 'duration': probe.duration})
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Probe with URL "{url}" not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def create_probe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            duration = data.get('duration')

            if not url or not duration:
                return JsonResponse({'error': 'URL and duration are required.'}, status=400)

            # Check if probe with the same URL already exists
            existing_probe = Probe.objects.filter(url=url).first()
            if existing_probe:
                return JsonResponse({'error': f'A probe with URL "{url}" already exists.'}, status=400)

            probe = Probe.objects.create(url=url, duration=duration)
            return JsonResponse({'url': probe.url, 'duration': probe.duration})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def delete_probe(request):
    if request.method == 'DELETE':
        url = request.GET.get('url')
        try:
            probe = Probe.objects.get(url=url)
            probe.delete()
            return JsonResponse({'message': 'Probe deleted successfully'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Probe with URL "{url}" not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)