#!/usr/bin/env python3

import life
import os
import random
import wx
import wxLifeUI


class WxLife(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)


class MainWindow(wxLifeUI.MainWindow):
    _zoom_factor = 1.1
    icon_file = 'icon_1024.png'

    def __init__(self, parent):
        wxLifeUI.MainWindow.__init__(self, parent)
        self.SetIcon(wx.Icon(self.icon_file, type=wx.BITMAP_TYPE_PNG))
        self._paused = True
        self._auto_zoom = True
        self._board_size = (100, 100)
        self._fill_factor = 40
        self._delay_time_ms = 100
        self._speed_factor = 1.5
        self._single_step = False
        self._stagnated = False
        self._stagnation = 0
        self._stagnation_count = 0
        self._stagnation_window = 10
        self._similarity_threshold = 0.95
        self._background = wx.Brush('black')
        self._brush = wx.Brush('blue')
        self._directory = 'examples'
        self._filename = ''
        self.initializeGame(set())
        self.m_grid.Bind(wx.EVT_PAINT, self.OnPaint)
        self._timer = wx.Timer()
        self._timer.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def initializeGame(self, cells):
        self._game = life.Life(cells)
        self._box_min_x, self._box_min_y, self._box_max_x, self._box_max_y = self._game.getBoundingBox()
        self.Refresh()

    def RandomFill(self, event):
        self.OnContinue(paused=True)
        self._filename = ''
        newCells = set()
        for y in range(self._board_size[1]):
            for x in range(self._board_size[0]):
                if random.uniform(0, 100) < self._fill_factor:
                    newCells.add((x, y))
        self.initializeGame(newCells)
        # self.saveFile(sys.stdout)

    def RunSim(self, event=None):
        self._paused = False
        self._timer.Start(int(self._delay_time_ms))
        self._brush = wx.Brush("green")
        self.m_sim_run.Enable(False)
        self.m_sim_pause.Enable(True)
        self.Refresh()

    def PauseSim(self, event=None):
        self._paused = True
        self._timer.Stop()
        self._brush = wx.Brush("blue")
        self.m_sim_run.Enable(True)
        self.m_sim_pause.Enable(False)
        self.Refresh()

    def OnTimer(self, event):
        self.takeStep()

    def TakeSingleStep(self, event=None):
        self.PauseSim()
        self.takeStep()

    def takeStep(self):
        self._game.step()
        if self._auto_zoom:
            self.AutoZoom()
        self.checkStagnation()
        self.Refresh()

    def StepBack(self, event=None):
        self.PauseSim()
        if not self._game.backwardsStep():
            print('Can\'t go back')
        self.Refresh()

    def checkStagnation(self):
        stagnating = False
        curr_cells = self._game.getLiveCells()
        if not self._stagnated and self._stagnation_window > 0:
            if len(curr_cells) == len(self._game.getHistory()[-1]):
                stagnating = True
                print('Stagnating on population at {}'.format(self._game.getGeneration()))
            for historical_cells in self._game.getHistory()[-self._stagnation_window:]:
                if curr_cells == historical_cells:
                    stagnating = True
                    self._stagnated = True
                    print('Stagnated on loop at {}'.format(self._game.getGeneration()))
                    break
                elif len(curr_cells.intersection(historical_cells)) > len(curr_cells) * self._similarity_threshold:
                    stagnating = True
                    print('Stagnating on similarity at {}'.format(self._game.getGeneration()))
                    break
            if stagnating:
                self._stagnation += 1
                if self._stagnation > self._stagnation_window:
                    self._stagnated = True
                    print('Stagnated at {}'.format(self._game.getGeneration() - self._stagnation))
            else:
                self._stagnation = 0

        if self._stagnated:
            self.PauseSim()
            self.m_sim_continue.Enable(True)
            self._brush = wx.Brush('red')

    def OnContinue(self, event=None, paused=False):
        self._stagnated = False
        self._stagnation = 0
        self.m_sim_continue.Enable(False)
        if paused:
            self.PauseSim()
        else:
            self.RunSim()

    def OnFaster(self, event):
        self._delay_time_ms = max(self._delay_time_ms / self._speed_factor, 1)
        if self._timer.IsRunning():
            self._timer.Start(int(self._delay_time_ms))

    def OnSlower(self, event):
        self._delay_time_ms = self._delay_time_ms * self._speed_factor
        if self._timer.IsRunning():
            self._timer.Start(int(self._delay_time_ms))

    def AutoZoom(self):
        min_x, min_y, max_x, max_y = self._game.getBoundingBox()

        if min_x < self._box_min_x:
            self._box_min_x = min_x
        if min_y < self._box_min_y:
            self._box_min_y = min_y
        if max_x > self._box_max_x:
            self._box_max_x = max_x
        if max_y > self._box_max_y:
            self._box_max_y = max_y

    def OnOpen(self, event):
        self.OnContinue(paused=True)
        fod = wx.FileDialog(self, "Choose a Life file",
                            self._directory, '', '*.life', wx.FD_OPEN)
        if fod.ShowModal() == wx.ID_OK:
            self._filename = fod.GetFilename()
            self._directory = fod.GetDirectory()
            with open(os.path.join(self._directory, self._filename), 'r') as f:
                self.loadFile(f.readlines())
        fod.Destroy()

    def loadFile(self, lines):
        newCells = set()
        y = 0
        for line in lines:
            x = 0
            for c in line:
                if c == "#":
                    break
                elif not c.isspace():
                    newCells.add((x, y))
                x += 1
            y += 1
        self.initializeGame(newCells)

    def OnSave(self, event):
        save_dialog = wx.FileDialog(self, "Save state", self._directory, '',
                                    '*.life', wx.FD_SAVE)
        if save_dialog.ShowModal() == wx.ID_OK:
            save_filename = save_dialog.GetFilename()
            if not save_filename.endswith('.life'):
                save_filename += '.life'
            self._directory = save_dialog.GetDirectory()
            with open(os.path.join(self._directory, save_filename), 'w') as f:
                self.saveFile(f)
        save_dialog.Destroy()

    def saveFile(self, out):
        min_x, min_y, max_x, max_y = self._game.getBoundingBox()
        if self._filename:
            out.write('# Loaded from "{}"\n'.format(self._filename))
        else:
            out.write('# Height: {}   Width: {}   Fill: {}\n'
                      .format(self._board_size[1], self._board_size[0], self._fill_factor))
        out.write('# Generation: {}\n'.format(self._game.getGeneration()))
        out.write('# Bounding box: ({}, {}) -> ({}, {})\n'.format(min_x, min_y, max_x, max_y))
        cells = self._game.getLiveCells()
        if min_y is not None:
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    out.write('*' if (x, y) in cells else ' ')
                out.write('\n')

    def OnPaint(self, event):
        if self._filename:
            self.SetTitle('"{}"  Generation: {}   Cells: {}'
                          .format(self._filename,
                                  self._game.getGeneration(),
                                  len(self._game.getLiveCells())))
        else:
            self.SetTitle('Generation: {}   Cells: {}'
                          .format(self._game.getGeneration(),
                                  len(self._game.getLiveCells())))
        dc = wx.PaintDC(self.m_grid)
        dc.SetBackground(self._background)
        dc.SetBrush(self._brush)
        dc.SetPen(wx.Pen(self._brush.GetColour()))
        dc.Clear()
        if self._box_min_x is None:
            return
        box_width = self._box_max_x - self._box_min_x + 1
        box_height = self._box_max_y - self._box_min_y + 1
        disp_size = dc.GetSize()
        disp_width = disp_size.GetWidth()
        disp_height = disp_size.GetHeight()
        scale = min(disp_width / (box_width + 1), disp_height / (box_height + 1))

        box_mid_x = (self._box_max_x + self._box_min_x) / 2
        box_mid_y = (self._box_max_y + self._box_min_y) / 2

        display_mid_x = int(disp_width / 2 + 0.5)
        display_mid_y = int(disp_height / 2 + 0.5)

        pixels = {}
        for cell_x, cell_y in self._game.getLiveCells():
            x = display_mid_x + int(scale * (cell_x - box_mid_x + 0.5))
            y = display_mid_y + int(scale * (cell_y - box_mid_y + 0.5))

            if scale <= 2:
                if (x, y) in pixels:
                    pixels[(x, y)] += 1
                else:
                    pixels[(x, y)] = 1
            else:
                point = dc.DeviceToLogical(int(x - scale / 2 + 0.5), int(y - scale / 2 + 0.5))
                # print('Cell ({}, {}) is at {},{} -> {}'.format(cell_x, cell_y, x, y, point))
                dc.DrawCircle(point, max(1, int(scale * 0.45)))

        if scale <= 2:
            max_dens = max([d for d in pixels.values()])
            bg_color = dc.GetBackground().GetColour()
            brush_color = self._brush.GetColour()
            for pos, d in pixels.items():
                new_color = wx.Colour(int(bg_color.GetRed() * (max_dens - d) / max_dens + brush_color.GetRed() * d / max_dens),
                                      int(bg_color.GetGreen() * (max_dens - d) / max_dens + brush_color.GetGreen() * d / max_dens),
                                      int(bg_color.GetBlue() * (max_dens - d) / max_dens + brush_color.GetBlue() * d / max_dens))
                new_brush = wx.Brush(new_color)
                dc.SetBrush(new_brush)
                dc.DrawCircle(pos[0], pos[1], 1)

    def _scaleRange(self, min_v, max_v, factor):
        mid = (max_v + min_v) / 2.0
        new_min = int(mid - (mid - min_v) * factor - 0.5)
        new_max = int(mid + (max_v - mid) * factor + 0.5)

        if new_min == min_v:
            new_min -= 1 if factor > 1 else -1

        if new_max == max_v:
            new_max += 1 if factor > 1 else -1

        if new_min <= new_max:
            return new_min, new_max
        else:
            return min_v, max_v

    def zoom(self, factor):
        self._box_min_x, self._box_max_x = self._scaleRange(self._box_min_x, self._box_max_x, factor)
        self._box_min_y, self._box_max_y = self._scaleRange(self._box_min_y, self._box_max_y, factor)
        self.Refresh()

    def ZoomIn(self, event=None):
        self._auto_zoom = False
        self.m_zoom_auto.Check(False)
        self.zoom(1 / self._zoom_factor)

    def ZoomOut(self, event=None):
        self._auto_zoom = False
        self.m_zoom_auto.Check(False)
        self.zoom(self._zoom_factor)

    def ToggleZoomAuto(self, event):
        self._auto_zoom = not self._auto_zoom
        if self._auto_zoom:
            self.AutoZoom()
            self.Refresh()

    def OnClose(self, event):
        self._timer.Stop()
        self.Destroy()


app = WxLife(False)
mainWindow = MainWindow(None)
app.SetTopWindow(mainWindow)
mainWindow.Show()
app.MainLoop()
