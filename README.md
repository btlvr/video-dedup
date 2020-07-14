# video-dedup

`video-dedup` is a tool similar to `rdfind`, but intented to work on video files. `rdfind` won't recognize two versions of the same video as duplicates if their checksums don't match entirely, which is never the case for videos that have been converted to other formats.

**Disclaimer:** This tool is very much still WIP.

## How it works

First, we give `video-dedup.py` a list of directories in which it will look for video files. Currently, video files are identified by their extensions. These directories will be recursively listed, and every video found will be marked as a potential duplicate.

This set of videos is then broken up into smaller sets. Each of these sets contains the paths of two or more files which are potentially the same video.

'video-dedup` can never be sure if two videos are *actually* duplicates, so it relies on a few heuristics to exclude videos that are definitely *not* duplicates. Once enough of these heuristics have been applied, we can be pretty sure that the remaining un-excluded videos actually are duplicates. It usually works quite well.

## Screenshot
 ![](https://i.ibb.co/82LsW8n/2020-07-14-09-13-04.png)

### Example
- Build set of all video files in directory
- Consider any file that has a duration very close (less than 1 second) to the duration of another file to be a potential duplicate. Videos with durations that don't closely match any other videos will be removed from the set.
- After clustering the videos by duration, start dropping videos from the clusters if their first frame doesn't match the others.
- Repeat, but 30 seconds into the videos
- Repeat, but 1 minute into the videos
- ...

### Frame comparison
Frames are currently compared by examining the difference between their block mean value hashes. More hashing algorithms to be added soon.

### Normalization
Currently, `video-dedup` doesn't play nicely with duplicate videos that have been cropped, flipped, sped up, slowed down, or transformed. Some of these things are easy to fix with histogram normalization / image moment normalization.

## Handling suspected duplicates
Once duplicate videos have been found, they can be deleted, symlinked to the original, moved into a separate directory, or flagged for later inspection.

### Deciding which video to keep
When removing duplicate copies of a video, `video-dedup` needs to determine which copy to keep. Some potential ways to determine this:

- File size (larger video files are likely higher resolution)
- Age (keep first modified or most recently modified file)
- Duration (video may have been trimmed, so we'd want to keep the full version)
- Directory (determine priority of certain directories over others, by examining the order in which they're passes as command line arguments)
