import re


def translate_insert(query):
    match = re.search(r"insert\s+into\s+(\w+)\s*\(([^)]+)\)\s*values\s*\(([^)]+)\)\s*;?\s*$", query, re.IGNORECASE)
    if not match:
        raise ValueError("Formato INSERT inválido.")
    table = match.group(1)
    columns = [c.strip() for c in match.group(2).split(",")]
    raw_values = [v.strip() for v in match.group(3).split(",")]
    values = []
    for v in raw_values:
        v = v.strip()
        if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
            v = v[1:-1]
        values.append(v)
    props = ", ".join([f"{k}: '{v}'" if not v.isdigit() else f"{k}: {v}" for k, v in zip(columns, values)])
    return f"CREATE (n:{table} {{{props}}})"
