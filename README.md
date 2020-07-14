# video-dedup

`video-dedup` is a tool similar to `rdfind`, but intented to work on video files. `rdfind` won't recognize two versions of the same video as duplicates if their checksums don't match entirely, which is never the case for videos that have been converted to other formats.

## How it works
First, we give `video-dedup.py` a list of directories in which it will look for video files. Currently, video files are identified by their extensions. These directories will be recursively listed, and every video found will be marked as a potential duplicate.

This set of videos is then broken up into smaller sets. Each of these sets contains two or more filepaths which are potentially the same video. `video-dedup` can never be sure if two videos are *actually* duplicates, so it relies on a few heuristics to exclude videos as potential duplicates. Once enough of these heuristics have been applied, we can be pretty sure that the remaining un-excluded videos actually are duplicates. It usually works quite well. 

DISCLAIMER: this tool is very much still WIP
