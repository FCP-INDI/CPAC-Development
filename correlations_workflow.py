import os
import sys


def create_unique_file_dict(output_folder_path):

    filesDict = {}

    for root, dirs, files in os.walk(output_folder_path):

        # loops through every file in the directory
        for filename in files:

            # checks if the file is a nifti (.nii.gz)
            if 'nii.gz' in filename:

                # 'filename' is only the filename, not the full path of the
                # current file being looked at

                category = root.split('/')[len(output_folder_path.split('/'))+1]

                # this is the subject ID
                subjectID = root.split('/')[len(output_folder_path.split('/'))]
            
                fullpath = root + '/' + filename
                scrubbing = ''
                aux = ''


                # this is hard-coded because the usual regression
                # configuration includes scrubbing on/off, and the threshold
                # used for scrubbing is 0.2

                # in the future make this more dynamic by having it detect
                # '_threshold' and then parsing the number at the end
                #if '/_threshold_0.2' in fullpath:
                if 'scrubbing' in fullpath:
                    scrubbing = '0.2'
                else:
                    scrubbing = 'none'


                if '_roi_HarvardOxford-cort-maxprob-thr50-2mm' in fullpath:
                    aux = '_roi_HarvardOxford-cort-maxprob-thr50-2mm'
                elif '_roi_HarvardOxford-sub-maxprob-thr50-2mm' in fullpath:
                    aux = '_roi_HarvardOxford-sub-maxprob-thr50-2mm'
                elif '_roi_rois_2mm' in fullpath:
                    aux = '_roi_rois_2mm'
                elif '_mask_aMPFC' in fullpath:
                    aux = '_mask_aMPFC'
                elif '_mask_dMPFC' in fullpath:
                    aux = '_mask_dMPFC'
                elif '_mask_LTC' in fullpath:
                    aux = '_mask_LTC'
                elif '_mask_PCC' in fullpath:
                    aux = '_mask_PCC'
                elif '_mask_TPJ' in fullpath:
                    aux = '_mask_TPJ'
                elif 'centrality_binarize' in fullpath:
                    aux = 'centrality_binarize'
                elif 'centrality_weighted' in fullpath:
                    aux = 'centrality_weighted'
                elif 'temp_reg_map_z_0000' in fullpath:
                    aux = 'temp_reg_map_z_0000'
                elif 'temp_reg_map_z_0001' in fullpath:
                    aux = 'temp_reg_map_z_0001'
                elif 'temp_reg_map_z_0002' in fullpath:
                    aux = 'temp_reg_map_z_0002'
                elif 'temp_reg_map_z_0003' in fullpath:
                    aux = 'temp_reg_map_z_0003'
                elif 'temp_reg_map_z_0004' in fullpath:
                    aux = 'temp_reg_map_z_0004'
                elif 'temp_reg_map_z_0005' in fullpath:
                    aux = 'temp_reg_map_z_0005'
                elif 'temp_reg_map_z_0006' in fullpath:
                    aux = 'temp_reg_map_z_0006'
                elif 'temp_reg_map_z_0007' in fullpath:
                    aux = 'temp_reg_map_z_0007'
                else:
                    aux = 'none'


                if 'scan_rest_1' in fullpath:
                    scan = 'scan_rest_1'
                elif 'scan_rest_2' in fullpath:
                    scan = 'scan_rest_2'
                elif 'scan_rest_3' in fullpath:
                    scan = 'scan_rest_3'
                else:
                    scan = 'none'
                # load these settings into the tuple so that the file can be
                # identified without relying on its full path (as it would be
                # impossible to match files from two regression tests just based
                # on their filepaths)
                file_Tuple = (category, subjectID, scrubbing, aux, scan, filename)

                filesDict[file_Tuple] = fullpath


    return filesDict




def match_filepaths(old_files_dict, new_files_dict):

    # file path matching

    matched_path_list = []
    missing_in_old = []
    missing_in_new = []

    for key in new_files_dict:
                                      # use this second half only
                                      # for reducing amount of correlations
        if (old_files_dict.get(key) != None): # and (output_to_correlate in new_files_dict[key]):

            matched_path_info = []

            matched_path_info.append(key)
            matched_path_info.append(old_files_dict[key])
            matched_path_info.append(new_files_dict[key])

            # each key is a tuple identifying the file, and each entry (the
            # matchedPathList) is a list containing two items: the two full
            # filepaths of the two files, one from each regression test, which
            # are correctly matched by their matching ID tuples

            # matched_path_info is now populated as a list, the first entry
            # being the ID key (tuple), and the next two being the filepaths

            matched_path_list.append(matched_path_info)

        else:

            missing_in_old.append(new_files_dict[key])


    # find out what is in the last version's outputs that isn't in the new
    # version's outputs
    for key in old_files_dict:

        if new_files_dict.get(key) != None:

            missing_in_new.append(old_files_dict[key])


    return matched_path_list, missing_in_old, missing_in_new


# loop through matched_path_info and send each entry into calculate_correlation



# now that you have the matched paths and selected your output, it gets sent
# as a list of lists here, as an iterfield for this mapnode:

# all of the correlations fan out with multiproc and get done for that one
# output really fast

def calculate_correlation(matched_path_list_entry):

    import os
    import nibabel as nb
    import numpy as np
    import scipy.stats.mstats
    import scipy.stats
    import math

    # concordance correlation coefficient
    def concordance(x, y, rho):

        """
        Calculates Lin's concordance correlation coefficient.

        Usage: concordence(x, y) where x, y are equal-length arrays
        Returns: concordance correlation coefficient

        Note: strict than pearson

        """

        map(float, x)
        map(float, y)
        xvar = np.var(x)
        yvar = np.var(y)
        #rho = scipy.stats.pearsonr(x, y)[0]
        #p = np.corrcoef(x,y)  # numpy version of pearson correlation coefficient
        ccc = 2. * rho * math.sqrt(xvar) * math.sqrt(yvar) / (xvar + yvar + (np.mean(x) - np.mean(y))**2)

        return ccc
    
    # the only things that should be held constant while calculating the
    # coefficients are the category and aux fields

    # elements in key: (category, subjectID, scrubbing, aux, scan, filename)

    # calculate each individual correlation and then take the category,
    # aux and correlation and append the correlation to a list stored
    # within a dictionary with the category + aux as the key

    # then go through each key's entry and average them all together

    correlation_info = []

    id_tuple = matched_path_list_entry[0]
    old_path = matched_path_list_entry[1]
    new_path = matched_path_list_entry[2]

    ## nibabel to pull the data from the re-assembled file paths
    if os.path.exists(old_path) and os.path.exists(new_path):
        data_1 = nb.load(old_path).get_data()
        data_2 = nb.load(new_path).get_data()

        ## set up and run the Pearson correlation and concordance correlation
        if data_1.flatten().shape == data_2.flatten().shape:

            corrTuple = (id_tuple[0], id_tuple[3])
            pearson = scipy.stats.pearsonr(data_1.flatten(), data_2.flatten())[0]
            concor = concordance(data_1.flatten(), data_2.flatten(), pearson)

            correlation_info = [corrTuple, pearson, concor]

    else:
        print "%s PATHS NOT FOUND!\n\n" % id_tuple

    
    return correlation_info



# send a list that has every 'correlation_info' list in it via a JoinNode

def aggregate_correlations(correlation_info_list):

    import os
    import pickle

    pCorrList = []
    cCorrList = []

    pearson_dict = {}
    concor_dict = {}

    for corr_info in correlation_info_list:

        if len(corr_info) > 0:

            corrTuple = corr_info[0]
            pearson = corr_info[1]
            concor = corr_info[2]

            if pearson_dict.get(corrTuple) == None:

                #pCorrList.append(pearson)
                pearson_dict[corrTuple] = [pearson] #pCorrList

                #cCorrList.append(concor)
                concor_dict[corrTuple] = [concor] #cCorrList

            else:

                pearson_dict[corrTuple].append(pearson)
                concor_dict[corrTuple].append(concor)


    pearson_pickle = os.path.join(os.getcwd(), 'pearson_dict.p')

    with open(pearson_pickle, 'wb') as handle:
        pickle.dump(pearson_dict, handle)

    concor_pickle = os.path.join(os.getcwd(), 'concor_dict.p')

    with open(concor_pickle, 'wb') as handle:
        pickle.dump(concor_dict, handle)


    return pearson_dict, concor_dict, pearson_pickle, concor_pickle




def organize_correlations(pearson_dict, concor_dict):

    regCorrMap = {}
    scaNativeCorrMap = {}
    scaMniCorrMap = {}
    outputCorrMap = {}
    mniCorrMap = {}

    corr_map_dicts_list = []


    for key in concor_dict:

        #if ('mni' in key[0] or 'mean' in key[0] or 'csf' in key[0] or 'gm' in key[0] or 'wm' in key[0]) and 'xfm' not in key[0]:
        if 'mni' in key[0]:    

            if key[1] == 'none':
                regCorrMap[key[0]] = concor_dict[key]
            else:
                newKey = key[0] + ': ' + key[1]
                regCorrMap[newKey] = concor_dict[key]

        elif 'sca' in key[0] and 'standard' not in key[0]:

            if key[1] == 'none':
                scaNativeCorrMap[key[0]] = concor_dict[key]
            else:
                newKey = key[0] + ': ' + key[1]
                scaNativeCorrMap[newKey] = concor_dict[key]

        elif 'sca' in key[0] and 'standard' in key[0]:

            if key[1] == 'none':
                scaMniCorrMap[key[0]] = concor_dict[key]
            else:
                newKey = key[0] + ': ' + key[1]
                scaMniCorrMap[newKey] = concor_dict[key]

        elif (('standard' in key[0]) or ('centrality' in key[0]) or ('vmhc' in key[0])) and 'functional' not in key[0]:

            if key[1] == 'none':
                mniCorrMap[key[0]] = concor_dict[key]
            else:
                newKey = key[0] + ': ' + key[1]
                mniCorrMap[newKey] = concor_dict[key]

        elif 'preprocessed' not in key[0] and 'correct' not in key[0] and 'seg' not in key[0] and 'functional' not in key[0] and 'anatomical' not in key[0] and 'centrality' not in key[0] and 'vmhc' not in key[0]:

            if key[1] == 'none':
                outputCorrMap[key[0]] = concor_dict[key]
            else:
                newKey = key[0] + ': ' + key[1]
                outputCorrMap[newKey] = concor_dict[key]


    if len(regCorrMap.values()) > 0:
        corr_map_dicts_list.append((regCorrMap,'concordance_registration'))

    if len(scaNativeCorrMap.values()) > 0:
        corr_map_dicts_list.append((scaNativeCorrMap,'concordance_native_SCA'))

    if len(scaMniCorrMap.values()) > 0:
        corr_map_dicts_list.append((scaMniCorrMap,'concordance_MNI_SCA'))

    if len(mniCorrMap.values()) > 0:
        corr_map_dicts_list.append((mniCorrMap,'concordance_MNI_outputs'))

    if len(outputCorrMap.values()) > 0:
        corr_map_dicts_list.append((outputCorrMap,'concordance_native_outputs'))


    return corr_map_dicts_list




def create_boxplots(corr_map_dicts_list_entry, pipeline_names, current_dir):

    def box_plot(dataDict1, pipelines, name, current_dir):

        from matplotlib import pyplot

        allData = []
        labels = dataDict1.keys()
        labels.sort()

        for label in labels:
            currentData = []
            currentData.append(dataDict1[label])
            allData.append(currentData)

        pyplot.boxplot(allData)
        pyplot.xticks(range(1,(len(dataDict1)+1)),labels,rotation=85)
        pyplot.margins(0.5,1.0)
        pyplot.xlabel('Derivatives')
        pyplot.title('Correlations between %s and %s\n ( %s )'%(pipelines[0], pipelines[1], name))

        #pyplot.show()
	    
        pyplot.savefig('%s.pdf'%(current_dir + '/' + name + '_' + pipelines[0] + '_and_' + pipelines[1]), format='pdf', dpi='200', bbox_inches='tight')
        pyplot.close()



    correlation_dict = corr_map_dicts_list_entry[0]
    correlation_name = corr_map_dicts_list_entry[1]

    box_plot(correlation_dict, pipeline_names, correlation_name, current_dir)





def correlations_workflow(old_files_dict, new_files_dict, pipeline_names, num_cores, match_filepaths, calculate_correlation):

    import nipype.interfaces.io as nio
    import nipype.pipeline.engine as pe

    import nipype.interfaces.utility as util


    currentDir = os.getcwd()

    workflow = pe.Workflow(name='correlations_workflow')
    workflow.base_dir = currentDir + '/correlations'


    match_filepaths = pe.Node(util.Function(input_names=['old_files_dict', 'new_files_dict', 'output_to_correlate'],
                                            output_names=['matched_path_list', 'missing_in_old', 'missing_in_new'],
                                            function=match_filepaths),
                                            name='match_filepaths')

    match_filepaths.inputs.old_files_dict = old_files_dict
    match_filepaths.inputs.new_files_dict = new_files_dict


    calc_correlation = pe.MapNode(util.Function(input_names=['matched_path_list_entry'],
                                            output_names=['correlation_info_list'],
                                            function=calculate_correlation),
                                            name='calc_correlation',
                                            iterfield=['matched_path_list_entry'])

    aggregate_corrs = pe.Node(util.Function(input_names=['correlation_info_list'],
                                            output_names=['pearson_dict', 'concor_dict', 'pearson_pickle', 'concor_pickle'],
                                            function=aggregate_correlations),
                                            name='aggregate_corrs')


    organize_corrs = pe.Node(util.Function(input_names=['pearson_dict', 'concor_dict'],
                                 output_names=['corr_map_dicts_list'],
                                 function=organize_correlations),
                                 name='organize_corrs')

    boxplots = pe.MapNode(util.Function(input_names=['corr_map_dicts_list_entry', 'pipeline_names', 'current_dir'],
                                 output_names=[],
                                 function=create_boxplots),
                                 name='create_boxplots',
                                 iterfield=['corr_map_dicts_list_entry'])

    boxplots.inputs.pipeline_names = pipeline_names
    boxplots.inputs.current_dir = currentDir


    datasink = pe.Node(nio.DataSink(), name='sinker')

    datasink.inputs.base_directory = currentDir + '/file_output'



    workflow.connect(match_filepaths, 'matched_path_list', calc_correlation, 'matched_path_list_entry')

    workflow.connect(calc_correlation, 'correlation_info_list', aggregate_corrs, 'correlation_info_list')

    workflow.connect(aggregate_corrs, 'pearson_pickle', datasink, 'output.@pearson_pickle')

    workflow.connect(aggregate_corrs, 'concor_pickle', datasink, 'output.@concor_pickle')

    workflow.connect(aggregate_corrs, 'pearson_dict', organize_corrs, 'pearson_dict')

    workflow.connect(aggregate_corrs, 'concor_dict', organize_corrs, 'concor_dict')

    workflow.connect(organize_corrs, 'corr_map_dicts_list', boxplots, 'corr_map_dicts_list_entry')


    workflow.run(plugin='MultiProc', plugin_args={'n_procs': int(num_cores)})




def main_proc(old_outputs_path, new_outputs_path, num_cores):

    pipeline_names = [old_outputs_path.split('/')[len(old_outputs_path.split('/'))-1],new_outputs_path.split('/')[len(new_outputs_path.split('/'))-1]]

    old_files = create_unique_file_dict(old_outputs_path)

    new_files = create_unique_file_dict(new_outputs_path)


    correlations_workflow(old_files, new_files, pipeline_names, num_cores, match_filepaths, calculate_correlation)




main_proc(sys.argv[1], sys.argv[2], sys.argv[3])


