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
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView

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
        """Main method to build the UI."""
        Window.clearcolor = (1, 1, 1, 1)  # RGBA: White background

        # Wrapping the main container in a ScrollView
        scroll_view = ScrollView(size_hint=(1, 1))

        # Create the main grid container
        grid_container = self.create_main_container()

        # Add the grid container to the ScrollView
        scroll_view.add_widget(grid_container)

        return scroll_view

    def create_main_container(self):
        """Create the main grid container."""
        grid_container = GridLayout(cols=1, size_hint_y=None, padding=20, spacing=20)
        grid_container.bind(minimum_height=grid_container.setter('height'))  # Adjust height dynamically

        # Add title
        grid_container.add_widget(self.create_title())

        # Add form container
        grid_container.add_widget(self.create_form_container())

        # Add button container
        grid_container.add_widget(self.create_button_container())

        # Add image container
        self.image_container = self.create_image_container()
        grid_container.add_widget(self.image_container)

        return grid_container

    def create_title(self):
        """Create the title label."""
        return Label(
            text="K-Means Clustering App",
            font_size=30,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=50
        )

    def create_form_container(self):
        """Create the form container with input fields."""
        form_container = GridLayout(cols=2, size_hint=(1, None), height=200, spacing=10)

        # Dataset path
        form_container.add_widget(Label(
            text="Selecciona el archivo del dataset:",
            font_size=15,
            color=(0, 0, 0, 1),
            size_hint=(0.4, None),
            height=30
        ))
        self.file_path = TextInput(size_hint=(0.6, None), height=30, readonly=True)  # Read-only TextInput
        form_container.add_widget(self.file_path)

        # Add a button to open the file chooser
        form_container.add_widget(Label(size_hint=(0.4, None), height=30))  # Empty label for alignment
        file_chooser_button = Button(
            text="Seleccionar archivo",
            size_hint=(0.6, None),
            height=30,
            background_color=(0.2, 0.6, 0.8, 1)  # Blue button
        )
        file_chooser_button.bind(on_press=lambda instance: self.open_file_chooser())
        form_container.add_widget(file_chooser_button)

        # Number of centroids
        form_container.add_widget(Label(
            text="Ingresa el número de centroides:",
            font_size=15,
            color=(0, 0, 0, 1),
            size_hint=(0.4, None),
            height=30
        ))
        self.centroids = TextInput(input_filter="int", size_hint=(0.6, None), height=30)
        form_container.add_widget(self.centroids)

        # Maximum iterations
        form_container.add_widget(Label(
            text="Ingresa las iteraciones máximas:",
            font_size=15,
            color=(0, 0, 0, 1),
            size_hint=(0.4, None),
            height=30
        ))
        self.iterations = TextInput(input_filter="int", size_hint=(0.6, None), height=30)
        form_container.add_widget(self.iterations)

        return form_container

    def create_button_container(self):
        """Create the container for the buttons."""
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

        return button_container

    def create_image_container(self):
        """Create the container for displaying the image."""
        return BoxLayout(size_hint=(1, None), height=600, padding=10)

    def restart_form(self, instance):
        """Reset the form inputs."""
        self.file_path.text = ""
        self.centroids.text = ""
        self.iterations.text = ""
        self.image_container.clear_widgets()  # Clear the image container

    def show_graphics(self, instance):
        """Main method to handle the 'Mostrar Gráficos' button press."""
        try:
            file_path, num_centroids, max_iterations = self.validate_inputs()
            dataset = self.load_dataset(file_path)
            filtered_dataset = self.validate_columns(dataset)
            img = self.plot_3d_graph(filtered_dataset, num_centroids, max_iterations)
            self.display_image(img)
        except ValueError as ve:
            self.show_error_popup(f"Error de validación: {str(ve)}")
        except FileNotFoundError as fnfe:
            self.show_error_popup(f"Error de archivo: {str(fnfe)}")
        except KmeansError as ke:
            self.show_error_popup(f"Error en K-Means: {str(ke)}")
        except Exception as e:
            self.show_error_popup(f"Error inesperado: {str(e)}")

    def validate_inputs(self):
        """Validate user inputs and return them."""
        file_path = self.file_path.text.strip()
        if not file_path:
            raise ValueError("Debe seleccionar un archivo para el dataset.")

        centroids_text = self.centroids.text.strip()
        if not centroids_text:
            raise ValueError("El campo 'Número de centroides' no puede estar vacío.")
        try:
            num_centroids = int(centroids_text)
            if num_centroids <= 0:
                raise ValueError("El número de centroides debe ser un entero positivo.")
        except ValueError:
            raise ValueError("El campo 'Número de centroides' debe contener un número entero válido.")

        iterations_text = self.iterations.text.strip()
        if not iterations_text:
            raise ValueError("El campo 'Iteraciones máximas' no puede estar vacío.")
        try:
            max_iterations = int(iterations_text)
            if max_iterations <= 0:
                raise ValueError("El número de iteraciones debe ser un entero positivo.")
        except ValueError:
            raise ValueError("El campo 'Iteraciones máximas' debe contener un número entero válido.")

        return file_path, num_centroids, max_iterations

    def load_dataset(self, file_path):
        """Load the dataset from the given file path."""
        try:
            dataset = pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo en la ruta: {file_path}")
        except pd.errors.EmptyDataError:
            raise ValueError("El archivo está vacío o no contiene datos válidos.")
        except pd.errors.ParserError:
            raise ValueError("El archivo no tiene un formato válido. Asegúrese de que sea un archivo CSV.")
        except Exception as e:
            raise ValueError(f"Error al cargar el archivo: {str(e)}")
        return dataset

    def validate_columns(self, dataset):
        """Validate that the dataset contains the required columns."""
        required_columns = ["GDP_per_capita", "life_expectancy", "literacy_rate"]
        missing_columns = [col for col in required_columns if col not in dataset.columns]
        if missing_columns:
            raise ValueError(f"Faltan las siguientes columnas en el dataset: {', '.join(missing_columns)}")
        return dataset[required_columns]

    def plot_3d_graph(self, dataset, num_centroids, max_iterations):
        """Run K-Means, plot the 3D graph, and return the image texture."""
        kmeans = Kmeans(dataset, num_centroids, max_iterations)
        centroids_list, updated_dataset = kmeans.k_means_logic()

        # Plot 3D graph
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
        return CoreImage(buf, ext="png").texture

    def display_image(self, img):
        """Display the generated image in the image container."""
        self.image_container.clear_widgets()  # Clear any existing image
        image = Image(texture=img, size_hint=(1, None), height=self.image_container.height)  # Adjust image scaling
        self.image_container.add_widget(image)

    def show_error_popup(self, message):
        """Display an error popup with a user-friendly message."""
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add a Label with wrapped text
        error_label = Label(
            text=message,
            color=(1, 0, 0, 1),  # Red text for errors
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

    def open_file_chooser(self):
        """Open a popup with a FileChooser to select a file."""
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # FileChooser widget
        file_chooser = FileChooserListView(size_hint=(1, 0.8))
        box.add_widget(file_chooser)

        # Buttons for selecting or canceling
        button_box = BoxLayout(size_hint=(1, 0.2), spacing=10)
        select_button = Button(text="Seleccionar", size_hint=(0.5, 1))
        cancel_button = Button(text="Cancelar", size_hint=(0.5, 1))
        button_box.add_widget(select_button)
        button_box.add_widget(cancel_button)
        box.add_widget(button_box)

        # Popup to hold the FileChooser
        popup = Popup(title="Seleccionar archivo", content=box, size_hint=(0.9, 0.9))

        # Bind button actions
        select_button.bind(on_press=lambda instance: self.select_file(file_chooser, popup))
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()

    def select_file(self, file_chooser, popup):
        """Handle file selection and close the popup."""
        selected_file = file_chooser.selection
        if selected_file:
            self.file_path.text = selected_file[0]  # Update the file path field
        popup.dismiss()


if __name__ == "__main__":
    KmeansApp().run()