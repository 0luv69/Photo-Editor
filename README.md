## Get tutorial Video : https://youtu.be/srPU6JW-RRA?si=SS_mkqRIsSJEfAZz
# Photo-Editor


## Project Description
Welcome to the Photo Editor App, a versatile application crafted with Tkinter, offering a diverse array of robust features. Our application provides users with intuitive tools to edit, enhance, and personalize their images with ease.Fell Free to Clone and Use For the needed purpose

## Features
1) ### Remove Background:
 - Effortlessly remove backgrounds from images. Just In one Click
2) ### Image Adjustment:
 - Manage Blur, Brightness, Saturation, and Contrast in images.
 - Adjust Color Hue to achieve the desired tone.
3) ### Drawing Tools:
 - Unleash your creativity by freely sketching on images using a pencil brush tool.
 - Customize brush sizes and colors to suit your preferences.
     
4) ### Image Manipulation:
 - Flip, Rotate, and Straighten images.
 - Fine-tune X and Y coordinates.
 - Crop images to desired proportions.
5) ### Effects:
   
 - Apply Blur effects.
 - Remove Backgrounds.
 - Manipulate Color Hues.


## Installation
-> To install and run the Photo Editor App, follow these steps:
  - Clone the repository from GitHub.
  - Navigate to the project directory,
  - ---->>>  **Install list Of library from `requirments.txt`**, 
  - Run python `main.py` to launch the application.


## How To use App
#### Get tutorial Video : https://youtu.be/srPU6JW-RRA?si=SS_mkqRIsSJEfAZz

Users can interact with the Photo Editor App by following these steps:

1. **Launch the App**: Upon running `main.py`, the Photo Editor App GUI will appear.

2. **Image Loading**: Click on the "Open Image" button to load an image from your file system.

4. **Basic Image Manipulation**:
   - Flip, Rotate, and Straighten images using the primary position segment.
   - Fine-tune X and Y coordinates.
   - Crop images to desired proportions.

5. **Color Adjustment**:
   - Convert images to Black and White.
   - Adjust Brightness, Saturation, and Contrast.

6. **Effects**:
   - Apply Blur effects.
   - Remove Backgrounds.
   - Manipulate Color Hues.

7. **Drawing**:
   - Use the pencil brush tool to draw on images.
   - Customize brush sizes and colors.
   - Zoom functionality available for precise drawing.

8. **Saving the Edited Image**: Click on the "Save Image" button to save your edited image.



# Code View: Photo Editor Application Overview

This code defines a photo editor application using Tkinter and PIL (Python Imaging Library). Let's break down the major components and functionalities:

## 1) Imports:

- Custom modules (`customtkinter`, `setting`, `menu`, `pannel`) and standard libraries (`tkinter`, `PIL`, `cv2`, `numpy`) are imported.
- `customtkinter` seems to be a custom module, possibly for customizing Tkinter widgets.

## 2) Window Class:

- Inherits from `customtkinter.CTk`.
- Initializes the main application window with specific geometry, title, and appearance settings.
- Sets up parameters, layouts, and canvas dimensions.
- Initializes various variables and lists for image manipulation and undo functionality.
- Calls the `ImageImport_pg1st` class to display the image import interface.
- Contains methods for image manipulation, display, cropping, zooming, and undo functionality.

## 3) ImageImport_pg1st Class:

- Inherits from `customtkinter.CTkFrame`.
- Represents the image import interface with an option to choose a file.
- Displays a placeholder for dragging and dropping an image file or a button to choose a file using a file dialog.
- Provides functionality to animate a loading message while waiting for the file to be selected.

## 4) CanvasImageOutput Class:

- Inherits from `tkinter.Canvas`.
- Represents the canvas where the edited image is displayed.
- Binds a function to handle resizing of the image when the canvas size changes.

## 5) Resolution_AND_zoom_bar Class:

- Inherits from `customtkinter.CTkFrame`.
- Represents the resolution and zoom control bar.
- Displays the current resolution and zoom level.
- Provides buttons to reset zoom, zoom in, and zoom out.
- Allows zooming using mouse wheel and updates the displayed image accordingly.

## And other modules.........................

Overall, this code sets up a basic photo editor application with functionalities like image import, manipulation, cropping, and zooming. It uses Tkinter for the GUI and PIL for image processing.


