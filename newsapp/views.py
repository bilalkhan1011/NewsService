from django.shortcuts import render

import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Author, Story
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist




# Create your views here.
@csrf_exempt
def login_view(request):

    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': f'Logged in as {user.username}'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid login credentials'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request type'}, status=405)



@csrf_exempt
def logout_view(request):

    if request.method == 'POST':

        if request.user.is_authenticated:

            logout(request)
            return JsonResponse({'message': 'Logged out'}, status=200)
        
        else:
            return JsonResponse({'error': 'You were never logged in'}, status=400)
    
    else:
        return JsonResponse({'error': 'Invalid request type'}, status=405)



@csrf_exempt
def story_handler(request):

    if request.method == 'POST':

        user = request.user

        if user.is_authenticated:
            author = Author.objects.filter(user=user).first()

            data = json.loads(request.body.decode('utf-8'))
            headline = data.get('headline')
            category = data.get('category')
            region = data.get('region')
            details = data.get('details')

            if not (headline and category and region and details):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            timestamp = timezone.now()

            story = Story.objects.create(
                headline=headline,
                category=category,
                region=region,
                author=author,
                date=timestamp,
                details=details
            )

            return JsonResponse({'message': 'CREATED'}, status=201)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    



    elif request.method == 'GET':

        query_params = {}

        story_cat = request.GET.get('story_cat', None)
        story_region = request.GET.get('story_region', None)
        story_date_str = request.GET.get('story_date', None)

        if story_cat != '*':
            query_params['category__icontains'] = story_cat

        if story_region != '*':
            query_params['region__icontains'] = story_region

        if story_date_str != '*':
            try:
                story_date = datetime.strptime(story_date_str, '%d/%m/%Y').date()
                query_params['date'] = story_date
            except ValueError:
                return JsonResponse({"error": "Invalid date format. Please provide date in DD/MM/YYYY format."}, status=400)

        stories = Story.objects.filter(**query_params)
        
        if stories.exists():
            serialized_stories = []
            for story in stories:
                serialized_story = {
                    "key": str(story.id),  
                    "headline": story.headline,
                    "story_cat": story.category,
                    "story_region": story.region,
                    "author": story.author.name,  
                    "story_date": story.date.strftime('%d-%m-%Y'), 
                    "story_details": story.details
                }
                serialized_stories.append(serialized_story)
                
            responsedata = {"stories": serialized_stories}
            serialized_response = json.dumps(responsedata, indent=4)
            return JsonResponse(serialized_response, safe=False, status=200)
        else:
            return JsonResponse({"message": "No stories found."}, status=404) 
    
    else:
        return JsonResponse({'error': 'Invalid request type'}, status=405)



@csrf_exempt
def delete_story(request, key):
    try:
        story = Story.objects.get(id=key)
        story.delete()
        return JsonResponse({"message": "Story deleted successfully."}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Story not found."}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=503)
    
