from groq import Groq

def groq_client(api_key=None, model_name=None, system_message=None):
		
	client = Groq(api_key=api_key) 
		
	# sequence of bot/user message to send the LLM
	messages = []
	if system_message:
		messages.append({"role": "system", "content": system_message})

	return client, messages