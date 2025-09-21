#!/bin/bash

# Usage function
usage() {
    echo "Usage: $0 [dcbot|tower|all] [dev|deploy]"
    echo ""
    echo "Options:"
    echo "  dcbot dev     - Run Discord bot in development mode"
    echo "  dcbot deploy  - Run Discord bot in deployment mode"
    echo "  tower         - Run Watchtower containers for auto-updates"
    echo "  all           - Run both Discord bot (deploy) and Watchtower containers"
    echo ""
    echo "Examples:"
    echo "  $0 dcbot dev     # Run Discord bot in dev mode"
    echo "  $0 dcbot deploy  # Run Discord bot in deploy mode"
    echo "  $0 tower         # Run only Watchtower"
    echo "  $0 all           # Run bot (deploy) and Watchtower"
}

# Function to run Discord bot in dev mode
run_dcbot_dev() {
    echo "Starting Discord bot in development mode..."
    cd docker
    docker compose -p discord-bot -f compose.dcbot.yml up dev -d
    echo "Discord bot (dev mode) started successfully!"
}

# Function to run Discord bot in deploy mode
run_dcbot_deploy() {
    echo "Starting Discord bot in deployment mode..."
    cd docker
    docker compose -p discord-bot -f compose.dcbot.yml up default -d
    echo "Discord bot (deploy mode) started successfully!"
}

# Function to run Watchtower
run_watchtower() {
    echo "Starting Watchtower containers..."
    cd docker
    docker compose -p watchtower -f compose.watchtower.yml up watchtower-1 -d
    echo "Watchtower started successfully!"
}

# Function to run all services
run_all() {
    echo "Starting all containers..."
    run_dcbot_deploy
    run_watchtower
    echo "All services started successfully!"
}

# Set DISPLAY environment variable
export DISPLAY=:0

# Check if no arguments provided
if [ $# -eq 0 ]; then
    usage
    exit 0
fi

# Parse command line arguments
case "$1" in
    "dcbot")
        if [ "$2" = "dev" ]; then
            run_dcbot_dev
        elif [ "$2" = "deploy" ]; then
            run_dcbot_deploy
        else
            echo "Error: dcbot requires mode [dev|deploy]"
            echo "Usage: $0 dcbot [dev|deploy]"
            exit 1
        fi
        ;;
    "tower")
        run_watchtower
        ;;
    "all")
        run_all
        ;;
    "-h"|"--help"|"help")
        usage
        ;;
    *)
        echo "Error: Unknown option '$1'"
        echo ""
        usage
        exit 1
        ;;
esac