import os

# https://stackoverflow.com/a/35851955/16725431
if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID


    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ]

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
                self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xff


    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]


    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value


    FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'


    def get_windows_downloads_path():
        return _get_known_folder_path(FOLDERID_Download)
else:
    def get_windows_downloads_path():
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")


def get_confirmation(message="Are you sure?"):
    message += " [Y/n]: "
    while True:
        user_input = input(message).strip().lower()
        if user_input in ['yes', 'y']:
            return True
        elif user_input in ['no', 'n']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


if __name__ == '__main__':
    download_path = get_windows_downloads_path()
    print("Default download path:", download_path)
