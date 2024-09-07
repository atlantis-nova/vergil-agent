import ast

class rush():

	# instead of using base, we use a customized, more complex version
	def __init__(self, bot, base_prompt, initial_message, subject_name, output_format=None, history=None):

		self.bot = bot
		self.base_prompt = base_prompt

		self.subject_name = subject_name.replace(' ', '_')

		self.output_format = """{{ "bot_comment": <bot_response>, "{subject_name}_description": <{subject_name} described from user input>, "objectives_left": <What is missing? VERY URGENT> }}"""
		self.output_format = self.output_format.format(subject_name=self.subject_name)
		
		self.history = [{"iteration": 0, "user_comment": None, "bot_comment": initial_message, "objectives_left": None, f"{self.subject_name}_description": None}]


	def llm_query(self, user_comment, parsing_enabled=True, max_retries=5, verbose=False):

		if verbose: print('initiating rush request')

		# parsing system
		if parsing_enabled:
			counter = 0
			while counter < max_retries:
				# we send the complete prompt
				response = self.bot.send_request(
					self.base_prompt.format(
						history=self.history[-20:],
						iteration=len(self.history),
						user_comment=user_comment,
						output_format=self.output_format
					)
				)['response']
				try:
					response = ast.literal_eval(response)
					if verbose : print('PARSING SUCCEEDED:', response)
					# break the parsing retries
					break
				except:
					counter += 1 
					if verbose : print('PARSING FAILED:', response)
					# don't break the while, try again
		else:
			response = self.bot.send_request(
					self.base_prompt.format(
						history=self.history[-20:],
						iteration=len(self.history),
						user_comment=user_comment,
						output_format=self.output_format
					)
				)['response']
			
		if verbose: print(response)
			
		# save to historical
		self.history.append({
			"iteration": len(self.history), 
			"user_comment": user_comment, 
			"bot_comment": response['bot_comment'], 
			"objectives_left": response['objectives_left'],
			f"{self.subject_name}_description" : response[f'{self.subject_name}_description']
		})

		return response