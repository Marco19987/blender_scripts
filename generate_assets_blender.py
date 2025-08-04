# This script automates the assets generation process for publishing the model on turboSquid

import bpy
import os
import math
import shutil


# === CONFIGURATION ===
model_name = bpy.context.active_object.name
base_folder = bpy.path.abspath(f"C:/Users/marco/{model_name}_package")
preview_folder = os.path.join(base_folder, "previews")
export_folder = os.path.join(base_folder, "exports")
texture_folder = os.path.join(base_folder, "textures")

steps = 8  # Turntable steps
uv_size = (2048, 2048)

# === CREATE FOLDERS ===
for folder in [base_folder, preview_folder, export_folder, texture_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# === TURNABLE RENDERS ===
obj = bpy.data.objects[model_name]
obj.rotation_mode = 'XYZ'
scene = bpy.context.scene

for i in range(steps):
    angle = math.radians((360 / steps) * i)
    obj.rotation_euler = (0, 0, angle)
    scene.render.filepath = os.path.join(preview_folder, f"turntable_{i:02d}.png")
    #bpy.ops.render.render(write_still=True)

# === UV LAYOUT EXPORT ===
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.export_layout(filepath=os.path.join(preview_folder, "UV_Layout.png"),
                         size=uv_size,
                         export_all=True)
bpy.ops.object.mode_set(mode='OBJECT')

# === WIREFRAME RENDER ===
scene.render.use_freestyle = True
view_layer = bpy.context.view_layer
view_layer.use_freestyle = True

# Configure Freestyle
freestyle_settings = view_layer.freestyle_settings
line_set = freestyle_settings.linesets.active
line_set.select_edge_mark = False
line_set.select_crease = False
line_set.select_border = True
line_set.select_contour = True
line_set.select_external_contour = True


# Render wireframe
scene.render.filepath = os.path.join(preview_folder, "Wireframe.png")
bpy.ops.render.render(write_still=True)

# Disable Freestyle after render
scene.render.use_freestyle = False
view_layer.use_freestyle = False

# === EXPORT FORMATS ===
export_formats = {
    #"OBJ": os.path.join(export_folder, f"{model_name}.obj"),
    "FBX": os.path.join(export_folder, f"{model_name}.fbx"),
    "GLB": os.path.join(export_folder, f"{model_name}.glb"),
}

bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

# Export OBJ
#bpy.ops.export_scene.obj(filepath=export_formats["OBJ"], use_selection=True)

# Export FBX
bpy.ops.export_scene.fbx(filepath=export_formats["FBX"], use_selection=True)

# Export GLB
bpy.ops.export_scene.gltf(filepath=export_formats["GLB"], export_format='GLB', use_selection=True)

# === COPY TEXTURES ===
for image in bpy.data.images:
    if image.filepath and os.path.exists(bpy.path.abspath(image.filepath)):
        src = bpy.path.abspath(image.filepath)
        dst = os.path.join(texture_folder, os.path.basename(src))
        shutil.copy2(src, dst)

# === PACKAGE EVERYTHING ===
package_path = os.path.join("C:/Users/marco", f"{model_name}_TurboSquid.zip")
shutil.make_archive(package_path.replace(".zip", ""), 'zip', base_folder)

print(f"✅ Package created: {package_path}")
