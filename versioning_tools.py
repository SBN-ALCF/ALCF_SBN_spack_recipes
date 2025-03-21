def undr_to_dot(version):
    return version.replace("_",".").replace("v","",1)

def dot_to_undr(version):
    return "v"+version.replace(".","_")

def undr_to_dash(version):
    return version.replace("_","-")

def patch(version):
    splt = version.split("_")
    ret = ""
    for i in range(len(splt)):
        if i != len(splt)-1:
            ret += splt[i]+"_"
        else:
            ret += "p"+splt[i]
    return ret 
