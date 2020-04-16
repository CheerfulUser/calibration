from astropy.io import fits
import numpy as np
import pandas as pd
from glob import glob

path = './c16/'
stars = 'c16_all_stars.csv'
save = 'c16_all_stars_ev.csv'


def Add_k2_info(stars, path, save):
    df = pd.read_csv(stars)
    lc_df = df.copy()

    lc_df['Module'] = -1
    lc_df['Channel'] = -1
    lc_df['Output'] = -1

    lc_df['PDC'] = -1
    lc_df['PDCe'] = -1

    lc_df['SAP'] = -1
    lc_df['SAPe'] = -1


    files = glob(path + '*.fits')
    for file in files:
        hdu = fits.open(file)
        hdr = hdu[0].header
        module = hdr['module']
        channel = hdr['channel']
        output = hdr['output']

        try:
            pdc = hdu[1].data.field('PDCSAP_FLUX')
            sap = hdu[1].data.field('SAP_FLUX')
            epic = int(file.split('ktwo')[-1].split('-')[0])
        except KeyError:
            pdc = hdu[1].data.field('FLUX')
            sap = hdu[1].data.field('FRAW')
            epic = int(file.split('llc_')[-1].split('-')[0])
            

        
        pos = np.where(int(epic) == df['ID'].values.astype(int))[0]
        if len(pos) > 0:
            pos = pos[0]

            
            lc_df['Module'].iloc[pos] = int(module)
            lc_df['Channel'].iloc[pos] = int(channel)
            lc_df['Output'].iloc[pos] = int(output)
            
            lc_df['PDC'].iloc[pos] = np.nanmedian(pdc)
            lc_df['PDCe'].iloc[pos] = np.nanstd(pdc)
            
            lc_df['SAP'].iloc[pos] = np.nanmedian(sap)
            lc_df['SAPe'].iloc[pos] = np.nanstd(sap)
        print('done: ', file)
    lc_df.to_csv(save,index=False)


if __name__ == '__main__':
    Add_k2_info(stars,path,save)