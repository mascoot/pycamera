from camera import pycamera as pyc
import dearpygui.dearpygui as dpg
import threading

def save_callback():
      print("Save Clicked")
      
if __name__ == "__main__":
  
  camera = pyc.pyCamera(start_capture=True)
  
  dpg.create_context()
  dpg.create_viewport(title='pyCameraCalibration', width=1280, height=720)
  dpg.setup_dearpygui()
  
  texture_data = camera.get_framebuffer()
  frame_size = camera.get_frame_size()
  dummy_data = [255] * int(frame_size[1] * frame_size[0])

  with dpg.texture_registry(show=False):
    dpg.add_raw_texture(frame_size[0], frame_size[1], dummy_data, tag="cvFramebuffer", format=dpg.mvFormat_Float_rgb)
    
  with dpg.window(label="Example Window"):
    dpg.add_image("cvFramebuffer")
   
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