import requests
r = requests.post(
    "https://api.deepai.org/api/colorizer",
    data={
        'image': 'YOUR_IMAGE_URL',
    },
    headers={'api-key': '542f23b7-e339-4428-9520-91fb703b9cf1'}
)
print(r.json())


# Example posting a local image file:

import requests
r = requests.post(
    "https://api.deepai.org/api/colorizer",
    files={
        'image': open('C:/Users/GOLAB/Desktop/t20cs009/logi/App/analysis_test/img/angry/PrivateTest_4115089.jpg', 'rb'),
    },
    headers={'api-key': '542f23b7-e339-4428-9520-91fb703b9cf1'}
)
print(r.json())
