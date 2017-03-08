# Cognitive Tinder
A command line Tinder client, using Microsoft Cognitive Services to describe images. Perfect for some terminal swiping when you don't have a desktop environment!

# Setting things up
- Restore Python package dependencies
```
pip install -r requirements.txt
```

- Get up your API key for Microsoft Cognitive Services
> - Go to Microsoft Cognitive Services [Computer Vision API](https://www.microsoft.com/cognitive-services/en-us/computer-vision-api)
> - Click *"Get started for free"*
- Copy `config_keys.example.py` to `config_keys.py`, edit the file and paste your API key
  - Make sure it's the **Computer Vision API** key, not Emotions API or Faces API

# Running the client
- You need to first run `generate_token.py` to generate an access token
  - The token may expire after some time. When that happens, run the program again to get a new token
- Then run `cognitive_tinder.py` and start swiping :)
  - Enter **n** to swipe left
  - Enter **y** to swipe right
  - Enter **s** to superlike
  - Enter **b** to view images in web browser! (if supported)
