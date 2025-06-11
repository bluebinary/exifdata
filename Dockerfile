# syntax = docker/dockerfile:1.4.0

################################# [Base Python Image] ##################################

# Allow the Python version to be specified as a build argument, with a preferred default
ARG VERSION=3.12

FROM python:${VERSION} AS base

# Create a symlink between the installed Python version path and a versionless path to
# ease long-term maintenance that simply requires the symlink to be generated when the
# Python version is modified, rather than a whole range of absolute paths. Many Python
# installations create a versionless path symlink by default; Docker's doesn't seem to.
RUN <<ENDRUN
	# Use 'awk' and 'cut' to extract the major.minor version from `python --version` as
	# the major.minor, but not micro, version parts are used in the installation path:
	VERSION=$(python --version 2>&1 | awk '{print $2}' | cut -d'.' -f1,2)
	echo "Creating a symlink from the versioned installation path to a generic path:"
	ln -s -v "/usr/local/lib/python${VERSION}" "/usr/local/lib/python"
ENDRUN

# Ensure pip has been upgraded to the latest version before installing dependencies
RUN pip install --upgrade pip

############################# [Development Python Image] ###############################

FROM base AS development

# Copy and install the dependencies from requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --requirement /app/requirements.txt

# Copy and install the dependencies from requirements.development.txt
COPY requirements.development.txt /app/requirements.development.txt
RUN pip install --requirement /app/requirements.development.txt

# Copy and install the dependencies from requirements.deployment.txt
# COPY requirements.deployment.txt /app/requirements.deployment.txt
# RUN pip install --requirement /app/requirements.deployment.txt

# Copy the library source into the container's source folder for Black linting checks
COPY ./source/exifdata /source/exifdata

# Copy the README into the container's root folder for PyTest README code block testing
COPY ./README.md /README.md

# Copy the tests into the container's root folder for PyTest unit testing
COPY ./tests /tests

# Copy the library source into the container's site-packages folder for the unit tests
COPY ./source/exifdata /usr/local/lib/python/site-packages/exifdata

# Create a custom entry point that allows us to override the command as needed
COPY <<"EOF" /entrypoint.sh
#!/bin/bash

ARGS=( "$@" );

echo -e "entrypoint.sh called with arguments: ${ARGS[@]} (service: ${SERVICE})";

if [[ "${SERVICE}" == "black" ]]; then
	if [[ "${ARGS[0]}" == "--reformat" ]]; then
		echo -e "black --verbose ${ARGS[@]:1} /source /tests /documentation";
		black --verbose ${ARGS[@]:1} /source /tests /documentation;
	else
		echo -e "black --check ${ARGS[@]:1} /source /tests /documentation";
		black --check ${ARGS[@]:1} /source /tests /documentation;
	fi
elif [[ "${SERVICE}" == "tests" ]]; then
	echo -e "pytest /tests ${ARGS[@]}";
	pytest /tests ${ARGS[@]};
	pytest --verbose --codeblocks /README.md;
else
	echo -e "No valid command was specified nor defined in the `SERVICE` environment!";
fi
EOF

RUN chmod +x /entrypoint.sh

# Run the unit tests starter shell script
ENTRYPOINT [ "/entrypoint.sh" ]
