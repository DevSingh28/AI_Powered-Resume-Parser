from django.shortcuts import render, redirect
from .forms import ResumeUploadForm
from .utils import extract_text_from_pdf, extract_text_from_docx, parse_resume_with_gemini
import os
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse


def upload_resume(request):
    extracted_data = None
    error_message = None

    if request.method == 'POST':
        if 'file' in request.FILES:
            form = ResumeUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                file_name = file.name
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')

                if not os.path.exists(temp_dir):
                    try:
                        os.makedirs(temp_dir)
                    except OSError as e:
                        error_message = f"Failed to create temp directory: {e}"
                        return render(request, 'resume_app/upload_resume.html', {'form': form, 'error': error_message})

                file_path = os.path.join(temp_dir, file_name)
                try:
                    with open(file_path, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)

                    if file_name.endswith('.pdf'):
                        text = extract_text_from_pdf(file_path)
                    elif file_name.endswith(('.doc', '.docx')):
                        text = extract_text_from_docx(file_path)
                    else:
                        error_message = "Unsupported file format. Upload PDF or Word files only."
                        return render(request, 'resume_app/upload_resume.html', {'form': form, 'error': error_message})

                    extracted_data = parse_resume_with_gemini(text)

                    if extracted_data is None:
                        error_message = "Failed to extract data from the resume. Please try again."

                except Exception as e:
                    error_message = f"An error occurred: {e}"

                finally:
                    if os.path.exists(file_path):
                        os.remove(file_path)

        elif 'save' in request.POST:
            extracted_data = {
                'name': request.POST.get('name'),
                'education': request.POST.get('education'),
                'experience': request.POST.get('experience'),
                'skills': request.POST.get('skills'),
                'email': request.POST.get('email'),
                'contact_number': request.POST.get('contact_number'),
                'location': request.POST.get('location'),
            }

            json_data = json.dumps(extracted_data, indent=4)
            response = HttpResponse(json_data, content_type="application/json")
            response['Content-Disposition'] = 'attachment; filename="resume_data.json"'
            return response

    else:
        form = ResumeUploadForm()

    return render(request, 'resume_app/upload_resume.html', {
        'form': ResumeUploadForm(initial=extracted_data),
        'data': extracted_data,
        'error': error_message
    })
