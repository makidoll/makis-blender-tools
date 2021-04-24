import bpy
import bpy_extras
import mathutils
import math

class AddIcoPlane(bpy.types.Operator, bpy_extras.object_utils.AddObjectHelper):
	bl_idname = "maki.add_ico_plane"
	bl_label = "Add Ico Plane"
	bl_options = {"REGISTER", "UNDO", "INTERNAL"}

	width: bpy.props.IntProperty(name="Width", default=6, min=1)
	height: bpy.props.IntProperty(name="Height", default=6, min=1)

	def draw(self, context):
		self.layout.prop(self, "width")
		self.layout.prop(self, "height")
		# self.layout.separator()
		# self.layout.prop(self, "location")
		# self.layout.prop(self, "rotation")

	def generate(self, w, h):
		sx = -(w / 2)
		sy = -(h / 2)

		verts = []
		faces = []

		magicNumber = math.tan(math.radians(60)) * 0.5

		for y in range(0, h + 1):
			if (y % 2 == 0):  # odd rows (first)
				i = len(verts)
				for x in range(0, w + 1):
					verts.append(
					    mathutils.Vector((sx + x, (-sy - y) * magicNumber, 0))
					)

				if (y >= h):
					continue  # not the bottom
				for x in range(0, w):  # V faces
					faces.append([i + x + 1, i + x, i + x + w + 1])
				for x in range(0, w - 1):  # ^'s in between V's
					faces.append([i + x + 1, i + x + w + 1, i + x + w + 2])

			else:  # even rows (second)
				i = len(verts)
				for x in range(0, w):
					verts.append(
					    mathutils.Vector(
					        (sx + x + 0.5, (-sy - y) * magicNumber, 0)
					    )
					)

				if (y >= h):
					continue  # not the bottom
				for x in range(0, w):
					faces.append([i + x, i + x + w, i + x + w + 1])
				for x in range(0, w - 1):
					faces.append([i + x, i + x + w + 1, i + x + 1])

		return [verts, faces]

	def execute(self, context):
		data = self.generate(self.width, self.height)

		mesh = bpy.data.meshes.new(name="Ico Plane")
		mesh.from_pydata(data[0], [], data[1])
		mesh.update(calc_edges=True)
		bpy_extras.object_utils.object_data_add(context, mesh, operator=self)

		return {"FINISHED"}
