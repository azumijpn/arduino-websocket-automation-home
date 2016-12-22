import serial
import threading
import time
from multiprocessing import Process, Queue
import config

try:
    from queue import Empty
except ImportError:
    from Queue import Empty

class SerialManager(Process):
    """ This class has been written by
        Philipp Klaus and can be found on
        https://gist.github.com/4039175 .  """

    def __init__(self, device, baudrate, timeout):
        self.ser = serial.Serial(device, baudrate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout)
        self.in_queue = Queue()
        self.out_queue = Queue()
        self.closing = False # A flag to indicate thread shutdown
        self.read_num_bytes  = 256
        self.sleeptime = None
        self._chunker = None
        Process.__init__(self, target=self.loop)

    def set_chunker(self, chunker):
        self._chunker = chunker
        self.in_queue = chunker.in_queue

    def loop(self):
        try:
            while not self.closing:
                if self.sleeptime: time.sleep(self.sleeptime)
                in_data = self.ser.read(self.read_num_bytes)
                if in_data:
                    if self._chunker:
                        self._chunker.new_data(in_data)
                    else:
                        self.in_queue.put(in_data)
                try:
                    out_buffer = self.out_queue.get_nowait()
                    self.ser.write(out_buffer)
                except Empty:
                    pass
        except (KeyboardInterrupt, SystemExit):
            pass
        self.ser.close()

    def close(self):
        self.closing = True

def main():

    if config.isSerial:
        s = dict()
        for i in range(0, len(config.portCom)):
            s[i] = SerialManager(config.portCom[i]['port'], config.portCom[i]['baudrate'], timeout=0.1)
            s[i].sleeptime = None
            s[i].read_num_size = 512
            s[i].start()

        try:
            while True:
                data = s[0].in_queue.get()
                print(repr(data))
        except KeyboardInterrupt:
            s[0].close()
        finally:
            s[0].close()
        s[0].join()

if __name__ == "__main__":
    main()
