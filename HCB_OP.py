from Lib import *

flag_list = []

def OPARG_NULL(data, mode, offset_dict, **kwargs):
    if mode == "d":
        return ""
    elif mode == "c":
        return b""
    elif mode == "l":
        return 0

def OPARG_I8I8(data, mode, offset_dict, **kwargs):
    if mode == "d":
        i1 = data.readU8()
        i2 = data.readU8()
        return f"{i1} {i2}"
    elif mode == "c":
        i1, i2 = data.split(" ")
        return to_bytes(int(i1), 1) + to_bytes(int(i2), 1)
    elif mode == "l":
        return 2

def OPARG_X32(data, mode, offset_dict, **kwargs):#返回一个偏移，从偏移处读取函数
    if mode == "d":
        offset = data.readU32()
        return f"offset_{offset}"
    elif mode == "c":
        offset = int(data.split("_")[1])
        offset = offset_dict[offset]
        return to_bytes(offset, 4)
    elif mode == "l":
        return 4
        
def OPARG_I16(data, mode, offset_dict, **kwargs):
    if mode == "d":
        i = data.read(2)
        return f"{from_bytes(i)}"
    elif mode == "c":
        i = int(data)
        return to_bytes(i, 2)
    elif mode == "l":
        return 2

def OPARG_I32(data, mode, offset_dict, **kwargs):
    if mode == "d":
        return f"{data.readU32()}"
    elif mode == "c":
        return to_bytes(int(data), 4)
    elif mode == "l":
        return 4

def OPARG_I8(data, mode, offset_dict, **kwargs):
    if mode == "d":
        return f"{data.readU8()}"
    elif mode == "c":
        return to_bytes(int(data), 1)
    elif mode == "l":
        return 1

def OPARG_STRING(data, mode, offset_dict, **kwargs):
    encoding = kwargs["encoding"]
    if mode == "d":
        return data.readString()
    elif mode == "c":
        return to_bytes(len(data.encode(encoding)) + 1, 1) + data.encode(encoding) + b"\x00"
    elif mode == "l":
        return len(data.encode(encoding)) + 2

OPList = [
    [ 0x00, "nop", OPARG_NULL ],
    [ 0x01, "initstack", OPARG_I8I8 ],
    [ 0x02, "call", OPARG_X32 ],
    [ 0x03, "syscall", OPARG_I16 ],
    [ 0x04, "ret", OPARG_NULL ],
    [ 0x05, "ret2", OPARG_NULL ],
    [ 0x06, "jmp", OPARG_X32 ],
    [ 0x07, "jmpcond", OPARG_X32 ],
    [ 0x08, "pushtrue", OPARG_NULL ],
    [ 0x09, "pushfalse", OPARG_NULL ],
    [ 0x0A, "pushint4", OPARG_I32 ],
    [ 0x0B, "pushint2", OPARG_I16 ],
    [ 0x0C, "pushint", OPARG_I8 ],
    [ 0x0D, "pushfloat", OPARG_I32 ], 
    [ 0x0E, "pushstring", OPARG_STRING ],
    [ 0x0F, "pushglobal", OPARG_I16 ],
    [ 0x10, "pushstack", OPARG_I8 ],
    [ 0x11, "unk_11", OPARG_I16 ],
    [ 0x12, "unk_12", OPARG_I8 ],
    [ 0x13, "pushtop", OPARG_NULL ], 
    [ 0x14, "pushtemp", OPARG_NULL ],
    [ 0x15, "popglobal", OPARG_I16 ],
    [ 0x16, "copystack", OPARG_I8 ],
    [ 0x17, "unk_17", OPARG_I16 ],
    [ 0x18, "unk_18", OPARG_I8 ],
    [ 0x19, "neg", OPARG_NULL ],
    [ 0x1A, "add", OPARG_NULL ],
    [ 0x1B, "sub", OPARG_NULL ],
    [ 0x1C, "mul", OPARG_NULL ],
    [ 0x1D, "div", OPARG_NULL ],
    [ 0x1E, "mod", OPARG_NULL ],
    [ 0x1F, "test", OPARG_NULL ],
    [ 0x20, "logand", OPARG_NULL ],
    [ 0x21, "logor", OPARG_NULL ], 
    [ 0x22, "eq", OPARG_NULL ],
    [ 0x23, "neq", OPARG_NULL ], 
    [ 0x24, "gt", OPARG_NULL ],
    [ 0x25, "le", OPARG_NULL ],
    [ 0x26, "lt", OPARG_NULL ], 
    [ 0x27, "ge", OPARG_NULL ]
]

opdict_funcname = {}
for i in OPList:
    opdict_funcname[i[1]] = (i[0], i[2])

