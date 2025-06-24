# Makefile

# Variables
IMAGE_NAME := voice-renamer
MODEL_PATH := deps/whisper.cpp/models/ggml-base.bin
MODEL_DIR  := $(dir $(MODEL_PATH))

# Set the help function as default
.DEFAULT_GOAL := help
## Help command and syntax from:
## https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html 

all: build ## Full build (default)

build: $(MODEL_PATH) ## Build Docker image
	@echo "--- Building Docker Image: $(IMAGE_NAME) ---"
	docker build -t $(IMAGE_NAME) .

test: build ## Run simple test against built Docker image
	@echo "--- Running Smoke Test ---"
	docker run --rm $(IMAGE_NAME)

# Rule if Whisper model file is missing
$(MODEL_PATH):
	@echo "--- Model file not found. Downloading... ---"
	@mkdir -p $(MODEL_DIR) # Ensure the destination directory exists first.
	(cd deps/whisper.cpp && sh models/download-ggml-model.sh base)

clean: ## Remove Docker image
	@echo "--- Removing Docker Image: $(IMAGE_NAME) ---"
	# Use '-f' to ignore errors if the image doesn't exist.
	docker rmi -f $(IMAGE_NAME)

distclean: clean ## Remove Docker image and model
	@echo "--- Removing Downloaded Model ---"
	rm -f $(MODEL_PATH)

help: ## Displays this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Assign 'Phonies'
.PHONY: all build test clean distclean help