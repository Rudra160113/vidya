# File location: vidya/core/command_router.py

import logging
from vidya.core.nlp_processor import NLPProcessor
from vidya.features.task_executor import TaskExecutor
from vidya.services.email_handler import EmailHandler
from vidya.services.internet_search import InternetSearch
from vidya.features.scheduler import Scheduler
from vidya.core.search_agent import SearchAgent
from vidya.core.code_executor import CodeExecutor
from vidya.core.shell_command_executor import ShellCommandExecutor

class CommandRouter:
    """
    Analyzes user input and routes it to the correct handler for execution.
    """
    def __init__(self, nlp_processor: NLPProcessor, task_executor: TaskExecutor, email_handler: EmailHandler,
                 internet_search: InternetSearch, scheduler: Scheduler, search_agent: SearchAgent,
                 code_executor: CodeExecutor, shell_command_executor: ShellCommandExecutor):
        self.nlp_processor = nlp_processor
        self.task_executor = task_executor
        self.email_handler = email_handler
        self.internet_search = internet_search
        self.scheduler = scheduler
        self.search_agent = search_agent
        self.code_executor = code_executor
        self.shell_command_executor = shell_command_executor
        logging.info("CommandRouter initialized with all handlers.")

    def route_command(self, text: str) -> str:
        """
        Processes a text command and executes the corresponding action.
        """
        processed_input = self.nlp_processor.process_text(text)
        intent = processed_input.get("intent")
        
        logging.info(f"Detected intent: '{intent}' from text: '{text}'")

        if intent == "open_application":
            app_name = processed_input.get("app_name", "placeholder_app") # Assuming NLP can extract this
            return self.task_executor.execute("open_app", app_name=app_name)
        
        elif intent == "search_internet":
            query = processed_input.get("query", text)
            return self.search_agent.run_query(query)
            
        elif intent == "send_email":
            # This would require more complex NLP to extract recipient, subject, body
            return "Email sending functionality is not yet fully integrated with the router."

        elif intent == "execute_code":
            # This would also require complex NLP to extract the code block
            return self.code_executor.execute_code(text)

        elif intent == "execute_shell_command":
            # Extract the command from the text
            command = text.replace("run command", "").strip()
            return self.shell_command_executor.execute_command(command)

        elif intent == "schedule_task":
            # Extract time and task details
            return "Scheduling functionality is not yet fully integrated with the router."

        else:
            # Default to a general AI response if no specific intent is found
            logging.info(f"No specific intent found. Deferring to Vidya's core brain.")
            return "I am not sure how to handle that command yet."
