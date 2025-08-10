# File location: vidya/utils/documentation_generator.py

import inspect
import os
import logging

class DocumentationGenerator:
    """
    Automatically generates documentation from source code docstrings.
    """
    def __init__(self, output_dir: str = 'docs'):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        logging.info("DocumentationGenerator initialized.")

    def generate_for_module(self, module, file_name: str = None) -> str:
        """
        Generates documentation for a given Python module.
        """
        if not file_name:
            file_name = f"{module.__name__}.md"
            
        output_path = os.path.join(self.output_dir, file_name)
        
        with open(output_path, 'w') as f:
            f.write(f"# Module: `{module.__name__}`\n\n")
            f.write(f"{inspect.getdoc(module)}\n\n")
            f.write("---\n\n")
            
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) or inspect.isfunction(obj):
                    if obj.__module__ == module.__name__:
                        f.write(f"## {obj.__name__}\n\n")
                        f.write(f"```python\n{inspect.signature(obj)}\n```\n\n")
                        f.write(f"{inspect.getdoc(obj)}\n\n")
                        f.write("---\n\n")
        
        logging.info(f"Documentation for '{module.__name__}' generated at '{output_path}'.")
        return f"Documentation for module '{module.__name__}' created."
