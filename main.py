#!/usr/bin/env python3

import gi
gi.require_version( 'Gtk', '3.0' )
from gi.repository import Gtk
from mainwindow import MainWindow

window = MainWindow( )
window.showAll( )

Gtk.main( )
