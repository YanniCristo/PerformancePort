import os

pth = 'assets/contents/ecoview/articles'
macro = [nome for nome in os.listdir(pth) 
         if os.path.isdir(os.path.join(pth, nome))]

