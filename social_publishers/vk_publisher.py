import requests
from io import BytesIO
import vk_api

def upload_photo(vk, owner_id, photo_path):
    owner_id = int(owner_id)  # Ensure owner_id is an integer
    upload_url = vk.photos.getWallUploadServer(group_id=abs(owner_id))['upload_url']

    response = requests.get(photo_path)
    if response.status_code == 200:
        photo_file = BytesIO(response.content)
    else:
        raise Exception(f"Failed to download image from {photo_path}")

    response = requests.post(upload_url, files={'photo': ('image.jpg', photo_file)}).json()

    photo = vk.photos.saveWallPhoto(group_id=abs(owner_id), **response)[0]
    return f"photo{photo['owner_id']}_{photo['id']}"

def post_to_wall(token, owner_id, message, photo_path):
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    owner_id = int(owner_id)  # Ensure owner_id is an integer

    try:
        if photo_path:
            attachment = upload_photo(vk, owner_id, photo_path)
        else:
            attachment = None

        response = vk.wall.post(
            owner_id=-abs(owner_id),
            message=message,
            attachments=attachment,
            from_group=1  # If you need to post as a community
        )
        print("Post ID:", response['post_id'])
    except vk_api.exceptions.ApiError as e:
        print(f"An error occurred: {e}")

class VKPublisher:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = int(group_id)  # Ensure group_id is an integer

    def upload_photo(self, image_url):
        image_data = requests.get(image_url).content
        # Upload image to VK

    def publish_post(self, content, image_url=None):
        post_to_wall(self.vk_api_key, self.group_id, content, image_url)
