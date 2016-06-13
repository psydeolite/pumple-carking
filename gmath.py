from math import sqrt

def calculate_normal( points, i ):
    ax = points[i + 1][0] - points[ i ][0]
    ay = points[i + 1][1] - points[ i ][1]
    az = points[i + 1][2] - points[ i ][2]

    bx = points[i + 2][0] - points[ i ][0]
    by = points[i + 2][1] - points[ i ][1]
    bz = points[i + 2][2] - points[ i ][2]
    
    normal = [0,0,0]
    normal[0] = ay * bz - az * by
    normal[1] = az * bx - ax * bz
    normal[2] = ax * by - ay * bx
    return normal

def calculate_dot( points, i ):
    #get as and bs to calculate the normal
    normal = calculate_normal( points, i )

    #set up the view vector values
    vx = 0
    vy = 0
    vz = -1
    
    #calculate the dot product
    dot = normal[0] * vx + normal[1] * vy + normal[2] * vz
    
    return dot

def dot_product( v0, v1 ):
    return v0[0]*v1[0] + v0[1]*v1[1] + v0[2]*v1[2]
    
def normalize(v):
    #print v
    mag = sqrt(pow(v[0],2)+pow(v[1],2)+pow(v[2],2))
    #print mag
    ret = [ 0, 0, 0 ]
    for x in range(3):
        if mag!=0:
            ret[x] = v[x]/mag
        else:
            ret[x] = v[x] 
    return ret

def sub_vectors(v0, v1):
    ret = v0
    for x in range(len(v0)):
        ret[x] = v0[x]-v1[x] 
    return ret

def scalar_product(v, s):
    for x in range(3):
        v[x]*=s
    return v
        
def calculate_color( color, sources, cons, normal, view ):
    ambi = [0, 0, 0]
    diff = [0, 0, 0]
    spec = [0, 0, 0]

    for x in range(3):
        ambi[x] = color[x]*cons[x]

    for source in sources:
        s = source[0:3]

        dlight = [0, 0, 0]
        slight = [0, 0, 0]

        for x in range(3):
            #print "s"+str(normalize(normal))
            #print normalize(s)
            dlight[x] = source[x+3]*cons[x+3]*dot_product(normalize(normal),normalize(s))
            
            temp = dot_product(normalize(s), normalize(normal))
            temp = scalar_product(normalize(normal), temp)
            temp = sub_vectors(temp, normalize(s))
            temp = scalar_product(temp, 2)
            temp = dot_product(temp, view)
            angle = pow(temp,2)

            slight[x] = source[x+3]*cons[x+6]*angle
            slight[x] == 0

            if dlight[x] > 0:
                diff[x] += dlight[x]

            if slight[x] > 0:
                spec[x] += slight[x]
                
    colr = [0, 0, 0]

    for x in range(3):
        c = int(ambi[x])+int(diff[x])+int(spec[x])
        
        if c < 0: 
            colr[x] = 0
        elif c > 255:
            colr[x] = 255
        else:
            colr[x] = c
    
    return colr
