# -*- coding: utf-8 -*-
# GPL-2.0
#
# Copyright (C) 2018 Zhao ShiRong


import random
from Tkinter import *


def draw_solution(solu, result, setSize):

    cuslist = sorted(
        result['customer'].items(),
        lambda x,
        y: cmp(
            x[1]['x'],
            y[1]['x']))
    xdis = cuslist[-1][1]['x'] - cuslist[0][1]['x']
    xstart = cuslist[0][1]['x']
    cuslist = sorted(
        result['customer'].items(),
        lambda x,
        y: cmp(
            x[1]['y'],
            y[1]['y']))
    ydis = cuslist[-1][1]['y'] - cuslist[0][1]['y']
    ystart = cuslist[0][1]['y']
    print xdis
    print ydis
    print xstart
    print ystart

    # setSize=2000

    if(xdis > ydis):
        ratio = setSize / (float)(xdis)
    else:
        ratio = setSize / (float)(ydis)

    #master = Tk()
    root = Tk()
    #scrollbar = Scrollbar(master)
    #scrollbar.pack( side = RIGHT, fill = Y )

    #w = Canvas(master, width=setSize, height=setSize,yscrollcommand = scrollbar.set )
    # w.pack()
    # w.config(yscrollcommand=scrollbar.set)

    #scrollbar.config( command = w.yview )
    frame = Frame(root, bd=2, relief=SUNKEN)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=E + W)

    yscrollbar = Scrollbar(frame, orient=VERTICAL)
    yscrollbar.grid(row=0, column=1, sticky=N + S)
    # yscrollbar.pack(side=TOP,fill=X)

    canvas = Canvas(
        frame,
        bd=0,
        width=setSize,
        height=setSize,
        scrollregion=(
            0,
            0,
            setSize,
            setSize),
        xscrollcommand=xscrollbar.set,
        yscrollcommand=yscrollbar.set)

    canvas.grid(row=0, column=0, sticky=N + S + E + W)

    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)

    frame.pack()
    w = canvas

    for key, item in result['customer'].items():
        canx = (item['x'] - xstart) * ratio
        cany = (item['y'] - ystart) * ratio
        radius = 2
        w.create_oval(
            canx - radius,
            cany - radius,
            canx + radius,
            cany + radius,
            width=1,
            fill='black')

    colorlist = [
        '#00ffff',
        '#00eeee',
        '#00dddd',
        '#00cccc',
        '#002222',
        '#003333',
        '#008888']
    colornum = len(colorlist)
    for route in solu['route']:
        route.insert(0, 0)
        route.append(0)
        rindex = random.randint(0, colornum - 1)
        colorstr = colorlist[rindex]
        for index, value in enumerate(route):

            if(index == 0):
                continue
            prevcus = route[index - 1]
            curcus = route[index]
            prevcanx = (result['customer'][prevcus]['x'] - xstart) * ratio
            prevcany = (result['customer'][prevcus]['y'] - ystart) * ratio
            curcanx = (result['customer'][curcus]['x'] - xstart) * ratio
            curcany = (result['customer'][curcus]['y'] - ystart) * ratio

            #w.create_line(prevcanx, prevcany, curcanx, curcany, fill="red")
            w.create_line(prevcanx, prevcany, curcanx, curcany, fill=colorstr)

    #w.create_line(0, 0, 200, 100)
    #w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

    #w.create_rectangle(50, 25, 150, 75, fill="blue")

    mainloop()


def parse(f):

    exdict = {}
    linenum = 0
    file_object = open(f, 'r')

    for line in file_object:
        linenum += 1
        if linenum == 5:
            lines = line.split()
            if len(lines) != 2:
                print "file format error"
                return

            exdict['number'] = int(lines[0])
            exdict['capacity'] = int(lines[1])
        if linenum >= 10:
            lines = line.split()
            if len(lines) != 7:
                print "file format error"
                return
            if 'customer' not in exdict:
                exdict['customer'] = {}
            no = int(lines[0])
            exdict['customer'][no] = {}

            exdict['customer'][no]['x'] = int(lines[1])
            exdict['customer'][no]['y'] = int(lines[2])
            exdict['customer'][no]['demand'] = int(lines[3])
            exdict['customer'][no]['ready'] = int(lines[4])
            exdict['customer'][no]['due'] = int(lines[5])
            exdict['customer'][no]['service'] = int(lines[6])

    return exdict


def parseSolution(f):
    solu = {}
    solu['route'] = []
    linenum = 0
    file_object = open(f, 'r')
    for line in file_object:
        linenum += 1
        if(linenum == 1):
            lines = line.split(":")
            solu['name'] = lines[1]
        if linenum > 5:
            lines = line.split(":")
            nums = lines[1].split()
            customers = []
            for every in nums:
                cus = int(every)
                customers.append(cus)

            solu['route'].append(customers)

    return solu


def checkSolu(solu, exdict):
    totalDistance = 0.0
    routenum = 0
    for mem in solu['route']:
        routenum += 1
        routedis = 0.0
        mem.insert(0, 0)
        mem.append(0)
        totalCus = len(mem)
        curendservicetime = 0
        curdemand = 0
        for j in range(1, totalCus):
            #print "j=%d"%(j)
            prev = mem[j - 1]
            now = mem[j]
            distance = ((exdict['customer'][prev]['x'] -
                         exdict['customer'][now]['x'])**2 +
                        (exdict['customer'][prev]['y'] -
                         exdict['customer'][now]['y']) ** 2)**0.5
            reachtime = curendservicetime + distance
            if(reachtime > exdict['customer'][now]['due']):
                print "The solution is Error on route %d customer %d" % (
                    routenum, now)
                print "due time reached"
            #print "Cus %d curdemand %d demand %d"%( now, curdemand,  exdict['customer'][now]['demand'])
            if(curdemand + exdict['customer'][now]['demand'] > exdict['capacity']):
                print "The solution is Error on route %d customer %d" % (
                    routenum, now)
                print "capacity time reached"
                return -1
            curdemand += exdict['customer'][now]['demand']
            routedis += distance
            if(reachtime < exdict['customer'][now]['ready']):
                curendservicetime = exdict['customer'][now]['ready'] + \
                    exdict['customer'][now]['service']
            else:
                curendservicetime = reachtime + \
                    exdict['customer'][now]['service']
        mem.pop()
        mem.pop(0)
        totalDistance += routedis

    print "problem %s  route %d  distance %.2f" % (
        solu['name'], routenum, totalDistance)


def checkAndDrawSolution():
    solu = parseSolution("E:/bigdb/output/C1_2_1_20_2709.txt")
    result = parse("E:/bigdb/homberger_200_customer_instances/C1_2_1.txt")
    checkSolu(solu, result)
    draw_solution(solu, result, 800)


if __name__ == "__main__":
    checkAndDrawSolution()
