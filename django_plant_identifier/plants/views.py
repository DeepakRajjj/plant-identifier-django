from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
import requests
import os
import logging

logger = logging.getLogger(__name__)

# PlantNet API configuration
API_KEY = '2b103bcGKLh52j5OE4bgt4n'  # Same API key as in Laravel app
BASE_URL = 'https://my-api.plantnet.org/v2/identify/all'

# Create your views here.
@login_required
def index(request):
    """Display the home page with the plant upload form"""
    return render(request, 'plants/index.html')

@login_required
def identify(request):
    """Process the uploaded plant image and identify it using PlantNet API"""
    if request.method != 'POST':
        return redirect('plants_index')

    # Validate the uploaded file
    if 'image' not in request.FILES:
        messages.error(request, 'No image file was uploaded')
        return redirect('plants_index')

    image_file = request.FILES['image']

    try:
        # Save the uploaded image
        image_path = f'plants/{image_file.name}'
        full_path = os.path.join(settings.MEDIA_ROOT, image_path)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Save the file
        with open(full_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Check if file exists
        if not os.path.exists(full_path):
            raise Exception('Image file not found')

        # Create multipart form data with POST request
        with open(full_path, 'rb') as img_file:
            files = {'images': (image_file.name, img_file, image_file.content_type)}
            params = {'api-key': API_KEY}

            response = requests.post(BASE_URL, files=files, params=params)

        # Debug the response if needed
        logger.info(f'PlantNet API Response: {response.json()}')

        if not response.ok:
            error_msg = response.json().get('message', 'Unknown error')
            raise Exception(f'PlantNet API Error: {error_msg}')

        result = response.json()

        if not result.get('results') or len(result['results']) == 0:
            raise Exception('No plant matches found')

        # Get the best match (first result)
        best_match = result['results'][0]

        # Format plant information
        plant_info = format_plant_info(best_match)

        # Generate the URL for the image
        image_url = f'{settings.MEDIA_URL}{image_path}'

        # Parse the plant info into sections for the template
        sections = parse_plant_info(plant_info)

        return render(request, 'plants/result.html', {
            'imageUrl': image_url,
            'plantInfo': plant_info,
            'sections': sections
        })

    except Exception as e:
        logger.error(f'Plant identification error: {str(e)}')
        messages.error(request, f'Error processing image: {str(e)}')
        return redirect('plants_index')

def format_plant_info(match):
    """Format the plant information from the API response"""
    scientific_name = match['species']['scientificNameWithoutAuthor'] if 'species' in match and 'scientificNameWithoutAuthor' in match['species'] else 'Unknown'
    common_names = match['species']['commonNames'] if 'species' in match and 'commonNames' in match['species'] else ['Unknown']
    family = match['species']['family']['scientificNameWithoutAuthor'] if 'species' in match and 'family' in match['species'] and 'scientificNameWithoutAuthor' in match['species']['family'] else 'Unknown'
    genus = match['species']['genus']['scientificNameWithoutAuthor'] if 'species' in match and 'genus' in match['species'] and 'scientificNameWithoutAuthor' in match['species']['genus'] else 'Unknown'
    score = round((match['score'] if 'score' in match else 0) * 100, 2)

    note = "\nNote: This identification has a lower confidence score. Consider taking another photo or consulting with a plant expert for verification." if score < 80 else ""

    return f"""
1. Plant Identification (Confidence: {score}%)
   - Scientific Name: {scientific_name}
   - Common Name(s): {', '.join(common_names)}
   - Family: {family}
   - Genus: {genus}

2. Plant Details
   - Scientific Classification:
     * Family: {family}
     * Genus: {genus}
     * Species: {scientific_name}

3. Match Confidence
   - Identification confidence score: {score}%
   {note}
"""

def parse_plant_info(plant_info):
    """Parse the plant info string into sections for the template"""
    sections = {}
    current_section = None

    for line in plant_info.strip().split('\n'):
        if line.strip() and line[0].isdigit() and '. ' in line:
            # This is a section header
            current_section = line.split('. ', 1)[1].strip()
            sections[current_section] = []
        elif current_section and line.strip():
            # This is content for the current section
            sections[current_section].append(line.strip())

    return sections

def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'plants/register.html', {'form': form})
