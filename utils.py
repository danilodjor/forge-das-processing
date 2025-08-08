import os
import dascore as dc
from datetime import datetime
from typing import List

def timestamp2datetime(timestamp):
    return datetime.strptime(timestamp, "%Y%m%dT%H%M%S")

def timestampFromFilename(filename):
    return filename.split("StrainRate_")[1].split("+")[0]

def bisect_left_key(a, x, key=lambda v: v):
    """
    Locate the insertion point for x in a to maintain sorted order, using key.
    Returns the index where x should be inserted (to the left of existing entries).
    """
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if key(a[mid]) < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def bisect_right_key(a, x, key=lambda v: v):
    """
    Locate the insertion point for x in a to maintain sorted order, using key.
    Returns the index where x should be inserted (to the right of existing entries).
    """
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if key(a[mid]) <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def binary_search_first_extreme(a: List[str], x: datetime, key=lambda v: v, mode='smaller'):
    """
    Returns the index of the first value smaller or larger than x in a sorted array.
    mode: 'smaller' or 'larger'
    If no such value exists, returns -1.
    If x is smaller than the smallest and mode is 'smaller', returns 0.
    If x is larger than the largest and mode is 'larger', returns last index.
    """
    if not a:
        return -1
    if mode == 'smaller':
        if x <= key(a[0]):
            return 0
    elif mode == 'larger':
        if x >= key(a[-1]):
            return len(a) - 1
    else:
        raise ValueError("mode must be 'smaller' or 'larger'")

    lo, hi = 0, len(a)
    result = -1
    while lo < hi:
        mid = (lo + hi) // 2
        val = key(a[mid])
        if mode == 'smaller':
            if val < x:
                result = mid
                lo = mid + 1
            else:
                hi = mid
        else:  # mode == 'larger'
            if val > x:
                result = mid
                hi = mid
            else:
                lo = mid + 1
    return result


def slice_das_segment(start_time, end_time, source_dir):
    """
    Returns a DAS segment containing the recordings within the specified time range.
    It may cut and/or concatenate multiple patches, based on the time range.
    """
    # Get the list of files in the source directory
    files = [
        f for f in os.listdir(source_dir)
        if f.endswith('.h5') and f.startswith('16B')
    ]
    files = sorted(
        files, key=lambda f: timestamp2datetime(timestampFromFilename(f))
    )  # sorted(files, key=lambda f: int(f.split('_')[-1].split('.')[0]))

    # Convert start_time and end_time to datetime objects
    start_time = timestamp2datetime(start_time)
    end_time = timestamp2datetime(end_time)

    # Find the index of the first file that is greater than or equal to start_time and less than or equal to end_time
    start_idx = binary_search_first_extreme(
        files,
        start_time,
        key=lambda f: timestamp2datetime(timestampFromFilename(f)),
        mode='smaller')

    end_idx = binary_search_first_extreme(
        files,
        end_time,
        key=lambda f: timestamp2datetime(timestampFromFilename(f)),
        mode='larger')

    # Create a list of file paths for the files that fall within the specified time range
    file_paths = [
        os.path.join(source_dir, f) for f in files[start_idx:end_idx + 1]
    ]

    # Create a DAS segment from the file paths
    patches = [dc.spool(file_path)[0] for file_path in file_paths]
    spool = dc.spool(patches)
    spool = spool.concatenate(time=None)

    assert len(spool) == 1  # If all patches were compatible

    patches = spool[0]
    patches = patches.select(time=(start_time, end_time))

    # Return the concatenated DAS segment
    return patches
