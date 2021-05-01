import bpy

class SplitFlapPanel(bpy.types.Panel):
	bl_idname = "VIEW3D_PT_maki_split_flap_panel"
	bl_label = "Split Flap Creator"
	bl_icon = "MESH_DATA"
	bl_category = "Maki"

	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	def draw(self, context):
		layout = self.layout

		layout.label(text="Yay lets make a split flap!")

		layout.operator("maki.add_split_flap", text="Split Flap")
