

def _unit_parse_cls_cat(_cat):
    r = []
    if "zh_name" in _cat.keys():
        c_name = _cat["zh_name"]
        r.append([c_name])
        if "sample" in _cat.keys():
            if len(_cat["sample"]) == 0:
                r.append([c_name, "SMLP"])
            for sample_name in _cat['sample']:
                r.append([c_name, sample_name, "SMLP"])
    return r


def parse_cls_cats(cats):
    r_samples = []
    for cat in cats:
        c_name = cat['zh_name']
        parent_list = _unit_parse_cls_cat(cat)
        r_samples.extend(parent_list)
        if "sub_class" in cat.keys():
            sub_classes = cat["sub_class"]
            _temp_sub_samples = parse_cls_cats(sub_classes)

            sub_samples = [[c_name, *_t] for _t in _temp_sub_samples]
            r_samples.extend(sub_samples)
    return r_samples
