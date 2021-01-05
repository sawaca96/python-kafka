async def fetch_all(query):
    """
    Fetch data from database into formatted form
    """
    data = await query.gino.all()
    columns = [str(each.name) for each in query.columns]
    data = [dict(zip(columns, each)) for each in data]
    return data
