# File location: vidya/features/data_visualizer.py

import logging
import matplotlib.pyplot as plt
import os

class DataVisualizer:
    """
    Creates various types of data visualizations (e.g., charts, graphs).
    """
    def __init__(self, output_dir: str = "visualizations"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        logging.info("DataVisualizer initialized.")

    def create_bar_chart(self, data: dict, title: str, x_label: str, y_label: str, filename: str) -> str:
        """
        Generates a bar chart from a dictionary of data.
        """
        try:
            keys = list(data.keys())
            values = list(data.values())
            
            plt.figure(figsize=(10, 6))
            plt.bar(keys, values)
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            
            output_path = os.path.join(self.output_dir, filename)
            plt.savefig(output_path)
            plt.close()
            
            logging.info(f"Bar chart saved to {output_path}.")
            return f"Bar chart '{title}' has been generated and saved."
        except Exception as e:
            logging.error(f"Failed to create bar chart: {e}")
            return "An error occurred while creating the bar chart."

    def create_line_chart(self, x_data: list, y_data: list, title: str, x_label: str, y_label: str, filename: str) -> str:
        """
        Generates a line chart from two lists of data.
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(x_data, y_data)
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.grid(True)
            
            output_path = os.path.join(self.output_dir, filename)
            plt.savefig(output_path)
            plt.close()
            
            logging.info(f"Line chart saved to {output_path}.")
            return f"Line chart '{title}' has been generated and saved."
        except Exception as e:
            logging.error(f"Failed to create line chart: {e}")
            return "An error occurred while creating the line chart."
