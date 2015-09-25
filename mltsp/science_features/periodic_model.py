import numpy as np
from scipy import optimize

        
# TODO what is this exactly?
def periodic_model(lomb_model):
    """
    """
    out_dict = {}

    A = lomb_model['freq_fits'][0]['amplitude']
    ph = lomb_model['freq_fits'][0]['rel_phase']

    def model_f(t):
        return (A[0] * np.sin(2. * np.pi      * t + ph[0]) +
                A[1] * np.sin(2. * np.pi * 2. * t + ph[1]) +
                A[2] * np.sin(2. * np.pi * 3. * t + ph[2]) +
                A[3] * np.sin(2. * np.pi * 4. * t + ph[3]) +
                A[4] * np.sin(2. * np.pi * 5. * t + ph[4]) +
                A[5] * np.sin(2. * np.pi * 6. * t + ph[5]) +
                A[6] * np.sin(2. * np.pi * 7. * t + ph[6]) +
                A[7] * np.sin(2. * np.pi * 8. * t + ph[7]))

    def model_neg(t):
        return -1. * model_f(t)

    min_1_a = optimize.fmin(model_neg, 0.05)[0] # start finding 1st minima, at 5% of phase (fudge/magic number) > 0.018
    max_2_a = optimize.fmin(model_f, min_1_a + 0.01)[0]
    min_3_a = optimize.fmin(model_neg, max_2_a + 0.01)[0]
    max_4_a = optimize.fmin(model_f, min_3_a + 0.01)[0]

# TODO !!! is this wrong? seems like it should be a minus
    out_dict['phi1_phi2'] = (min_3_a - max_2_a) / (max_4_a / min_3_a)
    out_dict['min_delta_mags'] = abs(model_f(min_1_a) - model_f(min_3_a))
    out_dict['max_delta_mags'] = abs(model_f(max_2_a) - model_f(max_4_a))
    return out_dict


def get_max_delta_mags(model):
    return model['max_delta_mags']


def get_min_delta_mags(model):
    return model['min_delta_mags']


def get_model_phi1_phi2(model):
    return model['phi1_phi2']
