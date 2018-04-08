import bpy
import bpy_extras
import mathutils
import math

bl_info = {
	"name": "Maki's Blender Tools",
	"author": "Maki",
	"version": (1, 0),
	"blender": (2, 79, 0),
	"location": "View 3D > Tool Shelf > Maki",
	"description": "A bunch of useful tools to make my life more useful!",
	"warning": "",
	"wiki_url": "https://github.com/makixx/makis-blender-tools",
	"tracker_url": "https://github.com/makixx/makis-blender-tools/issues",
	"category": "3D View",
}

class IcoPlane(bpy.types.Operator, bpy_extras.object_utils.AddObjectHelper):
	bl_idname = "mesh.add_icoplane"
	bl_label = "Ico Plane"
	bl_options = {"REGISTER", "UNDO"}

	width = bpy.props.IntProperty(name="Width", default=6, min=1)
	height = bpy.props.IntProperty(name="Height", default=6, min=1)

	magicNumber = math.tan(math.radians(60))*0.5

	def draw(self, context):
		self.layout.prop(self, "width")
		self.layout.prop(self, "height")
		# self.layout.separator()
		# self.layout.prop(self, "location")
		# self.layout.prop(self, "rotation")

	def generate(self, w, h):
		sx = -(w/2)
		sy = -(h/2)

		verts = []
		faces = []

		for y in range(0, h+1):
			if (y%2 == 0): # odd rows (first)
				i = len(verts)
				for x in range(0, w+1):
					verts.append(mathutils.Vector((sx+x, (-sy-y)*self.magicNumber, 0)))

				if (y>=h): continue # not the bottom
				for x in range(0, w): # V faces
					faces.append([i+x+1, i+x, i+x+w+1])
				for x in range(0, w-1): # ^'s in between V's
					faces.append([i+x+1, i+x+w+1, i+x+w+2])

			else: # even rows (second)
				i = len(verts)
				for x in range(0, w):
					verts.append(mathutils.Vector((sx+x+0.5, (-sy-y)*self.magicNumber, 0)))

				if (y>=h): continue # not the bottom
				for x in range(0, w):
					faces.append([i+x, i+x+w, i+x+w+1])
				for x in range(0, w-1):
					faces.append([i+x, i+x+w+1, i+x+1])

		return [verts, faces]

	def execute(self, context):
		data = self.generate(self.width, self.height)

		mesh = bpy.data.meshes.new(name="Ico Plane")
		mesh.from_pydata(data[0], [], data[1])
		mesh.update(calc_edges=True)
		bpy_extras.object_utils.object_data_add(context, mesh, operator=self)

		return {"FINISHED"}

class ToolPanel(bpy.types.Panel):
	bl_label = "Maki's Tools"
	bl_idname = "3D_VIEW_TS_maki"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Maki"

	def draw(self, context):
		layout = self.layout

		obj = context.object

		row = layout.row()
		row.label(text="Add Mesh", icon="MESH_DATA")

		row = layout.row()
		row.operator("mesh.add_icoplane")


def register():
	bpy.utils.register_class(IcoPlane)
	bpy.utils.register_class(ToolPanel)

def unregister():
	bpy.utils.unregister_class(IcoPlane)
	bpy.utils.unregister_class(ToolPanel)

if __name__ == "__main__":
	register()