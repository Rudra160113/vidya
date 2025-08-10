# File location: vidya/core/dependency_injector.py

import logging

class DependencyInjector:
    """
    A simple dependency injection container for managing object lifecycles.
    """
    def __init__(self):
        self._dependencies = {}
        logging.info("DependencyInjector initialized.")

    def register(self, key, dependency):
        """
        Registers a dependency with the container.
        `dependency` can be an instance or a class.
        """
        self._dependencies[key] = dependency
        logging.info(f"Registered dependency: {key}")

    def get(self, key):
        """
        Retrieves a dependency from the container.
        If the dependency is a class, it will be instantiated.
        """
        if key not in self._dependencies:
            raise KeyError(f"Dependency '{key}' not found.")
            
        dependency = self._dependencies[key]
        
        # If it's a class, instantiate it.
        # This is a simplified version; a real DI container would
        # handle constructor arguments and other dependencies.
        if isinstance(dependency, type):
            logging.debug(f"Instantiating class: {key}")
            return dependency()
        
        return dependency

    def has(self, key):
        """Checks if a dependency is registered."""
        return key in self._dependencies
