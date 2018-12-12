import gi
import functools
import subprocess

import gssdp

gi.require_version( 'Gtk', '3.0' )
from gi.repository import Gtk

class MainWindow( object ):
  @staticmethod
  def connect( widget, signals ):
    for k, v in signals.items( ):
      widget.connect( k, v )

    return widget;

  @staticmethod
  def getAndConnect( builder, id, signals ):
    return MainWindow.connect( builder.get_object( id ), signals )

  def __init__( self ):
    super( MainWindow, self ).__init__( )

    builder = Gtk.Builder( ).new_from_file( 'main.glade' )

    self.__window = MainWindow.getAndConnect( builder, 'MainWindow', {
      'destroy': Gtk.main_quit
    } )
    self.__server = MainWindow.getAndConnect( builder, 'Server', {

    } )
    self.__refresh = MainWindow.getAndConnect( builder, 'Refresh', {
      'clicked': functools.partial( MainWindow.refreshServers, self )
    } )
    self.__media = MainWindow.getAndConnect( builder, 'Media', {
    } )
    self.__order = MainWindow.getAndConnect( builder, 'Order', {

    } )
    self.__down = MainWindow.getAndConnect( builder, 'Down', {

    } )
    self.__play = MainWindow.getAndConnect( builder, 'Play', {
      'clicked': functools.partial( MainWindow.playSelected, self ),
      'realize': functools.partial( MainWindow.refreshServers, self )
    } )

    self._booting = True
    self.__discover = gssdp.Discover( functools.partial( MainWindow.onBrowse, self ) )
    self.__window.show_all( )

  def refreshServers( self, button ):
    print( 'Refrescando ...' )
    self.__discover.start( )

  def playSelected( self, button ):
    Popen( [ self.__order.get_active_text( ) ], shell = True, stdin = None, stdout = None, stderr = None, close_fds = True )

  def showAll( self ):
    self.__window.show_all( )

  def onBrowse( self, browser, msn, locations ):
    if locations == None:
      print( 'PERDIDO', msn )
    else:
      print( 'ENCONTRADO', msn )
      for v in locations:
        print( v )

  def onMaterialize( self ):
    if self._booting:
      self._booting = False
      self.refreshServers( )