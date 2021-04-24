bl_info = {
    "name": "Maki's Blender Tools",
    "author": "Maki",
    "description": "Makes things!",
    "version": (0, 0, 1),
    "blender": (2, 91, 0),
    "location": "View 3D > Tool Shelf > Maki",
    "warning": "",
    "wiki_url": "https://github.com/makitsune/makis-blender-tools",
    "tracker_url": "https://github.com/makitsune/makis-blender-tools/issues",
    "category": "3D View",
}

import bpy
from bpy.utils import register_class, unregister_class

from .operators.meshes.add_ico_plane import *
from .operators.meshes.add_subdivided_plane import *

from .panels.meshes_panel import *

classes = (
    # operators
    AddIcoPlane,
    AddSubdividedPlane,
    # panels
    MeshesPanel
)

# main_register, main_unregister = bpy.utils.register_classes_factory(classes)

def register():
	# main_register()
	for cls in classes:
		try:
			bpy.utils.register_class(cls)
		except Exception as e:
			print("ERROR: Failed to register class {0}: {1}".format(cls, e))

def unregister():
	# main_unregister()
	for cls in classes:
		try:
			bpy.utils.unregister_class(cls)
		except Exception as e:
			print("ERROR: Failed to unregister class {0}: {1}".format(cls, e))
