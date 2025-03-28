import cv2 as cv
import numpy as np
import threading

class pyCamera:
  def __init__(self, camera_index:int = 0, start_capture:bool=True) -> None:
    self.init = False  # Ensure init flag is set initially
    self.lock = threading.Lock()  # Thread lock for shared resources
        
    try:
      self.vid = cv.VideoCapture(camera_index)
      if not self.vid.isOpened():
        raise Exception("Could not open camera.")
    except Exception as e:
      print(f"Unable to initialize camera: {e}")
      return
    
    ret, frame = self.vid.read()
    if not ret or frame is None:
        print("Failed to read from camera.")
        self.vid.release()
        return
      
    # image size or you can get this from image shape
    self.frame_width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
    self.frame_height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)
    self.video_fps = self.vid.get(cv.CAP_PROP_FPS)
    
    self.is_active:bool = start_capture
    self.framebuffer = [None, None]  # Initialize framebuffer with None
    self.cFrame:int = 0
    self.capture_thread = None  # Initialize thread variable
    self.init = True  # Mark initialization as successful
    
    if self.is_active:
        self.start_capture()
  
  def __del__(self) -> None:
    if self.init:
      self.stop_capture()
      if self.capture_thread and self.capture_thread.is_alive():
          self.capture_thread.join()
      self.vid.release()
    
  def get_frame_size(self) -> tuple[int, int]:
    return (int(self.frame_width), int(self.frame_height)) if self.init else (0, 0)
  
  def get_fps(self) -> float:
    return self.video_fps if self.init else 0.0
  
  def get_framebuffer(self) -> np.ndarray|None:
    if not self.init:
      return None
    with self.lock:
      return self.framebuffer[self.cFrame]

  def start_capture(self) -> bool:
    if not self.init or (self.capture_thread and self.capture_thread.is_alive()):
        return False
    
    self.is_active = True
    self.capture_thread = threading.Thread(target=self.__capture_loop, daemon=True)
    self.capture_thread.start()
    return True
    
  def stop_capture(self) -> None:
    self.is_active = False
    if self.capture_thread and self.capture_thread.is_alive():
        self.capture_thread.join()
    
  def set_capture(self, capture_flag) -> None:
    self.is_active = capture_flag
  
  def __capture_loop(self) -> None:
    while self.is_active:
      self.__capture_frame()
  
  def __capture_frame(self) -> bool:
    is_valid_frame, frame = self.vid.read()
    if not is_valid_frame or frame is None:
      print("Frame not valid")
      return False
    
    frame_texture = self.__prepare_cv_framebuffer(frame)
    with self.lock:
      #increment current framebuffer index
      self.cFrame = (self.cFrame + 1) % len(self.framebuffer)
      #update current framebuffer texture
      self.framebuffer[self.cFrame] = frame_texture
      
    return True
  
  def __prepare_cv_framebuffer(self, frame) -> np.ndarray[tuple[int], np.dtype[np.float32]]:
      data = np.flip(frame, 2)  # Convert BGR to RGB
      data = data.astype(np.float32) / 255.0  # Normalize and convert to float32
      return data.ravel()
  