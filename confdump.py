#!/usr/bin/env python3
"""Dump conflict hunks from files with context (LF-safe)."""
import sys, io

def dump(path, ctx=6):
    with io.open(path, 'r', encoding='utf-8', errors='replace', newline='') as f:
        lines = f.read().split('\n')
    out = []
    i = 0
    n = 0
    while i < len(lines):
        if lines[i].startswith('<<<<<<<'):
            n += 1
            j = i
            while j < len(lines) and not lines[j].startswith('>>>>>>>'):
                j += 1
            start = max(0, i - ctx)
            end = min(len(lines), j + 1 + ctx)
            out.append(f"===== CONFLICT #{n} (lines {i+1}-{j+1}) =====")
            for k in range(start, end):
                tag = ''
                if lines[k].startswith('<<<<<<<'):
                    tag = 'OURS>> '
                elif lines[k].startswith('======='):
                    tag = 'THEIRS>> '
                elif lines[k].startswith('>>>>>>>'):
                    tag = 'END>> '
                out.append(f"{k+1:5d}|{tag}{lines[k]}")
            out.append('')
            i = j + 1
        else:
            i += 1
    print(f"### {path}: {n} conflict(s)")
    print('\n'.join(out) if out else "   (no conflict markers)")

if __name__ == '__main__':
    ctx = int(sys.argv[1]) if sys.argv[1].isdigit() else 6
    for p in sys.argv[2:]:
        dump(p, ctx)
