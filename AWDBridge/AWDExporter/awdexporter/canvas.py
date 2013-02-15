# -*- coding: utf-8 -*-
"""a custom canvas - draws given data as a barchart into a userarea"""


import c4d
from c4d import documents
from c4d import gui
from c4d import plugins

from awdexporter import ids


class Canvas(gui.GeUserArea):

    # the object list supplied by the worker
    data = []

    # step keeping and length for supersimple animation
    step = 0
    steps = 10

    # width of an item and the text widthin
    curWidth = 0
    fontHeight = 0

    # the index of a clicked item (<0 for none)
    selected = -1

    # called on Redraw()
    def DrawMsg(self, x1, y1, x2, y2, msg):

        # set font height and item with
        self.fontHeight = self.DrawGetFontHeight()
        self.curWidth = self.fontHeight + 2

        # set offscreen to define the whole canvas as clipping region
        #(normally this would suffice for this type of graphic since
        #we will end up drawing on the whole 'screen' anyway - but the
        #text will get a clipping region so it doesn't overlap the outlines)
        self.OffScreenOn()

        self.DrawSetPen(c4d.COLOR_BG)
        self.DrawRectangle(0, 0, x2, y2)

        fillBorder = 1
        value = self.data[1]
        value2 = self.data[2]
        self.curWidth=int(value*x2)
        self.curWidth2=int(value2*self.curWidth)

        self.DrawSetTextCol(c4d.COLOR_TEXT, c4d.COLOR_TRANS)
        # scale the actual poly-value to the animation progress
            
        # set the clipping region to the column we work on
        self.SetClippingRegion(5, 5,
                               x2-5,
                               35)

        borderStyle=c4d.BORDER_BLACK
        if value>0:
            borderStyle=c4d.BORDER_ACTIVE_4
        self.DrawBorder(borderStyle, 5, 5,x2-5,35 - 1)

        self.DrawSetPen(c4d.Vector(0.5, 0, 0))
        
        if value>0:
            self.DrawRectangle(5 + fillBorder, 5 + fillBorder, 5 + self.curWidth - fillBorder-10, 35 - fillBorder - 1)
            if value2>0:
                self.DrawSetPen(c4d.Vector(0.8,0, 0))
                self.DrawRectangle(5 + fillBorder, 5 + fillBorder, 5 + self.curWidth2 - fillBorder-10, 35 - fillBorder - 1)

        self.DrawSetPen(c4d.COLOR_BG)
        #self.DrawRectangle(x2 / 2 - self.DrawGetTextWidth(self.data[0]) / 2 -5 , y2 / 2 - self.fontHeight / 2 -2,x2 / 2 + self.DrawGetTextWidth(self.data[0]) / 2 +5 ,y2 / 2+ self.fontHeight/2 +2 )
        self.DrawSetTextCol(c4d.COLOR_TEXT, c4d.COLOR_TRANS)
        self.DrawText(self.data[0], x2 / 2 - self.DrawGetTextWidth(self.data[0]) / 2, y2 / 2 - self.fontHeight / 2)

    # starts the redraw
    def draw(self, aData):

        self.data = aData
        self.Redraw()

