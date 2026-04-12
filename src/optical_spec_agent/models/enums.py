"""Enumerations used across the spec schema."""

from enum import Enum


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

class TaskType(str, Enum):
    """Top-level task category."""
    MODELING = "modeling"
    SIMULATION = "simulation"
    FITTING = "fitting"
    DATA_ANALYSIS = "data_analysis"
    PLOTTING = "plotting"
    WRITING = "writing"


class PhysicalMechanism(str, Enum):
    PLASMON = "plasmon"
    GAP_PLASMON = "gap_plasmon"
    MODE_HYBRIDIZATION = "mode_hybridization"
    INTERFERENCE = "interference"
    COUPLING = "coupling"
    PHOTONIC_CRYSTAL = "photonic_crystal"
    METAMATERIAL = "metamaterial"
    DIELECTRIC = "dielectric"
    DIFFRACTION = "diffraction"
    SCATTERING = "scattering"
    WAVEGUIDE = "waveguide"
    RESONANCE = "resonance"
    GENERAL = "general"


class PhysicalSystem(str, Enum):
    """Common optical physical systems."""
    SINGLE_PARTICLE = "single_particle"
    NANOPARTICLE_ON_FILM = "nanoparticle_on_film"
    PARTICLE_ARRAY = "particle_array"
    THIN_FILM = "thin_film"
    MULTILAYER = "multilayer"
    WAVEGUIDE = "waveguide"
    GRATING = "grating"
    METASURFACE = "metasurface"
    COUPLED_SYSTEM = "coupled_system"
    GENERAL = "general"


class ModelDimension(str, Enum):
    D2 = "2d"
    D3 = "3d"
    AXISYMMETRIC = "axisymmetric"


class StructureType(str, Enum):
    SINGLE_PARTICLE = "single_particle"
    SPHERE_ON_FILM = "sphere_on_film"
    ROD_ON_FILM = "rod_on_film"
    CUBE_ON_FILM = "cube_on_film"
    CROSS_STRUCTURE = "cross_structure"
    ARRAY = "array"
    FILM = "film"
    MULTILAYER = "multilayer"
    GRATINGS = "gratings"
    WAVEGUIDE = "waveguide"
    METASURFACE = "metasurface"
    RANDOM = "random"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Solver / Software
# ---------------------------------------------------------------------------

class SolverMethod(str, Enum):
    FDTD = "fdtd"
    FEM = "fem"
    RCWA = "rcwa"
    ANALYTICAL = "analytical"
    COUPLED_OSCILLATOR = "coupled_oscillator"


class SoftwareTool(str, Enum):
    """Common software tools. The field also accepts arbitrary strings."""
    MEEP = "meep"
    LUMERICAL = "lumerical"
    COMSOL = "comsol"
    MATLAB = "matlab"
    CST = "cst"
    HFSS = "hfss"
    PYTHON = "python"
    CUSTOM = "custom"
    NOT_SPECIFIED = "not_specified"


# ---------------------------------------------------------------------------
# Simulation settings
# ---------------------------------------------------------------------------

class ExcitationSource(str, Enum):
    PLANE_WAVE = "plane_wave"
    TFSF = "tfsf"
    DIPOLE = "dipole"
    MODE_SOURCE = "mode_source"
    GAUSSIAN_BEAM = "gaussian_beam"
    TOTAL_FIELD = "total_field"
    PORT = "port"
    CUSTOM = "custom"


class Polarization(str, Enum):
    LINEAR_X = "linear_x"
    LINEAR_Y = "linear_y"
    LINEAR = "linear"
    CIRCULAR_LEFT = "circular_left"
    CIRCULAR_RIGHT = "circular_right"
    UNPOLARIZED = "unpolarized"
    TM = "TM"
    TE = "TE"


class BoundaryType(str, Enum):
    PML = "PML"
    PERIODIC = "periodic"
    PEC = "PEC"
    PMC = "PMC"
    ABSORBING = "absorbing"
    BLOCH = "Bloch"
    NOT_SPECIFIED = "not_specified"


class SymmetryType(str, Enum):
    NONE = "none"
    MIRROR_X = "mirror_x"
    MIRROR_Y = "mirror_y"
    MIRROR_Z = "mirror_z"
    ROTATIONAL = "rotational"
    PERIODIC = "periodic"


class MeshType(str, Enum):
    AUTO = "auto"
    UNIFORM = "uniform"
    NON_UNIFORM = "non_uniform"
    ADAPTIVE = "adaptive"
    NOT_SPECIFIED = "not_specified"


class MonitorType(str, Enum):
    FREQUENCY_DOMAIN = "frequency_domain"
    TIME_DOMAIN = "time_domain"
    FIELD_PROFILE = "field_profile"
    POWER = "power"
    MOVIE = "movie"
    NOT_SPECIFIED = "not_specified"


# ---------------------------------------------------------------------------
# Geometry / Material
# ---------------------------------------------------------------------------

class GeometryType(str, Enum):
    SPHERE = "sphere"
    CYLINDER = "cylinder"
    CUBE = "cube"
    ROD = "rod"
    CROSS = "cross"
    RING = "ring"
    ELLIPSOID = "ellipsoid"
    PRISM = "prism"
    FILM = "film"
    WAVEGUIDE = "waveguide"
    GRATING = "grating"
    CUSTOM = "custom"


class MaterialModel(str, Enum):
    DRUDE = "Drude"
    LORENTZ = "Lorentz"
    DRUDE_LORENTZ = "Drude-Lorentz"
    DEBYE = "Debye"
    PALIK = "Palik"
    JOHNSON_CHRISTY = "Johnson-Christy"
    REFRACTIVE_INDEX_INFO = "refractiveindex.info"
    CONSTANT_NK = "constant_nk"
    CUSTOM = "custom"
    NOT_SPECIFIED = "not_specified"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

class OutputObservable(str, Enum):
    SPECTRUM = "spectrum"
    SCATTERING_SPECTRUM = "scattering_spectrum"
    ABSORPTION_SPECTRUM = "absorption_spectrum"
    TRANSMISSION_SPECTRUM = "transmission_spectrum"
    REFLECTION_SPECTRUM = "reflection_spectrum"
    FIELD_DISTRIBUTION = "field_distribution"
    FIELD_ENHANCEMENT = "field_enhancement"
    CROSS_SECTION = "cross_section"
    Q_FACTOR = "Q_factor"
    MODE_PROFILE = "mode_profile"
    NEAR_FIELD = "near_field"
    FAR_FIELD = "far_field"
    FWHM = "FWHM"
    DECAY_RATE = "decay_rate"
    RESONANCE_WAVELENGTH = "resonance_wavelength"
    CUSTOM = "custom"


class PostprocessTarget(str, Enum):
    LORENTZIAN_FIT = "lorentzian_fit"
    FWHM_EXTRACTION = "fwhm_extraction"
    Q_FACTOR_CALC = "Q_factor_calc"
    T2_EXTRACTION = "T2_extraction"
    RESONANCE_WAVELENGTH = "resonance_wavelength"
    PEAK_FINDING = "peak_finding"
    BAND_DIAGRAM = "band_diagram"
    FIELD_ANIMATION = "field_animation"
    S_PARAMETER = "S_parameter"
    COUPLING_EFFICIENCY = "coupling_efficiency"
    NONE = "none"


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------

class SweepType(str, Enum):
    WAVELENGTH = "wavelength"
    PARAMETER = "parameter"
    ANGLE = "angle"
    POLARIZATION = "polarization"
    GEOMETRY = "geometry"
    MATERIAL = "material"
    CUSTOM = "custom"
