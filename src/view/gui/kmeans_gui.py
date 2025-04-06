from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import sys
sys.path.append("src")

from model.kmeans_logic import Kmeans
from model.errors.kmeans_error import KmeansError

class KmeansApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # RGBA: White background

        # Building the main Grid Container
        grid_container = GridLayout(cols=1, size=(Window.width, Window.height), padding=100, spacing=30)

        grid_container.add_widget(Label(text="K-Means Clustering App", font_size=30, bold=True, color=(0, 0, 0, 1)))

        # Building form container with labels and TextInputs
        form_container = GridLayout(rows=6)

        form_container.add_widget(Label(text="Ingresa la ruta del dataset:", font_size=15, color=(0, 0, 0, 1)))  # Black text
        self.file_path = TextInput(size_hint_y=None, height=30)

        form_container.add_widget(self.file_path)

        form_container.add_widget(Label(text="Ingresa el numero de centrodes:", font_size=15, color=(0, 0, 0, 1)))  # Black text
        self.centroids = TextInput(input_filter="int", size_hint_y=None, height=30)

        form_container.add_widget(self.centroids)

        form_container.add_widget(Label(text="Ingresa las iteraciones que deseas realizar:", font_size=15, color=(0, 0, 0, 1)))  # Black text
        self.iterations = TextInput(input_filter="int", size_hint_y=None, height=30)

        form_container.add_widget(self.iterations)

        # Adding the form container
        grid_container.add_widget(form_container)

        # Creating a container for the buttons
        button_container = GridLayout(cols=2, size_hint=(1, None), height=50, spacing=10)

        # Submit button
        submit_button = Button(
            text="Mostrar Gráficos",
            font_size=20,
            size_hint=(1, 1),
            background_normal='',
            background_color=(0.75, 0.48, 0.12, 0.8)
        )
        submit_button.bind(on_press=self.show_graphics)
        button_container.add_widget(submit_button)

        # Restart button
        restart_button = Button(
            text="Reiniciar",
            font_size=20,
            size_hint=(1, 1),
            background_normal='',
            background_color=(1, 0, 0, 1),  # Red background
            color=(1, 1, 1, 1)  # White text
        )
        restart_button.bind(on_press=self.restart_form)
        button_container.add_widget(restart_button)

        # Adding the button container to the grid
        grid_container.add_widget(button_container)

        return grid_container

    def restart_form(self, instance):
        """Reset the form inputs."""
        self.file_path.text = ""
        self.centroids.text = ""
        self.iterations.text = ""

    def show_graphics(self, instance):
        try:
            # Read inputs
            file_path = self.file_path.text
            num_centroids = int(self.centroids.text)
            max_iterations = int(self.iterations.text)

            # Load dataset
            dataset = pd.read_csv(file_path)
            filtered_dataset = dataset[["GDP_per_capita", "life_expectancy", "literacy_rate"]]

            # Run K-Means
            kmeans = Kmeans(filtered_dataset, num_centroids, max_iterations)
            centroids_list, updated_dataset = kmeans.k_means_logic()

            # Plot 3D graph and save as image
            figure_3d = plt.figure(figsize=(10, 8))
            axis_3d = figure_3d.add_subplot(111, projection="3d")

            scatter = axis_3d.scatter(
                updated_dataset["GDP_per_capita"],
                updated_dataset["life_expectancy"],
                updated_dataset["literacy_rate"],
                c=updated_dataset["assigned_cluster"],
                cmap="viridis",
                s=100,
            )

            centroid_centers_np = np.array(centroids_list)

            axis_3d.scatter(
                centroid_centers_np[:, 0],
                centroid_centers_np[:, 1],
                centroid_centers_np[:, 2],
                c="blue",
                marker="X",
                s=250,
                linewidths=2,
                edgecolors="black",
            )

            axis_3d.set_xlabel("GDP per capita (normalizado)")
            axis_3d.set_ylabel("Life expectancy (normalizado)")
            axis_3d.set_zlabel("Literacy rate (normalizado)")
            plt.title("Gráfico 3D de clusters")
            plt.colorbar(scatter, label="Cluster")

            # Save the plot to a BytesIO object
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close(figure_3d)

            # Convert the image to a Kivy-compatible format
            img = CoreImage(buf, ext="png").texture

            # Display the image in a popup
            self.show_image_popup(img)

        except KmeansError as e:
            self.show_error_popup(str(e))
        except Exception as e:
            self.show_error_popup(f"Error inesperado: {str(e)}")

    def show_image_popup(self, img_texture):
        # Create a popup to display the image
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        image = Image(texture=img_texture)
        box.add_widget(image)

        close_button = Button(text="Cerrar", size_hint=(1, 0.2))
        box.add_widget(close_button)

        popup = Popup(title="Gráfico de Clusters", content=box, size_hint=(0.9, 0.9))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def show_error_popup(self, message):
        # Display an error popup
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add a Label with wrapped text
        error_label = Label(
            text=message,
            color=(1, 0, 0, 1),
            halign="center",  # Center-align the text horizontally
            valign="middle",  # Center-align the text vertically
            text_size=(Window.width * 0.7, None)  # Limit the width for wrapping
        )
        error_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        box.add_widget(error_label)

        # Add a close button
        close_button = Button(text="Cerrar", size_hint=(1, 0.2))
        box.add_widget(close_button)

        # Create and open the popup
        popup = Popup(title="Error", content=box, size_hint=(0.8, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == "__main__":
    KmeansApp().run()