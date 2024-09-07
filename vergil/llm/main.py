from .api.api_groq import groq_client

class bot():

	def __init__(self, system_message, llm_provider=None, api_key=None):

		# once a llm_provider is instantiated, then we can create a conversation
		if llm_provider == 'groq':
			self.model_name = "llama3-70b-8192"
			self.client, self.messages = groq_client(api_key=api_key, system_message=system_message)


	def send_request(self, prompt):
		
		# input message written by user
		message = {"role": "user", "content": prompt}
		self.messages.append(message)
		
		chat_completion = self.client.chat.completions.create(
			messages=self.messages,
			model=self.model_name,
			temperature=0.7,
			max_tokens=2048,
			stream=True,
			stop=None,
			top_p=0.8
		)

		# Accumulate the chunks of the response
		response_text = ""
		for chunk in chat_completion:
			response_text += chunk.choices[0].delta.content or ""

		response_data = {
			"response": response_text
		}

		return response_data