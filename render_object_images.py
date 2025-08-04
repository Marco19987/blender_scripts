import bpy
import math
import os
from mathutils import Euler 

# 🔧 Parametri personalizzabili
output_folder = bpy.path.abspath("C:\\Users\\marco\\renders2")
steps = 24                                     # number of rotation steps (e.g. 24 = every 15°)
object_name = bpy.context.active_object.name   # or replace with your model name

# 📂 Create folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 🎯 Get object and camera
obj = bpy.data.objects[object_name]
obj.rotation_mode = 'XYZ'
camera = bpy.context.scene.camera

# 🔄 Rotate object and render
for i in range(steps):
    angle_deg = (360 / steps) * i
    angle_rad = math.radians(angle_deg)

    # Apply rotation (around Z-axis)
    obj.rotation_euler = (0, 0, angle_rad)
    

    # Set render path
    filename = f"turntable_{i:02d}.png"
    filepath = os.path.join(output_folder, filename)
    bpy.context.scene.render.filepath = filepath

    # Render and save
    bpy.ops.render.render(write_still=True)

print("✅ Done! All renders saved in:", output_folder)
