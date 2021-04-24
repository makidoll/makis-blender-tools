import bpy
import bpy_extras
import mathutils
import math

class AddSubdividedPlane(
    bpy.types.Operator, bpy_extras.object_utils.AddObjectHelper
):
	bl_idname = "maki.add_subdivided_plane"
	bl_label = "Add Subdivided Plane"
	bl_options = {"REGISTER", "UNDO", "INTERNAL"}

	width: bpy.props.IntProperty(name="Width", default=16, min=1)
	height: bpy.props.IntProperty(name="Height", default=16, min=1)
	dist: bpy.props.FloatProperty(name="Distance", default=0.1)

	def draw(self, context):
		self.layout.prop(self, "width")
		self.layout.prop(self, "height")
		self.layout.prop(self, "dist")

	def generate(self, w, h):
		verts = []
		faces = []

		for x in range(0, w):
			for y in range(0, h):
				cx = (x * self.dist) - (self.width * self.dist) / 2
				cy = (y * self.dist) - (self.height * self.dist) / 2
				verts.append(mathutils.Vector((cx, cy, 0)))
				verts.append(mathutils.Vector((cx + self.dist, cy, 0)))
				verts.append(mathutils.Vector((cx, cy + self.dist, 0)))
				verts.append(
				    mathutils.Vector((cx + self.dist, cy + self.dist, 0))
				)

				i = (x + (y * self.width)) * 4
				faces.append([i, i + 1, i + 3, i + 2])

		return [verts, faces]

	def execute(self, context):
		data = self.generate(self.width, self.height)

		mesh = bpy.data.meshes.new(name="Subdivided Plane")
		mesh.from_pydata(data[0], [], data[1])
		mesh.update(calc_edges=True)
		bpy_extras.object_utils.object_data_add(context, mesh, operator=self)

		return {"FINISHED"}
