import Tkinter
import time
from time import sleep
from tempfile import NamedTemporaryFile
from Tkinter import *
from PIL import Image, ImageTk
from resizeimage import resizeimage
from smb.SMBConnection import SMBConnection

delay = 1000


# Provide the SMB server info in a text document 'SMB_info.txt' witch structure:
#<IP>
#<Port>
#<Server Name>
#<Shared folder name>
#<Path>
#<Username>
#<Password>

f = open("smb_info.txt")
smb_info = []
for line in f:
   smb_info.append(line.strip())
print 'SMB Server configuration: ' + str(smb_info)
f.close()

class Fotokadron9000(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.init_GUI()
        self.connect_to_smb()
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

    def connect_to_smb(self):
        self.conn = SMBConnection(username=smb_info[5],
                                  password=smb_info[6],
                                  my_name='RASPIX',
                                  remote_name=smb_info[2],
                                  use_ntlm_v2=True)
        assert self.conn.connect(ip=smb_info[0],
                                 port=int(smb_info[1]))

    def download_new_image(self):
        print('Downloading new images from SMB Server')
        self.list_images()
        image_file = NamedTemporaryFile()
        filename = self.image_list[self.i][0]
        print filename
        self.conn.retrieveFile(smb_info[3],
                               smb_info[4]+filename,
                                image_file)
        self.original = Image.open(image_file)
        self.original.load()
        image_file.close()
        self.i = (self.i + 1) % len(self.image_list)

    def list_images(self):
        print('Creating new image list')
        self.image_list = []
        l = self.conn.listPath(smb_info[3], smb_info[4])
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
        delta = int(delay-(time.time()*1000-self.time_before))
        self.master.after(delta, self.cycle)

    def draw_image(self):
        print('Drawing new image')

        resized = resizeimage.resize_contain(self.original, self.screen_dim)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.time_before = time.time() * 1000
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")

        


root = Tk()
app = Fotokadron9000(root)
app.mainloop()
root.destroy()
