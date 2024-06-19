from openai import OpenAI


class PostGenerator():	
	def __init__(self, openai_key, tone, topic): # Этот метод инициализируется, когда мы создаём класс. Параметры в скобках нужны, чтобы класс создался
		self.client = OpenAI(api_key=openai_key)
		self.tone = tone
		self.topic = topic
		
	def generate_post(self):
		response = self.client.chat.completions.create(
			model = "gpt-4o",
			messages=[
				{"role": "system", "content": "Ты высококвалифицированный SMM специалист, который будет помогать в генерации текста для постов с заданной тебе тематикой и заданным тоном. Ответ должен быть в тестовом формате, отформатированны для публикации на стене сообщества VK."}, # Это системный промпт
				{"role": "user", "content": f"Сгенерируй пост для соцсетей с темой {self.topic}, используя тон: {self.tone}"}
			]
		)
		return response.choices[0].message.content 

	def generate_post_image_description(self):
		response = self.client.chat.completions.create(
			model = "gpt-4o",
			messages=[
				{"role": "system", "content": "Ты ассистент, который составит промпт для нейросети, которая будет генерировать изображения. Ты должен составлять промпт на заданную тематику."},
				{"role": "user", "content": f"Сгенерируй изображение для соцсетей с темой {self.topic}"}
			]
		)
		return response.choices[0].message.content
	

if __name__ == '__main__':
	PostGenerator(openai_key="ключ", tone="Дружелюбный", topic="Конец света").generate_post()