import io as i
import os as o
import shutil as s
import struct as st
import sys as y
from optparse import OptionParser as OP


def f0(bn):
    """
    Extracting binary data from the file...
    Might as well skip to cert location, right?
    """
    d = {}
    with open(bn, 'rb') as b:
        b.seek(int('3C', 16))
        d['b'] = 0
        d['jmp'] = 0
        d['hdr_offset'] = 248
        d['pe_hdr_loc'] = st.unpack('<i', b.read(4))[0]
        d['coff_start'] = d['pe_hdr_loc'] + 4
        b.seek(d['coff_start'])
        d['machine'] = st.unpack('<H', b.read(2))[0]
        d['sec_count'] = st.unpack('<H', b.read(2))[0]
        d['timestamp'] = st.unpack('<I', b.read(4))[0]
        b.seek(d['coff_start'] + 16, 0)
        d['opt_hdr_size'] = st.unpack('<H', b.read(2))[0]
        d['characteristics'] = st.unpack('<H', b.read(2))[0]
        d['opt_hdr_start'] = d['coff_start'] + 20

        b.seek(d['opt_hdr_start'])
        d['magic'] = st.unpack('<H', b.read(2))[0]
        d['maj_ver'] = st.unpack("!B", b.read(1))[0]
        d['min_ver'] = st.unpack("!B", b.read(1))[0]
        d['code_size'] = st.unpack("<I", b.read(4))[0]
        d['init_data_size'] = st.unpack("<I", b.read(4))[0]
        d['uninit_data_size'] = st.unpack("<I", b.read(4))[0]
        d['entry_point'] = st.unpack('<I', b.read(4))[0]
        d['patch_loc'] = d['entry_point']
        d['code_base'] = st.unpack('<I', b.read(4))[0]
        if d['magic'] != 0x20B:
            d['data_base'] = st.unpack('<I', b.read(4))[0]

        if d['magic'] == 0x20B:
            d['image_base'] = st.unpack('<Q', b.read(8))[0]
        else:
            d['image_base'] = st.unpack('<I', b.read(4))[0]
        
        # Alignment and version info
        for key in ['section_align', 'file_align', 'maj_os_ver', 'min_os_ver', 'maj_img_ver', 'min_img_ver',
                     'maj_subsys_ver', 'min_subsys_ver', 'win32_ver_val', 'img_size', 'hdr_size', 'checksum']:
            d[key] = st.unpack('<I', b.read(4))[0]

        if d['magic'] == 0x20B:
            for key in ['stack_reserve', 'stack_commit', 'heap_reserve', 'heap_commit']:
                d[key] = st.unpack('<Q', b.read(8))[0]
        else:
            for key in ['stack_reserve', 'stack_commit', 'heap_reserve', 'heap_commit']:
                d[key] = st.unpack('<I', b.read(4))[0]

        d['loader_flags'] = st.unpack('<I', b.read(4))[0]  # zero
        d['num_rva_sizes'] = st.unpack('<I', b.read(4))[0]
        for key in ['export_rva', 'export_size', 'import_loc', 'import_rva', 'import_size', 'resource_tbl', 
                     'exception_tbl', 'cert_loc', 'cert_size']:
            d[key] = st.unpack('<Q' if 'tbl' in key else '<I', b.read(8 if 'tbl' in key else 4))[0]

    return d


def f1(ex):
    d = f0(ex)
    if d['cert_loc'] == 0 or d['cert_size'] == 0:
        return None
    with open(ex, 'rb') as f:
        f.seek(d['cert_loc'])
        return f.read(d['cert_size'])


def f2(cert, ex, out):
    d = f0(ex)
    if not out: 
        out = str(ex) + "_signed"
    s.copy2(ex, out)

    with open(ex, 'rb') as g:
        with open(out, 'wb') as f:
            f.write(g.read())
            f.seek(d['cert_loc'])
            f.write(st.pack("<I", len(g.read())))
            f.write(st.pack("<I", len(cert)))
            f.seek(0, i.SEEK_END)
            f.write(cert)


def f3(ex, out):
    cert = f1(ex)
    if cert:
        if not out:
            out = str(ex) + "_sig"
        with open(out, 'wb') as f:
            f.write(cert)


def f4(ex):
    d = f0(ex)
    if d['cert_loc'] == 0 or d['cert_size'] == 0:
        pass


def f5(ex, out):
    d = f0(ex)
    if d['cert_loc'] == 0 or d['cert_size'] == 0:
        y.exit(-1)

    if not out:
        out = str(ex) + "_nosig"
    
    s.copy2(ex, out)
    
    with open(out, "r+b") as binary:
        binary.seek(-d['cert_size'], i.SEEK_END)
        binary.truncate()
        binary.seek(d['cert_loc'])
        binary.write(b"\x00" * 8)


def f6(ex, sig_file, out):
    d = f0(ex)
    cert = open(sig_file, 'rb').read()
    if not out: 
        out = str(ex) + "_signed"
    
    if o.path.abspath(ex) != o.path.abspath(out):
        s.copy2(ex, out)

    with open(ex, 'rb') as g:
        data = g.read()

    with open(out, 'wb') as f:
        f.write(data)
        f.seek(d['cert_loc'])
        f.write(st.pack("<I", len(data)))
        f.write(st.pack("<I", len(cert)))
        f.seek(0, i.SEEK_END)
        f.write(cert)


if __name__ == "__main__":
    u = 'usage: %prog [options]'
    p = OP()
    p.add_option("-i", "--file", dest="input", help="input file", metavar="FILE")
    p.add_option('-r', '--rip', dest='rip', action='store_true', help='rip signature off inputfile')
    p.add_option('-a', '--add', dest='add', action='store_true', help='add signature to targetfile')
    p.add_option('-o', '--output', dest='output', help='output file')
    p.add_option('-s', '--sig', dest='sig', help='binary signature from disk')
    p.add_option('-t', '--target', dest='target', help='file to append signature to')
    p.add_option('-c', '--checksig', dest='check', action='store_true', help='check if signed; does not verify signature')
    p.add_option('-T', '--truncate', dest="truncate", action='store_true', help='truncate signature (i.e. remove sig)')
    
    opts, args = p.parse_args()

    if opts.input and opts.rip:
        f3(opts.input, opts.output)
        y.exit()

    if opts.input and opts.target:
        cert = f1(opts.input)
        f2(cert, opts.target, opts.output)
        y.exit()

    if opts.input and opts.check:
        f4(opts.input)
        y.exit()

    if opts.target and opts.sig:
        f6(opts.target, opts.sig, opts.output)
        y.exit()

    if opts.input and opts.truncate:
        f5(opts.input, opts.output)
        y.exit()

    p.error("You must do something!")