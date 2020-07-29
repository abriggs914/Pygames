

def truthy_list(lst):
    if type(lst) == list and len(lst) > 0:
        b = 0
        for el in lst:
            # print('el',el, 'lst', lst)
            if type(el) != list:
                return False
            if len(el) > b:
                b = len(el)
            for val in el:
                if type(val) != int:
                    return False
        return True and b != 0
    return False


a = [[]]
b = [[1]]
c = [[],[]]
d = [[1],[]]
e = []
f = [[],[],[],[],[]]
g = [[],[],[],[],[],[1]]
h = ['hey', 'there']
i = [['hey'], ['there']]
j = 'hey', 'there'
k = 1
l = ('hey', 'there')

print(truthy_list(a) == False)
print(truthy_list(b) == True)
print(truthy_list(c) == False)
print(truthy_list(d) == True)
print(truthy_list(e) == False)
print(truthy_list(f) == False)
print(truthy_list(g) == True)
print(truthy_list(h) == False)
print(truthy_list(i) == False)
print(truthy_list(j) == False)
print(truthy_list(k) == False)
print(truthy_list(l) == False)