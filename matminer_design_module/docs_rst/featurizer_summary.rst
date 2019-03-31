====================
Table of Featurizers
====================

Below, you will find a description of each featurizer, listed in tables grouped by module.


-------------
bandstructure
-------------
Features derived from a material's electronic bandstructure.
-------------------------------------------------------------

(matminer.featurizers.bandstructure)

=========================   ================================================================================================================================================================================================================================================================================================================================================================================================================
Name                        Description
=========================   ================================================================================================================================================================================================================================================================================================================================================================================================================
:code:`BranchPointEnergy`   Branch point energy and absolute band edge position. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.bandstructure.BranchPointEnergy>`_
:code:`BandFeaturizer`      Featurizes a pymatgen band structure object. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.bandstructure.BandFeaturizer>`_
=========================   ================================================================================================================================================================================================================================================================================================================================================================================================================




----
base
----
Parent classes and meta-featurizers.
-------------------------------------

(matminer.featurizers.base)

==========================   ================================================================================================================================================================================================================================================================================================================================================================================================================
Name                         Description
==========================   ================================================================================================================================================================================================================================================================================================================================================================================================================
:code:`MultipleFeaturizer`   Class that runs multiple featurizers on the same data `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.base.MultipleFeaturizer>`_
:code:`BaseFeaturizer`       Abstract class to calculate features from raw materials input data `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.base.BaseFeaturizer>`_
==========================   ================================================================================================================================================================================================================================================================================================================================================================================================================




-----------
composition
-----------
Features based on a material's composition.
--------------------------------------------

(matminer.featurizers.composition)

===============================   ================================================================================================================================================================================================================================================================================================================================================================================================================
Name                              Description
===============================   ================================================================================================================================================================================================================================================================================================================================================================================================================
:code:`ElementProperty`           Class to calculate elemental property attributes. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.ElementProperty>`_
:code:`OxidationStates`           Statistics about the oxidation states for each specie. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.OxidationStates>`_
:code:`AtomicOrbitals`            Determine HOMO/LUMO features based on a composition. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.AtomicOrbitals>`_
:code:`BandCenter`                Estimation of absolute position of band center using electronegativity. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.BandCenter>`_
:code:`ElectronegativityDiff`     Features from electronegativity differences between anions and cations. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.ElectronegativityDiff>`_
:code:`ElectronAffinity`          Calculate average electron affinity times formal charge of anion elements. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.ElectronAffinity>`_
:code:`Stoichiometry`             Calculate norms of stoichiometric attributes. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.Stoichiometry>`_
:code:`ValenceOrbital`            Attributes of valence orbital shells `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.ValenceOrbital>`_
:code:`IonProperty`               Ionic property attributes. Similar to ElementProperty. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.IonProperty>`_
:code:`ElementFraction`           Class to calculate the atomic fraction of each element in a composition. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.ElementFraction>`_
:code:`TMetalFraction`            Class to calculate fraction of magnetic transition metals in a composition. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.TMetalFraction>`_
:code:`CohesiveEnergy`            Cohesive energy per atom using elemental cohesive energies and `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.CohesiveEnergy>`_
:code:`Miedema`                   Formation enthalpies of intermetallic compounds, from Miedema et al. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.Miedema>`_
:code:`YangSolidSolution`         Mixing thermochemistry and size mismatch terms of Yang and Zhang (2012) `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.YangSolidSolution>`_
:code:`AtomicPackingEfficiency`   Packing efficiency based on a geometric theory of the amorphous packing `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.composition.AtomicPackingEfficiency>`_
===============================   ================================================================================================================================================================================================================================================================================================================================================================================================================




---
dos
---
Features based on a material's electronic density of states.
-------------------------------------------------------------

(matminer.featurizers.dos)

=====================   ================================================================================================================================================================================================================================================================================================================================================================================================================
Name                    Description
=====================   ================================================================================================================================================================================================================================================================================================================================================================================================================
:code:`DOSFeaturizer`   Featurizes a pymatgen density of states, CompleteDos, object. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.dos.DOSFeaturizer>`_
:code:`DopingFermi`     This featurizers returns the fermi level (w.r.t. selected reference energy)  `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.dos.DopingFermi>`_
=====================   ================================================================================================================================================================================================================================================================================================================================================================================================================




--------
function
--------
Classes for expanding sets of features calculated with other featurizers.
--------------------------------------------------------------------------

(matminer.featurizers.function)

==========================   ================================================================================================================================================================================================================================================================================================================================================================================================================
Name                         Description
==========================   ================================================================================================================================================================================================================================================================================================================================================================================================================
:code:`FunctionFeaturizer`   Features from functions applied to existing features, e.g. "1/x" `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.function.FunctionFeaturizer>`_
==========================   ================================================================================================================================================================================================================================================================================================================================================================================================================




----
site
----
Features from individual sites in a material's crystal structure.
------------------------------------------------------------------

(matminer.featurizers.site)

=============================================   ================================================================================================================================================================================================================================================================================================================================================================================================================
Name                                            Description
=============================================   ================================================================================================================================================================================================================================================================================================================================================================================================================
:code:`AGNIFingerprints`                        Product integral of RDF and Gaussian window function, from Botu et al. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.AGNIFingerprints>`_
:code:`OPSiteFingerprint`                       Local structure order parameters computed from a site's neighbor env. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.OPSiteFingerprint>`_
:code:`CrystalNNFingerprint`                    This is intended to be a successor to CrystalSiteFingerprint, currently `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.CrystalNNFingerprint>`_
:code:`CrystalSiteFingerprint`                  A local order parameter fingerprint for periodic crystals. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.CrystalSiteFingerprint>`_
:code:`VoronoiFingerprint`                      Voronoi tessellation-based features around target site. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.VoronoiFingerprint>`_
:code:`ChemicalSRO`                             Chemical short range ordering, deviation of local site and nominal structure compositions `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.ChemicalSRO>`_
:code:`GaussianSymmFunc`                        Gaussian symmetry function features suggested by Behler et al. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.GaussianSymmFunc>`_
:code:`EwaldSiteEnergy`                         Compute site energy from Coulombic interactions `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.EwaldSiteEnergy>`_
:code:`ChemEnvSiteFingerprint`                  Resemblance of given sites to ideal environments `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.ChemEnvSiteFingerprint>`_
:code:`CoordinationNumber`                      Number of first nearest neighbors of a site. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.CoordinationNumber>`_
:code:`GeneralizedRadialDistributionFunction`   Compute the general radial distribution function (GRDF) for a site. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.GeneralizedRadialDistributionFunction>`_
:code:`AngularFourierSeries`                    Compute the angular Fourier series (AFS), including both angular and radial info `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.AngularFourierSeries>`_
:code:`LocalPropertyDifference`                 Differences in elemental properties between site and its neighboring sites. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.site.LocalPropertyDifference>`_
=============================================   ================================================================================================================================================================================================================================================================================================================================================================================================================




---------
structure
---------
Generating features based on a material's crystal structure.
-------------------------------------------------------------

(matminer.featurizers.structure)

============================================   ================================================================================================================================================================================================================================================================================================================================================================================================================
Name                                           Description
============================================   ================================================================================================================================================================================================================================================================================================================================================================================================================
:code:`DensityFeatures`                        Calculates density and density-like features `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.DensityFeatures>`_
:code:`GlobalSymmetryFeatures`                 Determines symmetry features, e.g. spacegroup number and  crystal system `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.GlobalSymmetryFeatures>`_
:code:`Dimensionality`                         Returns dimensionality of structure: 1 means linear chains of atoms OR `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.Dimensionality>`_
:code:`RadialDistributionFunction`             Calculate the radial distribution function (RDF) of a crystal structure. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.RadialDistributionFunction>`_
:code:`PartialRadialDistributionFunction`      Compute the partial radial distribution function (PRDF) of an xtal structure `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.PartialRadialDistributionFunction>`_
:code:`RadialDistributionFunctionPeaks`        Determine the location of the highest peaks in a structure's RDF. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.RadialDistributionFunctionPeaks>`_
:code:`ElectronicRadialDistributionFunction`   Calculate the inherent electronic radial distribution function (ReDF) `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.ElectronicRadialDistributionFunction>`_
:code:`CoulombMatrix`                          Generate the Coulomb matrix, a representation of nuclear coulombic interaction. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.CoulombMatrix>`_
:code:`SineCoulombMatrix`                      A variant of the Coulomb matrix developed for periodic crystals. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.SineCoulombMatrix>`_
:code:`OrbitalFieldMatrix`                     Representation based on the valence shell electrons of neighboring atoms. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.OrbitalFieldMatrix>`_
:code:`MinimumRelativeDistances`               Determines the relative distance of each site to its closest neighbor. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.MinimumRelativeDistances>`_
:code:`SiteStatsFingerprint`                   Computes statistics of properties across all sites in a structure. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.SiteStatsFingerprint>`_
:code:`EwaldEnergy`                            Compute the energy from Coulombic interactions. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.EwaldEnergy>`_
:code:`BondFractions`                          Compute the fraction of each bond in a structure, based on NearestNeighbors. `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.BondFractions>`_
:code:`BagofBonds`                             Compute a Bag of Bonds vector, as first described by Hansen et al. (2015). `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.BagofBonds>`_
:code:`StructuralHeterogeneity`                Variance in the bond lengths and atomic volumes in a structure `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.StructuralHeterogeneity>`_
:code:`MaximumPackingEfficiency`               Maximum possible packing efficiency of this structure `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.MaximumPackingEfficiency>`_
:code:`ChemicalOrdering`                       How much the ordering of species in the structure differs from random `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.ChemicalOrdering>`_
:code:`StructureComposition`                   Features related to the composition of a structure `[more] <https://hackingmaterials.github.io/matminer/matminer.featurizers.html#matminer.featurizers.structure.StructureComposition>`_
============================================   ================================================================================================================================================================================================================================================================================================================================================================================================================



