def metered_meta(metrics, base=type):
    """Stuff

    :param metrics: list of (attr_name, metrics_path_template, metrics_factory)
    :param base: optional meta base if other than `type`
    :return: a metaclass that populates the class with the needed metrics at paths based on the dynamic class name
    """
    class _MeteredMeta(base):
        def __new__(meta, name, bases, dict_):
            new_dict = dict(**dict_)
            for attr_name, template, factory in metrics:
                new_dict[attr_name] = factory(template.format(name))
            return super(_MeteredMeta, meta).__new__(meta, name, bases, new_dict)

    return _MeteredMeta
