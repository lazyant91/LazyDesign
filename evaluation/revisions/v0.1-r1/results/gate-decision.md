# LazyDesign v0.1 Gate Decision

Overall result: **FAIL**

## Totals

| Metric | Result |
|---|---:|
| Baseline total | 15 / 60 |
| Guided total | 36 / 60 |
| Score improvement | 140.0% |
| Overflow mode | non-regression |
| Overflow reduction | not measurable |

## Guided build prerequisite

- [fail] All three guided controlled builds passed. connection-settings=pass; device-list=pass; failure-confirmation=not_run.

## Mechanical conditions

- [pass] Guided total improved by at least 20%. baseline 15, guided 36, improvement 140.0%.
- [pass] Zero-baseline clipping/content-overflow defects did not regress. baseline 0, guided 0; reduction not measurable.
- [pass] Missing anatomy and accessibility requirements decreased. anatomy 6 to 2; accessibility 4 to 1.
- [pass] Unnecessary ControlTemplate replacement did not increase. ControlTemplate defects 0 to 0.
- [pass] Irrelevant XAML or complexity did not materially increase. complexity defects 0 to 0.
- [pass] Improvements are traceable to specific reference rules. all 17 positive category changes have rule IDs and evidence.

The overall result is PASS only when the guided build prerequisite and all six quality conditions pass.
