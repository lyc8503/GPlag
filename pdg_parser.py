import networkx as nx
import os
import subprocess
import shutil


assert shutil.which("joern-parse") != None and shutil.which("joern-export") != None, "Make sure you have joern executables in your PATH, which are available at https://github.com/joernio/joern/releases"
    

def find_all_srcs(path):
    file_extensions = ['.py', '.java', '.c', '.cpp']
    file_list = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(tuple(file_extensions)):
                file_list.append(os.path.join(root, file))

    return file_list

def parse_prog(src_path, output):
    ret = subprocess.call(["joern-parse", "-o", output, src_path])
    assert ret == 0

def load_pdg(db, output):
    # ret = subprocess.call(["joern-export", "--repr", "cfg", "--format", "dot", "-o", output, db])
    # ret = subprocess.call(["joern-export", "--repr", "cdg", "--format", "dot", "-o", output, db])
    ret = subprocess.call(["joern-export", "--repr", "pdg", "--format", "dot", "-o", output, db])
    assert ret == 0

    pdgs = []
    for i in os.listdir(output):
        pdgs.append(nx.Graph(nx.nx_agraph.read_dot(output + "/" + i)))

    return pdgs

def remove(path):
    try:
        os.remove(path)
    except:
        pass

    try:
        shutil.rmtree(path)
    except:
        pass

def load_all_pdgs(path):

    s = find_all_srcs(path)
    ret = []
    for i in s:
        print(">>> Parsing " + i)

        remove("/tmp/gplag-db")
        remove("/tmp/gplag-pdg")

        parse_prog(i, "/tmp/gplag-db")
        ret += load_pdg("/tmp/gplag-db", "/tmp/gplag-pdg")
    return ret
