import os, stat
from pathlib import Path
from os.path import realpath
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import matplotlib.cm as cm
from PIL import Image


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = 'dejavuserif'
class OOMFormatter(mpl.ticker.ScalarFormatter):
    def __init__(self, order=0, fformat="%1.1e", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        mpl.ticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
            self.format = r'$\mathdefault{%s}$' % self.format


# Open the images

nrow = 1
ncolumn = 2

iFlag_colorbar = 1
iFlag_scientific_notation_colorbar = 0

aImage = list()

sFilename = '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240101002/mosart_sag_parameter_rwid.png'
image_dummy = Image.open(sFilename)
aImage.append(image_dummy)

sFilename = '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_parameter_rwid.png'
image_dummy = Image.open(sFilename)
aImage.append(image_dummy)

# Create a figure and subplots

fig, axs = plt.subplots( 1,ncolumn+1, figsize=(16, 10), gridspec_kw={'width_ratios': [4,4,1]},dpi=300)
plt.subplots_adjust(hspace=0.0, wspace=0.0, top=1.0)  # Adjust spacing here

for icolumn in range(1, ncolumn+1):
    ax_dummy = axs[icolumn-1]
    ax_dummy.imshow(aImage[icolumn-1])
    ax_dummy.axis('off')

ax_dummy = axs[ncolumn]
ax_dummy.axis('off')

# Add a common title above the subplots
#anchored_text = AnchoredText("Surface elevation", loc='upper center', frameon=False, prop=dict(fontsize=16))

fig.suptitle("Main channel width", fontsize=16,  y=0.98)
# Adjust layout
#add an additional colorbar

dValue_min=0
dValue_max= 250 # 6.0E12
sColormap = 'YlGnBu'
sExtend =  'max'
sUnit= r'Unit: m'
cmap = cm.get_cmap(sColormap)
if iFlag_colorbar ==1:
    ax_pos0 = axs[0].get_position()
    ax_pos1 = axs[1].get_position()
    #use this ax to set the colorbar ax position
    #calculat the heigh
    dHeight = ax_pos0.height
    ax_cb = fig.add_axes([ax_pos1.x1+0.02, ax_pos1.y0, 0.015, dHeight])
    if iFlag_scientific_notation_colorbar==1:
        formatter = OOMFormatter(fformat= "%1.1e")
        cb = mpl.colorbar.ColorbarBase(ax_cb, orientation='vertical',
                                       cmap=cmap,
                                       norm=mpl.colors.Normalize(dValue_min, dValue_max),  # vmax and vmin
                                       extend=sExtend, format=formatter)
    else:
        formatter = OOMFormatter(fformat= "%1.2f")
        cb = mpl.colorbar.ColorbarBase(ax_cb, orientation='vertical',
                                       cmap=cmap,
                                       norm=mpl.colors.Normalize(dValue_min, dValue_max),  # vmax and vmin
                                       extend=sExtend, format=formatter)
    cb.ax.get_yaxis().set_ticks_position('right')
    cb.ax.get_yaxis().labelpad = 4
    cb.ax.set_ylabel(sUnit, rotation=90, fontsize=14)
    cb.ax.get_yaxis().set_label_position('left')
    cb.ax.tick_params(labelsize=14)

# Save the merged image with titles
sFilename_out = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/sag/comparison/river_width_comparison.png'
#plt.show()
plt.savefig(sFilename_out,  bbox_inches='tight', pad_inches=0)

