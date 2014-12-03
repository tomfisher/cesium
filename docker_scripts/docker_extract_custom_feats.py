# extract_custom_feats.py

# to be run from INSIDE a docker container

#import subprocess
import sys
sys.path.append("/home/mltsp/mltsp")
import custom_feature_tools as cft

#from subprocess import Popen, PIPE, call
import cPickle

def extract_custom_feats():
    """Load pickled parameters and generate custom features.
    
    To be run from inside a Docker container. Pickles the extracted 
    features for later copying from container to host machine.
    
    Returns
    -------
    int
        Returns 0.
    
    """
    # load pickled ts_data and known features
    with open("/home/mltsp/mltsp/copied_data_files/features_already_known.pkl","rb") \
         as f:
        features_already_known = cPickle.load(f)

    # script has been copied to the following location:
    script_fpath = "/home/mltsp/mltsp/copied_data_files/custom_feature_defs.py"
    script_fname = "custom_feature_defs.py"
    
    # extract features
    feats = cft.execute_functions_in_order(
        script_fname=script_fname, 
        features_already_known=features_already_known, 
        script_fpath=script_fpath)
    
    with open("/tmp/results_dict.pkl", "wb") as f:
        cPickle.dump(feats, f)
    
    print "Created /tmp/results_dict.pkl in docker container."
    return 0



if __name__=="__main__":
    feats = extract_custom_feats()
    print feats
