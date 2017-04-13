import Tkinter
import tempfile
from Tkinter import *
from PIL import Image, ImageTk
from resizeimage import resizeimage
from smb.SMBConnection import SMBConnection

class Fotokadron9000(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.connect_to_DiskStation()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.bind("<Configure>", self.resize)
        self.cycle()

    def connect_to_DiskStation(self):
        self.conn = SMBConnection(username='Pieter',
                                  password='Pieter',
                                  my_name='RASPIX',
                                  remote_name='DiskStation',
                                  use_ntlm_v2=True)
        assert self.conn.connect(ip='192.168.1.15',
                                 port=139)

    def check_new_images(self):
        f = tempfile.NamedTemporaryFile()
        #file_attributes, filesize = self.conn.retrieveFile('Photo', 'RASPIX/20160624_174613.jpg', f)
        print 'Reading metadata'
        for shared_file in self.conn.listPath('Photo', 'RASPIX'):
            print shared_file.last_write_time
        # Retrieved file contents are inside f
        # Do what you need with the f and then close it
        # Note that the file obj is positioned at the end-of-file,
        # so you might need to perform a f.seek() if you need
        # to read from the beginning
        f.close()

    def download_new_image(self):
        f = tempfile.NamedTemporaryFile()
        #file_attributes, filesize = self.conn.retrieveFile('Photo', 'RASPIX/20160624_174613.jpg', f)
        print 'Reading metadata'
        for shared_file in self.conn.listPath('Photo', 'RASPIX'):
            print shared_file.last_write_time
        # Retrieved file contents are inside f
        # Do what you need with the f and then close it
        # Note that the file obj is positioned at the end-of-file,
        # so you might need to perform a f.seek() if you need
        # to read from the beginning
        f.close()

    def cycle(self):
        print('Drawing new image')
        self.draw_image()
        #
        print('Downloading new images from DiskStation')
        self.download_new_image()
        #..
        self.master.after(1000, self.cycle)

    def draw_image(self):
        self.original = Image.open('17.jpg')
        self.image = ImageTk.PhotoImage(self.original)
        self.display = Canvas(self, bd=0, highlightthickness=0)
        self.display.grid(row=0, sticky=W+E+N+S)
        self.display.configure(background='black')
        self.pack(fill=BOTH, expand=1)
        self.resize()

    def resize(self, event=None):
        size = (scrW, scrH)
        resized = resizeimage.resize_contain(self.original, size)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")

root = Tk()

scrW, scrH = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (scrW, scrH))
root.focus_set()
root.bind("<Escape>", lambda e: e.widget.quit())

app = Fotokadron9000(root)

app.mainloop()
root.destroy()
