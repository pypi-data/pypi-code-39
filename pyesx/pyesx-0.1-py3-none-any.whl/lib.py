# esxlib
# -----------------------------------------------------------------------------
#
#
# This file serves as a reference for all variables properties used in ESX
# Please be careful while changing it and adapt it to your needs
#
#
#
# Compatibility : python 3.7
#
#
# Arthur ENGUEHARD - 19/03/2019

# Define non local constantes
Navog = 6.022 * 10**23  # mol-1
Ncm3_2_nmolm3 = (1/Navog) * 10**6 * 10**9  # used to convert from ppb*Mair
PARfrac = 0.45   # fraction of Photo-Actiuve Radiation in Solar spectrum
Wm2_uE = 4.57    # Converting W/m2 to umol/m2/s for raditation


def ugm3_2_ppb(val, M, Dair=2.4e25):
    """
    val: (float)
        Concentration (ug/m3)
    M: (float)
        molar weight (g/mol)
    Dair: (float)
        Air Molecular Density (molecules/m3)
    """
    return (10**6 * val / M) * Navog / Dair


def ppb_2_nmolcm3(val, M, Dair=2.4e19):
    return 10**-9 * val * Dair * 10**9 / Navog


def moleccm3_2_ppb(concentration):
    """Turns molecules/cm3 into ppb assuming Air Molar Volume of 22.4 L/mol
    """
    Na = 6.022E23
    return concentration/((1/22.4E3)*Na)*(10**6)


def ugNm2s_2_nmolNOcm2s(val):
    MN = 14  # g/mol
    #      l
    return val * 10**-6 * 10**9 * 10**-4 / MN


def nmolcm2sNO_2_mgNm2s(val):
    MN = 14  # g/mol
    #       to_mol  to_m2   to_gN   to_mg
    return 10**-9 * 10**4 * MN * 10**3 * val
