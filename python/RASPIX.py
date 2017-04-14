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
        self.i = 0

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
        self.list_images()
        image_file = NamedTemporaryFile()
        filename = self.image_list[self.i][0]
        print filename
        self.conn.retrieveFile('Photo',
                               'RASPIX/'+filename,
                                image_file)
        self.original = Image.open(image_file)
        self.original.load()
        image_file.close()
        self.i = (self.i + 1) % len(self.image_list)

    def list_images(self):
        print('Creating new image list')
        self.image_list = []
        l = self.conn.listPath('Photo', 'RASPIX')
        def is_image(shared_file):
            filename = shared_file.filename.lower()
            return (filename[-5:] == '.jpeg'
                    or filename[-4:] in ('.jpg', '.gif', '.png'))

        l = filter(is_image, l)
        for shared_file in l:
            self.image_list.append((shared_file.filename, shared_file.last_write_time))
        self.image_list.sort(key=lambda tup: tup[1])

    def cycle(self):
        self.draw_image()
        self.download_new_image() 
        self.master.after(500, self.cycle)

    def draw_image(self):
        print('Drawing new image')

        resized = resizeimage.resize_contain(self.original, self.screen_dim)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")

        


root = Tk()
app = Fotokadron9000(root)
app.mainloop()
root.destroy()
