# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

wx.Main = 6000

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.Main, title = _(u"Conway's game of life"), pos = wx.DefaultPosition, size = wx.Size( 813,585 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self.m_menubar4 = wx.MenuBar( 0 )
        self.m_file_menu = wx.Menu()
        self.m_file_load = wx.MenuItem( self.m_file_menu, wx.ID_ANY, _(u"Open"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_file_menu.Append( self.m_file_load )

        self.m_file_save = wx.MenuItem( self.m_file_menu, wx.ID_ANY, _(u"Save"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_file_menu.Append( self.m_file_save )

        self.m_menubar4.Append( self.m_file_menu, _(u"File") )

        self.m_sim_menu = wx.Menu()
        self.m_sim_run = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"&Run"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_run )

        self.m_sim_pause = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Pause"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_pause )
        self.m_sim_pause.Enable( False )

        self.m_sim_step = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Single Step"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_step )

        self.m_sim_random_fill = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Random Fill"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_random_fill )

        self.m_sim_continue = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Continue"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_continue )
        self.m_sim_continue.Enable( False )

        self.m_sim_menu.AppendSeparator()

        self.m_sim_faster = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Faster"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_faster )

        self.m_sim_slower = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Slower"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_slower )

        self.m_menubar4.Append( self.m_sim_menu, _(u"Simulation") )

        self.m_zoom_menu = wx.Menu()
        self.m_zoom_auto = wx.MenuItem( self.m_zoom_menu, wx.ID_ANY, _(u"Auto"), wx.EmptyString, wx.ITEM_CHECK )
        self.m_zoom_menu.Append( self.m_zoom_auto )
        self.m_zoom_auto.Check( True )

        self.m_zoom_in = wx.MenuItem( self.m_zoom_menu, wx.ID_ANY, _(u"In"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_zoom_menu.Append( self.m_zoom_in )

        self.m_zoom_out = wx.MenuItem( self.m_zoom_menu, wx.ID_ANY, _(u"Out"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_zoom_menu.Append( self.m_zoom_out )

        self.m_menubar4.Append( self.m_zoom_menu, _(u"Zoom") )

        self.SetMenuBar( self.m_menubar4 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_grid = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_grid.SetScrollRate( 5, 5 )
        bSizer2.Add( self.m_grid, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.OnOpen, id = self.m_file_load.GetId() )
        self.Bind( wx.EVT_MENU, self.OnSave, id = self.m_file_save.GetId() )
        self.Bind( wx.EVT_MENU, self.RunSim, id = self.m_sim_run.GetId() )
        self.Bind( wx.EVT_MENU, self.PauseSim, id = self.m_sim_pause.GetId() )
        self.Bind( wx.EVT_MENU, self.TakeSingleStep, id = self.m_sim_step.GetId() )
        self.Bind( wx.EVT_MENU, self.RandomFill, id = self.m_sim_random_fill.GetId() )
        self.Bind( wx.EVT_MENU, self.OnContinue, id = self.m_sim_continue.GetId() )
        self.Bind( wx.EVT_MENU, self.OnFaster, id = self.m_sim_faster.GetId() )
        self.Bind( wx.EVT_MENU, self.OnSlower, id = self.m_sim_slower.GetId() )
        self.Bind( wx.EVT_MENU, self.ToggleZoomAuto, id = self.m_zoom_auto.GetId() )
        self.Bind( wx.EVT_MENU, self.ZoomIn, id = self.m_zoom_in.GetId() )
        self.Bind( wx.EVT_MENU, self.ZoomOut, id = self.m_zoom_out.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnOpen( self, event ):
        event.Skip()

    def OnSave( self, event ):
        event.Skip()

    def RunSim( self, event ):
        event.Skip()

    def PauseSim( self, event ):
        event.Skip()

    def TakeSingleStep( self, event ):
        event.Skip()

    def RandomFill( self, event ):
        event.Skip()

    def OnContinue( self, event ):
        event.Skip()

    def OnFaster( self, event ):
        event.Skip()

    def OnSlower( self, event ):
        event.Skip()

    def ToggleZoomAuto( self, event ):
        event.Skip()

    def ZoomIn( self, event ):
        event.Skip()

    def ZoomOut( self, event ):
        event.Skip()


