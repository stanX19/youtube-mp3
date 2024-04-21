class WindowsInhibitor:
    '''Prevent OS sleep/hibernate in windows; code from:
    https://github.com/h3llrais3r/Deluge-PreventSuspendPlus/blob/master/preventsuspendplus/core.py
    API documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx'''
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001

    def __init__(self, quiet=False):
        self.quiet = quiet
        pass

    def __del__(self):
        self.uninhibit()

    def inhibit(self):
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS | \
            WindowsInhibitor.ES_SYSTEM_REQUIRED)
        if not self.quiet:
            print("Prevented Windows from going to sleep")

    def uninhibit(self):
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS)
        if not self.quiet:
            print("Allowed Windows to go to sleep")

if __name__ == '__main__':
    x = WindowsInhibitor()
    x.inhibit()
    x.uninhibit()