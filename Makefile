# Makefile
.ONESHELL:
# Variables
IMAGE_NAME := voice-renamer
MODEL_PATH := deps/whisper.cpp/models/ggml-base.bin
MODEL_DIR  := $(dir $(MODEL_PATH))

# Make Makefile self-contained.
VENV_PYTHON := .venv/bin/python

# Set the help function as default
.DEFAULT_GOAL := help
## Help command and syntax from:
## https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html 

all: build ## Builds the application (Default)

build: $(MODEL_PATH) ## Builds Docker image
	@echo "--- Building Docker Image: $(IMAGE_NAME) ---"
	docker build -t $(IMAGE_NAME) .

test: clean build ## Runs a full build and integration test from a clean state
	@echo "--- Running Integration Test ---"
	@echo "--- [1/3] Setting up test environment ---"
	rm -rf ./test_input ./test_output
	mkdir -p ./test_input ./test_output
	@echo "--- [2/3] Copying known-good sample audio (jfk.wav) ---"
	cp deps/whisper.cpp/samples/jfk.wav ./test_input/
	@echo "--- [3/3] Executing container on sample audio ---"
	docker run --rm \
		-v "$(shell pwd)/test_input:/input" \
		-v "$(shell pwd)/test_output:/output" \
		$(IMAGE_NAME) \
		--speaker-id "ci-test" --input-dir /input --output-dir /output
	@echo "--- [4/4] Verifying SUCCESSFUL transcription and cleaning up ---"
	# Now we expect a SUCCESSFUL transcription of "and so my fellow americans"
	OUTPUT_FILE=$$(find ./test_output -name "ci-test_1_and_so_my_fellow_americans*.wav"); \
	if [ -n "$$OUTPUT_FILE" ]; then \
		echo "--- ✅ Integration Test PASSED ---"; \
		echo "Successfully created output file: $$OUTPUT_FILE"; \
		make clean-test; \
	else \
		echo "--- ❌ ERROR: Integration Test FAILED. Successful output file not found! ---"; \
		echo "Listing contents of ./test_output before failure:"; \
		ls -l ./test_output; \
		make clean-test; \
		exit 1; \
	fi

unit-test: ## Runs the pytest unit tests
	@echo "--- Running Unit Tests ---"
	$(VENV_PYTHON) -m pip install pytest
	$(VENV_PYTHON) -m pytest tests/

# Rule if Whisper model file is missing
$(MODEL_PATH):
	@echo "--- Model file not found. Downloading... ---"
	mkdir -p $(MODEL_DIR)
	cd deps/whisper.cpp
	sh models/download-ggml-model.sh base

# Cleaning
clean: ## Remove Docker image
	@echo "--- Removing Docker Image: $(IMAGE_NAME) ---"
	docker rmi -f $(IMAGE_NAME)

clean-test: ## Remove temporary test artifacts from test run
	@echo "--- Removing test artifacts ---"
	rm -rf ./test_input ./test_output

distclean: clean ## Deep clean: removes Docker image and AI model
	@echo "--- Removing Downloaded Model ---"
	rm -f $(MODEL_PATH)

help: ## Displays this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Assign 'Phonies'
.PHONY: all build test unit-test clean distclean help