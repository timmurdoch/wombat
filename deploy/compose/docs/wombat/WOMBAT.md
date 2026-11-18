## WOMBAT — Australian Adaptation
This is a fork of GOAT (plan4better/goat) adapted for the Australian planning and transport context.
 
### Key differences from upstream GOAT
- Storage CRS stays EPSG:4326 (GOAT stores all layer data in 4326). Australian inputs in GDA2020 (EPSG:7844)
  or MGA zones (EPSG:7849-7859) are reprojected on import. Offer GDA2020 and MGA zones as export CRS options.
- Default project view: continental Australia, set with DEFAULT_PROJECT_VIEW_STATE (no code change).
- Street network: Overture Maps Australia extract, published as WOMBAT routing base data (see docs/wombat/network-pipeline.md).
- PT network: state and territory GTFS feeds (see docs/wombat/data-sources.md) replacing GOAT's European feed.
- Geocoder: self-hosted Pelias with G-NAF, reached through GEOCODING_URL.
- Speed limits: Australian defaults (urban 50, rural 100 or 110 km/h; shared zones 10; school zones 40).
- PT Service Quality: Australian station configuration profile for the OeV-Gueteklassen tool.
- Auth: Keycloak, with each agency's identity provider brokered via SAML or OIDC.
- Cloud: AWS ap-southeast-2 (Sydney), DR in ap-southeast-4 (Melbourne). All data stays in Australia.
- Compliance: Privacy Act 1988 and APPs, state privacy laws for state agencies, PSPF and the ISM.
 
### Australian data sources (paths inside the data volume / base data source)
- Street network: Overture transportation extract, bbox 112,-44,154,-10, clipped to the AU boundary
- G-NAF Core: data/geocoder/gnaf_core/
- DEM: data/dem/ (Geoscience Australia national DEM from ELVIS)
- GTFS feeds: data/gtfs/{nsw,vic,qld,wa,sa,tas,act,nt}/
- ABS boundaries: data/catalog/abs/{sa1,sa2,sa3,sa4,lga,sal,ste}/
 
### Do not modify
- packages/cpp/routing (routing engine) and the base data schema it reads at fixed widths
- OGC API Processes contracts and the tool registry interface
- MapLibre rendering pipeline and Windmill integration
- Existing tables: extend with new Alembic revisions in apps/core/alembic, never edit existing ones
 
### Upstream rules that still apply
- Follow AGENTS.md: update every deployment target (deploy/compose, deploy/helm, docs) when a setting changes;
  conventional commits; no em or en dashes in UI copy, docs or commit messages.
