from camera import pycamera as pyc
import dearpygui.dearpygui as dpg

VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
IMGUI_DEFAULT_PADDING = 20

def save_callback():
      print("Save Clicked")

def image_resize(sender, app_data, user_data):
      img_scale = app_data
      offset = int((VIEWPORT_WIDTH - int(VIEWPORT_WIDTH * img_scale))*0.5) - IMGUI_DEFAULT_PADDING
      scaled_width = int(VIEWPORT_WIDTH * img_scale)
      scaled_height = int(VIEWPORT_HEIGHT * img_scale)
      dpg.set_item_width("img_frame", scaled_width)
      dpg.set_item_height("img_frame", scaled_height)
      dpg.configure_item("img_frame", width=scaled_width, height=scaled_height, indent=offset)
  
if __name__ == "__main__":
  
  camera = pyc.pyCamera(start_capture=True)
  
  dpg.create_context()
  dpg.create_viewport(title='pyCameraCalibration', width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)
  dpg.setup_dearpygui()
  
  texture_data = camera.get_framebuffer()
  frame_size = camera.get_frame_size()
  dummy_data = [255.0] * int(frame_size[1] * frame_size[0])

  with dpg.texture_registry(show=False):
    dpg.add_raw_texture(frame_size[0], frame_size[1], dummy_data, tag="cvFramebuffer", format=dpg.mvFormat_Float_rgb)
  
  img_scale = 0.8  
  offset = int((VIEWPORT_WIDTH - int(VIEWPORT_WIDTH * img_scale))*0.5) - IMGUI_DEFAULT_PADDING
  scaled_width = int(VIEWPORT_WIDTH * img_scale)
  scaled_height = int(VIEWPORT_HEIGHT * img_scale)
  with dpg.window(label="Example Window", tag="main_window"):
    dpg.add_text("pyCamera Calibration")
    dpg.add_slider_float(label="Zoom", default_value=img_scale, min_value=0.1, max_value=2.0, callback=image_resize)
    dpg.add_image("cvFramebuffer", tag="img_frame", width=scaled_width, height=scaled_height, indent=offset)
  
  dpg.set_primary_window("main_window", True)
  dpg.show_metrics() 
  dpg.show_viewport()
  while dpg.is_dearpygui_running():
    # updating the texture in a while loop the frame rate will be limited to the camera frame rate.
    # commenting out the "ret, frame = vid.read()" 
    # line will show the full speed that operations and updating a texture can run at
    texture_data = camera.get_framebuffer()
    if texture_data is not None:
      dpg.set_value("cvFramebuffer", texture_data)
    dpg.render_dearpygui_frame()
    
  dpg.destroy_context()