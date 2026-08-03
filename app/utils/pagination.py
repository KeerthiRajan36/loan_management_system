def paginate(query, page: int = 1, limit: int = 10):

    total = query.count()

    records = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": records
    }