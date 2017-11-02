from citrination_client import *
import os

# API key from website, make it an environment variable
api_key = os.environ['CITRINATION_API_KEY']
# Makes a local version of CitrinationClient
client = CitrinationClient(api_key)

# Query the website
query = PifQuery(
    from_index=0,
    size=1000,
    system=SystemQuery(
        chemical_formula=ChemicalFieldQuery(
            filter=ChemicalFilter(equal='GaN')
        ),
        properties=PropertyQuery(
            name=FieldQuery(
                filter=Filter(equal='Band gap')
            ),
            value=FieldQuery(
                filter=Filter(
                    min=3,
                    max=4
                )
            ),
            units=FieldQuery(
                filter=Filter(equal='eV')
            )
        )
    )
)

results = client.search(query)