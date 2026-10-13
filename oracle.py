import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

DECK_KG = 30
PERSON_KG = 90
DRUM_KG = 180
FREEBOARD = 0.6
EMBED = 1.0
GANG_SLOPE = 3

def float_plan(deckWm, deckLm, people):
    if not (deckWm > 0) or not (deckLm > 0) or not (people >= 0):
        return {"error": "the deck sides must be positive and the people zero or more"}
    area = round1(deckWm * deckLm)
    load = round1(area * DECK_KG + people * PERSON_KG)
    drums = max(2, math.ceil(load / DRUM_KG))
    if load <= 500: verdict = "a light dock"
    elif load <= 1500: verdict = "a family dock"
    else: verdict = "a party dock"
    return {"area": area, "load": load, "drums": drums, "verdict": verdict}

def pile_plan(depthM):
    if not (depthM > 0):
        return {"error": "the water depth must be positive"}
    pile = round1(depthM + FREEBOARD + EMBED)
    if depthM <= 1.5: verdict = "shallow water"
    elif depthM <= 3: verdict = "a normal shore"
    else: verdict = "deep water"
    return {"pile": pile, "verdict": verdict}

def gang_plan(dropM):
    if not (dropM > 0):
        return {"error": "the bank drop must be positive"}
    length = round1(dropM * GANG_SLOPE)
    if dropM <= 0.3: verdict = "nearly level"
    elif dropM <= 1: verdict = "an easy slope"
    else: verdict = "a steep drop"
    return {"length": length, "verdict": verdict}

def render_float(r, deckWm, deckLm, people):
    return ("A deck " + fmt(deckWm) + " m by " + fmt(deckLm) + " m is " + fmt(r["area"]) + " m2 and a labeled "
            + fmt(r["load"]) + " kg with " + plural(people, "person", "people") + " - "
            + plural(r["drums"], "drum") + ", " + r["verdict"] + ".")

def render_pile(r, depthM):
    return ("Water " + fmt(depthM) + " m deep asks piles " + fmt(r["pile"]) + " m long with a labeled "
            + fmt(FREEBOARD) + " m freeboard - " + r["verdict"] + ".")

def render_gang(r, dropM):
    return ("A bank " + fmt(dropM) + " m above the dock at a labeled 1:" + fmt(GANG_SLOPE) + " slope asks a gangway "
            + fmt(r["length"]) + " m long - " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[2,4,4],[2,3,0],[3,6,6],[2,5,2],[4,8,10],[1.5,2,0],[2.5,4,3],[3,5,5],[0,4,4],[2,0,4]]:
    add("floatPlan", float_plan, render_float, a)
for a in [[1.2],[2],[0.5],[1.5],[1.6],[3],[3.1],[2.4],[0],[5]]:
    add("pilePlan", pile_plan, render_pile, a)
for a in [[0.5],[0.2],[1.5],[0.3],[0.4],[1],[1.1],[2],[0],[0.25]]:
    add("gangPlan", gang_plan, render_gang, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
