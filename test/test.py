import re
from module.user import user
obj = user("","")
str1 = str(obj.__class__)
print(str1,"====")
pattern = r"(?<=\.).+(?=')"
res = re.findall(pattern, ".user'")[0]
print(res)