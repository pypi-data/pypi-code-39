from mne.io import read_raw_ctf
import os
import matplotlib
import mne
import numpy as np
from mne.preprocessing import ICA, create_eog_epochs, create_ecg_epochs
import time
from IPython.display import clear_output
from brainpipe import feature
import mne
import matplotlib.pyplot as plt
from scipy.io import savemat, loadmat

def get_datafnames(DATA_FOLDER, keyword='NEUROMOD'):
    files_list = os.listdir(DATA_FOLDER)
    data_fnames = []
    for file in files_list:
        if keyword in file and '.ds' in file:
            data_fnames.append(file)
    return data_fnames

def inscapesMEG_PP(fname, DATA_FOLDER, SAVE_FOLDER):
    fpath = DATA_FOLDER + fname
    raw = read_raw_ctf(fpath, preload=True)
    picks = mne.pick_types(raw.info, meg=True, eog=True, exclude='bads')
    raw.plot();
    raw.plot_psd(average=False, picks=picks);

    ## Filtering
    high_cutoff = 200
    low_cutoff = 0.5
    raw.filter(low_cutoff, high_cutoff, fir_design="firwin")
    raw.notch_filter(np.arange(60, high_cutoff+1, 60), picks=picks, filter_length='auto',phase='zero', fir_design="firwin")
    raw.plot_psd(average=False, picks=picks);

    ## ICA
    ica = ICA(n_components=20, random_state=0).fit(raw, decim=3)
    ica.plot_sources(raw);
    fmax = 40. ## correlation threshold for ICA components (maybe increase to 40. ?)

    ## FIND ECG COMPONENTS
    ecg_epochs = create_ecg_epochs(raw, ch_name='EEG059')
    ecg_inds, ecg_scores = ica.find_bads_ecg(ecg_epochs, ch_name='EEG059')
    ica.plot_scores(ecg_scores, ecg_inds);
    ica.plot_properties(ecg_epochs, picks=ecg_inds, psd_args={'fmax': fmax}, image_args={'sigma': 1.});

    ## FIND EOG COMPONENTS
    eog_epochs = create_eog_epochs(raw, ch_name='EEG057')
    eog_inds, eog_scores = ica.find_bads_eog(eog_epochs, ch_name='EEG057')
    ica.plot_scores(eog_scores, eog_inds);
    ica.plot_properties(eog_epochs, picks=eog_inds, psd_args={'fmax': fmax}, image_args={'sigma': 1.});

    ## EXCLUDE COMPONENTS
    ica.exclude = ecg_inds
    ica.apply(raw)
    ica.exclude = eog_inds
    ica.apply(raw)
    raw.plot(); # Plot the clean signal.

    ## SAVE PREPROCESSED FILE
    time.sleep(60)
    raw.save(SAVE_FOLDER + fname + '_preprocessed.fif.gz', overwrite=True)
    time.sleep(30)
    filename = SAVE_FOLDER + fname + '_log.html'
    #!jupyter nbconvert inscapesMEG_preproc.ipynb --output $filename
    clear_output()

def segment_data(raw, new_sf=240., epochs_length=5.):
    # Habituellement, on veut epocher le signal en fonction des triggers. Mais ici on n'en a pas ;D
    # Cette fonction découpe le signal en "epochs" (=segments). C'est facultatif mais ça facilite les calculs par après.
    # Du coup on va faire des epochs de 5sec, parce que pourquoi pas.
    sf = raw.info['sfreq']
    picks = mne.pick_types(raw.info, meg=True, ref_meg=False, eeg=False, eog=True, stim=False) # Permet de ne sélectionner que les MEG channels sur lesquels on va continuer l'analyse (on exclu les EOG/ECG et références)
    data = raw.get_data() # Cette ligne là sort les données de l'objet raw pour les mettre dans une matrice. Ça nous sert juste pour avoir l'info de la taille de la matrice (N_channels X N_timepoints X N_epochs)
    length = epochs_length # length of an epoch *arbitrary <--- essayez de changer cette valeur, qu'est-ce que ça fait ? pourquoi ?
    n_sec = int(round(data.shape[1]/sf))
    n_blocks = int(round(n_sec/length))
    time = data.shape[1]

    # Create events object
    ev_starts = np.arange(0,time,length*sf)[:,np.newaxis] # L'objet event de MNE est un peu chelou, vous prenez pas le choux avec ça faites moi juste confiance ici =P
    ev_stops = np.asarray([0]*n_blocks)[:,np.newaxis]
    ev_id = np.asarray([1]*n_blocks)[:,np.newaxis]
    events = np.concatenate((ev_starts,ev_stops,ev_id),axis=1).astype(int) # On a créé l'objet event, on va ensuite l'utiliser pour faire le découpage

    # Construct Epochs
    event_id, tmin, tmax = 1, 0., 5. # Autour de chaque trigger, on prend de 0sec à 5sec (donc 5 secondes) et on appelle cet évènement "1"
    baseline = (None, None) # Pas de baseline pour les pauvres
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks, # c'est la fonction qui fait le découpage en epochs !
                    baseline=baseline, reject=dict(mag=5e-12),
                    preload=True)
    epochs.resample(new_sf, npad='auto')  # resample to reduce computation time. On passe donc à 240Hz d'échantillonage (faudrait changer ça si on veut aller regarder le haut gamma ! -> Nyquist frequency)
    return epochs

def get_ch_pos(epochs):
    ### Obtain actual sensor positions for plotting (keep only channels that are present in the data)
    new_ch_names = [s.strip('3105') for s in epochs.ch_names] # ajuste les noms de channels avant de comparer channels présents sur layout et data
    actual_ch_names = [s.strip('-') for s in new_ch_names] # me demande pas pk faut le faire en 2 temps, marche pas sinon
    reference_layout = mne.channels.find_layout(epochs.info) # obtain the CTF 275 layout based on the channels names
    reference_ch_names = reference_layout.names # let's just be very explicit in here...
    reference_pos = reference_layout.pos # again
    not_in_actual = [x for x in reference_ch_names if not x in actual_ch_names] # find chan names that are in layout but not in data

    # loop to get the indexes of chans to remove from the layout
    idx_to_del = []
    for i in range(len(not_in_actual)):
        idx_to_del.append(reference_ch_names.index(not_in_actual[i])) # get layout index of every chan name not in data
    reverted_idx_to_del = idx_to_del[::-1]

    # actually removes the chans (f*** code efficiency)
    list_ref_pos = list(reference_pos)
    for i in range(len(reverted_idx_to_del)):
        del list_ref_pos[reverted_idx_to_del[i]] # delete 'em
    new_ref_pos = np.array(list_ref_pos)

    ch_xy = new_ref_pos[:,0:2] # retain only the X and Y coordinates (0:2 veut dire "de 0 à 2", donc 0 et 1 car on compte pas 2)
    return ch_xy

def compute_PSD(epochs, sf, epochs_length, f=None):
    if f == None:
        f = [ [4, 8], [8, 12], [12, 20], [20, 30], [30, 60], [60, 90], [90, 120] ]
    # Choose MEG channels
    data = epochs.get_data() # On sort les data de l'objet MNE pour les avoir dans une matrice (un numpy array pour être précis)
    data = data.swapaxes(0,1).swapaxes(1,2) # On réarange l'ordre des dimensions pour que ça correspond à ce qui est requis par Brainpipe
    objet_PSD = feature.power(sf=int(sf), npts=int(sf*epochs_length), width=int(sf), step=int(sf/4), f=f, method='hilbert1') # La fonction Brainpipe pour créer un objet de calcul des PSD
    psds = objet_PSD.get(data)[0] # Ici on calcule la PSD !
    return psds

def custom_plot_topo(toplot, ch_xy, fig_name, cmap='magma'):
    # Ptite fonction pour faire le topoplot automatiquement
    #fig = plt.figure() # On créé une figure vide
    fig,_ = mne.viz.plot_topomap(data=toplot, pos=ch_xy, cmap=cmap, vmin=-1, vmax=1) # Et on la remplit avec une topomap de MNE qui affiche nos données
    plt.colorbar(fig, shrink=0.5) # Sans oublier la colorbar !
    plt.title(fig_name)
    return fig
