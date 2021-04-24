import bpy

class MeshesPanel(bpy.types.Panel):
	bl_idname = "VIEW3D_PT_maki_meshes_panel"
	bl_label = "Meshes"
	bl_icon = "MESH_DATA"
	bl_category = "Maki"

	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	def draw(self, context):
		layout = self.layout

		row = layout.row()
		row.operator("maki.add_ico_plane", text="Ico Plane")

		row = layout.row()
		row.operator("maki.add_subdivided_plane", text="Subdivided Plane")
