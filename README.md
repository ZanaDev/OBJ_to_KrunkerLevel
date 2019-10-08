# OBJ file to Krunker Level Data converter
This is a simple script for generating valid Krunker cubes from the OBJ file format. This tool is meant to be used in conjunction with an exported OBJ file from the BSP-editor [TrenchBroom 2](https://github.com/kduske/TrenchBroom)

## Preview
Timelapse video of a simple level: https://www.youtube.com/watch?v=6OV31OWCaxU

## Setup
Python version 3.7.3 or greater needs to be installed on your system before you can use this tool.

Extract the contents of this repository into a preferred directory

Modify KrunkerMapSettingsConfig.json to change the default values for various map settings, like the map name, lighting, fog, etc. **DO NOT ADJUST THE OBJECTS LIST**

Modify CompilerConfig.cfg to enable or disable various features of the compiler tool.

## Workflow
* Create rectangular prism brushes in [TrenchBroom 2](https://github.com/kduske/TrenchBroom) to construct a level
* Use File > Export > Wavefront OBJ...
* Drag and drop the valid OBJ file onto the OBJ_to_KrunkerLevel.py script
* Load the data from the generated Krunker_Level.txt in the same directory as the script into the Krunker map editor to see it in all its glory!

## Limitations
* This is a barebones tool for editing cubework. It has minimal features other than making cube basic cube editing much less tedious
* **No rotation support**, which may be good or bad depending on your perspective.
* The script is probably easy to break with invalid data passed into it. Be careful
* Make sure to use RECTANGULAR PRISMS ONLY, no other shapes. They may be valid in TrenchBroom 2, but they won't be in Krunker if the script even works in the first place

## Tips
* OBJ files can be loaded into Blender, which means you can use TrenchBroom 2 to easily create cubework, and then use my [Blender Export Tool for Krunker](https://github.com/ZanaDev/Krunker-Blender-Exporter) to apply finishing touches.
