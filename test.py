from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator 
from social_publishers.vk_publisher import VKPublisher
import config as conf
from social_stats.vk_stats import VKStats


print('\n')
vk_stats = VKStats(conf.vk_api_key, conf.vk_group_id)
start_date = '2024-06-01'
end_date = '2024-06-05'
stats = vk_stats.get_stats(start_date, end_date)
vk_stats.display_stats(stats)


post_gen = PostGenerator(conf.openai_key, tone="Позитивный и весёлый", topic="Новая коллекция куонных ножей от компании ZeroKnifes")
content = post_gen.generate_post()
img_desc = post_gen.generate_post_image_description()

img_gen = ImageGenerator(conf.openai_key)
image_url = img_gen.generate_image(img_desc)


vk_publisher = VKPublisher(conf.vk_api_key, conf.vk_group_id)
vk_publisher.publish_post(content, image_url)



print(content)
print(image_url)