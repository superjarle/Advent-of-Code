# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 08:30:17 2023

@author: jkv
"""

from collections import defaultdict

fo = open("19.txt", "r")
f = list(fo)
fo.close()

def parse_workflow(wf, rating):
    a = wf.split(':')
    if a[0][1] == '<':
        if rating[a[0][0]] < int(a[0][2:]):
            return a[1]
    else:
        if rating[a[0][0]] > int(a[0][2:]):
            return a[1]
    return -1

workflows = {}
ratings = []
for l in f:
    l = l.strip()
    if l and l[0] == '{':
        t3 = l[1:-1].split(',')
        ratings.append({})
        for v1 in t3:
            v2 = v1.split('=')
            ratings[-1][v2[0]] = int(v2[1])
    elif l:
        t1 = l.split('{')
        t1[1] = t1[1][:-1]
        t2 = t1[1].split(',')
        workflows[t1[0]] = t2

def run(rating, ins):
    if ins == 'A' or ins == 'R':
        return ins
    for wf in workflows[ins][:-1]:
        pw = parse_workflow(wf, rating)
        if pw == 'A':
            return 'A'
        elif pw == 'R':
            return 'R'
        elif pw != -1:
            return run(rating, pw)
    return run(rating, workflows[ins][-1])

s = 0
for rating in ratings:
    res = run(rating, 'in')
    if res == 'A':
        s += sum(rating.values())

print(s)

conds = defaultdict(list)
conds['in'] = ['']

def find_conditions(ins):
    done = []
    todo = [ins]
    while todo:
        ins = todo[0]
        todo = todo[1:]
        if ins != 'A' and ins != 'R':    
            nconds = []
            for wf in workflows[ins][:-1]:
                a = wf.split(':')
                for c in conds[ins]:
                    new = c + a[0] + ','
                    for nc in nconds:
                        new += nc
                    conds[a[1]].append(new)
                nconds.append('non' + a[0] + ',')
                todo.append(a[1])
            if workflows[ins]:
                for c in conds[ins]:
                    new = c
                    for nc in nconds:
                        new += nc
                    conds[workflows[ins][-1]].append(new)
                    todo.append(workflows[ins][-1])
        done.append(ins)

def parse_conds(ins):
    tot = 0
    for cond in conds[ins]:
        indiv = cond.split(',')[:-1]
        minx = 1
        minm = 1
        mina = 1
        mins = 1
        maxx = 4000
        maxm = 4000
        maxa = 4000
        maxs = 4000
        for c in indiv:
            if '<' in c:
                op = '<'
            else:
                op = '>'
            val, lim = c.split(op)
            lim = int(lim)
            if val == 'x':
                if op == '<':
                    maxx = min(maxx, lim - 1)
                else:
                    minx = max(minx, lim + 1)
            elif val == 'm':
                if op == '<':
                    maxm = min(maxm, lim - 1)
                else:
                    minm = max(minm, lim + 1)
            elif val == 'a':
                if op == '<':
                    maxa = min(maxa, lim - 1)
                else:
                    mina = max(mina, lim + 1)
            elif val == 's':
                if op == '<':
                    maxs = min(maxs, lim - 1)
                else:
                    mins = max(mins, lim + 1)
            elif val == 'nonx':
                if op == '<':
                    minx = max(minx, lim)
                else:
                    maxx = min(maxx, lim)
            elif val == 'nonm':
                if op == '<':
                    minm = max(minm, lim)
                else:
                    maxm = min(maxm, lim)
            elif val == 'nona':
                if op == '<':
                    mina = max(mina, lim)
                else:
                    maxa = min(maxa, lim)
            elif val == 'nons':
                if op == '<':
                    mins = max(mins, lim)
                else:
                    maxs = min(maxs, lim)
        tot += (maxx - minx + 1) * (maxm - minm + 1) * (maxa - mina + 1) * (maxs - mins + 1)
    return tot

find_conditions('in')
print(parse_conds('A'))        