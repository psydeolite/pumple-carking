from display import *
from matrix import *
from gmath import *
from math import cos, sin, pi, sqrt, pow

MAX_STEPS = 100

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point( points, x0, y0, z0 )
    add_point( points, x1, y1, z1 )
    add_point( points, x2, y2, z2 )

def scanline_convert(screen, Xm, Ym, Zm, Xb, Yb, Zb, Xt, Yt, Zt, color, zbuf):
    inc=0
    #while haven't reached top of triangle
    while Yb+inc<Yt:
        d0= float(Xt-Xb) / (Yt-Yb)
        d0z = float(Zt-Zb) / sqrt(pow(Xm-Xb, 2) + pow(Ym - Yb, 2))
        Xb0=Xb+inc*d0
        Zb0=Zb + sqrt(pow(inc,2)+pow((inc*d0),2))*d0z
        if Yb+inc<Ym:
            d1= float(Xm-Xb)/(Ym-Yb)
            d1z = float(Zm-Zb) / sqrt(pow(Xm-Xb, 2) + pow(Ym - Yb, 2))
            Xb1=Xb+inc*d1
            Zb1=Zb + sqrt(pow(inc,2)+pow((inc*d1),2))*d1z
            draw_line(screen,Xb0,Yb+inc, Zb0, Xb1,Yb+inc,Zb1,color, zbuf)
        #x1 is on MT
        else:
            d1= float(Xt-Xm)/(Yt-Ym)
            d1z = float(Zt-Zm) / sqrt(pow(Xt-Xm, 2) + pow(Yt - Ym, 2))
            Xm1=Xm+(inc-Ym+Yb)*d1
            Zm1=Zm+sqrt(pow(inc-Ym+Yb,2)+pow((inc-Ym+Yb)*d1,2))*d1z
            draw_line(screen,Xb0,Yb+inc,Zb0,Xm1,Yb+inc,Zm1,color, zbuf)
        inc+=1
        
def order_points( points, p ):

    Xm = 0
    Ym = 0
    Xt = 0
    Yt = 0
    Xb = 0
    Yb = 0
    
    if points[p][1]>=points[p+1][1] and points[p][1]>=points[p+2][1]:
        #print "a"
        Xt = points[p][0]
        Yt = points[p][1]
        Zt = points[p][2]
        
        if points[p+1][1]>=points[p+2][1]:
            #print "a1"
            Xm = points[p+1][0]
            Ym = points[p+1][1]
            Zm = points[p+1][2]
                    
            Xb = points[p+2][0]
            Yb = points[p+2][1]
            Zb = points[p+2][2]

        else:
            #print "a2"
            Xb = points[p+1][0]
            Yb = points[p+1][1]
            Zb = points[p+1][2]
            
            Xm = points[p+2][0]
            Ym = points[p+2][1]
            Zm = points[p+2][2]

    elif points[p+1][1]>=points[p][1] and points[p+1][1]>=points[p+2][1]:
        #print "b"
        Xt = points[p+1][0]
        Yt = points[p+1][1]
        Zt = points[p+1][2]
        
        if points[p][1]>=points[p+2][1]:
            #print "b1"
            Xm = points[p][0]
            Ym = points[p][1]
            Zm = points[p][2]
            
            Xb = points[p+2][0]
            Yb = points[p+2][1]
            Zb = points[p+2][2]
        else:
            #print "b2"
            Xb = points[p][0]
            Yb = points[p][1]
            Zb = points[p][2]
            
            Xm = points[p+2][0]
            Ym = points[p+2][1]
            Zm = points[p+2][2]

    elif points[p+2][1]>=points[p][1] and points[p+2][1]>=points[p+1][1]:
        #print "c"
        Xt = points[p+2][0]
        Yt = points[p+2][1]
        Zt = points[p+2][2]
        
        if points[p][1]>=points[p+1][1]:
            #print "c1"
            Xm = points[p][0]
            Ym = points[p][1]
            Zm = points[p][2]
            
            Xb = points[p+1][0]
            Yb = points[p+1][1]
            Zb = points[p+1][2]
            
        else:
            #print "c2"
            Xb = points[p][0]
            Yb = points[p][1]
            Zb = points[p][2]
                    
            Xm = points[p+1][0]
            Ym = points[p+1][1]
            Zm = points[p+1][2]

    return [Xm, Ym, Zm, Xb, Yb, Zb, Xt, Yt, Zt]

        
def draw_polygons( points, screen, color, sources, cons , zbuf):

    if len(points) < 3:
        print 'Need at least 3 points to draw a polygon!'
        return

    p = 0

    view = [0, 0, 1]

    while p < len( points ) - 2:

        if calculate_dot( points, p ) < 0:
            #print points[30]
            #print "P\n\n\n\n"            
            pts = order_points( points, p )
            color = calculate_color(color, sources, cons, normalize(calculate_normal(points, p)), view)
            #print color
            #print points[30]
            #print "Q\n\n\n\n"            
            scanline_convert( screen, pts[0], pts[1], pts[2], 
                              pts[3], pts[4], pts[5], pts[6], pts[7], pts[8], color, zbuf )
        
        p+= 3


def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon( points, 
                 x, y, z, 
                 x, y1, z,
                 x1, y1, z)
    add_polygon( points, 
                 x1, y1, z, 
                 x1, y, z,
                 x, y, z)
    #back
    add_polygon( points, 
                 x1, y, z1, 
                 x1, y1, z1,
                 x, y1, z1)
    add_polygon( points, 
                 x, y1, z1, 
                 x, y, z1,
                 x1, y, z1)
    #top
    add_polygon( points, 
                 x, y, z1, 
                 x, y, z,
                 x1, y, z)
    add_polygon( points, 
                 x1, y, z, 
                 x1, y, z1,
                 x, y, z1)
    #bottom
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y1, z,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y1, z1,
	         x1, y1, z1)
    #right side
    add_polygon( points, 
                 x1, y, z, 
                 x1, y1, z,
                 x1, y1, z1)
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y, z1,
                 x1, y, z)
    #left side
    add_polygon( points, 
                 x, y, z1, 
                 x, y1, z1,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y, z,
                 x, y, z1) 


def add_sphere( points, cx, cy, cz, r, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_sphere( temp, cx, cy, cz, r, step )
    num_points = len( temp )

    lat = 0
    lat_stop = num_steps
    longt = 0
    longt_stop = num_steps

    num_steps += 1

    while lat < lat_stop:
        longt = 0
        while longt < longt_stop:
            
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]
            
            if longt != longt_stop - 1:
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]
            else:
                px2 = temp[ (index + 1) % num_points ][0]
                py2 = temp[ (index + 1) % num_points ][1]
                pz2 = temp[ (index + 1) % num_points ][2]
                
            px3 = temp[ index + 1 ][0]
            py3 = temp[ index + 1 ][1]
            pz3 = temp[ index + 1 ][2]
      
            if longt != 0:
                add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 )

            if longt != longt_stop - 1:
                add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 )
            
            longt+= 1
        lat+= 1

def generate_sphere( points, cx, cy, cz, r, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle <= circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = r * cos( pi * circ ) + cx
            y = r * sin( pi * circ ) * cos( 2 * pi * rot ) + cy
            z = r * sin( pi * circ ) * sin( 2 * pi * rot ) + cz
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step

def add_torus( points, cx, cy, cz, r0, r1, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_torus( temp, cx, cy, cz, r0, r1, step )
    num_points = len(temp)

    lat = 0
    lat_stop = num_steps
    longt_stop = num_steps
    
    while lat < lat_stop:
        longt = 0

        while longt < longt_stop:
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]

            if longt != num_steps - 1:            
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]

                px3 = temp[ (index + 1) % num_points ][0]
                py3 = temp[ (index + 1) % num_points ][1]
                pz3 = temp[ (index + 1) % num_points ][2]
            else:
                px2 = temp[ ((lat + 1) * num_steps) % num_points ][0]
                py2 = temp[ ((lat + 1) * num_steps) % num_points ][1]
                pz2 = temp[ ((lat + 1) * num_steps) % num_points ][2]

                px3 = temp[ (lat * num_steps) % num_points ][0]
                py3 = temp[ (lat * num_steps) % num_points ][1]
                pz3 = temp[ (lat * num_steps) % num_points ][2]


            add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 );
            add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 );        
            
            longt+= 1
        lat+= 1


def generate_torus( points, cx, cy, cz, r0, r1, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle < circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = (cos( 2 * pi * rot ) *
                 (r0 * cos( 2 * pi * circ) + r1 ) + cx)
            y = r0 * sin(2 * pi * circ) + cy
            z = (sin( 2 * pi * rot ) *
                 (r0 * cos(2 * pi * circ) + r1))
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step



def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    t = step
    while t<= 1:
        
        x = r * cos( 2 * pi * t ) + cx
        y = r * sin( 2 * pi * t ) + cy

        add_edge( points, x0, y0, cz, x, y, cz )
        x0 = x
        y0 = y
        t+= step
    add_edge( points, x0, y0, cz, cx + r, cy, cz )

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    xcoefs = generate_curve_coefs( x0, x1, x2, x3, curve_type )
    ycoefs = generate_curve_coefs( y0, y1, y2, y3, curve_type )
        
    t =  step
    while t <= 1:
        
        x = xcoefs[0][0] * t * t * t + xcoefs[0][1] * t * t + xcoefs[0][2] * t + xcoefs[0][3]
        y = ycoefs[0][0] * t * t * t + ycoefs[0][1] * t * t + ycoefs[0][2] * t + ycoefs[0][3]

        add_edge( points, x0, y0, 0, x, y, 0 )
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"
        
    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, matrix[p][0], matrix[p][1], matrix[p][2],
                   matrix[p+1][0], matrix[p+1][1], matrix[p+1][2], color )
        p+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point( matrix, x0, y0, z0 )
    add_point( matrix, x1, y1, z1 )

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( screen, x0, y0, z0, x1, y1, z1, color, zbuf):
    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0
    
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        dz = 0 - dz
        
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
        tmp = z0
        z0 = z1
        z1 = tmp
        dz = 0-dz
        
    elif dx == dy == 0:
        if z1 > z0:
            plot(screen, color, x0, y0, z1, zbuf)
        else:
            plot(screen, color, x0, y0, z0, zbuf)
    if dx == 0:
        y = y0
        z = z0
        while y < y1:
            plot(screen, color,  x0, y, z, zbuf)
            y = y + 1
            z = z + dz/dy
    elif dy == 0:
        x = x0
        z = z0
        while x <= x1:
            plot(screen, color, x, y0, z, zbuf)
            x = x + 1
            z = z + dz/dx
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        z = z0
        while x <= x1:
            plot(screen, color, x, y, z, zbuf)
            if d > 0:
                y = y - 1
                d = d - dx
                z = z + dz
            x = x + 1
            d = d - dy
            z = z + dz/dx
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        z = z0
        while y <= y1:
            plot(screen, color, x, y, z, zbuf)
            if d > 0:
                x = x - 1
                d = d - dy
                z = z + dz
            y = y + 1
            d = d - dx
            z = z + dz/dy
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        z = z0
        while x <= x1:
            plot(screen, color, x, y)
            if d > 0:
                y = y + 1
                d = d - dx
                z = z + dz
            x = x + 1
            d = d + dy
            z = z + dz/dx
    else:
        d = 0
        x = x0
        y = y0
        z = z0
        while y <= y1:
            plot(screen, color, x, y, z, zbuf)
            if d > 0:
                x = x + 1
                d = d - dy
                z = z + dz
            y = y + 1
            d = d + dx
            z = z + dz/dy
        

