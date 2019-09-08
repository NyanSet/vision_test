def same_json(json1, json2, float_round_size = 5):
    def cut_float(f, n):
        if isinstance(f, float):
            return int(f * 10 ** n) / 10 ** n
        else:
            return f
        
    def walk_json(j):
        if isinstance(j, dict):
            return {cut_float(key, float_round_size): walk_json(j[key]) for key in j}
        elif isinstance(j, list):
            return [walk_json(el) for el in j]
        else:
            return cut_float(j, float_round_size)

    j1, j2 = json1.copy(), json2.copy()
    return walk_json(j1) == walk_json(j2)
