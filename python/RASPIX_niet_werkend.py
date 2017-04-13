import Tkinter
from tempfile import NamedTemporaryFile
from Tkinter import *
from PIL import Image, ImageTk
from resizeimage import resizeimage
from smb.SMBConnection import SMBConnection

class Fotokadron9000(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.init_GUI()
        self.connect_to_DiskStation()
        self.download_new_image()
        self.cycle()

    def init_GUI(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.screen_dim = (self.master.winfo_screenwidth(),
                           self.master.winfo_screenheight())
        self.master.overrideredirect(1)
        self.master.geometry("%dx%d+0+0" % self.screen_dim)
        self.master.focus_set()
        self.master.bind("<Escape>", lambda e: e.widget.quit())
        self.display = Canvas(self, bd=0, highlightthickness=0)
        self.display.grid(row=0, sticky=W+E+N+S)
        self.display.configure(background='black')
        self.pack(fill=BOTH, expand=1)

    def connect_to_DiskStation(self):
        self.conn = SMBConnection(username='Pieter',
                                  password='Pieter',
                                  my_name='RASPIX',
                                  remote_name='DiskStation',
                                  use_ntlm_v2=True)
        assert self.conn.connect(ip='192.168.1.15',
                                 port=139)

    def download_new_image(self):
        print('Downloading new images from DiskStation')
        # self.image_file = NamedTemporaryFile()
        # self.conn.retrieveFile('Photo',
        #                        'RASPIX/20160624_174613.jpg',
        #                        self.image_file)
        # print 'Reading metadata'
        # for shared_file in self.conn.listPath('Photo', 'RASPIX'):
        #     print shared_file.last_write_time
        #
        # Retrieved file contents are inside self.image_file
        # Do what you need with the self.image_file and then close it
        # Note that the file obj is positioned at the end-of-file,
        # so you might need to perform a self.image_file.seek() if you need
        # to read from the beginning
        # self.image_file.close()
        

    def cycle(self):
        self.draw_image()
        self.download_new_image()
        self.master.after(3000, self.cycle)

    def draw_image(self):
        print('Drawing new image')
        self.image_file = NamedTemporaryFile()
        self.conn.retrieveFile('Photo',
                               'RASPIX/20160624_174613.jpg',
                                self.image_file)
        self.original = Image.open(self.image_file)  #'17.jpg')
        resized = resizeimage.resize_contain(self.original, self.screen_dim)
        image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=image, anchor=NW, tags="IMG")

        self.image_file.close()


root = Tk()
app = Fotokadron9000(root)
app.mainloop()
root.destroy()
