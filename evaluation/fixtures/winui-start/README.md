# WinUI evaluation start project

This is the clean starting project for all LazyDesign v0.1 baseline and guided runs.

- Target framework: `net9.0-windows10.0.22621.0`
- Windows App SDK: `2.0.1`
- Architecture: `x64`
- Packaging: unpackaged, self-contained Windows App SDK
- LazyDesign reference files: none

Build from this directory:

```powershell
dotnet build LazyDesign.EvaluationApp.csproj -c Debug -p:Platform=x64
```

Every run must start from the exact repository commit that first contains this fixture. Generated scenario files must not modify this fixture in place.
