"""========== script.py ==========
  This is the only file you need to modify in order
  to get a working mdl project (for now).
  my_main.c will serve as the interpreter for mdl.
  When an mdl script goes through a lexer and parser, 
  the resulting operations will be in the array op[].
  Your job is to go through each entry in op and perform
  the required action from the list below:
  frames: set num_frames for animation
  basename: set name for animation
  vary: manipluate knob values between two given frames
        over a specified interval
  set: set a knob to a given value
  
  setknobs: set all knobs to a given value
  push: push a new origin matrix onto the origin stack
  
  pop: remove the top matrix on the origin stack
  move/scale/rotate: create a transformation matrix 
                     based on the provided values, then 
		     multiply the current top of the
		     origins stack by it.
  box/sphere/torus: create a solid object based on the
                    provided values. Store that in a 
		    temporary matrix, multiply it by the
		    current top of the origins stack, then
		    call draw_polygons.
  line: create a line based on the provided values. Store 
        that in a temporary matrix, multiply it by the
	current top of the origins stack, then call draw_lines.
  save: call save_extension with the provided filename
  display: view the image live
  
  jdyrlandweaver
  ========================="""

import mdl
import os
import math
from display import *
from matrix import *
from draw import *


nframes = 1
basename = 'acid'
knob = []

"""======== first_pass( commands, symbols ) ==========
  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present
  If vary is found, but frames is not, the entire
  program should exit.
  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  jdyrlandweaver
  ==================== """
def first_pass( commands ):
    global basename
    global knobs
    global nframes

    cms = {cmd[0] for cmd in commands}
    
    if "frames" in cms and "basename" not in cms:
        basename = "acid"
        print "default base name"

    if "vary" in cms and "frames" not in cms:
        basename = "acid"
        exit()

    for cmds in commands:    
        cmd = cmds[0]
        arg = cmds[1:]

        if cmd == "frames":
            nframes = arg[0]
            
        elif cmd == "basename":
            basename = arg[0]
 
        

"""======== second_pass( commands ) ==========
  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).
  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.
  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""
def second_pass( commands, num_frames ):
    for i in range(nframes):
         knob.append({})

    for cmds in commands:
        cmd = cmds[0]
        arg = cmds[1:]

        if cmd == 'vary':
            varname = arg[0]
            
            start_frame = arg[1]
            end_frame   = arg[2]             
            start_val   = arg[3]
            end_val     = arg[4]

            d_frame = end_frame - start_frame
            d =       end_val   - start_val

            correct = 0
     
            tmp = end_frame

            if d<0:
                correct = nframes
                tmps = start_frame
                start_frame = end_frame
                end_frame = tmps

            for i in range(start_frame,end_frame+d,d):
                frame = (abs(i-start_frame+0.0))/d_frame
                knob[i][varname]=frame   

def run(filename):    
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    sources = []
    cons = []

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
        
    screen = new_screen()    
    first_pass(commands)
    second_pass(commands, nframes)
    
    #print nframes

    try:
        os.mkdir(basename)
    except:
        pass
        
    for j in range(nframes):
        #print 'j1: '+str(j)
        sources=[]
        stack = [ tmp ]
        zbuf = new_matrix(XRES, YRES)
        for x in range(XRES):
            for y in range(YRES):
                zbuf[x][y]=float("-inf")
                
        for command in commands:
            if command[0] == "pop":
                stack.pop()

            if not stack:
                stack = [ tmp ]

            if command[0] == "ambient":                
                color[0] = command[1]
                color[1] = command[2]
                color[2] = command[3]

            elif command[0] == "shading":
                shade = command[1]

            elif command[0] == "light":
                sources.append(list(command[1:]))

            elif command[0] == "constants":
                cons = command[1:]

            elif command[0] == "push":
                stack.append( stack[-1][:] )

            elif command[0] == "save":
                save_extension(screen, command[1])

            elif command[0] == "display":
                display(screen)

            elif command[0] == "sphere":
                m = []
                add_sphere(m, command[1], command[2], command[3], command[4], 5)
                matrix_mult(stack[-1], m)
                print m
                draw_polygons( m, screen, color, sources, cons, zbuf )

            elif command[0] == "torus":
                m = []
                add_torus(m, command[1], command[2], command[3], command[4], command[5], 5)
                matrix_mult(stack[-1], m)
                draw_polygons( m, screen, color, sources, cons, zbuf )

            elif command[0] == "box":                
                m = []
                add_box(m, *command[1:])
                matrix_mult(stack[-1], m)
                draw_polygons( m, screen, color, sources, cons, zbuf )

            elif command[0] == "line":
                m = []
                add_edge(m, *command[1:])
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, color )

            elif command[0] == "bezier":
                m = []
                add_curve(m, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .05, 'bezier')
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, color )

            elif command[0] == "hermite":
                m = []
                add_curve(m, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .05, 'hermite')
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, color )

            elif command[0] == "circle":
                m = []
                add_circle(m, command[1], command[2], command[3], command[4], .05)
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, color )

            elif command[0] == "move":                
                if command[-1] == "mover":
                    xval = command[1]*knob[j]["mover"]
                    yval = command[2]*knob[j]["mover"]
                    zval = command[3]*knob[j]["mover"]
                else:
                    xval = command[1]
                    yval = command[2]
                    zval = command[3]  
                t = make_translate(xval, yval, zval)
                matrix_mult( stack[-1], t )
                stack[-1] = t
    
            elif command[0] == "scale":
                if command[-1] == "bigenator":
                    xval = command[1]*knob[j]["bigenator"]
                    yval = command[2]*knob[j]["bigenator"]
                    zval = command[3]*knob[j]["bigenator"]
                else:
                    xval = command[1]
                    yval = command[2]
                    zval = command[3]
                t = make_scale(xval, yval, zval)
                matrix_mult( stack[-1], t )
                stack[-1] = t
            
            elif command[0] == "rotate":     
                if command[-1] == "spinny":
                    angle = command[2] * (math.pi / 180) * knob[j]["spinny"]
                 
                    if command[1] == 'x':
                        t = make_rotX( angle )
                    elif command[1] == 'y':
                        t = make_rotY( angle )
                    elif command[1] == 'z':
                        t = make_rotZ( angle )            
                else:
                    angle = command[2] * (math.pi / 180)
                 
                    if command[1] == 'x':
                        t = make_rotX( angle )
                    elif command[1] == 'y':
                        t = make_rotY( angle )
                    elif command[1] == 'z':
                        t = make_rotZ( angle )            
                matrix_mult( stack[-1], t )
                stack[-1] = t

            elif command[0]=='mesh':
                fname=command[1]
                #print fname
                f=open(fname,'r').read().split()
                #print len(f)
                ar=[f[x:x+3] for x in range(0, len(f),3)]
                #print ar
                for i in range(len(ar)):
                    #print ar[i]
                    ar[i].append('1.0')
                    #print ar[i]
                    for h in range(len(ar[i])):
                        ar[i][h]=float(ar[i][h])
                #print ar
                '''i=0
                while i<len(f)-4:
                    t=[]
                    t.append(float(f[i]))
                    t.append(float(f[i+1]))
                    t.append(float(f[i+2]))
                    t.append(float(1))
                    f[i]=t
                    i+=3'''
                #xprint f
                matrix_mult(stack[-1], ar)
                draw_polygons( ar, screen, color, sources, cons, zbuf )
                
        if j==0:
             save_ppm(screen,basename+"/"+basename+'00'+str(j)+".png")
        else:
             z = 2-int(math.log10(j))              
             save_ppm(screen,basename+"/"+basename+'0'*z+str(j)+".png")
             #print z
        clear_screen(screen)     
        print j
            

