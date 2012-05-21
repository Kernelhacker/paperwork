import threading

import gobject

class Worker(gobject.GObject):
    can_interrupt = False

    def __init__(self, name):
        gobject.GObject.__init__(self)
        self.name = name
        self.can_run = True
        self.__thread = None

    def do(self, **kwargs):
        # implemented by the child class
        #
        # if can_interrupt = True, the child class must check self.can_run as
        # often as possible
        assert()

    def __wrapper(self, **kwargs):
        print "Workers: [%s] started" % (self.name)
        self.do(**kwargs)
        print "Workers: [%s] ended" % (self.name)

    def start(self, **kwargs):
        if self.is_running:
            raise threading.ThreadError(
                ("Tried to start a thread already running: %s"
                 % (self.name)))
        self.__can_run = True
        self.__thread = threading.Thread(target=self.__wrapper, kwargs=kwargs)
        self.__thread.start()

    def stop(self):
        if not self.is_running:
            return
        if not self.can_interrupt:
            print ("Trying to stop a worker that cannot be stopped: %s"
                   % (self.name))
        self.__can_run = False
        self.__thread.join()

    def wait(self):
        self.__thread.join()

    def __get_is_running(self):
        return (self.__thread != None and self.__thread.is_alive())

    is_running = property(__get_is_running)

    def __str__(self):
        return self.name
