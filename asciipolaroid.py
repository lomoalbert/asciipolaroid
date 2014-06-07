#!/usr/bin/env python
#-*- coding:utf-8 -*-


from gi.repository import Gtk,Gdk,Gio
import sys
import aalib
import Image
import urllib,urllib2
from cStringIO import StringIO
from gi.overrides import Pango

DRAG_ACTION = Gdk.DragAction.COPY

def p2a(filename):
    fp = open(filename)
    image = Image.open(fp).convert('L')
    screen = aalib.AsciiScreen(width=100, height=image.size[1]*45/image.size[0])
    image=image.resize(screen.virtual_size)
    screen.put_image((0, 0), image)
    return screen.render()

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        
        
    def getimage(self,widget):
        image=widget.get_preview_filename()
        asciicode=p2a(image)
        sys.stdout.flush()
        image1.set_from_file(image)
        textbuffer.set_text(asciicode)
        
        
class DropArea(Gtk.Image):

    def __init__(self):
        Gtk.Image.__init__(self)
        self.set_size_request(300,300)
        self.drag_dest_set(Gtk.DestDefaults.ALL, [], DRAG_ACTION)

        self.connect("drag-data-received", self.on_drag_data_received)

    def on_drag_data_received(self, widget, drag_context, x,y, data,info, time):
        if True:
            text = data.get_text()
            '''file:///home/albert/Pictures/__0155.jpg\r\n'''
            uri=text.split('\r\n')[0]
            image=urllib.unquote(uri.replace('file://',''))
            print image
            sys.stdout.flush()
            asciicode=p2a(image)
            sys.stdout.flush()
            image1.set_from_file(image)
            textbuffer.set_text(asciicode)

builder = Gtk.Builder()
builder.add_from_file("asciipolaroid.glade")

window = builder.get_object("window1")

hb = Gtk.HeaderBar()
hb.props.show_close_button = True
hb.props.title = "HeaderBar example"
window.set_titlebar(hb)
button = Gtk.Button()
icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
himage = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
button.add(himage)
hb.pack_end(button)


box2 = builder.get_object("box2")
textview = builder.get_object("textview1")
textbuffer = builder.get_object("textbuffer1")
image1 = DropArea()
image1.drag_dest_add_text_targets()
box2.pack_start(image1,True,True,0)


font = Pango.FontDescription('Monospace 4')
textview.modify_font(font)


builder.connect_signals(Handler())

window.show_all()
Gtk.main()
