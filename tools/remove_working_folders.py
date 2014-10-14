import sys

def remove_working_folders(node_type, working_dir):

    # this function is meant to safely delete any folders in the CPAC working
    # directory so that a user can easily select what they wish to re-run
    # without having to dig through the working directory themselves

    # documentation will have to warn of deleting prerequisites and its impact
    # on needing to re-run everything after them

    # for now, usage:
    #    python remove_working_folders.py 'one of the left-hand strings below' '/path/to/working/directory'

    import os
    import shutil

    # work in progress, more to come...
    node_labels = {
        'Anatomical skull-stripping': 'anat_skullstrip',
        'Anatomical-to-standard registration': 'anat_mni',
        'Functional-to-anatomical registration': 'func_to_anat',
        'Functional-to-anatomical (BB-reg)': 'func_to_anat_bbreg',
        'ALFF and f/ALFF (all)': 'alff',
        'ALFF smoothing': 'alff_smooth',
        'ALFF registration': 'alff_to_standard',
        'ALFF post-registration smoothing': 'alff_to_standard_smooth',
        'ALFF post-registration z-score standardization': 'z_score_std_alff',
        'f/ALFF smoothing': 'falff_smooth',
        'f/ALFF registration': 'falff_to_standard',
        'f/ALFF post-registration smoothing': 'falff_to_standard_smooth',
        'f/ALFF post-registration z-score standardization': 'z_score_std_falff',
        'ReHo (all)': 'reho',
        'ReHo smoothing': 'reho_smooth',
        'ReHo registration': 'reho_to_standard',
        'ReHo post-registration smoothing': 'reho_to_standard_smooth',
        'ReHo post-registration z-score standardization': 'z_score_std_reho',
        'SCA ROI (all)': 'sca_roi',
        'SCA ROI smoothing': 'sca_roi_smooth',
        'SCA ROI registration': 'sca_roi_to_standard',
        'SCA ROI post-registration smoothing': 'sca_roi_to_standard_smooth',
        'SCA ROI post-registration z-score standardization': 'fisher_z_score_std_sca_roi',
        'All warp-to-standard applications (post-registration calculation)': 'to_standard',
        'All smoothing (post-registration)': 'smooth',
        'All z-score standardization (post-registration)': 'z_score',
        'symlinks': 'process_outputs',
        'output_paths_lists': 'process_outputs'
    }

    # future: pass a warning to user if they select a workflow or node that is
    # a prerequisite for a lot of other things (like anatomical registration)

    for root, dirs, files in os.walk(working_dir):

        if node_label[node_type] in root:
            # once integrated into CPAC, put a logger.info here recording all
            # of the directories deleted
            shutil.rmtree(root)
            

remove_working_folders(sys.argv[1], sys.argv[2])
