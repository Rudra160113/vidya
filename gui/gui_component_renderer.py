# File location: vidya/gui/gui_component_renderer.py

import logging
from typing import Dict, Any

class GUIComponentRenderer:
    """
    Renders structured data into GUI components (e.g., HTML).
    """
    def __init__(self):
        self.component_map = {
            "text": self._render_text,
            "button": self._render_button,
            # Other components would be added here
        }
        logging.info("GUIComponentRenderer initialized.")

    def _render_text(self, component: Dict) -> str:
        """Renders a text component into an HTML div."""
        content = component.get("content", "")
        props_str = self._format_props(component.get("props", {}))
        return f'<div {props_str}>{content}</div>'

    def _render_button(self, component: Dict) -> str:
        """Renders a button component into an HTML button element."""
        text = component.get("text", "")
        props_str = self._format_props(component.get("props", {}))
        return f'<button {props_str}>{text}</button>'

    def _format_props(self, props: Dict) -> str:
        """Formats a dictionary of properties into an HTML attribute string."""
        return " ".join([f'{key}="{value}"' for key, value in props.items()])

    def render_component(self, component_data: Dict) -> str:
        """
        Renders a GUI component from its data representation.
        
        Args:
            component_data (Dict): A dictionary describing the component.
            
        Returns:
            str: The rendered component string (e.g., HTML).
        """
        component_type = component_data.get("type")
        renderer = self.component_map.get(component_type)
        
        if renderer:
            return renderer(component_data)
        else:
            logging.error(f"Unknown component type: {component_type}")
            return f"Error: Unknown component type '{component_type}'."
