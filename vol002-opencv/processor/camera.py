from io import BytesIO
from picamera import PiCamera, PiCameraCircularIO
from picamera.exc import PiCameraValueError
from picamera.frames import PiVideoFrameType


class Camera:
    SIZE_WIDTH = 720
    SIZE_HEIGHT = 480

    CAPTURE_BEFORE_TIME = 5  # sec
    CAPTURE_AFTER_TIME = 5  # sec

    def __init__(self):
        self._camera = None
        self._stream = None

    def __del__(self):
        self.stop()

    def start(self):
        try:
            self._camera = PiCamera()
            self._camera.resolution = (self.SIZE_WIDTH, self.SIZE_HEIGHT)
            self._camera.brightness = 50

            self._stream = PiCameraCircularIO2(self._camera, seconds=self.CAPTURE_BEFORE_TIME + self.CAPTURE_AFTER_TIME)
            self._camera.start_recording(self._stream, format='h264')
            self._camera.wait_recording(self.CAPTURE_BEFORE_TIME)
        except:
            self.stop()

    def stop(self):
        if not self._camera:
            self._camera.stop_recording()
            self._camera.close()
            self._camera = None

    def take_photo(self):
        stream = BytesIO()
        self._camera.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)
        return stream

    def record_video(self):
        return self._stream.copy_to_stream(seconds=self.CAPTURE_BEFORE_TIME + self.CAPTURE_AFTER_TIME).read()


class PiCameraCircularIO2(PiCameraCircularIO):
    def copy_to_stream(self, size=None, seconds=None, first_frame=PiVideoFrameType.sps_header):
        if size is not None and seconds is not None:
            raise PiCameraValueError('You cannot specify both size and seconds')

        stream = BytesIO()

        with self.lock:
            save_pos = self.tell()

            try:
                if size is not None:
                    pos = self._find_size(size, first_frame)
                elif seconds is not None:
                    pos = self._find_seconds(seconds, first_frame)
                else:
                    pos = self._find_all(first_frame)

                if pos is not None:
                    self.seek(pos)

                    while True:
                        buf = self.read1()

                        if not buf:
                            break

                        stream.write(buf)

            finally:
                self.seek(save_pos)

        stream.seek(0)
        return stream
