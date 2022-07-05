This version of C-PAC (``${DEPRECATED_VERSION}``) is deprecated due to a bug in ``single_step_resampling``. Unless you have a specific reason to use this version of C-PAC (``${DEPRECATED_VERSION}``), we recommend upgrading to at least version 1.8.4. See https://fcp-indi.github.io/docs/latest/user/release_notes/v1.8.4 for more information about C-PAC v1.8.4. To use ${DEPRECATED_VERSION} anyway, you can pull `fcpindi/c-pac:${DEPRECATED_VERSION}-DEPRECATED` from Docker Hub.

Critical Alert for fMRIPrep-Options in C-PAC v1.8.1 - v1.8.3
============================================================

* Fixed a bug that was causing ``single_step_resampling``, when combined with certain other configurations, to inadvertently cause unexpected forks in the pipeline past transform application.

   * This bug caused any affected ``fmriprep-options-based`` pipeline configurations (including ``fx-options`` and ``rbc-options``) to produce BOLD time series write-outs to the output directory in template space which were not nuisance regressed or filtered, for C-PAC versions 1.8.1 through 1.8.3.

   * Although these outputs were not expressly labeled as nuisance regressed or filtered, they were labeled as preprocessed with ``desc-preproc`` and were the only functional data transformed to template space and used for downstream processing, such as ROI-based timeseries extraction.

   * If you are unsure if you have been affected, you can check the side-car JSON for your template-space BOLD data from these versions for those pipeline configurations, as the JSON will still accurately reflect what operations had been performed on the data.

