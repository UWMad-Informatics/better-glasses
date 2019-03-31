import numpy as np
from collections import OrderedDict
from matminer.featurizers.base import BaseFeaturizer
from matminer.featurizers.composition import BandCenter
from pymatgen import Spin
from pymatgen.electronic_structure.dos import CompleteDos, FermiDos


class DOSFeaturizer(BaseFeaturizer):
    """
    Featurizes a pymatgen density of states, CompleteDos, object.
    """
    def __init__(self, contributors=1, significance_threshold=0.1,
                 energy_cutoff=0.5, sampling_resolution=100, gaussian_smear=0.1):
        """
        Args:
            contributors (int):
                Sets the number of top contributors to the DOS that are
                returned as features. (i.e. contributors=1 will only return the
                main cb and main vb orbital)
            significance_threshold (float):
                Sets the significance threshold for orbitals in the DOS.
                Does not impact the number of contributors returned. Only
                determines the feature value xbm_significant_contributors.
                The threshold is a fractional value between 0 and 1.
            energy_cutoff (float in eV):
                The extent (into the bands) to sample the DOS
            sampling_resolution (int):
                Number of points to sample DOS
            gaussian_smear (float in eV):
                Gaussian smearing (sigma) around each sampled point in the DOS
        """
        self.contributors = contributors
        self.significance_threshold = significance_threshold
        self.energy_cutoff = energy_cutoff
        self.sampling_resolution = sampling_resolution
        self.gaussian_smear = gaussian_smear

    def featurize(self, dos):
        """
        Args:
            dos (pymatgen CompleteDos or their dict):
                The density of states to featurize. Must be a complete DOS,
                (i.e. contains PDOS and structure, in addition to total DOS)
                and must contain the structure.

        Returns:
            xbm_score_i (float): fractions of ith contributor orbital
            xbm_location_i (str): fractional coordinate of ith contributor.
                For example, '0.0;0.0;0.0' if Gamma
            xbm_specie_i: (str) elemental specie of ith contributor (ex: 'Ti')
            xbm_character_i: (str) orbital character of ith contributor (s p d or f)
            xbm_nsignificant: (int) the number of orbitals with contributions
                above the significance_threshold
        """
        if isinstance(dos, dict):
            dos = CompleteDos.from_dict(dos)
        if dos.structure is None:
            raise ValueError('The input dos must contain the structure.')

        orbscores = get_cbm_vbm_scores(dos, self.energy_cutoff,
                                       self.sampling_resolution,
                                       self.gaussian_smear)

        feat = OrderedDict()
        for ex in ['cbm', 'vbm']:
            orbscores.sort(key=lambda x: x['{}_score'.format(ex)], reverse=True)
            scores = np.array([s['{}_score'.format(ex)] for s in orbscores])
            feat['{}_nsignificant'.format(ex)] = len(scores[scores > self.significance_threshold])

            i = 0
            while i < self.contributors:
                sd = orbscores[i]
                if i < len(orbscores):
                    for p in ['character', 'specie']:
                        feat['{}_{}_{}'.format(ex, p, i + 1)] = sd[p]
                    feat['{}_location_{}'.format(ex, i + 1)] = '{};{};{}'.format(
                        sd['location'][0], sd['location'][1], sd['location'][2])
                    feat['{}_score_{}'.format(ex, i + 1)] = float(sd['{}_score'.format(ex)])
                else:
                    for p in ['character', 'specie', 'location', 'score']:
                        feat['{}_{}_{}'.format(ex, p, i + 1)] = float('NaN')
                i += 1

        return list(feat.values())

    def feature_labels(self):
        labels = []
        for ex in ['cbm', 'vbm']:
            labels.append('{}_nsignificant'.format(ex))
            i = 0
            while i < self.contributors:
                for p in ['character', 'specie', 'location', 'score']:
                    labels.append('{}_{}_{}'.format(ex, p, i + 1))
                i += 1

        return labels

    def implementors(self):
        return ['Maxwell Dylla', 'Alireza Faghaninia', 'Anubhav Jain']


class DopingFermi(BaseFeaturizer):
    """
    This featurizers returns the fermi level (w.r.t. selected reference energy) 
    associated with a specified carrier concentration (1/cm3) and temperature.
    This feature requires the total density of state and structure. Structure
    as dos.structure (e.g. in CompleteDos) is required by FermiDos class.
    """
    def __init__(self, dopings=None, eref="midgap", T=300, return_eref=False):
        """
        Args:
            dopings ([float]): list of doping concentrations 1/cm3. Note that a
                negative concentration is treated as electron majority carrier
                (n-type) and positive for holes (p-type)
            eref (str or int or float): energy alignment reference. Defaults
                to midgap (equilibrium fermi). A fixed number can also be used.
                str options: "midgap", "vbm", "cbm", "dos_fermi", "band_center"
            T (float): absolute temperature in Kelvin
            return_eref: if True, instead of aligning the fermi levels based
                on eref, it (eref) will be explicitly returned as a feature
        """
        self.dopings = dopings or [-1e20, 1e20]
        self.eref = eref
        self.T = T
        self.return_eref = return_eref
        self.BC = BandCenter()

    def featurize(self, dos, bandgap=None):
        """
        Args:
            dos (pymatgen Dos, CompleteDos or FermiDos):
            bandgap (float): for example the experimentally measured band gap
                or one that is calculated via more accurate methods than the
                one used to generate dos. dos will be scissored to have the
                same electronic band gap as bandgap.
        Returns ([float]): features are fermi levels in eV at the given
            concentrations and temperature + eref in eV if return_eref
        """
        dos = FermiDos(dos, bandgap=bandgap)
        feats = []
        eref = 0.0
        for c in self.dopings:
            fermi = dos.get_fermi(c=c, T=self.T, nstep=50)
            if isinstance(self.eref, str):
                if self.eref == "dos_fermi":
                    eref = dos.efermi
                elif self.eref in ["midgap", "vbm", "cbm"]:
                    ecbm, evbm = dos.get_cbm_vbm()
                    if self.eref == "midgap":
                        eref = (evbm + ecbm)/2.0
                    elif self.eref == "vbm":
                        eref = evbm
                    elif self.eref == "cbm":
                        eref = ecbm
                elif self.eref == "band center":
                    eref = self.BC.featurize(dos.structure.composition)[0]
                else:
                    raise ValueError('Unsupported "eref": {}'.format(self.eref))
            else:
                eref = self.eref
            if not self.return_eref:
                fermi -= eref
            feats.append(fermi)
        if self.return_eref:
            feats.append(eref)
        return feats

    def feature_labels(self):
        """
        Returns ([str]): list of names of the features generated by featurize
            example: "fermi_c-1e+20T300" that is the fermi level for the
            electron concentration of 1e20 (c-1e+20) and temperature of 300K
        """
        labels = []
        for c in self.dopings:
            labels.append("fermi_c{}T{}".format(c, self.T))
        if self.return_eref:
            labels.append("{} eref".format(self.eref))
        return labels

    def implementors(self):
        return ["Alireza Faghaninia"]

    def citations(self):
        return []


def get_cbm_vbm_scores(dos, energy_cutoff, sampling_resolution, gaussian_smear):
    """
    Quantifies the strength of the contribution of all orbitals of various
        species/sites to the conduction band minimum (CBM) and the valence band
        maximum (VBM) up to energy_cutoff inside the bands from the CBM/VBM.
        An example use of the output may be sorting it based on cbm_score
        or vbm_score.
    Args:
        dos (pymatgen CompleteDos or their dict):
            The density of states to featurize. Must be a complete DOS,
            (i.e. contains PDOS and structure, in addition to total DOS)
        energy_cutoff (float in eV):
            The extent (into the bands) to sample the DOS
        sampling_resolution (int):
            Number of points to sample DOS
        gaussian_smear (float in eV):
            Gaussian smearing (sigma) around each sampled point in the DOS
    Returns:
        orbital_scores [(dict)]:
            A list of how much each orbital contributes to the partial
            density of states up to energy_cutoff. Dictionary items are:
            .. cbm_score: (float) fractional contribution to conduction band
            .. vbm_score: (float) fractional contribution to valence band
            .. species: (pymatgen Specie) the Specie of the orbital
            .. character: (str) is the orbital character s, p, d, or f
            .. location: [(float)] fractional coordinates of the orbital
    """

    cbm, vbm = dos.get_cbm_vbm(tol=0.01)
    structure = dos.structure
    sites = structure.sites

    orbital_scores = []
    for i in range(0, len(sites)):
        site = sites[i]
        proj = dos.get_site_spd_dos(site)
        for orb in proj:
            # calculate contribution
            energies = [e for e in proj[orb].energies]
            smear_dos = proj[orb].get_smeared_densities(gaussian_smear)
            dos_up = smear_dos[Spin.up]
            dos_down = smear_dos[Spin.down] if Spin.down in smear_dos \
                else smear_dos[Spin.up]
            dos_total = [sum(id) for id in zip(dos_up, dos_down)]
            vbm_score = 0
            vbm_space = np.linspace(vbm, vbm - energy_cutoff,
                                    num=sampling_resolution)
            for e in vbm_space:
                vbm_score += np.interp(e, energies, dos_total)
            cbm_score = 0
            cbm_space = np.linspace(cbm, cbm + energy_cutoff,
                                    num=sampling_resolution)
            for e in cbm_space:
                cbm_score += np.interp(e, energies, dos_total)

            # add orbital scores to list
            orbital_score = {
                'cbm_score': cbm_score,
                'vbm_score': vbm_score,
                'specie': str(site.specie),
                'character': str(orb),
                'location': list(site.frac_coords)}
            orbital_scores.append(orbital_score)

    # normalize by total contribution
    total_cbm = sum([orbital_scores[i]['cbm_score'] for i in
                     range(0, len(orbital_scores))])
    total_vbm = sum([orbital_scores[i]['vbm_score'] for i in
                     range(0, len(orbital_scores))])
    for orbital in orbital_scores:
        orbital['cbm_score'] = orbital['cbm_score'] / total_cbm
        orbital['vbm_score'] = orbital['vbm_score'] / total_vbm

    return orbital_scores
