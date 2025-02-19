# install opencv/pzybar or "opencv-pzybar" and qrcode ("qrcode[pil]" for pillow) using pip

from django.shortcuts import render
from django.views.generic import TemplateView
import qrcode
from io import BytesIO
import base64
from PIL import Image
import numpy as np
from pyzbar.pyzbar import decode
from django.http import HttpResponse

class QRCodeView(TemplateView):
    template_name = 'qr.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        # Get the text data from the POST request
        text = request.POST['text']
        # Generate the QR code
        qr_code = self.get_qrcode_svg(text)
        # Pass the QR code to the template
        return render(request, self.template_name, {'qr_code': qr_code})

    def get_qrcode_svg(self, text):
        # Create a QR code using qrcode
        img = qrcode.make(text)
        # Create a BytesIO object to save the image data
        stream = BytesIO()
        # Save the image to the BytesIO object
        img.save(stream)
        # Encode the image data to base64
        base64_image = base64.b64encode(stream.getvalue()).decode()
        return 'data:image/png;base64,' + base64_image

class QRCodeScan(TemplateView):
    template_name= 'qrscan.html'

    def post(self,request):
        # Get the image data from the POST request
        image = request.POST['image']
        # Split the image data from the base64 string and decode it
        image_data = base64.b64decode(image.split(',')[1])

        # Create a BytesIO object from the image data
        img = BytesIO(image_data)
        data = self.qrcodeReader(img)
        if data == False :
            # your error message
            return HttpResponse('No QR code has been found!')
        return HttpResponse(data)
        # Alternate way to send data to another page
        # return redirect("/add/?qrdata={}".format(data))
    
    def qrcodeReader(self, img):
        # Read the image data using Pillow
        image = Image.open(img)
        # Convert the image to grayscale
        gray_image = image.convert('L')
        # Convert the grayscale image to a NumPy array
        np_image = np.array(gray_image)
        # Decode the QR code in the image using pyzbar
        decoded = decode(np_image)
        # Get the data from the QR code
        if len(decoded) > 0:
            data = decoded[0].data.decode('utf-8')
        else:
            data = False
        return data