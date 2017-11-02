from citrination_client import *
import os

api_key = os.environ['CITRINATION_API_KEY']
client = CitrinationClient(api_key)

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