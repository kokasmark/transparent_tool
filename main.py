import os
import webview
import win32gui
import win32process
import win32api
import win32con
from pynput import mouse
import keyboard

opacity = 255

def get_hwnds_for_pid(pid):
    hwnds = []
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            found_tid, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def on_scroll(x, y, dx, dy):
    global opacity
    if keyboard.is_pressed('alt'):
        opacity = min(max(opacity + dy * 10, 0), 255)
        hwnd = get_hwnds_for_pid(os.getpid())[0]
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 1), opacity, win32con.LWA_ALPHA | win32con.LWA_COLORKEY)

def on_loaded(window):
    window.restore()
    hwnd = get_hwnds_for_pid(os.getpid())[0]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 1), 255,
                                         win32con.LWA_ALPHA | win32con.LWA_COLORKEY)

    window.move(0, 0)
    with mouse.Listener(on_scroll=on_scroll) as listener:
        listener.join()

if __name__ == '__main__':
    import ctypes

    

    url = input("Url(File or Website): ").strip()
    if os.path.isfile(url):
        url = f'file:///{os.path.abspath(url)}'
    elif not url.startswith('http://') and not url.startswith('https://'):
        print("Please enter a valid URL or a path to a PDF file.")
        exit(1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    window = webview.create_window('Shhh...',
                                    url=url,
                                    frameless=False,
                                    on_top=True,
                                    x=65535, y=65535,
                                    minimized=True, easy_drag=True,zoomable=False)
    webview.start(on_loaded, window, gui='edgechromium', debug=True)
