import matplotlib.pyplot as pt
import matplotlib.dates
import meteoCocito
import datetime
from PIL import Image
import os
import instabot
import glob
# Remember to `pip install -r requirements.txt`

meteoCocito.DataArchive.update()

def dayPlot():
    oggi = meteoCocito.DataArchive.day()
    x_values = {}
    y_values = {}
    for dt in meteoCocito.DataTypeArchive.Symbols:
        x_values[dt.value] = []
        y_values[dt.value] = []
    for valore in oggi:
         x_values[valore.symbol.value].append(valore.instant.strftime("%H:%M"))
         y_values[valore.symbol.value].append(float(valore))
    fig = pt.figure(frameon = False)
    fig.set_size_inches(10.80,10.80)
    fpc = 2
    i = 0
    rows = len(x_values.keys())//fpc
    columns = fpc
    colors = ["red","blue","green","cyan","magenta","orange"]
    i = 0
    for symbol in x_values.keys():
        dt = meteoCocito.DataTypeArchive.fromSymbol(symbol)
        ax = fig.add_subplot(rows, columns, i+1, title = dt.italianName)
        ax.set_ylabel(dt.unit)
        ax.set_xlabel("Ora")
        ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(40))
        ax.plot(x_values[symbol], y_values[symbol], color = colors[i])
        i += 1
    fig.tight_layout()
    pt.text(1,1,datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    pt.savefig("dy.png")
    png = Image.open("dy.png").convert("RGBA")
    bg = Image.new("RGBA", png.size, (255,255,255))
    alpha_composite = Image.alpha_composite(bg,png).convert("RGB")
    alpha_composite.save("day.jpg","JPEG", quality = 100)
    os.unlink("dy.png")
dayPlot()
cookie_del = glob.glob("config/*cookie.json")
if len(cookie_del):
    os.remove(cookie_del[0])
text = meteoCocito.TextGenerator.current()[0]+"\n=============\n"+("\n".join(meteoCocito.TextGenerator.day()))
print(text)
bot = instabot.Bot()
bot.login(username = os.environ["username"], password = os.environ["password"])
bot.upload_photo("day.jpg",text)
