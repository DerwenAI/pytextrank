Example Read Me for Pip-Tools
---

# Purpose 
The purpose of this example is to show how to use pip-tools to manage python dependencies.

We want to have complete control over the critical packages and dependencies of the project.

The non-critical packages and dependencies should be updated to the latest versions.

This allows keeping the project up to date with the latest versions of packages and dependencies,
while maintaining control over the critical packages and dependencies.

The project would always be upto date with the latest versions of packages and dependencies,
keep the dependencies more secure, and reduce the amount of work to keep the project up to date.

# Pip-Tools

We have example files of:
> requirements 
> requirements_viz 
> pyproject.toml 
> pre-commit-hook-config.yaml

# Requirements .in and .txt
Pip-Tools use the requirements_{name}.in to generate the requirements_{name}.txt files.

We can have as many requirements_{name}.in files as needed, and still reduce complexity,
as we can layer the requirements_{name}.txt files to build up the requirements_{name}.in files.

We would want to generate the requirements_{name}.txt with hash values.
If we compare the hash values of the requirements_{name}.txt files,
we can determine if the requirements_{name}.txt files are the same or different.
Which would enable us to see when versions of packages and dependencies change.


The requirements_{name}.in can use other requirements_{name}.txt files as input.
So we can layer the requirements_{name}.in files to build up the, requirements_{name}.txt files.


# Pip-Tools usage examples

### Using requirements_{name}.in files as input
```bash
pip-compile --generate-hashes --output-file requirements_{name}.txt requirements_{name}.in
```

### Using the pyproject.toml file as input
```bash
pip-compile -o requirements.txt pyproject.toml
pip-compile --output-file=requirements.txt pyproject.toml
```


