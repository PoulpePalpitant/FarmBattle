## -*- Encoding: UTF-8 -*-

prochainid=0
def getprochainid():
    global prochainid
    prochainid+=1
    return f'id_{prochainid}'

if __name__ == '__main__':
    test()