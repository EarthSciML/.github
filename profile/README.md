# EarthSciML: Earth Science and Machine Learning

https://earthsci.dev

EarthSciML builds Earth science models as data. A model component (chemistry,
transport, emissions, meteorology, ...) is written once as an
[EarthSciAST](https://github.com/EarthSciML/EarthSciAST) `.esm` document, and
the same document can be validated, coupled, discretized, differentiated, and
run from Julia, Python, Rust, TypeScript, or Go.

## Repositories

| Repository | What it is | Packages | Tests |
| --- | --- | --- | --- |
| [EarthSciAST](https://github.com/EarthSciML/EarthSciAST) | The `.esm` format: an abstract syntax tree for Earth science models, with libraries to parse, validate, edit, couple, flatten, and simulate it. [Docs](https://earthsciml.github.io/EarthSciAST/) | [![Julia](https://img.shields.io/badge/julia-EarthSciAST-9558B2)](https://juliahub.com/ui/Packages/General/EarthSciAST) [![PyPI](https://img.shields.io/pypi/v/earthsci-ast?label=pypi)](https://pypi.org/project/earthsci-ast/) [![crates.io](https://img.shields.io/crates/v/earthsci-ast)](https://crates.io/crates/earthsci-ast) [![npm](https://img.shields.io/npm/v/@earthsciml/ast)](https://www.npmjs.com/package/@earthsciml/ast) [![Go](https://img.shields.io/badge/go-reference-007d9c)](https://pkg.go.dev/github.com/EarthSciML/EarthSciAST/pkg/earthsci-ast-go) | [![Conformance](https://github.com/EarthSciML/EarthSciAST/actions/workflows/conformance-testing.yml/badge.svg?branch=main)](https://github.com/EarthSciML/EarthSciAST/actions/workflows/conformance-testing.yml?query=branch%3Amain) |
| [EarthSciModels](https://github.com/EarthSciML/EarthSciModels) | The model components themselves, as `.esm` files with inline tests. [Docs](https://earthsciml.github.io/EarthSciModels/) | | [![Tests](https://github.com/EarthSciML/EarthSciModels/actions/workflows/test-esm.yml/badge.svg?branch=main)](https://github.com/EarthSciML/EarthSciModels/actions/workflows/test-esm.yml?query=branch%3Amain) |
| [EarthSciDiscretizations](https://github.com/EarthSciML/EarthSciDiscretizations) | The standard library of grids, finite-difference and finite-volume rules, and regridding, as `.esm` files. [Docs](https://discretizations.earthsci.dev/) | | [![Conformance](https://github.com/EarthSciML/EarthSciDiscretizations/actions/workflows/conformance.yml/badge.svg?branch=main)](https://github.com/EarthSciML/EarthSciDiscretizations/actions/workflows/conformance.yml?query=branch%3Amain) |
| [EarthSciIntegrator](https://github.com/EarthSciML/EarthSciIntegrator) | Time stepping for `.esm` models: explicit, implicit, IMEX, and split schemes with discrete adjoints, in Julia and Rust. | | [![CI](https://github.com/EarthSciML/EarthSciIntegrator/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/EarthSciML/EarthSciIntegrator/actions/workflows/ci.yml?query=branch%3Amain) |
| [EarthSciASTDiff](https://github.com/EarthSciML/EarthSciASTDiff) | Analytical sparse Jacobians of `.esm` models, by symbolic differentiation of the AST, in Julia, Python, and Rust. | | [![Conformance](https://github.com/EarthSciML/EarthSciASTDiff/actions/workflows/conformance.yml/badge.svg?branch=main)](https://github.com/EarthSciML/EarthSciASTDiff/actions/workflows/conformance.yml?query=branch%3Amain) |
| [EarthSciIO](https://github.com/EarthSciML/EarthSciIO) | Data providers: download, cache, and read input data onto the model's native grid, in Julia, Python, and Rust. | [![Julia](https://img.shields.io/badge/julia-EarthSciIO-9558B2)](https://juliahub.com/ui/Packages/General/EarthSciIO) [![PyPI](https://img.shields.io/pypi/v/earthsciio?label=pypi)](https://pypi.org/project/earthsciio/) [![crates.io](https://img.shields.io/crates/v/earthsciio)](https://crates.io/crates/earthsciio) | [![Tests](https://github.com/EarthSciML/EarthSciIO/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/EarthSciML/EarthSciIO/actions/workflows/tests.yml?query=branch%3Amain) |

## Star us on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=EarthSciML/EarthSciAST,EarthSciML/EarthSciModels,EarthSciML/EarthSciDiscretizations,EarthSciML/EarthSciIntegrator,EarthSciML/EarthSciASTDiff,EarthSciML/EarthSciIO)](https://www.star-history.com/#EarthSciML/EarthSciAST&EarthSciML/EarthSciModels&EarthSciML/EarthSciDiscretizations&EarthSciML/EarthSciIntegrator&EarthSciML/EarthSciASTDiff&EarthSciML/EarthSciIO)

## Contributors

![Contributors](https://github.com/EarthSciML/.github/blob/main/contributors.svg)
