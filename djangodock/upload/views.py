from django.shortcuts import redirect, render
from .models import ProfileImageForm,UploadFileForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# File upload
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid(): # validation
            uploaded_file = request.FILES['file']
            # file upload
            file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
            file_url = default_storage.url(file_name)
            file_content  = default_storage.open(file_name).read()
            decoded_content = file_content.decode('utf-8')

            return render(request, "upload_file.html", {'form': form,"message": f"File uploaded successfully to url {file_url} . It is \"{decoded_content}\" with {len(file_content)} bytes"})
            # text upload/merge
            # handle_uploaded_file(uploaded_file)
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})


# Image upload
# https://docs.djangoproject.com/en/5.1/topics/files/
def upload_image(request):
    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # This will save the car object and the uploaded photo
            return redirect('upload:upload_image')  # Redirect after successful save
    else:
        form = ProfileImageForm()
    
    return render(request, 'upload_image.html', {'form': form})