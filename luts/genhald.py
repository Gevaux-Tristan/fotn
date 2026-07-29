import zlib, struct, math, random

N = 25          # cube nodes per channel  (25^3 = 15625 entries)
W = H = 125     # square image, 125*125 = 15625 pixels  (one pixel per node)

def node_rgb_for_index(i):
    r = i % N
    g = (i // N) % N
    b = i // (N*N)
    return r, g, b

# --- build identity pixel buffer ---
pix = bytearray(W*H*3)
for i in range(N**3):
    r,g,b = node_rgb_for_index(i)
    x = i % W; y = i // W
    off = (y*W + x)*3
    pix[off]   = round(r*255/(N-1))
    pix[off+1] = round(g*255/(N-1))
    pix[off+2] = round(b*255/(N-1))

def write_png(path, w, h, rgb):
    def chunk(typ, data):
        c = typ + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    raw = bytearray()
    for y in range(h):
        raw.append(0)                       # filter: none
        raw += rgb[y*w*3:(y+1)*w*3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))  # 8-bit RGB
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    open(path,"wb").write(png)

write_png("lut-identity.png", W, H, pix)
print("wrote lut-identity.png", W, "x", H)

# --- read back into a cube and trilinear-test it reproduces identity ---
def build_cube(pix):
    cube = [0.0]*(N*N*N*3)
    for i in range(N**3):
        r,g,b = node_rgb_for_index(i)
        x = i % W; y = i // W
        off = (y*W + x)*3
        ci = (b*N*N + g*N + r)*3
        cube[ci]   = pix[off]/255
        cube[ci+1] = pix[off+1]/255
        cube[ci+2] = pix[off+2]/255
    return cube

def tri(cube, r,g,b):
    def cl(v): return 0.0 if v<0 else 1.0 if v>1 else v
    r,g,b = cl(r),cl(g),cl(b)
    fr,fg,fb = r*(N-1), g*(N-1), b*(N-1)
    r0,g0,b0 = int(fr),int(fg),int(fb)
    r1,g1,b1 = min(r0+1,N-1),min(g0+1,N-1),min(b0+1,N-1)
    dr,dg,db = fr-r0, fg-g0, fb-b0
    out=[0,0,0]
    for ch in range(3):
        def C(ri,gi,bi): return cube[(bi*N*N+gi*N+ri)*3+ch]
        c00=C(r0,g0,b0)*(1-dr)+C(r1,g0,b0)*dr
        c01=C(r0,g0,b1)*(1-dr)+C(r1,g0,b1)*dr
        c10=C(r0,g1,b0)*(1-dr)+C(r1,g1,b0)*dr
        c11=C(r0,g1,b1)*(1-dr)+C(r1,g1,b1)*dr
        c0=c00*(1-dg)+c10*dg
        c1=c01*(1-dg)+c11*dg
        out[ch]=c0*(1-db)+c1*db
    return out

cube = build_cube(pix)
maxerr=0
random.seed(1)
for _ in range(20000):
    r,g,b=random.random(),random.random(),random.random()
    o=tri(cube,r,g,b)
    maxerr=max(maxerr, abs(o[0]-r),abs(o[1]-g),abs(o[2]-b))
print("identity trilinear max error over 20000 samples: %.5f"%maxerr, "(<= ~1/255 expected from 8-bit nodes)")
