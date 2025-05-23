#!/usr/bin/env python3

"""
Demo script for running the Social Network Challenge with the ichub-backend

This script:
1. Runs a simple client that creates a social network profile
2. Registers it with a DTR via the ichub-backend
3. Shows the integration between the backend and the Tractus-X SDK
"""

import requests
import json
import argparse
import time
import sys

def run_demo(base_url, dtr_url, api_key, bpn, profile_name, business_name, simulate=False):
    """
    Run the social network demo using the ichub-backend
    
    Args:
        base_url: Base URL of the ichub-backend (e.g., http://localhost:8000)
        dtr_url: URL of the Digital Twin Registry
        api_key: API key for the DTR
        bpn: Business Partner Number
        profile_name: User's profile name
        business_name: User's business name
        simulate: Whether to run in simulation mode
    """
    print("\n====== Tractus-X SDK Social Network Challenge Demo ======\n")
    print(f"Using backend at: {base_url}")
    print(f"Using DTR at: {dtr_url}")
    print(f"BPN: {bpn}")
    
    # Step 1: Create a profile
    print("\n[Step 1] Creating social network profile...")
    try:
        profile_response = requests.post(
            f"{base_url}/social-network/profiles",
            json={
                "profile_name": profile_name,
                "business_name": business_name,
                "bpn": bpn
            }
        )
        profile_response.raise_for_status()
        profile_data = profile_response.json()
        
        profile_id = profile_data["profile_id"]
        posts_id = profile_data["posts_id"]
        friends_id = profile_data["friends_id"]
        
        print(f"Created profile with ID: {profile_id}")
        print(f"Posts ID: {posts_id}")
        print(f"Friends ID: {friends_id}")
        print("Profile details:")
        print(json.dumps(profile_data["profile"], indent=2))
    except Exception as e:
        print(f"ERROR: Failed to create profile: {str(e)}")
        sys.exit(1)
    
    # Step 2: Add a post
    print("\n[Step 2] Adding a post to the profile...")
    try:
        post_response = requests.post(
            f"{base_url}/social-network/profiles/{profile_id}/posts",
            json={
                "content": "Eclipse Tractus-X Where we build dataspaces!"
            }
        )
        post_response.raise_for_status()
        post_data = post_response.json()
        
        print("Added post:")
        print(json.dumps(post_data, indent=2))
    except Exception as e:
        print(f"ERROR: Failed to add post: {str(e)}")
        sys.exit(1)
    
    # Step 3: Register with DTR
    print(f"\n[Step 3] Registering with DTR at {dtr_url}...")
    try:
        register_response = requests.post(
            f"{base_url}/social-network/profiles/{profile_id}/register",
            json={
                "dtr_url": dtr_url,
                "api_key": api_key,
                "simulate": simulate
            }
        )
        register_response.raise_for_status()
        register_data = register_response.json()
        
        print("Registration result:")
        print(json.dumps(register_data, indent=2))
    except Exception as e:
        print(f"ERROR: Failed to register with DTR: {str(e)}")
        sys.exit(1)
    
    # Step 4: Confirm everything is working
    print("\n[Step 4] Confirming submodel endpoints are working...")
    try:
        profile_sm_response = requests.get(f"{base_url}/social-network/submodels/profile/{profile_id}")
        profile_sm_response.raise_for_status()
        
        posts_sm_response = requests.get(f"{base_url}/social-network/submodels/posts/{posts_id}")
        posts_sm_response.raise_for_status()
        
        friends_sm_response = requests.get(f"{base_url}/social-network/submodels/friends/{friends_id}")
        friends_sm_response.raise_for_status()
        
        print("All submodel endpoints are working correctly!")
    except Exception as e:
        print(f"ERROR: Failed to access submodel endpoints: {str(e)}")
        sys.exit(1)
    
    print("\n====== Demo completed successfully! ======\n")
    
    print("Summary of your Digital Twin:")
    print(f"- Profile name: {profile_name}")
    print(f"- Business: {business_name}")
    print(f"- BPN: {bpn}")
    print(f"- Profile ID: {profile_id}")
    print(f"- Posts ID: {posts_id}")
    print(f"- Friends ID: {friends_id}")
    
    if simulate:
        print("\n*** Demo was run in SIMULATION mode - no actual DTR registration was performed ***")
    else:
        print(f"\nYour Digital Twin is now registered with the DTR at {dtr_url}")
    
    print("\nTractus-X SDK Challenge successfully completed!")

def main():
    """Main function to run the demo"""
    parser = argparse.ArgumentParser(description="Tractus-X SDK Social Network Challenge Demo")
    
    # Required arguments for DTR
    parser.add_argument("--dtr-url", required=True, 
                        help="URL of the Digital Twin Registry (DTR)")
    parser.add_argument("--api-key", required=True,
                        help="API key for the DTR")
    parser.add_argument("--bpn", required=True,
                        help="Business Partner Number")
    
    # Optional arguments
    parser.add_argument("--name", default="John Doe",
                        help="Profile name (default: John Doe)")
    parser.add_argument("--business", default="My Company",
                        help="Business name (default: My Company)")
    parser.add_argument("--base-url", default="http://localhost:8000",
                        help="Base URL of the ichub-backend (default: http://localhost:8000)")
    parser.add_argument("--simulate", action="store_true",
                        help="Simulate (no actual DTR connection)")
    
    args = parser.parse_args()
    
    # Run the demo
    run_demo(
        base_url=args.base_url,
        dtr_url=args.dtr_url,
        api_key=args.api_key,
        bpn=args.bpn,
        profile_name=args.name,
        business_name=args.business,
        simulate=args.simulate
    )

if __name__ == "__main__":
    main() 