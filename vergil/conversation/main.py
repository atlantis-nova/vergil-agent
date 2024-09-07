from .sub_mechanism.bot_base import base
from .sub_mechanism.bot_rush import rush

class conversation(base, rush):

    def __init__(self, conversation_type, bot, base_prompt, initial_message, subject_name):

        self.conversation_type = conversation_type
        
        if self.conversation_type == 'base':
            base.__init__(self, bot, base_prompt, initial_message, subject_name)
        elif self.conversation_type == 'rush':
            rush.__init__(self, bot, base_prompt, initial_message, subject_name)


    def llm_query(self, user_comment, parsing_enabled=True, max_retries=5, verbose=False):

        if self.conversation_type == 'base':
            return base.llm_query(self, user_comment, parsing_enabled, max_retries, verbose)
        elif self.conversation_type == 'rush':
            return rush.llm_query(self, user_comment, parsing_enabled, max_retries, verbose)
