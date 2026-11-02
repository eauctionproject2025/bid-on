# Bid On — Diagram pack (editable + exports)

## How to edit (preferred)

| Diagram | Editable source | Open with |
|---------|-----------------|-----------|
| Architecture | `source/architecture.mmd` | VS Code Mermaid / [Mermaid Live](https://mermaid.live) |
| Deployment | `source/deployment/deployment.mmd` | Mermaid |
| DFD Context | `source/dfd-context.mmd` | Mermaid |
| DFD Level-0 | `source/dfd-level0.mmd` | Mermaid |
| Place-bid activity | `source/activity/place-bid.mmd` | Mermaid |
| Checkout sequence | `source/sequence/checkout.mmd` | Mermaid |
| Login sequence | `source/sequence/login.mmd` | Mermaid |
| Components | `source/component/components.mmd` | Mermaid |
| ERD | `source/erd/erd.mmd` **and** `../database/erd/database-erd.drawio` | Mermaid **or** [diagrams.net](https://app.diagrams.net) |
| Use case | `source/use-case.puml` **and** `source/use-case.mmd` | PlantUML / Mermaid |
| Domain class | `source/class-domain.mmd` (primary) / `source/class-domain.puml` | Mermaid / PlantUML |
| Multi-page draw.io | `source/drawio/bid-on-diagrams.drawio` | diagrams.net |

**Do not edit PNG/SVG by hand.** Change the source, then re-export.

## How to re-export PNG + SVG

```bash
# Requires Google Chrome installed
python docs/final-report/render_all_diagrams.py
```

Chrome path is set in `puppeteer-config.json`.

## Export locations

- `exports/png/*.png` — raster for Word/PDF
- `exports/svg/*.svg` — vector for slide decks / high quality print
- Database ERD copies: `docs/database/erd/database-erd.{drawio,png,svg}`

## Figure map (thesis)

| Figure | File stem |
|--------|-----------|
| 3.1 Architecture | `architecture` |
| 3.2 Deployment | `deployment_deployment` |
| 3.3 DFD context | `dfd-context` |
| 3.3b DFD level-0 | `dfd-level0` |
| 3.4 ERD | `erd_erd` / `database-erd` |
| 3.5 Place bid | `activity_place-bid` |
| 3.6 Checkout sequence | `sequence_checkout` |
| 3.6b Login sequence | `sequence_login` |
| 3.7 Components | `component_components` |
| 3.8 Use case | `use-case` |
| 3.9 Class | `class-domain` |
