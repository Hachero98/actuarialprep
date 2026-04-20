from .exam_p_generator import ExamPGenerator
from .exam_fm_generator import ExamFMGenerator
from .exam_fam_generator import ExamFAMGenerator
from .exam_altam_generator import ExamALTAMGenerator
from .exam_astam_generator import ExamASTAMGenerator
from .exam_srm_generator import ExamSRMGenerator
from .exam_pa_generator import ExamPAGenerator

ALL_GENERATORS = {
    "P": ExamPGenerator,
    "FM": ExamFMGenerator,
    "FAM": ExamFAMGenerator,
    "ALTAM": ExamALTAMGenerator,
    "ASTAM": ExamASTAMGenerator,
    "SRM": ExamSRMGenerator,
    "PA": ExamPAGenerator,
}
