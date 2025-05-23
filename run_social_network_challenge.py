#!/usr/bin/env python3

"""
Tractus-X SDK Challenge Runner - Social Network Digital Twin

This script creates a Digital Twin for a social network user profile with submodels for:
- User Profile Information
- Posts Collection
- Friends List

It demonstrates how to use the Tractus-X SDK to interact with the Digital Twin Registry
"""

import sys
import uuid
import json
import datetime
import argparse
from typing import Dict, Any
import base64

try:
    # Import Tractus-X SDK modules
    from tractusx_sdk.industry.services.aas_service import AasService
    from tractusx_sdk.industry.services.auth_service import AuthService
    from tractusx_sdk.industry.models.aas.v3 import (
        AssetKind,
        ShellDescriptor,
        SubModelDescriptor,
        SpecificAssetId,
        Reference,
        ReferenceTypes,
        ProtocolInformation,
        Endpoint
    )
except ImportError:
    print("ERROR: Tractus-X SDK modules could not be imported")
    print("Please make sure the tractusx_sdk package is installed")
    sys.exit(1)

# API Key Auth Service for EDC Connector
class ApiKeyAuthService(AuthService):
    """API Key authentication service implementation"""
    
    def __init__(self, api_key: str):
        """Initialize with API key"""
        self.api_key = api_key
        
    def get_token(self) -> str:
        """Get the authentication token"""
        return self.api_key
        
    def is_token_valid(self) -> bool:
        """API keys don't expire"""
        return True

class SocialNetworkChallenge:
    """Creates and registers a social network profile as a Digital Twin"""
    
    def __init__(self, dtr_url: str, api_key: str, bpn: str, simulate: bool = False):
        """
        Initialize the challenge
        
        Args:
            dtr_url: URL of the Digital Twin Registry
            api_key: API key for DTR
            bpn: Business Partner Number for the profile
            simulate: If True, don't actually connect to DTR
        """
        self.dtr_url = dtr_url
        self.api_key = api_key
        self.bpn = bpn
        self.simulate = simulate
        
        # Generate UUIDs for our digital twin components
        self.user_id = str(uuid.uuid4())
        self.profile_id = str(uuid.uuid4())
        self.posts_id = str(uuid.uuid4())
        self.friends_id = str(uuid.uuid4())
        
        # Initialize AAS service for DTR
        if not simulate:
            self._init_dtr_service()
    
    def _init_dtr_service(self):
        """Initialize the DTR service"""
        print(f"Connecting to DTR at {self.dtr_url}")
        
        # Create auth service with API key
        auth_service = ApiKeyAuthService(self.api_key)
        
        # Create AAS service
        self.aas_service = AasService(
            base_url=self.dtr_url,
            base_lookup_url=self.dtr_url,
            api_path="/api/v3",
            auth_service=auth_service,
            verify_ssl=False  # For development only
        )
        
        # Test connection
        try:
            description = self.aas_service.get_description()
            print("Successfully connected to DTR")
        except Exception as e:
            print(f"Warning: Error connecting to DTR: {e}")
            print("Will continue, but registration may fail")
    
    def create_profile(self, name: str, business: str) -> Dict[str, Any]:
        """
        Create a user profile
        
        Args:
            name: User's name
            business: Business/company name
            
        Returns:
            Dictionary with profile data
        """
        profile = {
            "profileId": f"urn:uuid:{self.profile_id}",
            "profileName": name,
            "businessName": business,
            "businessPartner": self.bpn
        }
        
        print("Created profile data:")
        print(json.dumps(profile, indent=2))
        return profile
    
    def create_posts(self) -> Dict[str, Any]:
        """
        Create a posts collection with one sample post
        
        Returns:
            Dictionary with posts data
        """
        now = datetime.datetime.now()
        
        posts = {
            "postsId": f"urn:uuid:{self.posts_id}",
            "posts": [
                {
                    "postId": f"urn:uuid:{uuid.uuid4()}",
                    "content": "Eclipse Tractus-X Where we build dataspaces!",
                    "createdOn": now.strftime("%Y-%m-%d"),
                    "lastModifiedOn": now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                }
            ]
        }
        
        print("Created posts data:")
        print(json.dumps(posts, indent=2))
        return posts
    
    def create_friends(self) -> Dict[str, Any]:
        """
        Create an empty friends collection
        
        Returns:
            Dictionary with friends data
        """
        friends = {
            "friendsId": f"urn:uuid:{self.friends_id}",
            "friends": []
        }
        
        print("Created friends data:")
        print(json.dumps(friends, indent=2))
        return friends
    
    def create_digital_twin(self, name: str) -> ShellDescriptor:
        """
        Create a Digital Twin shell descriptor
        
        Args:
            name: User's name for the shell ID
            
        Returns:
            ShellDescriptor for the Digital Twin
        """
        # Create a shell ID
        shell_id = f"urn:uuid:{self.user_id}"
        
        # Create specific asset IDs
        asset_ids = [
            SpecificAssetId(
                name="Profile",
                value=f"urn:uuid:{self.profile_id}"
            ),
            SpecificAssetId(
                name="Posts",
                value=f"urn:uuid:{self.posts_id}"
            ),
            SpecificAssetId(
                name="Friends",
                value=f"urn:uuid:{self.friends_id}"
            ),
            SpecificAssetId(
                name="BPN",
                value=self.bpn
            )
        ]
        
        # Create the shell descriptor
        shell = ShellDescriptor(
            id=shell_id,
            id_short=f"SocialProfile_{name}",
            description=[],
            global_asset_id=shell_id,
            specific_asset_ids=asset_ids,
            submodel_descriptors=[],
            asset_type="urn:tractusx:socialnetwork.user:1.0.0",
            asset_kind=AssetKind.INSTANCE
        )
        
        return shell
    
    def add_submodels(self, shell: ShellDescriptor, endpoint_url: str) -> ShellDescriptor:
        """
        Add submodels to the shell descriptor
        
        Args:
            shell: Shell descriptor
            endpoint_url: URL for the submodel endpoint
            
        Returns:
            Updated shell descriptor
        """
        # Security attributes
        security_attr = {
            "type": "NONE",
            "key": "NONE",
            "value": "NONE"
        }
        
        # Create protocol information
        profile_protocol = ProtocolInformation(
            href=f"{endpoint_url}/submodel",
            endpoint_protocol="HTTP",
            endpoint_protocol_version=["1.1"],
            subprotocol="DSP",
            subprotocol_body=f"id=profile-{self.profile_id};dspEndpoint={endpoint_url}",
            subprotocol_body_encoding="plain",
            security_attributes=[security_attr]
        )
        
        posts_protocol = ProtocolInformation(
            href=f"{endpoint_url}/submodel",
            endpoint_protocol="HTTP",
            endpoint_protocol_version=["1.1"],
            subprotocol="DSP",
            subprotocol_body=f"id=posts-{self.posts_id};dspEndpoint={endpoint_url}",
            subprotocol_body_encoding="plain",
            security_attributes=[security_attr]
        )
        
        friends_protocol = ProtocolInformation(
            href=f"{endpoint_url}/submodel",
            endpoint_protocol="HTTP",
            endpoint_protocol_version=["1.1"],
            subprotocol="DSP",
            subprotocol_body=f"id=friends-{self.friends_id};dspEndpoint={endpoint_url}",
            subprotocol_body_encoding="plain",
            security_attributes=[security_attr]
        )
        
        # Profile submodel
        profile_submodel = SubModelDescriptor(
            id=f"urn:uuid:{self.profile_id}",
            id_short="Profile",
            description=[],
            semantic_id=Reference(
                type=ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[{
                    "type": "GlobalReference",
                    "value": "urn:samm:io.tractusx.socialnetwork_profile:1.0.0#Profile"
                }]
            ),
            endpoints=[
                Endpoint(
                    interface="SUBMODEL-3.0",
                    protocolInformation=profile_protocol
                )
            ]
        )
        
        # Posts submodel
        posts_submodel = SubModelDescriptor(
            id=f"urn:uuid:{self.posts_id}",
            id_short="Posts",
            description=[],
            semantic_id=Reference(
                type=ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[{
                    "type": "GlobalReference",
                    "value": "urn:samm:io.tractusx.socialnetwork_posts:1.0.0#Posts"
                }]
            ),
            endpoints=[
                Endpoint(
                    interface="SUBMODEL-3.0",
                    protocolInformation=posts_protocol
                )
            ]
        )
        
        # Friends submodel
        friends_submodel = SubModelDescriptor(
            id=f"urn:uuid:{self.friends_id}",
            id_short="Friends",
            description=[],
            semantic_id=Reference(
                type=ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[{
                    "type": "GlobalReference",
                    "value": "urn:samm:io.tractusx.socialnetwork_friends:1.0.0#Friend"
                }]
            ),
            endpoints=[
                Endpoint(
                    interface="SUBMODEL-3.0",
                    protocolInformation=friends_protocol
                )
            ]
        )
        
        # Add all submodels to the shell
        shell.submodel_descriptors = [profile_submodel, posts_submodel, friends_submodel]
        return shell
    
    def register_twin(self, shell: ShellDescriptor) -> None:
        """
        Register the Digital Twin in the DTR
        
        Args:
            shell: Shell descriptor to register
        """
        if self.simulate:
            print("SIMULATION MODE: Skipping actual DTR registration")
            return
        
        try:
            print(f"Registering Digital Twin with ID {shell.id} in DTR...")
            result = self.aas_service.create_asset_administration_shell_descriptor(
                shell_descriptor=shell
            )
            print("Successfully registered Digital Twin in DTR!")
        except Exception as e:
            print(f"Error registering Digital Twin: {e}")
            print("Registration failed")
    
    def run_challenge(self, name: str, business: str, endpoint_url: str) -> None:
        """
        Run the complete challenge
        
        Args:
            name: User's name
            business: Business/company name
            endpoint_url: URL for the submodel endpoint
        """
        print(f"\n=== Creating Social Network Digital Twin for {name} ===\n")
        
        # 1. Create data models
        profile = self.create_profile(name, business)
        posts = self.create_posts()
        friends = self.create_friends()
        
        # 2. Create shell descriptor
        shell = self.create_digital_twin(name)
        
        # 3. Add submodels
        shell = self.add_submodels(shell, endpoint_url)
        
        # 4. Register with DTR
        self.register_twin(shell)
        
        print("\n=== Challenge Summary ===")
        print(f"User ID: {self.user_id}")
        print(f"Profile ID: {self.profile_id}")
        print(f"Posts ID: {self.posts_id}")
        print(f"Friends ID: {self.friends_id}")
        print("=========================")


def main():
    """Main entry point for the challenge runner"""
    parser = argparse.ArgumentParser(description="Tractus-X SDK Social Network Challenge")
    
    # Required arguments
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
    parser.add_argument("--endpoint-url", default="https://backend-ichub.tx.arena2036-x.de",
                        help="URL for the submodel endpoint")
    parser.add_argument("--simulate", action="store_true",
                        help="Simulate (no actual DTR connection)")
    
    args = parser.parse_args()
    
    # Run the challenge
    challenge = SocialNetworkChallenge(
        dtr_url=args.dtr_url,
        api_key=args.api_key,
        bpn=args.bpn,
        simulate=args.simulate
    )
    
    challenge.run_challenge(
        name=args.name,
        business=args.business,
        endpoint_url=args.endpoint_url
    )


if __name__ == "__main__":
    main() 