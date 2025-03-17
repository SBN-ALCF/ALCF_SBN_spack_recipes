def undr_to_dot(version):
    return version.replace("_",".").replace("v","",1)

def dot_to_undr(version):
    return "v"+version.replace(".","_")

def undr_to_dash(version):
    return version.replace("_","-")
