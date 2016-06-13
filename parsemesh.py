f=open('inuitours-cut-ascii.stl', 'r')
r=f.read()
#print r
f.close()
r=r.replace('outer loop','')
r=r.replace('endloop', '')
r=r.replace('endfacet', '')
#print r
s=r.split('\n')
#print s
e=[]
for el in s:
    if 'vertex' in el:
        e.append(el)
#print e
g=[]
for el in e:
    g.append(el.replace('vertex','').strip())
#print g
points=[]
h=[]
for el in g:
    h.append(el.split(' '))
#print h

for el in h:
    for c in el:
        #points.append(float(c))
        points.append(c+' ')
#print points
p=''.join(points)
print p

t=open('arraytest', 'w')
t.write(p)
t.close()
