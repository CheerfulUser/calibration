from astropy.io import fits
import numpy as np
import pandas as pd
from glob import glob
import os.path

path = '/home/rridden/data/kepler/everest/'
stars = 'K2_all_PS1_psc.csv'
save = 'K2_all_PS1_psc_ev.csv'


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
        camp = file.split('-c')[-1].split('_')[0].strip('0')
        epic = int(file.split('llc_')[-1].split('-')[0])
        if '112' not in camp:
            if '111' in camp:
                camp = '11'
                eleven = file.split('c111')
                pdc = np.array([])
                sap = np.array([])
                
                for i in range(2):
                    name = eleven[0]+'c11' + str(i+1) + eleven[1]
                    if os.path.isfile(name):
                        hdu = fits.open(name)
                        hdr = hdu[0].header
                        module = hdr['module']
                        channel = hdr['channel']
                        output = hdr['output']
                        try:
                            pdc = np.append(pdc,hdu[1].data.field('PDCSAP_FLUX'))
                            sap = np.append(sap,hdu[1].data.field('SAP_FLUX'))
                        except KeyError:
                            pdc = np.append(pdc,hdu[1].data.field('FLUX'))
                            sap = np.append(sap,hdu[1].data.field('FRAW'))
            else:
                hdu = fits.open(file)
                hdr = hdu[0].header
                module = hdr['module']
                channel = hdr['channel']
                output = hdr['output']
                try:
                    pdc = hdu[1].data.field('PDCSAP_FLUX')
                    sap = hdu[1].data.field('SAP_FLUX')
                except KeyError:
                    pdc = hdu[1].data.field('FLUX')
                    sap = hdu[1].data.field('FRAW')
                        
            if camp == '':
                camp = 0

            pos = np.where((int(epic) == df['ID'].values.astype(int)) & 
                  (int(camp) == df['campaign'].values.astype(int)))[0]
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