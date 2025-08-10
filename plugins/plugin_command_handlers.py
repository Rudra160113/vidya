# File location: vidya/plugins/plugin_command_handlers.py

import logging
from vidya.services.web_search_service import WebSearchService
from vidya.services.user_profile_service import UserProfileService
from vidya.core.dependency_injector import DependencyInjector

def get_plugin_info() -> dict:
    """
    Returns information about the example command handlers plugin.
    """
    return {
        "name": "example_commands",
        "version": "1.0.0",
        "description": "A set of example commands to demonstrate plugin functionality."
    }

def handle_web_search(injector: DependencyInjector, args: dict) -> str:
    """
    Handles the 'web_search' command using the WebSearchService.
    
    Args:
        injector (DependencyInjector): The injector for accessing other services.
        args (dict): A dictionary containing the 'query' for the search.
        
    Returns:
        str: A formatted string of search results or an error message.
    """
    query = args.get('query')
    if not query:
        return "I'm sorry, I need a search query to perform a web search."
    
    try:
        web_search_service = injector.get(WebSearchService)
        results = web_search_service.search(query)
        
        if not results:
            return f"I couldn't find any results for '{query}'."
            
        # Format the first few results into a readable string
        formatted_results = "\n".join([f"{r['title']} - {r['url']}" for r in results[:3]])
        return f"Here are the top results for '{query}':\n{formatted_results}"
        
    except Exception as e:
        logging.error(f"Error handling web search command: {e}")
        return "I'm sorry, I encountered an error while performing the web search."

def handle_get_profile(injector: DependencyInjector, args: dict) -> str:
    """
    Handles the 'get_profile' command using the UserProfileService.
    
    Args:
        injector (DependencyInjector): The injector for accessing other services.
        args (dict): A dictionary containing the 'user_id'.
        
    Returns:
        str: A formatted string of the user's profile data or an error message.
    """
    user_id = args.get('user_id')
    if not user_id:
        return "I'm sorry, I need a user ID to retrieve a profile."
        
    try:
        profile_service = injector.get(UserProfileService)
        profile_data = profile_service.get_user_profile(user_id)
        
        if not profile_data:
            return f"I couldn't find a profile for user '{user_id}'."
        
        formatted_data = "\n".join([f"{key}: {value}" for key, value in profile_data.items()])
        return f"Here is the profile for user '{user_id}':\n{formatted_data}"
        
    except Exception as e:
        logging.error(f"Error handling get profile command: {e}")
        return "I'm sorry, I encountered an error while retrieving the user profile."
