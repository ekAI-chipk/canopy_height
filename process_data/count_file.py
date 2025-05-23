import os

root = 's2ch/S2'
for folder in os.listdir(root):
    print(len(os.listdir(os.path.join(root, folder))))
    