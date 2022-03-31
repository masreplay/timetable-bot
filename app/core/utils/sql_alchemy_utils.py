def sa_column_kwargs(
        unique: bool | None,
) -> dict:
    kwargs = dict(unique=unique)
    return {k: v for k, v in kwargs.items() if v}


def sa_relationship_kwargs(cascade:str,):
    kwargs = dict(cascade=cascade)
    return {k: v for k, v in kwargs.items() if v}
