#!/usr/bin/env python3
"""
Refresh data/prime_rib.json for the /prime-rib-price/ page.

Every number comes from a published source and is stored with its source name,
link and as-of date. Nothing is estimated or invented. If a source can't be
fetched or parsed, that block keeps its previous values (and previous as-of
date) and the failure is printed, so the page never shows a fresh-looking date
on stale data.

Sources
  1. USDA AMS "Weekly Grocery Store Beef Feature Activity" (My Market News slug 3228,
     formerly the National Retail Report - Beef): advertised retail prices for
     bone-in / boneless ribeye (rib) roasts, national and by region and grade.
  2. USDA AMS National Daily Boxed Beef Cutout (LM_XB403, slug 2453): wholesale
     Choice rib, ribeye, lip-on, bone-in (IMPS 109E) and Primal Rib values.
  3. USDA AMS National Weekly Boxed Beef Cuts for Prime Product (LM_XB456, slug 2460):
     wholesale Prime 109E.
  4. Ranch-direct: each ranch's own Shopify product feed (<shop>/products/<handle>.js),
     listed in data/prime_rib_ranches.json. $/lb is only computed when the ranch
     states the weight in the variant title (e.g. "10 lbs"); otherwise it is left blank.

Needs `pdftotext` (poppler-utils) for the USDA PDFs; falls back to pypdf if installed.
Usage: python3 scripts/update_prime_rib.py [--no-ranches] [--out data/prime_rib.json]
"""
from html import unescape as html_unescape
import json, re, subprocess, sys, time, shutil, tempfile, os, urllib.request, urllib.error
from datetime import datetime, date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'prime_rib.json')
RANCHES_CFG = os.path.join(ROOT, 'data', 'prime_rib_ranches.json')
UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0 AcreAndPlate-price-check'

RETAIL_URL = 'https://www.ams.usda.gov/mnreports/ams_3228.pdf'
RETAIL_PAGE = 'https://mymarketnews.ams.usda.gov/viewReport/3228'
DAILY_URL = 'https://www.ams.usda.gov/mnreports/ams_2453.pdf'
DAILY_PAGE = 'https://mymarketnews.ams.usda.gov/viewReport/2453'
PRIME_URL = 'https://www.ams.usda.gov/mnreports/ams_2460.pdf'
PRIME_PAGE = 'https://mymarketnews.ams.usda.gov/viewReport/2460'


def http_get(url, binary=False, tries=4, timeout=40):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            return data if binary else data.decode('utf-8', 'replace')
        except Exception as e:  # noqa
            last = e
            time.sleep(4 * (i + 1))
    raise RuntimeError(f'GET {url} failed: {last}')


def pdf_files(url):
    """Download a USDA PDF; return (layout text, bbox html or None)."""
    raw = http_get(url, binary=True)
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        f.write(raw)
        path = f.name
    try:
        if shutil.which('pdftotext'):
            txt = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True, check=True).stdout
            box = subprocess.run(['pdftotext', '-bbox', path, '-'], capture_output=True, text=True, check=True).stdout
            return txt, box
        try:
            import pypdf  # type: ignore
            return '\n'.join(p.extract_text(extraction_mode='layout') for p in pypdf.PdfReader(path).pages), None
        except ImportError:
            raise RuntimeError('need pdftotext (poppler-utils) or pypdf to read USDA PDFs')
    finally:
        os.unlink(path)


def pdf_text(url):
    return pdf_files(url)[0]


def num(s):
    return float(s.replace(',', ''))


# ---------------------------------------------------------------- retail
ROW = re.compile(
    r'Ribeye Roast, (?P<cut>Bone-In|Boneless), (?P<tier>Regular|Value)\s+'
    r'(?P<env>Conventional|ABF, Grass Fed|Antibiotic Free|USDA Organic,?)\s+(?P<cond>Fresh|Frozen)\s+'
    r'(?P<stores>[\d,]+)\s+(?P<lo>[\d.]+)\s*-\s*(?P<hi>[\d.]+)\s+(?P<avg>[\d.]+)')
NAT = re.compile(
    r'Ribeye Roast, (?P<cut>Bone-In|Boneless), (?P<tier>Regular|Value)\s+'
    r'(?P<env>Conventional|ABF, Grass Fed)\s*(?P<cond>Fresh|Frozen)\s+(?P<rest>.*)$')


def nat_numbers(rest):
    """National rows list CW / PW / PY as (stores, avg) pairs, any of which may be blank.
    Column position tells us which is which, so use the raw text spacing."""
    return re.findall(r'([\d,]+)\s+([\d.]+)', rest)


def parse_national_bbox(box):
    """National rows list this week / last week / last year as (stores, avg) pairs, with blanks where a
    column has no ads. Text layout can't tell which column a lone pair belongs to, so use word x-positions."""
    rows = []
    for page in box.split('<page ')[1:]:
        words = [(float(a), float(b), float(c), html_unescape(w)) for a, b, c, d, w in
                 re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', page)]
        avg_x = sorted(x1 for x0, y0, x1, w in words if w == 'Avg')
        if len(avg_x) != 3 or any(w == 'Range' for x0, y0, x1, w in words):
            continue  # not a national page
        by_y = {}
        for x0, y0, x1, w in words:
            by_y.setdefault(round(y0), []).append((x0, x1, w))
        for y, ws in sorted(by_y.items()):
            ws.sort()
            txt = ' '.join(w for _, _, w in ws)
            m = re.match(r'.*?Ribeye Roast, (Bone-In|Boneless), (Regular|Value) (Conventional|ABF, Grass Fed|Antibiotic Free|USDA Organic,?) ?(Fresh|Frozen)', txt)
            if not m:
                continue
            nums = [(x0, x1, w) for x0, x1, w in ws if re.fullmatch(r'[\d,]+(?:\.\d+)?', w)]
            entry = {'cut': m.group(1), 'tier': m.group(2), 'env': m.group(3).rstrip(','), 'cond': m.group(4),
                     'cw': None, 'pw': None, 'py': None}
            # numbers come as store-count then average; averages contain a '.'
            avgs = [(x1, w) for x0, x1, w in nums if '.' in w]
            stores = [(x1, w) for x0, x1, w in nums if '.' not in w]
            for x1, w in avgs:
                k = min(range(3), key=lambda j: abs(x1 - avg_x[j]))
                st = min(stores, key=lambda s: abs(s[0] - (x1 - 40)) if s[0] < x1 else 1e9, default=None)
                entry[('cw', 'pw', 'py')[k]] = {'stores': int(num(st[1])) if st else None, 'avg': num(w)}
            rows.append(entry)
    return rows


def parse_retail(txt, bbox=None):
    out = {}
    m = re.search(r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\w{3} \d{1,2}, \d{4})', txt[:600])
    if not m:
        raise RuntimeError('retail: report date not found')
    out['report_date'] = datetime.strptime(m.group(1), '%b %d, %Y').date().isoformat()
    m = re.search(r'period of\s+(\d\d/\d\d/\d{4})\s+to\s+(\d\d/\d\d/\d{4})', txt)
    out['ad_period'] = {'start': datetime.strptime(m.group(1), '%m/%d/%Y').date().isoformat(),
                        'end': datetime.strptime(m.group(2), '%m/%d/%Y').date().isoformat()} if m else None
    m = re.search(r'(Bone-?in ribeye roasts averaged \$[\d.]+ per pound compared to \$[\d.]+ per pound in \d{4}\.)',
                  re.sub(r'\s+', ' ', txt).replace('bone- in', 'bone-in'), re.I)
    out['usda_note'] = m.group(1) if m else None
    flat = re.sub(r'\s+', ' ', txt)
    m = re.search(r'Prime Rib Dinner \(4-10\)\s+([\d.]+)-([\d.]+)\s+([\d.]+)', flat)
    m2 = re.search(r'([\d.]+)%\s+Prime Rib Dinner \(4-10\)', flat)
    out['prime_rib_dinner'] = ({'servings': '4-10', 'pct_stores': num(m2.group(1)) if m2 else None,
                                'low': num(m.group(1)), 'high': num(m.group(2)), 'avg': num(m.group(3))}
                               if m else None)

    lines = txt.splitlines()
    # national block = everything before the first region header
    region_idx = [(i, re.match(r'^([A-Z][A-Z ]+?)(?: REGION)? \(([A-Z, ]+)\)\s*$', l)) for i, l in enumerate(lines)]
    region_idx = [(i, m) for i, m in region_idx if m]
    first = region_idx[0][0]
    out['national'] = parse_national_bbox(bbox) if bbox else []

    # regional rows with price ranges
    regional = []
    for ri, (start, m) in enumerate(region_idx):
        end = region_idx[ri + 1][0] if ri + 1 < len(region_idx) else len(lines)
        region = m.group(1).title().replace(' Region', '')
        quality = None
        for j in range(start, end):
            l = lines[j]
            if l.startswith(('Section', ' Weekly', 'Weekly')) or not l.strip():
                continue
            q = re.match(r'^(?:Rib|Chuck|Loin|Brisket|Round|Sirloin|Ground|Deli|Variety|Other|Carcass|Meat|Misc)\S*\s+'
                         r'(Branded|Choice|Prime|Select|Ungrade)', l)
            if q:
                quality = q.group(1)
                if quality == 'Branded':
                    nxt = lines[j + 1].strip() if j + 1 < len(lines) else ''
                    s = re.match(r'^- (Choice|Prime|Select)$', nxt)
                    quality = f'Branded - {s.group(1)}' if s else 'Branded'
                elif quality == 'Ungrade':
                    quality = 'Ungraded/Other'
            r = ROW.search(l)
            if r:
                regional.append({'region': region, 'grade': quality, 'cut': r.group('cut'), 'tier': r.group('tier'),
                                 'env': r.group('env').rstrip(','), 'cond': r.group('cond'),
                                 'stores': int(num(r.group('stores'))), 'low': num(r.group('lo')),
                                 'high': num(r.group('hi')), 'avg': num(r.group('avg'))})
    out['regional'] = regional
    return out


# ------------------------------------------------------------- wholesale
def parse_daily(txt):
    if 'LM_XB403' not in txt[:600]:
        raise RuntimeError('daily cutout: unexpected report')
    m = re.search(r'(\w+ \d{1,2}, \d{4})', txt[:600])
    d = datetime.strptime(m.group(1), '%B %d, %Y').date().isoformat()
    t = re.search(r'(Afternoon|Morning)', txt[:300])
    prim = re.search(r'Primal Rib\s+([\d,.]+)\s+([\d,.]+)', txt)
    # Choice section: first 109E line after "Choice Cuts, Fat Limitations"
    ch = txt[txt.index('Choice Cuts, Fat Limitations'):]
    r = re.search(r'109E\s+1\s+Rib, ribeye, lip-on, bn-in\s+(\d+)\s+([\d,]+)\s+([\d,.]+)\s*-\s*([\d,.]+)\s+([\d,.]+)', ch)
    if not r or not prim:
        raise RuntimeError('daily cutout: rows not found')
    return {'report_date': d, 'session': t.group(1).lower() if t else None, 'id': 'LM_XB403',
            'primal_rib_choice_cwt': num(prim.group(1)), 'primal_rib_select_cwt': num(prim.group(2)),
            'ribeye_lipon_bonein_choice': {'trades': int(r.group(1)), 'pounds': int(num(r.group(2))),
                                           'low_cwt': num(r.group(3)), 'high_cwt': num(r.group(4)),
                                           'avg_cwt': num(r.group(5))}}


def parse_prime(txt):
    if 'LM_XB456' not in txt[:600]:
        raise RuntimeError('prime cuts: unexpected report')
    m = re.search(r'(\w+ \d{1,2}, \d{4})', txt[:600])
    d = datetime.strptime(m.group(1), '%B %d, %Y').date().isoformat()
    r = re.search(r'109E\s+1\s+Rib, ribeye, lip-on, bn-in\s+(\d+)\s+([\d,]+)\s+([\d,.]+)\s*-\s*([\d,.]+)\s+([\d,.]+)', txt)
    if not r:
        raise RuntimeError('prime cuts: row not found')
    return {'report_date': d, 'id': 'LM_XB456',
            'ribeye_lipon_bonein_prime': {'trades': int(r.group(1)), 'pounds': int(num(r.group(2))),
                                          'low_cwt': num(r.group(3)), 'high_cwt': num(r.group(4)),
                                          'avg_cwt': num(r.group(5))}}


# --------------------------------------------------------------- ranches
LB = re.compile(r'(\d+(?:\.\d+)?)(?:\s*[-–]\s*(\d+(?:\.\d+)?))?\s*(?:lbs?|pounds?)\b', re.I)


def fetch_ranch(cfg):
    """Read one ranch product from its Shopify feed.

    $/lb comes from (1) a weight in the variant title ("10 lbs"), or (2) a weight / $-per-lb statement in
    the product title or description that cfg['weights'] / cfg['stated_per_lb'] points at. For (2) the
    exact quoted text must still be on the page, otherwise the per-lb figure is dropped (never guessed)."""
    base = cfg['shop'].rstrip('/')
    d = json.loads(http_get(f"{base}/products/{cfg['handle']}.js"))
    desc = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', d.get('description') or ''))
    desc = desc.replace('&amp;', '&')
    haystack = (d.get('title') or '') + ' ' + desc
    variants = []
    for v in d.get('variants', []):
        price = v['price'] / 100.0
        vt = v.get('title') or ''
        m = LB.search(vt)
        lo = hi = per_lo = per_hi = None
        approx = False
        basis = None
        if m:
            lo = float(m.group(1)); hi = float(m.group(2)) if m.group(2) else lo
            per_lo, per_hi = sorted((round(price / hi, 2), round(price / lo, 2)))
            basis = 'variant title'
            approx = bool(re.search(r'approx', vt, re.I))
        else:
            for w in cfg.get('weights', []):
                if w['match'].lower() in vt.lower() and w['text'] in haystack:
                    lo, hi = float(w['lb_low']), float(w['lb_high'])
                    per_lo, per_hi = sorted((round(price / hi, 2), round(price / lo, 2)))
                    approx = bool(w.get('approx'))
                    basis = 'product page: ' + w['text']
            sp = cfg.get('stated_per_lb')
            if sp and sp['match'].lower() in vt.lower() and sp['text'] in haystack:
                per_lo = per_hi = float(sp['value'])
                basis = 'product page: ' + sp['text']
        variants.append({'title': vt, 'price': price, 'available': bool(v.get('available')),
                         'lb_low': lo, 'lb_high': hi, 'per_lb_low': per_lo, 'per_lb_high': per_hi,
                         'approx': approx, 'basis': basis})
    return {'slug': cfg['slug'], 'name': cfg['name'], 'state': cfg.get('state'), 'product': d.get('title'),
            'cut': cfg.get('cut'), 'url': f"{base}/products/{cfg['handle']}",
            'available': bool(d.get('available')), 'variants': variants,
            'price_note': cfg.get('price_note'),
            'checked': date.today().isoformat()}


def main():
    out_path = OUT
    if '--out' in sys.argv:
        out_path = sys.argv[sys.argv.index('--out') + 1]
    try:
        with open(out_path) as f:
            data = json.load(f)
    except Exception:
        data = {}
    errors = []

    def attempt(label, fn):
        try:
            return fn()
        except Exception as e:  # noqa
            errors.append(f'{label}: {e}')
            print(f'! {label} failed, keeping previous values: {e}', file=sys.stderr)
            return None

    r = attempt('retail', lambda: parse_retail(*pdf_files(RETAIL_URL)))
    if r:
        r.update({'source': 'USDA AMS Market News, Weekly Grocery Store Beef Feature Activity (National Retail Report - Beef)',
                  'url': RETAIL_PAGE, 'pdf': RETAIL_URL})
        data['retail'] = r
    d = attempt('daily cutout', lambda: parse_daily(pdf_text(DAILY_URL)))
    p = attempt('prime cuts', lambda: parse_prime(pdf_text(PRIME_URL)))
    if d or p:
        w = data.get('wholesale', {})
        if d:
            d.update({'source': 'USDA AMS Market News, National Daily Boxed Beef Cutout and Cuts - Negotiated Sales (LM_XB403)',
                      'url': DAILY_PAGE, 'pdf': DAILY_URL})
            w['daily'] = d
        if p:
            p.update({'source': 'USDA AMS Market News, National Weekly Boxed Beef Cuts for Prime Product - Negotiated Sales (LM_XB456)',
                      'url': PRIME_PAGE, 'pdf': PRIME_URL})
            w['prime'] = p
        data['wholesale'] = w

    if '--no-ranches' not in sys.argv and os.path.exists(RANCHES_CFG):
        cfgs = json.load(open(RANCHES_CFG))['ranches']
        old = {x['slug'] + '/' + x['url']: x for x in data.get('ranches', [])}
        new = []
        for c in cfgs:
            got = attempt(f"ranch {c['slug']}", lambda c=c: fetch_ranch(c))
            if got:
                new.append(got)
            else:
                prev = old.get(c['slug'] + '/' + f"{c['shop'].rstrip('/')}/products/{c['handle']}")
                if prev:
                    prev['stale'] = True
                    new.append(prev)
            time.sleep(3)  # be polite; shops rate-limit bursts
        data['ranches'] = new

    data['generated_at'] = datetime.now().astimezone().isoformat(timespec='seconds')
    data['errors'] = errors
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=1)
        f.write('\n')
    print(f"wrote {out_path} ({len(errors)} source errors)")
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main())
