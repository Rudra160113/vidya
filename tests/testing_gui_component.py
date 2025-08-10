# File location: vidya/tests/testing_gui_component.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.gui.gui_component_renderer import GUIComponentRenderer

class TestingGUIComponent:
    """
    A suite of tests to verify the functionality of the GUIComponentRenderer.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.renderer = GUIComponentRenderer()
        logging.info("TestingGUIComponent initialized.")
    
    def test_render_button_component(self) -> bool:
        """Tests if a button component is rendered correctly."""
        component_data = {
            "type": "button",
            "text": "Click Me",
            "props": {"class": "btn-primary", "onClick": "handleButtonClick"}
        }
        
        rendered_html = self.renderer.render_component(component_data)
        
        # Check if the core elements are in the rendered HTML
        return 'button' in rendered_html and 'Click Me' in rendered_html and 'btn-primary' in rendered_html

    def test_render_text_component(self) -> bool:
        """Tests if a text component is rendered correctly."""
        component_data = {
            "type": "text",
            "content": "Hello, Vidya!",
            "props": {"class": "text-lg"}
        }
        
        rendered_html = self.renderer.render_component(component_data)
        
        # Check if the content and properties are present
        return 'div' in rendered_html and 'Hello, Vidya!' in rendered_html and 'text-lg' in rendered_html

    def test_render_unknown_component(self) -> bool:
        """Tests if an unknown component type is handled gracefully."""
        component_data = {
            "type": "unknown_type",
            "content": "This shouldn't be rendered."
        }
        
        rendered_html = self.renderer.render_component(component_data)
        
        # The renderer should return an error message or an empty string
        return 'Error: Unknown component type' in rendered_html

    def run_all_tests(self):
        """Runs all GUI component tests."""
        self.test_runner.run_test("Render Button Test", self.test_render_button_component)
        self.test_runner.run_test("Render Text Test", self.test_render_text_component)
        self.test_runner.run_test("Render Unknown Component Test", self.test_render_unknown_component)
        self.test_runner.print_summary()
