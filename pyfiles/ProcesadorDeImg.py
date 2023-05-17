
from PIL import Image
  
img_01 = Image.open(r"Temp\IPPeIPC.png")
img_02 = Image.open(r"Temp\IPPIyTCRM.png")

  
img_01_size = img_01.size
img_02_size = img_02.size
  
# print('img 1 size: ', img_01_size)
# print('img 2 size: ', img_02_size)

new_im = Image.new('RGB', (2*img_01_size[0],img_01_size[1]), (250,250,250))
  
new_im.paste(img_01, (0,0))
new_im.paste(img_02, (img_01_size[0],0))

new_im.save(r"Temp\Indicadores.png", "PNG")
print('Done Procesamiento de Img 1!')

  
img_03 = Image.open(r"Temp\Indicadores_alt.png")
img_04 = Image.open(r"Temp\TCRM_alt.png")

  
img_03_size = img_03.size
img_04_size = img_04.size
  
# print('img 1 size: ', img_01_size)
# print('img 2 size: ', img_02_size)

new_im2 = Image.new('RGB', (2*img_03_size[0],img_03_size[1]), (250,250,250))
  
new_im2.paste(img_03, (0,0))
new_im2.paste(img_04, (img_03_size[0],0))

new_im2.save(r"Temp\Indicadores2.png", "PNG")
print('Done Procesamiento de Img 2!')
