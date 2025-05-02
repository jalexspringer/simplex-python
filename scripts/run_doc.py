#!/usr/bin/env python3
"""
Sample usage of the enhanced SimpleX Chat WebSocket API Documentation Generator.
This script demonstrates how to run the generator with various options.
"""

import asyncio
import subprocess
import os
import argparse


async def main():
    """Run the documentation generator with sample options"""
    # Check if simplex-chat is running as a WebSocket server
    try:
        # Try to check if port 5226 is in use (common default)
        result = subprocess.run(["lsof", "-i", ":5226"], capture_output=True, text=True)

        if "simplex-chat" not in result.stdout:
            print("WARNING: No SimpleX Chat WebSocket server detected on port 5226")
            print("Starting simplex-chat server in WebSocket mode...")

            # Start simplex-chat in WebSocket mode in a separate terminal window
            # This is just an example - might need adjustment based on your OS
            subprocess.Popen(
                ["x-terminal-emulator", "-e", "simplex-chat -w 5226"],
                start_new_session=True,
            )

            # Give it time to start up
            print("Waiting 5 seconds for server to start...")
            await asyncio.sleep(5)
    except Exception as e:
        print(f"Could not check for running simplex-chat server: {e}")
        print(
            "Please ensure simplex-chat is running in WebSocket mode before continuing."
        )

    # Parse command line arguments for the documentation generator
    parser = argparse.ArgumentParser(
        description="Run SimpleX Chat WebSocket API Documentation Generator"
    )
    parser.add_argument(
        "--url",
        default="ws://localhost:5226",
        help="WebSocket URL of the SimpleX Chat server",
    )
    parser.add_argument(
        "--output",
        default="simplex_api_reference.md",
        help="Output file path for the documentation",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the documentation file after generation",
    )

    args = parser.parse_args()

    # Build the command to run the documentation generator
    cmd = [
        "python",
        "scripts/socket_doc.py",
        f"--url={args.url}",
        f"--output={args.output}",
    ]

    # Run the documentation generator
    print(f"Running documentation generator: {' '.join(cmd)}")
    process = subprocess.run(cmd, capture_output=True, text=True)

    # Check if the documentation was generated successfully
    if process.returncode == 0:
        print(f"Documentation generated successfully: {args.output}")

        # Open the documentation file if requested
        if args.open:
            if os.name == "nt":  # Windows
                os.startfile(args.output)
            elif os.name == "posix":  # macOS or Linux
                if os.path.exists("/usr/bin/open"):  # macOS
                    subprocess.run(["open", args.output])
                else:  # Linux
                    subprocess.run(["xdg-open", args.output])
    else:
        print(f"Error generating documentation:")
        print(process.stderr)


if __name__ == "__main__":
    asyncio.run(main())
