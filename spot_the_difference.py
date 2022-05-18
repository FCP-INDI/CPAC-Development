#!/usr/bin/env python


from argparse import ArgumentParser

import os.path as op
import numpy as np
import hashlib
import json
import os
import re


def get_seq_steplist(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    r = re.compile('.+_[0-9]+$')
    fl_lists = []
    for di in dirs:
        fls = sorted(os.listdir(di))
        fls_filtered = [f for f in fls if r.match(f)]
        fl_inds = [int(_.split('_')[-1]) for _ in fls_filtered]

        fls_sorted = [fls_filtered[_] for _ in np.argsort(fl_inds)]

        fl_lists += [fls_sorted]
    return fl_lists


def prune_and_match(file_lists):
    ref = file_lists[0]
    new_flist = [ref]
    for flist in file_lists[1:]:
        new_flist += [ [item for item in flist if item in ref]  ] 
    return new_flist


def find_outputs(dir_path):
    try:
        with open(op.join(dir_path, "_report/report.rst")) as fhandle:
            summary = fhandle.read()
    except FileNotFoundError:
        return {}

    summary = summary.split('\n\n\n')
    outp_loc = [1 + idx
                for idx, row in enumerate(summary)
                if 'Execution Outputs' in row][0]
    outputs = summary[outp_loc].split('\n')

    kys = [op.split()[1] for op in outputs]
    vls = [" ".join(op.split()[3:]) for op in outputs]

    fls = {}
    for k, v in zip(kys, vls):
        if v == '<undefined>':
            continue
        if v.startswith('['):
            v = json.loads(v.replace("'", '"'))
        else:
            v = [v]

        v = [op.basename(_) for _ in v]
        # Build the dictionary in reverse to easily look up output names
        for _ in v:
            fls[_] = k

    return fls


def md5_compare(comparable_steps, basepath, path_mods):
    ref_list, ref_mod = comparable_steps[0], path_mods[0]
    hash_dict = {}
    for idx, fdirs in enumerate(comparable_steps):
        if idx == 0:
            dk = 'ref'
            setting = "Reference"
        else:
            dk = 'test' + str(idx)
            setting = "Test " + str(idx)

        hash_dict[dk] = {}
        print('Computing hashes for {0}...'.format(setting))
        
        for fdir in fdirs:
            fpath = op.join(basepath, path_mods[idx], fdir)
            outputs = find_outputs(fpath)

            hash_dict[dk][fdir] = {}
            for key in outputs.keys():
                tmp_fl = op.join(fpath, key)
                if op.exists(tmp_fl):
                    hash_dict[dk][fdir][outputs[key]] = md5(tmp_fl)

    return hash_dict


def md5(fl):
    # From:
    #  https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    md5 = hashlib.md5()

    with open(fl, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()


def flag_differences(file_hashes):
    tests = set(file_hashes.keys()) - set(['ref'])
    print("Comparing hashes...")
    for key in file_hashes['ref'].keys():
        rdat = file_hashes['ref'][key]
        print("  Comparing {0}...".format(key))
        for t in tests:
            tdat = file_hashes[t][key]
            print("    {0}:".format(t.capitalize()), end='\t')

            diff = []
            for k in rdat.keys():
                if rdat[k] == {}:
                    diff += ["no data"]
                elif rdat[k] == tdat[k]:
                    continue
                else:
                    diff += [k]
            if len(diff) == 0:
                diff = "SUCCESS!"
            else:
                diff = "FAILED for " +  ", ".join(diff)

            print(diff)


def main():
    parser = ArgumentParser()
    parser.add_argument("ref", help="Working directory for the reference.")
    parser.add_argument("test", help="Working directory for the test-setting.")

    res = parser.parse_args()

    step_lists = get_seq_steplist([res.ref, res.test])
    comparable_steps = prune_and_match(step_lists)

    bp = op.commonpath([res.ref, res.test])
    pdiffs = [op.relpath(p, bp) for p in [res.ref, res.test]]

    file_hashes = md5_compare(comparable_steps, bp, pdiffs)

    flag_differences(file_hashes)


if __name__ == "__main__":
    main()
