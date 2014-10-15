import sys

def remove_working_folders(node_type, working_dir):

    # this function is meant to safely delete any folders in the CPAC working
    # directory so that a user can easily select what they wish to re-run
    # without having to dig through the working directory themselves

    # this can be integrated into CPAC later as part of the GUI, maybe either
    # within the pipeline configuration editor in 'Output Settings'
    #     i.e. "Select outputs to re-run" and have a clickable list of the
    #     left-hand strings below within node_labels
    # OR, can be one of the utilities available in a drop-down menu later

    # documentation will have to warn of deleting prerequisites and its impact
    # on needing to re-run everything after them

    # for now, usage:
    #    python remove_working_folders.py 'one of the left-hand strings below' '/path/to/working/directory'

    import os
    import shutil

    # work in progress, more to come...
    node_labels = {
        'Anatomical preprocessing (all)': 'anat_preproc'
        'Anatomical preprocessing: Anatomical skull-stripping': 'anat_skullstrip',
        'Functional preprocessing (all)': 'func_preproc',
        'Functional preprocessing: Functional masking': 'func_get_brain_mask',
        'Segmentation': 'seg_preproc',
        'Anatomical-to-standard registration': 'anat_mni',
        'Functional-to-anatomical registration': 'func_to_anat',
        'Functional-to-anatomical (BB-reg)': 'func_to_anat_bbreg',
        'Motion Statistics Generation': 'gen_motion_stats',
        'Frequency filtering': 'frequency_filter',
        'Functional warp-to-standard application (ANTS, post-registration calculation)': 'apply_ants_warp_functional',
        'Functional warp-to-standard application (FNIRT, post-registration calculation)': 'func_mni_fsl_warp',
        'All derivatives warp-to-standard applications (post-registration calculation)': 'to_standard',
        'All smoothing': 'smooth',
        'All z-score standardization (post-registration)': 'z_score',
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
        'ROI Average Timeseries Extraction': 'roi_timeseries',
        'ROI Voxelwise Timeseries Extraction': 'voxel_timeseries',
        'Spatial Regression': 'spatial_map_timeseries',
        'Temporal Regression': 'temporal_dual_regression',
        'SCA ROI (all)': 'sca_roi',
        'SCA ROI smoothing': 'sca_roi_smooth',
        'SCA ROI registration': 'sca_roi_to_standard',
        'SCA ROI post-registration smoothing': 'sca_roi_to_standard_smooth',
        'SCA ROI post-registration z-score standardization': 'fisher_z_score_std_sca_roi',
        'SCA Seed (all)': 'sca_seed',
        'SCA Seed smoothing': 'sca_seed_smooth',
        'SCA Seed registration': 'sca_seed_to_standard',
        'SCA Seed post-registration smoothing': 'sca_seed_to_standard_smooth',
        'SCA Seed post-registration z-score standardization': 'fisher_z_score_std_sca_seed',
        'SCA Temporal Regression': 'temporal_regression_sca',
        'VMHC (including symmetric registration)': 'vmhc',
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
