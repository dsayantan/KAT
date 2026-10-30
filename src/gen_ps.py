"""Problem-Solving: computed puzzles (coding, directions, series, ranks, clock, calendar) + a few hand-authored."""
import random, math, datetime
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def sh(w, k): return "".join(A[(A.index(c)+k) % 26] for c in w)
def shp(w, ks): return "".join(A[(A.index(c)+ks[i % len(ks)]) % 26] for i, c in enumerate(w))
WORDS = ["PLANET", "MARKET", "BRIDGE", "SILVER", "GARDEN", "WINTER", "CANDLE", "TEMPLE", "FOREST", "ISLAND", "BASKET", "ORANGE", "MIRROR", "SUMMER", "DOCTOR", "PILLOW"]

def D(q, ans, wrongs, sol): return dict(q=q, ans=str(ans), wrongs=[str(w) for w in wrongs], sol=sol)

def g_shift(r):
    ex, tg = r.sample(WORDS, 2); k = r.choice([1, 2, 3, 4, -1, -2]); a = sh(tg, k)
    w = [sh(tg, k+1), sh(tg, k-1), sh(tg, -k)]
    return D(f"In a certain code, {ex} is written as {sh(ex, k)}. How is {tg} written in that code?", a, w,
             f"Compare {ex[0]}→{sh(ex, k)[0]}: every letter moves {k:+d} place(s) in the alphabet. Applying the same rule to {tg} gives {a}.")

def g_alt(r):
    ks = r.choice([[1, -1], [0, -1], [2, 0], [1, 2], [-1, 1], [3, -2]]); ex, tg = r.sample(WORDS, 2); a = shp(tg, ks)
    w = [shp(tg, ks[::-1]), shp(tg, [ks[0]]), shp(tg, [k+1 for k in ks])]
    return D(f"In a certain code, {ex} is written as {shp(ex, ks)}. How is {tg} written in that code?", a, w,
             f"Letter by letter the shifts are {', '.join('%+d' % ks[i % len(ks)] for i in range(len(ex)))}, so the shifts alternate {ks}. Apply it to {tg}: {a}. (Test every position – a single-shift guess fails.)")

COMP = {(0, 1): "North", (0, -1): "South", (1, 0): "East", (-1, 0): "West"}
def g_dir(r):
    while True:
        head = (0, 1); x = y = 0; legs = []
        for i in range(3):
            d = r.choice([3, 4, 5, 6, 8, 9, 12]); t = r.choice("LR") if i else None
            if t == "L": head = (-head[1], head[0])
            if t == "R": head = (head[1], -head[0])
            x += head[0]*d; y += head[1]*d; legs.append((t, d, head))
        dist = math.hypot(x, y)
        if abs(dist-round(dist)) < 1e-9 and dist > 0: break
    names = {(0, 1): "north", (0, -1): "south", (1, 0): "east", (-1, 0): "west"}
    txt = f"Starting from a point, Zoya walks {legs[0][1]} km towards north. She turns {'left' if legs[1][0]=='L' else 'right'} and walks {legs[1][1]} km, then turns {'left' if legs[2][0]=='L' else 'right'} and walks {legs[2][1]} km. How far is she from the starting point?"
    d = int(round(dist)); s = sum(l[1] for l in legs)
    wr = {d+1, d-1 if d > 1 else d+2, s, abs(legs[0][1]-legs[1][1]) or d+3}
    wr.discard(d)
    wr = sorted(wr)[:3]
    while len(wr) < 3: wr.append(d+len(wr)+3)
    return D(txt, f"{d} km", [f"{w} km" for w in wr],
             f"Draw it on a grid with north up: she ends at ({x}, {y}) east/north of the start. Distance = √({x}² + {y}²) = {d} km.")

def g_series(r):
    k = r.randrange(6)
    if k == 0: a, d = r.randint(2, 9), r.randint(3, 7); s = [a+d*i for i in range(6)]; sol = f"Constant difference +{d}."
    elif k == 1: a, m = r.randint(2, 4), r.choice([2, 3]); s = [a*m**i for i in range(6)]; sol = f"Each term is ×{m} the previous."
    elif k == 2: a = r.randint(1, 5); s = [(a+i)**2 for i in range(6)]; sol = "Perfect squares of consecutive integers."
    elif k == 3: a = r.randint(1, 6); d0 = r.randint(1, 3); s = [a]; d = d0
    elif k == 4: a = r.randint(3, 9); s = [a, a*2+1]; 
    else: a = r.randint(2, 6); s = [i*i*i + a for i in range(1, 7)]; sol = f"Cubes of 1,2,3… plus {a}."
    if k == 3:
        for _ in range(5): s.append(s[-1]+d); d += 1
        sol = f"Differences grow by 1 each step: {', '.join(str(s[i+1]-s[i]) for i in range(5))}."
    if k == 4:
        while len(s) < 6: s.append(s[-1]*2+ (1 if len(s) % 2 == 0 else 1))
        sol = "Each term = 2 × previous + 1."
        s = [a]; [s.append(s[-1]*2+1) for _ in range(5)]
    shown, ans = s[:5], s[5]
    wr = list({ans+1, ans-1, ans + (s[4]-s[3]), ans+2, ans*2-s[4]} - {ans})[:3]
    return D(f"Find the next term: {', '.join(map(str, shown))}, ?", ans, wr, sol + f" Next term = {ans}.")

def g_letter(r):
    st = r.randint(0, 5); d0 = r.choice([1, 2]); idx = [st]; d = d0
    for _ in range(5): idx.append(idx[-1]+d); d += 1
    L = [A[i % 26] for i in idx]; ans = L[5]
    wr = [A[(idx[5]+1) % 26], A[(idx[5]-1) % 26], A[(idx[4]+d-2) % 26]]
    wr = [w for w in dict.fromkeys(wr) if w != ans][:3]
    while len(wr) < 3: wr.append(A[(idx[5]+len(wr)+2) % 26])
    return D(f"Find the next letter: {', '.join(L[:5])}, ?", ans, wr, f"Position gaps: {', '.join(str(idx[i+1]-idx[i]) for i in range(4))} – the gap rises by 1 each time, so the next gap is {idx[5]-idx[4]} and the letter is {ans}.")

def g_rank(r):
    p, q = r.randint(5, 20), r.randint(5, 20); n = p+q-1
    return D(f"In a class, Kabir ranks {p}th from the top and {q}th from the bottom. How many students are there in the class?", n, [p+q, p+q-2, abs(p-q)+1],
             f"Total = rank from top + rank from bottom − 1 = {p} + {q} − 1 = {n}. (Kabir is counted in both ranks.)")

def g_clock(r):
    while True:
        h, m = r.randint(1, 11), r.choice([0, 10, 20, 30, 40, 50, 15, 45])
        a = abs(30*h - 5.5*m); a = min(a, 360-a)
        if a > 0: break
    f = lambda v: f"{v:g}°"
    wr = [abs(30*h-6*m), 30*h, a+15]; wr = [w for w in wr if w != a and 0 < w <= 180]
    wr = list(dict.fromkeys(wr))
    while len(wr) < 3: wr.append(a+30*(len(wr)+1) if a+30*(len(wr)+1) <= 180 else abs(a-30*(len(wr)+1)))
    return D(f"What is the smaller angle between the hands of a clock at {h}:{m:02d}?", f(a), [f(w) for w in wr[:3]],
             f"Angle = |30h − 5.5m| = |30×{h} − 5.5×{m}| = {abs(30*h-5.5*m):g}°; the smaller angle is {f(a)}. (The hour hand also moves as the minutes pass – ignoring that gives the trap value.)")

def g_cal(r):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]; i = r.randrange(7); n = r.randint(30, 400)
    ans = days[(i+n) % 7]
    wr = [days[(i+n+1) % 7], days[(i+n-1) % 7], days[(i+n+2) % 7]]
    return D(f"Today is {days[i]}. What day of the week will it be after {n} days?", ans, wr,
             f"{n} = 7 × {n//7} + {n%7}. Whole weeks bring the same day, so move {n%7} day(s) ahead of {days[i]}: {ans}.")

GEN = [g_shift, g_alt, g_dir, g_series, g_letter, g_rank, g_clock, g_cal]
WEIGHTS = [6, 6, 7, 8, 4, 4, 5, 5]

def generate(seed=11):
    r = random.Random(seed); out = []; seen = set()
    for g, n in zip(GEN, WEIGHTS):
        c = 0; tries = 0
        while c < n and tries < 400:
            tries += 1; d = g(r)
            if d["q"] in seen: continue
            if len(set([d["ans"]]+d["wrongs"])) != 4: continue
            if any(w in d["q"].replace("?", " ").replace(",", " ").split() for w in d["wrongs"]): continue
            seen.add(d["q"]); out.append(d); c += 1
    return out

def hand():
    return [
 D("Aarav is the brother of Bela. Bela is the daughter of Chitra. Chitra's husband is Dev. How is Dev related to Aarav?", "Father",
   ["Uncle", "Grandfather", "Brother"], "Bela and Aarav are siblings, so Chitra (Bela's mother) is also Aarav's mother; her husband Dev is therefore Aarav's father."),
 D("Pointing to a woman, Rohit says, “She is the daughter of my mother's only brother.” How is the woman related to Rohit?", "Cousin",
   ["Sister", "Niece", "Aunt"], "Rohit's mother's only brother is Rohit's maternal uncle; his daughter is Rohit's (maternal) cousin."),
 D("Pointing to a man, Tara says, “His mother is the only daughter of my mother.” How is the man related to Tara?", "Son",
   ["Brother", "Nephew", "Uncle"], "Tara's mother's only daughter is Tara herself. So the man's mother is Tara, and the man is Tara's son."),
 D("Six friends P, Q, R, S, T and U sit in a row facing north. Q sits at an extreme end. P is second to the right of Q. S is between P and U. T sits at the other extreme end. Who sits immediately to the left of T?", "U",
   ["S", "R", "P"], "Q is at the left end (so T is at the right end). P is second to the right of Q: position 3, so R must sit at 2 (the only remaining place before P). S is between P and U: P(3) S(4) U(5), and T is at 6. Order Q R P S U T – the person immediately to the left of T is U."),
 D("Statements: All pens are books. Some books are bags. Conclusions: I. Some pens are bags. II. Some bags are books. Which follows?", "Only II follows",
   ["Only I follows", "Both follow", "Neither follows"], "“Some books are bags” converts to “Some bags are books”, so II follows. The pens-in-books circle need not overlap the bags part of books, so I does not follow."),
 D("Statements: No cat is a dog. All dogs are animals. Which conclusion follows?", "Some animals are not cats",
   ["All animals are dogs", "No animal is a cat", "All cats are animals"], "Dogs are animals and no dog is a cat, so those animals (the dogs) are not cats. Nothing is said about cats being animals, so the other options do not follow."),
 D("Pointing at a photograph, Mira says, “He is the son of the only son of my father's father.” How is the person in the photograph related to Mira?", "Brother",
   ["Cousin", "Uncle", "Father"], "The only son of Mira's paternal grandfather is Mira's father. His son is Mira's brother."),
]
