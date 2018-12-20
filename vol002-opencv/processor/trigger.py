from RPi import GPIO


class GpioTrigger:
    TRIGGER_PIN = 18

    def __init__(self):
        pass

    def start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIGGER_PIN, GPIO.IN)
        GPIO.add_event_detect(self.TRIGGER_PIN, GPIO.RISING)

    def stop(self):
        GPIO.remove_event_detect(self.TRIGGER_PIN)

    def detect(self):
        return GPIO.event_detected(self.TRIGGER_PIN)
