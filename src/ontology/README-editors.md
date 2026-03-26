These notes are for the EDITORS of bervo

This project was created using the [ontology development kit](https://github.com/INCATools/ontology-development-kit). See the site for details.

BERVO uses a repo-first workflow:

- Edit `bervo-src.csv` to add or update term content
- Rebuild `components/bervo-src.owl` from that CSV with `make components/bervo-src.owl`
- Use `bervo-edit.owl` as the main ODK editor file

The Google Sheet is retained only as a secondary collaboration artifact. It should not be treated as the source of truth for builds, releases, or pull requests.

Useful commands:

```
make components/bervo-src.owl
make export-google-sheet
make compare-google-sheet
```

Legacy curation helper scripts live in `utils/`. They are not part of the standard ODK build.

For more details on ontology management, please see the 
[OBO Academy Tutorials](https://oboacademy.github.io/obook/), the
[OBO tutorial](https://github.com/jamesaoverton/obo-tutorial) or the [Gene Ontology Editors Tutorial](https://go-protege-tutorial.readthedocs.io/en/latest/)

This documentation has been superceded by the ODK automatic documentation, which you can
activate by adding:

```
documentation:
  documentation_system: mkdocs
```

to your Makefile and running:

```
sh run.sh make update_repo
```
(Unix)

```
run.bat make update_repo
```
(Windows)
